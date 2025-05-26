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

@router.post("/get_price")
async def get_price(
    id: Optional[str] = None,
    book_name: Optional[str] = None,
    db: Session = Depends(get_flipkart_db)
):
    if not id and not book_name:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'book_name'")
    
    if id:
        product = db.query(flipkart).filter(flipkart.id == id).first()
    else:
        product = db.query(flipkart).filter(flipkart.name == book_name).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    price_id = (product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    return {            "unit_price": price_obj.price   }


@router.get("/name_from_id")
async def name_from_id(
    id: str,
    db: Session = Depends(get_flipkart_db)
):
    """Return product name given the flipkart ID"""
    flipkart_product = db.query(flipkart).filter(flipkart.id == id).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"id": id, "name": flipkart_product.name}


@router.get("/id_from_name")
async def id_from_name(
    name: str,
    db: Session = Depends(get_flipkart_db)
):
    """Return flipkart ID given the product name"""
    flipkart_product = db.query(flipkart).filter(flipkart.name == name).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"name": name, "id": flipkart_product.id}


@router.post("/stock_by_id")
async def stock_by_id(
    id: str,
    db: Session = Depends(get_flipkart_db)
):
    """Tell me how much stock you have for this book id — I want it all!"""
    flipkart_product = db.query(flipkart).filter(flipkart.id == id).first()
    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    total_stock = random.randint(5, 100)    
    return total_stock


@router.post("/delivery_status")
async def delivery_status(
    name: Optional[str] = None,
    id: Optional[str] = None,
    
):
    if not name and not id:
        raise HTTPException(status_code=400, detail="Either 'name' or 'id' must be provided")

    # Fetch product by name or id
    if name:
        flipkart_product = db.query(flipkart).filter(flipkart.name == name).first()
    else:
        flipkart_product = db.query(flipkart).filter(flipkart.id == id).first()

    if not flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delivery status messages
    messages = { 1: "Can be delivered today",0: "Deliverable", -1: "Not deliverable"  }

    # Check delivery info using pincode
    delivery_info = db.query(Deliverable).filter(Deliverable.pincode == flipkart_product.pincode).first()

    if not delivery_info:        status = -1
    elif delivery_info.delivery_time == 1:
        status = 1
    else:        status = 0

    identifier = name if name else id

    return {
        "message": f"Delivery status for '{identifier}': {messages[status]}",
        "status_code": status
    }


@router.post("/delivery_status")
async def delivery_status(
    pincode: str,
    db: Session = Depends(get_flipkart_db)
):
    # Delivery messages mapping
    messages = {
        1: "Can be delivered today",
        0: "Deliverable",
        -1: "Not deliverable"
    }

    # Check deliverability for the pincode
    delivery_info = db.query(Deliverable).filter(Deliverable.pincode == pincode).first()

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

@router.post("/discount")
async def calculate_discount(
    quantity: int,
    name: Optional[str] = None,
    id: Optional[str] = None,
    db: Session = Depends(get_flipkart_db)
):
    if not name and not id:
        raise HTTPException(status_code=400, detail="Either 'name' or 'id' must be provided")

    # Get product
    if name:
        product = db.query(flipkart).filter(flipkart.name == name).first()
    else:
        product = db.query(flipkart).filter(flipkart.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_cost = product.price * quantity

    # Get discount
    discount = db.query(Discount).filter(
        Discount.cost_from <= total_cost,
        Discount.cost_to > total_cost
    ).first()

    discount_percent = discount.percent_off if discount else 0
    discounted_price = total_cost * (1 - discount_percent / 100)

    return {
        "original_price": total_cost,
        "discounted_price": discounted_price
    }