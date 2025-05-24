from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # Correct relative import

class Amazon(Base):
    __tablename__ = "amazons"
    
    id = Column(Integer, primary_key=True, index=True)
    amazon_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=False)
    subject_code = Column(String(10), nullable=False)
    serial_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Price(Base):
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Deliverable(Base):
    __tablename__ = "deliverables"
    
    id = Column(Integer, primary_key=True, index=True)
    pincode = Column(String(10), nullable=False)
    delivery_time = Column(Integer, nullable=False)  # in days
    created_at = Column(DateTime, default=datetime.utcnow)

class Discount(Base):
    __tablename__ = "discounts"
    
    id = Column(Integer, primary_key=True, index=True)
    cost_from = Column(Float, nullable=False)
    cost_to = Column(Float, nullable=False)
    percent_off = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
