from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Flipkart(Base):
    __tablename__ = "flipkart_books"  # Changed from "flipkart" to "flipkarts"

    id = Column(Integer, primary_key=True, index=True)
    flipkart_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=False)
    subject_code = Column(String(10), nullable=False)
    serial_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Price(Base):
    __tablename__ = "flipkart_prices"  # Changed to avoid conflicts

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Deliverable(Base):
    __tablename__ = "flipkart_deliverables"  # Changed to avoid conflicts

    id = Column(Integer, primary_key=True, index=True)
    pincode = Column(String(10), nullable=False)
    delivery_time = Column(Integer, nullable=False)  # in days
    created_at = Column(DateTime, default=datetime.utcnow)

class Discount(Base):
    __tablename__ = "flipkart_discounts"  # Changed to avoid conflicts

    id = Column(Integer, primary_key=True, index=True)
    cost_from = Column(Float, nullable=False)
    cost_to = Column(Float, nullable=False)
    percent_off = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)