from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine, SessionLocal
from app.models import amazon_models
from app.models.amazon_models import Amazon, AmazonPrice, AmazonDeliverable, AmazonDiscount  # Updated imports
from app.schemas.amazon_schemas import (
    AMAZON_SEED_DATA,
    AMAZON_PRICE_SEED_DATA,  # Updated import names
    AMAZON_DELIVERABLE_SEED_DATA,  # Updated import names
    AMAZON_DISCOUNT_SEED_DATA  # Updated import names
)
from typing import Optional
import random

router = APIRouter()

def seed_amazon_database():
    """Seed the Amazon database with initial data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Amazon).count() == 0:
            # Seed Amazon products
            for item in AMAZON_SEED_DATA:
                amazon_product = Amazon(**item)
                db.add(amazon_product)

        if db.query(AmazonPrice).count() == 0:  # Updated class name
            # Seed Amazon Prices
            for item in AMAZON_PRICE_SEED_DATA:  # Updated variable name
                amazon_price = AmazonPrice(**item)  # Updated class name
                db.add(amazon_price)

        if db.query(AmazonDeliverable).count() == 0:  # Updated class name
            # Seed Amazon Deliverables
            for item in AMAZON_DELIVERABLE_SEED_DATA:  # Updated variable name
                amazon_deliverable = AmazonDeliverable(**item)  # Updated class name
                db.add(amazon_deliverable)

        if db.query(AmazonDiscount).count() == 0:  # Updated class name
            # Seed Amazon Discounts
            for item in AMAZON_DISCOUNT_SEED_DATA:  # Updated variable name
                amazon_discount = AmazonDiscount(**item)  # Updated class name
                db.add(amazon_discount)

        db.commit()
        print("Amazon database seeded successfully!")

    except Exception as e:
        print(f"Error seeding Amazon database: {e}")
        db.rollback()
    finally:
        db.close()

# Create Amazon database tables and seed data
amazon_models.Base.metadata.create_all(bind=engine)
seed_amazon_database()

@router.get("/")
async def amazon_root():
    return {"message": "Amazon Management System API - All endpoints ready!"}

@router.post("/get_price")
async def get_price(
    id: Optional[str] = None,
    book_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not id and not book_name:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'book_name'")

    if id:
        product = db.query(Amazon).filter(Amazon.id == id).first()
    else:
        product = db.query(Amazon).filter(Amazon.name == book_name).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_count = db.query(AmazonPrice).count()  # Updated class name
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    price_id = (product.id % price_count) + 1
    price_obj = db.query(AmazonPrice).filter(AmazonPrice.id == price_id).first()  # Updated class name

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    return {"unit_price": price_obj.price}

@router.get("/name_from_id")
async def name_from_id(
    id: str,
    db: Session = Depends(get_db)
):
    """Return product name given the Amazon ID"""
    amazon_product = db.query(Amazon).filter(Amazon.id == id).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"id": id, "name": amazon_product.name}

@router.get("/id_from_name")
async def id_from_name(
    name: str,
    db: Session = Depends(get_db)
):
    """Return Amazon ID given the product name"""
    amazon_product = db.query(Amazon).filter(Amazon.name == name).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"name": name, "id": amazon_product.id}

@router.post("/stock_by_id")
async def stock_by_id(
    id: str,
    db: Session = Depends(get_db)
):
    """Tell me how much stock you have for this book id — I want it all!"""
    amazon_product = db.query(Amazon).filter(Amazon.id == id).first()
    if not amazon_product:
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
    delivery_info = db.query(AmazonDeliverable).filter(AmazonDeliverable.pincode == pincode).first()  # Updated class name

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
    discount = db.query(AmazonDiscount).filter(AmazonDiscount.cost_from <= total_price,  AmazonDiscount.cost_to > total_price).first()
    percent = discount.percent_off if discount else 0
    reduced_amount = (percent / 100) * total_price
    payable_amount = total_price - reduced_amount
    return {"discount_percent": percent,"reduced_amount": round(reduced_amount, 2),"payable_amount": round(payable_amount, 2) }