from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine, SessionLocal
from app.models import flipkart_models
from app.models.flipkart_models import Flipkart, Price, Deliverable, Discount
from app.schemas.flipkart_schemas import (
    FLIPKART_SEED_DATA,
    PRICE_SEED_DATA,
    DELIVERABLE_SEED_DATA,
    DISCOUNT_SEED_DATA,  # Updated import names
)
from typing import Optional
import random

router = APIRouter()

def seed_flipkart_database():
    """Seed the Flipkart database with initial data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Flipkart).count() == 0:
            # Seed Flipkart products
            for item in FLIPKART_SEED_DATA:
                flipkart_product = Flipkart(**item)
                db.add(flipkart_product)

        if db.query(Price).count() == 0:  # Updated class name
            # Seed Flipkart Prices
            for item in PRICE_SEED_DATA:  # Updated variable name
                flipkart_price = Price(**item)  # Updated class name
                db.add(flipkart_price)

        if db.query(Deliverable).count() == 0:  # Updated class name
            # Seed Flipkart Deliverables
            for item in DELIVERABLE_SEED_DATA:  # Updated variable name
                flipkart_deliverable = Deliverable(**item)  # Updated class name
                db.add(flipkart_deliverable)

        if db.query(Discount).count() == 0:  # Updated class name
            # Seed Flipkart Discounts
            for item in DISCOUNT_SEED_DATA:  # Updated variable name
                flipkart_discount = Discount(**item)  # Updated class name
                db.add(flipkart_discount)

        db.commit()
        print("Flipkart database seeded successfully!")

    except Exception as e:
        print(f"Error seeding Flipkart database: {e}")
        db.rollback()
    finally:
        db.close()

# Create Flipkart database tables and seed data
flipkart_models.Base.metadata.create_all(bind=engine)
seed_flipkart_database()

@router.get("/")
async def flipkart_root():
    return {"message": "Flipkart Management System API - All endpoints ready!"}

@router.post("/get_price")
async def get_price(
    id: Optional[str] = None,
    book_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not id and not book_name:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'book_name'")

    if id:
        product = db.query(Flipkart).filter(Flipkart.id == id).first()
    else:
        product = db.query(Flipkart).filter(Flipkart.name == book_name).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_count = db.query(Price).count()  # Updated class name
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    price_id = (product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()  # Updated class name

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    return {"unit_price": price_obj.price}

@router.get("/name_from_id")
async def name_from_id(
    id: str,
    db: Session = Depends(get_db)
):
    """Return product name given the Flipkart ID"""
    flipkart_product = db.query(Flipkart).filter(Flipkart.id == id).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"id": id, "name": flipkart_product.name}

@router.get("/id_from_name")
async def id_from_name(
    name: str,
    db: Session = Depends(get_db)
):
    """Return Flipkart ID given the product name"""
    flipkart_product = db.query(Flipkart).filter(Flipkart.name == name).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"name": name, "id": flipkart_product.id}

@router.post("/stock_by_id")
async def stock_by_id(
    id: str,
    db: Session = Depends(get_db)
):
    """Tell me how much stock you have for this book id — I want it all!"""
    flipkart_product = db.query(Flipkart).filter(Flipkart.id == id).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_stock = random.randint(5, 100)
    return total_stock

@router.post("/delivery_status")
async def delivery_status(
    pincode: str,
    db: Session = Depends(get_db)
):
    # Delivery messages mapping
    messages = {
        1: "Can be delivered today",
        0: "Deliverable",
        -1: "Not deliverable"
    }

    # Check deliverability for the pincode
    delivery_info = db.query(Deliverable).filter(Deliverable.pincode == pincode).first()  # Updated class name

    if not delivery_info:
        status = -1
    elif delivery_info.delivery_time == 1:
        status = 1
    else:
        status = 0

    return {
        "message": f"Delivery status to pincode '{pincode}': {messages[status]}",
        "status_code": status
    }
@router.post("/get_discount")
async def get_discount(    total_price: float,    db: Session = Depends(get_db)):
    discount = db.query(Discount).filter(Discount.cost_from <= total_price,  Discount.cost_to > total_price).first()
    percent = discount.percent_off if discount else 0
    reduced_amount = (percent / 100) * total_price
    payable_amount = total_price - reduced_amount
    return {"discount_percent": percent,"reduced_amount": round(reduced_amount, 2),"payable_amount": round(payable_amount, 2) }