import pytest
import allure
from fastapi.testclient import TestClient
from apiserver import app
from config import Config

# Create a test client
client = TestClient(app)

# Define test cases as a list of tuples for parameterized testing
testcases = [
    ("/add/2/2", 4, "Test addition of 2 and 2"),
    ("/subtract/2/2", 0, "Test subtraction of 2 from 2"),
    ("/multiply/2/2", 4, "Test multiplication of 2 and 2"),
    ("/add/-1/1", 0, "Test addition of -1 and 1"),
    ("/multiply/0/5", 0, "Test multiplication by zero"),
    ("/add/999999999/1", 1000000000, "Test addition of large numbers"),
    ("/subtract/-5/-3", -2, "Test subtraction of negative numbers"),
]

@pytest.mark.parametrize("endpoint, expected, description", testcases)
@allure.step("Testing API endpoint")
def test_api(endpoint, expected, description):
    """
    Parameterized test for API endpoints.
    """
    with allure.step(f"Making request to {endpoint}"):
        response = client.get(endpoint)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        result = response.json()["result"]
        assert result == expected, f"{description}. Expected {expected}, got {result}"

@allure.feature("API Endpoints")
@allure.story("Root Endpoint")
def test_root_endpoint():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@allure.feature("Error Handling")
@allure.story("Invalid Inputs")
def test_invalid_input():
    """
    Test error handling for invalid inputs.
    """
    # Test with non-numeric input
    response = client.get("/add/abc/2")
    assert response.status_code == 422  # FastAPI validation error

    # Test with missing parameters
    response = client.get("/add/1")
    assert response.status_code == 404  # Not found error

    # Test with invalid URL
    response = client.get("/invalid/endpoint")
    assert response.status_code == 404

@allure.feature("Edge Cases")
@allure.story("Large Numbers")
def test_large_numbers():
    """
    Test handling of large numbers.
    """
    response = client.get("/add/999999999/1")
    assert response.status_code == 200
    assert response.json()["result"] == 1000000000

@allure.feature("Edge Cases")
@allure.story("Negative Numbers")
def test_negative_numbers():
    """
    Test handling of negative numbers.
    """
    response = client.get("/subtract/-5/-3")
    assert response.status_code == 200
    assert response.json()["result"] == -2

@allure.feature("Edge Cases")
@allure.story("Zero Operations")
def test_zero_operations():
    """
    Test handling of zero in operations.
    """
    # Test multiplication with zero
    response = client.get("/multiply/5/0")
    assert response.status_code == 200
    assert response.json()["result"] == 0

    # Test addition with zero
    response = client.get("/add/5/0")
    assert response.status_code == 200
    assert response.json()["result"] == 5

@allure.feature("Performance")
@allure.story("Response Time")
def test_response_time():
    """
    Test API response time.
    """
    import time
    start_time = time.time()
    response = client.get("/add/2/3")
    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < Config.TEST_TIMEOUT

if __name__ == "__main__":
    pytest.main([
        "-v",
        "--cov=apiserver",
        "--html=report.html",
        "--self-contained-html",
        "--alluredir=./allure-results"
    ])
