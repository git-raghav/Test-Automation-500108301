from fastapi import FastAPI


#Initialize the FastAPI app


app = FastAPI()


#Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}



# Addition endpoint
@app.get("/add/{num1}/{num2}")
def add(num1: int, num2: int):
    """
    Adds two numbers.
    Example: /add/2/3 returns {"result": 5}
    """
    return {"result": num1 + num2}


# Subtraction endpoint
@app.get("/subtract/{num1}/{num2}")
def subtract(num1: int, num2: int):
    """
    Subtracts the second number from the first.
    Example: /subtract/5/3 returns {"result": 2}
    """
    return {"result": num1 - num2}

# Multiplication endpoint
@app.get("/multiply/{num1}/{num2}")
def multiply(num1: int, num2: int):
    """
    Multiplies two numbers.
    Example: /multiply/2/3 returns {"result": 6}
    """
    return {"result": num1 * num2}

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apiserver:app", host="0.0.0.0", port=8000, reload=True)
