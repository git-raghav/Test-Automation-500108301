from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


#add function
@app.get("/add/{num1}/{num2}")
def add(num1: int, num2: int):
    return {"result": num1 + num2}

#subtract function
@app.get("/subtract/{num1}/{num2}")
def subtract(num1: int, num2: int):
    return {"result": num1 - num2}

#multiply function
@app.get("/multiply/{num1}/{num2}")
def multiply(num1: int, num2: int):
    return {"result": num1 * num2}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)