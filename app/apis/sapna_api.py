from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_sapna_db, sapna_engine, SapnaSessionLocal
from app.models import sapna_models
from app.models.sapna_models import sapna, Price, Deliverable, Discount
from app.schemas.sapna_schemas import (
    sapna_SEED_DATA,
    PRICE_SEED_DATA,
    DELIVERABLE_SEED_DATA,
    DISCOUNT_SEED_DATA
)
from typing import Optional
import random

router = APIRouter()

def seed_database():
    """Seed the database with initial data"""
    db = SapnaSessionLocal()
    try:
        # Check if data already exists
        if db.query(sapna).count() == 0:
            # Seed sapna products
            for item in sapna_SEED_DATA:
                sapna_product = sapna(**item)
                db.add(sapna_product)

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
        print("Sapna database seeded successfully!")

    except Exception as e:
        print(f"Error seeding sapna database: {e}")
        db.rollback()
    finally:
        db.close()

# Create database tables and seed data
sapna_models.Base.metadata.create_all(bind=sapna_engine)
seed_database()

@router.get("/")
async def sapna_root():
    return {"message": "Sapna Management System API - All endpoints ready!"}

@router.post("/get_price_from_sapna_by_bookid")
async def get_price_from_sapna_by_bookid(
    sapna_id: str,
    quantity: int = 1,
    db: Session = Depends(get_sapna_db)
):
    """Get price for a specific sapna product by book ID"""
    sapna_product = db.query(sapna).filter(sapna.sapna_id == sapna_id).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    price_id = (sapna_product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    total_price = price_obj.price * quantity

    return {
        "sapna_id": sapna_id,
        "product_name": sapna_product.name,
        "unit_price": price_obj.price,
        "quantity": quantity,
        "total_price": total_price,
        "currency": "INR"
    }

@router.post("/get_price_from_sapna_by_bookname")
async def get_price_from_sapna_by_bookname(
    book_name: str,
    quantity: int = 1,
    db: Session = Depends(get_sapna_db)
):
    """Get price for a specific sapna product by book name"""
    sapna_product = db.query(sapna).filter(sapna.name == book_name).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    price_id = (sapna_product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    total_price = price_obj.price * quantity

    return {
        "sapna_id": sapna_product.sapna_id,
        "product_name": book_name,
        "unit_price": price_obj.price,
        "quantity": quantity,
        "total_price": total_price,
        "currency": "INR"
    }

@router.post("/stock_by_name")
async def stock_by_name(
    name: str,
    db: Session = Depends(get_sapna_db)
):
    """Tell me how much stock you have for this book name — I want it all!"""
    sapna_product = db.query(sapna).filter(sapna.name == name).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_stock = random.randint(5, 100)  # Simulated stock

    return {
        "message": f"Hey! For '{name}', we have {total_stock} in stock. Take it all!"
    }

@router.post("/stock_by_id")
async def stock_by_id(
    sapna_id: str,
    db: Session = Depends(get_sapna_db)
):
    """Tell me how much stock you have for this book id — I want it all!"""
    sapna_product = db.query(sapna).filter(sapna.sapna_id == sapna_id).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_stock = random.randint(5, 100)  # Simulated stock

    return {
        "message": f"Hey! For book ID '{sapna_id}', we have {total_stock} in stock. Take it all!"
    }

@router.post("/delivery_status_by_name")
async def delivery_status_by_name(
    name: str,
    db: Session = Depends(get_sapna_db)
):
    sapna_product = db.query(sapna).filter(sapna.name == name).first()
    if not sapna_product:
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
    sapna_id: str,
    db: Session = Depends(get_sapna_db)
):
    sapna_product = db.query(sapna).filter(sapna.sapna_id == sapna_id).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")

    status = random.choice([1, 0, -1])

    messages = {
        1: "Can be delivered today",
        0: "Deliverable",
        -1: "Not deliverable"
    }

    return {
        "message": f"Delivery status for book ID '{sapna_id}': {messages[status]}",
        "status_code": status
    }
