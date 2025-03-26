from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OperationHistory(Base):
    __tablename__ = "operation_history"

    id = Column(Integer, primary_key=True)
    operation = Column(String)
    num1 = Column(Float)
    num2 = Column(Float)
    result = Column(Float)
    timestamp = Column(DateTime)
