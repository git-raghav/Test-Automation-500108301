from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI(
    title="Arithmetic API",
    description="A simple API for basic arithmetic operations",
    version="1.0.0"
)

# Root endpoint
@app.get("/", tags=["root"])
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"Hello": "World"}

# Addition endpoint
@app.get("/add/{num1}/{num2}", tags=["arithmetic"])
def add(num1: int, num2: int):
    """
    Adds two numbers.

    Args:
        num1 (int): First number
        num2 (int): Second number

    Returns:
        dict: Result containing the sum

    Example:
        /add/2/3 returns {"result": 5}
    """
    try:
        result = num1 + num2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Subtraction endpoint
@app.get("/subtract/{num1}/{num2}", tags=["arithmetic"])
def subtract(num1: int, num2: int):
    """
    Subtracts the second number from the first.

    Args:
        num1 (int): First number
        num2 (int): Second number

    Returns:
        dict: Result containing the difference

    Example:
        /subtract/5/3 returns {"result": 2}
    """
    try:
        result = num1 - num2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Multiplication endpoint
@app.get("/multiply/{num1}/{num2}", tags=["arithmetic"])
def multiply(num1: int, num2: int):
    """
    Multiplies two numbers.

    Args:
        num1 (int): First number
        num2 (int): Second number

    Returns:
        dict: Result containing the product

    Example:
        /multiply/2/3 returns {"result": 6}
    """
    try:
        result = num1 * num2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handling middleware
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apiserver:app", host="0.0.0.0", port=8000, reload=True)
