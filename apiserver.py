from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel, Field
from models import User, OperationHistory
from database import get_db, init_db
from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from logger import logger
import uvicorn
from fastapi.responses import JSONResponse
import math

# Initialize the FastAPI app
app = FastAPI(
    title="Arithmetic API",
    description="A simple API for basic arithmetic operations with authentication and logging",
    version="1.0.0"
)

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str

class OperationResult(BaseModel):
    result: float | None = None
    operation: str | None = None
    num1: float
    num2: float

class RootOperation(BaseModel):
    number: float = Field(..., ge=0)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables"""
    try:
        # Initialize database
        await init_db()
        logger.info("Application startup")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

# User registration
@app.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user exists
        result = await db.execute(select(User).where(User.username == user.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )

        # Create new user
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        # Create access token
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        logger.info("User registered", username=user.username)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during registration"
        )

# Login endpoint
@app.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(User).where(User.username == form_data.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        logger.info("User logged in", username=user.username)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during login"
        )

# Root endpoint
@app.get("/", tags=["root"])
async def read_root(current_user: User = Depends(get_current_user)):
    try:
        logger.info("Root endpoint accessed", username=current_user.username)
        return {"Hello": "World"}
    except Exception as e:
        logger.error(f"Error accessing root endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# Addition endpoint
@app.post("/add", tags=["arithmetic"], response_model=OperationResult)
async def add(
    operation: OperationResult,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = operation.num1 + operation.num2
        # Log operation to database
        db_operation = OperationHistory(
            operation="add",
            num1=operation.num1,
            num2=operation.num2,
            result=result,
            user_id=current_user.id
        )
        db.add(db_operation)
        await db.commit()

        logger.info(
            "Addition operation performed",
            username=current_user.username,
            num1=operation.num1,
            num2=operation.num2,
            result=result
        )
        return {"result": result, "operation": "add", "num1": operation.num1, "num2": operation.num2}
    except Exception as e:
        logger.error(
            "Error in addition operation",
            username=current_user.username,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

# Subtraction endpoint
@app.post("/subtract", tags=["arithmetic"], response_model=OperationResult)
async def subtract(
    operation: OperationResult,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = operation.num1 - operation.num2
        # Log operation to database
        db_operation = OperationHistory(
            operation="subtract",
            num1=operation.num1,
            num2=operation.num2,
            result=result,
            user_id=current_user.id
        )
        db.add(db_operation)
        await db.commit()

        logger.info(
            "Subtraction operation performed",
            username=current_user.username,
            num1=operation.num1,
            num2=operation.num2,
            result=result
        )
        return {"result": result, "operation": "subtract", "num1": operation.num1, "num2": operation.num2}
    except Exception as e:
        logger.error(
            "Error in subtraction operation",
            username=current_user.username,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

# Multiplication endpoint
@app.post("/multiply", tags=["arithmetic"], response_model=OperationResult)
async def multiply(
    operation: OperationResult,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = operation.num1 * operation.num2
        # Log operation to database
        db_operation = OperationHistory(
            operation="multiply",
            num1=operation.num1,
            num2=operation.num2,
            result=result,
            user_id=current_user.id
        )
        db.add(db_operation)
        await db.commit()

        logger.info(
            "Multiplication operation performed",
            username=current_user.username,
            num1=operation.num1,
            num2=operation.num2,
            result=result
        )
        return {"result": result, "operation": "multiply", "num1": operation.num1, "num2": operation.num2}
    except Exception as e:
        logger.error(
            "Error in multiplication operation",
            username=current_user.username,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

# Square root endpoint
@app.post("/root", tags=["arithmetic"], response_model=OperationResult)
async def root(
    operation: RootOperation,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        if operation.number < 0:
            raise HTTPException(status_code=400, detail="Cannot calculate square root of negative number")

        result = math.sqrt(operation.number)
        # Log operation to database
        db_operation = OperationHistory(
            operation="root",
            num1=operation.number,
            num2=0,  # Not used for root operation
            result=result,
            user_id=current_user.id
        )
        db.add(db_operation)
        await db.commit()

        logger.info(
            "Square root operation performed",
            username=current_user.username,
            number=operation.number,
            result=result
        )
        return {"result": result, "operation": "root", "num1": operation.number, "num2": 0}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error in square root operation",
            username=current_user.username,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

# Get user's operation history
@app.get("/history", tags=["user"])
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(OperationHistory)
            .where(OperationHistory.user_id == current_user.id)
            .order_by(OperationHistory.timestamp.desc())
        )
        operations = result.scalars().all()

        logger.info(
            "User history accessed",
            username=current_user.username,
            operation_count=len(operations)
        )
        return operations
    except Exception as e:
        logger.error(
            "Error accessing user history",
            username=current_user.username,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

# Error handling middleware
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

# Run the app using Uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "apiserver:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload in production
        log_level="info"
    )
