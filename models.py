from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with operation history
    operations = relationship("OperationHistory", back_populates="user")

class OperationHistory(Base):
    __tablename__ = "operation_history"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String)  # add, subtract, multiply
    num1 = Column(Float)
    num2 = Column(Float)
    result = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship with user
    user = relationship("User", back_populates="operations")
