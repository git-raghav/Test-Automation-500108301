from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from database import get_db
from models import OperationHistory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Arithmetic API")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/add/{num1}/{num2}")
def add(num1: int, num2: int, db: Session = Depends(get_db)):
    try:
        result = num1 + num2
        # Log operation to database
        history = OperationHistory(
            operation="add",
            num1=num1,
            num2=num2,
            result=result,
            timestamp=datetime.utcnow()
        )
        db.add(history)
        db.commit()
        logger.info(f"Addition: {num1} + {num2} = {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in addition: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/subtract/{num1}/{num2}")
def subtract(num1: int, num2: int, db: Session = Depends(get_db)):
    try:
        result = num1 - num2
        # Log operation to database
        history = OperationHistory(
            operation="subtract",
            num1=num1,
            num2=num2,
            result=result,
            timestamp=datetime.utcnow()
        )
        db.add(history)
        db.commit()
        logger.info(f"Subtraction: {num1} - {num2} = {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in subtraction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/multiply/{num1}/{num2}")
def multiply(num1: int, num2: int, db: Session = Depends(get_db)):
    try:
        result = num1 * num2
        # Log operation to database
        history = OperationHistory(
            operation="multiply",
            num1=num1,
            num2=num2,
            result=result,
            timestamp=datetime.utcnow()
        )
        db.add(history)
        db.commit()
        logger.info(f"Multiplication: {num1} * {num2} = {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in multiplication: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    try:
        history = db.query(OperationHistory).order_by(OperationHistory.timestamp.desc()).limit(10).all()
        return [{"operation": h.operation, "num1": h.num1, "num2": h.num2,
                "result": h.result, "timestamp": h.timestamp} for h in history]
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apiserver:app", host="0.0.0.0", port=8000, reload=True)
