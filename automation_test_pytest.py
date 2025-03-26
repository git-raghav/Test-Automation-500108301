import pytest
import allure
import os
import sys
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from apiserver import app
from models import Base, User, OperationHistory
from database import get_db
from auth import get_password_hash
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create necessary directories
os.makedirs("logs", exist_ok=True)
os.makedirs("allure-results", exist_ok=True)

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Override the get_db dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Create test client
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Test data
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword"
}

@pytest.fixture(autouse=True)
async def setup_database():
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def test_user_token():
    # Register test user
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.mark.asyncio
@allure.feature("Authentication")
@allure.story("User Registration")
async def test_register():
    """Test user registration endpoint"""
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
@allure.feature("Authentication")
@allure.story("User Login")
async def test_login(test_user_token):
    """Test user login endpoint"""
    response = client.post(
        "/token",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
@allure.feature("Authentication")
@allure.story("Unauthorized Access")
async def test_unauthorized_access():
    """Test unauthorized access to protected endpoints"""
    response = client.get("/add/2/3")
    assert response.status_code == 401

@pytest.mark.asyncio
@allure.feature("Database Operations")
@allure.story("Operation History")
async def test_operation_history(test_user_token):
    """Test operation history endpoint"""
    # Perform some operations
    headers = {"Authorization": f"Bearer {test_user_token}"}
    client.get("/add/2/3", headers=headers)
    client.get("/subtract/5/3", headers=headers)

    # Get history
    response = client.get("/history", headers=headers)
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2
    assert history[0]["operation"] == "subtract"
    assert history[1]["operation"] == "add"

@pytest.mark.asyncio
@allure.feature("Database Operations")
@allure.story("Operation Logging")
async def test_operation_logging(test_user_token):
    """Test that operations are logged to database"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/add/2/3", headers=headers)
    assert response.status_code == 200

    # Verify operation was logged
    async with TestingSessionLocal() as session:
        result = await session.execute(
            select(OperationHistory).where(OperationHistory.operation == "add")
        )
        operation = result.scalar_one_or_none()
        assert operation is not None
        assert operation.num1 == 2
        assert operation.num2 == 3
        assert operation.result == 5

@pytest.mark.asyncio
@allure.feature("Error Handling")
@allure.story("Invalid Inputs")
async def test_invalid_inputs(test_user_token):
    """Test error handling for invalid inputs"""
    headers = {"Authorization": f"Bearer {test_user_token}"}

    # Test with non-numeric input
    response = client.get("/add/abc/2", headers=headers)
    assert response.status_code == 422

    # Test with missing parameters
    response = client.get("/add/1", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
@allure.feature("Performance")
@allure.story("Response Time")
async def test_response_time(test_user_token):
    """Test API response time"""
    import time
    headers = {"Authorization": f"Bearer {test_user_token}"}

    start_time = time.time()
    response = client.get("/add/2/3", headers=headers)
    end_time = time.time()

    assert response.status_code == 200
    assert end_time - start_time < 1.0  # Response should be under 1 second

@pytest.mark.asyncio
@allure.feature("Logging")
@allure.story("Operation Logs")
async def test_operation_logs(test_user_token):
    """Test that operations are properly logged"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/add/2/3", headers=headers)
    assert response.status_code == 200

    # Check log file
    with open("logs/app.log", "r") as f:
        log_lines = f.readlines()
        assert any("Addition operation performed" in line for line in log_lines)
        assert any("username=testuser" in line for line in log_lines)
        assert any("num1=2" in line for line in log_lines)
        assert any("num2=3" in line for line in log_lines)
        assert any("result=5" in line for line in log_lines)

if __name__ == "__main__":
    pytest.main([
        "-v",
        "--cov=apiserver",
        "--html=report.html",
        "--self-contained-html",
        "--alluredir=./allure-results",
        "--tb=short",
        "--capture=no"
    ])
