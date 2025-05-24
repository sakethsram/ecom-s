from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_flipkart_db, flipkart_engine, FlipkartSessionLocal
from app.models import flipkart_models
from app.models.flipkart_models import flipkart, Price, Deliverable, Discount
from app.schemas.flipkart_schemas import (
    flipkart_SEED_DATA,
    PRICE_SEED_DATA,
    DELIVERABLE_SEED_DATA,
    DISCOUNT_SEED_DATA
)
from typing import Optional
import random

router = APIRouter()

def seed_database():
    """Seed the database with initial data"""
    db = FlipkartSessionLocal()
    try:
        # Check if data already exists
        if db.query(flipkart).count() == 0:
            # Seed flipkart products
            for item in flipkart_SEED_DATA:
                flipkart_product = flipkart(**item)
                db.add(flipkart_product)

        if db.query(Price).count() == 0:
            # Seed Prices
            for item in PRICE_SEED_DATA:
                price = Price(**item)
                db.add(price)

        if db.query(Deliverable).count() == 0:
            # Seed Deliverables
            for item in DELIVERABLE_SEED_DATA:
                deliverable = Deliverable(**item)
                db.add(deliverable)

        if db.query(Discount).count() == 0:
            # Seed Discounts
            for item in DISCOUNT_SEED_DATA:
                discount = Discount(**item)
                db.add(discount)

        db.commit()
        print("Flipkart database seeded successfully!")

    except Exception as e:
        print(f"Error seeding flipkart database: {e}")
        db.rollback()
    finally:
        db.close()

# Create database tables and seed data
flipkart_models.Base.metadata.create_all(bind=flipkart_engine)
seed_database()

@router.get("/")
async def flipkart_root():
    return {"message": "Flipkart Management System API - All endpoints ready!"}

@router.post("/get_price_from_flipkart_by_bookid")
async def get_price_from_flipkart_by_bookid(
    flipkart_id: str,
    quantity: int = 1,
    db: Session = Depends(get_flipkart_db)
):
    """Get price for a specific flipkart product by book ID"""
    flipkart_product = db.query(flipkart).filter(flipkart.flipkart_id == flipkart_id).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    price_id = (flipkart_product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    total_price = price_obj.price * quantity

    return {
        "flipkart_id": flipkart_id,
        "product_name": flipkart_product.name,
        "unit_price": price_obj.price,
        "quantity": quantity,
        "total_price": total_price,
        "currency": "INR"
    }

@router.post("/get_price_from_flipkart_by_bookname")
async def get_price_from_flipkart_by_bookname(
    book_name: str,
    quantity: int = 1,
    db: Session = Depends(get_flipkart_db)
):
    """Get price for a specific flipkart product by book name"""
    flipkart_product = db.query(flipkart).filter(flipkart.name == book_name).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    price_id = (flipkart_product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    total_price = price_obj.price * quantity

    return {
        "flipkart_id": flipkart_product.flipkart_id,
        "product_name": book_name,
        "unit_price": price_obj.price,
        "quantity": quantity,
        "total_price": total_price,
        "currency": "INR"
    }

@router.post("/stock_by_name")
async def stock_by_name(
    name: str,
    db: Session = Depends(get_flipkart_db)
):
    """Tell me how much stock you have for this book name — I want it all!"""
    flipkart_product = db.query(flipkart).filter(flipkart.name == name).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_stock = random.randint(5, 100)  # Simulated stock

    return {
        "message": f"Hey! For '{name}', we have {total_stock} in stock. Take it all!"
    }

@router.post("/stock_by_id")
async def stock_by_id(
    flipkart_id: str,
    db: Session = Depends(get_flipkart_db)
):
    """Tell me how much stock you have for this book id — I want it all!"""
    flipkart_product = db.query(flipkart).filter(flipkart.flipkart_id == flipkart_id).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_stock = random.randint(5, 100)  # Simulated stock

    return {
        "message": f"Hey! For book ID '{flipkart_id}', we have {total_stock} in stock. Take it all!"
    }

@router.post("/delivery_status_by_name")
async def delivery_status_by_name(
    name: str,
    db: Session = Depends(get_flipkart_db)
):
    flipkart_product = db.query(flipkart).filter(flipkart.name == name).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Random status for demonstration: 1, 0, or -1
    status = random.choice([1, 0, -1])

    messages = {
        1: "Can be delivered today",
        0: "Deliverable",
        -1: "Not deliverable"
    }

    return {
        "message": f"Delivery status for '{name}': {messages[status]}",
        "status_code": status
    }

@router.post("/delivery_status_by_id")
async def delivery_status_by_id(
    flipkart_id: str,
    db: Session = Depends(get_flipkart_db)
):
    flipkart_product = db.query(flipkart).filter(flipkart.flipkart_id == flipkart_id).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    status = random.choice([1, 0, -1])

    messages = {
        1: "Can be delivered today",
        0: "Deliverable",
        -1: "Not deliverable"
    }

    return {
        "message": f"Delivery status for book ID '{flipkart_id}': {messages[status]}",
        "status_code": status
    }
    