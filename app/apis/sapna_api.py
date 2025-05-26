from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_sapna_db, sapna_engine, SapnaSessionLocal
from app.models import sapna_models
from app.models.sapna_models import sapna, Price, Deliverable, Discount
from app.schemas.sapna_schemas import (
    SAPNA_SEED_DATA,
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
            for item in SAPNA_SEED_DATA:
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


@router.post("/get_price")
async def get_price(
    id: Optional[str] = None,
    book_name: Optional[str] = None,
    db: Session = Depends(get_sapna_db)
):
    if not id and not book_name:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'book_name'")
    
    if id:
        product = db.query(sapna).filter(sapna.id == id).first()
    else:
        product = db.query(sapna).filter(sapna.name == book_name).first()

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
    db: Session = Depends(get_sapna_db)
):
    """Return product name given the sapna ID"""
    sapna_product = db.query(sapna).filter(sapna.id == id).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"id": id, "name": sapna_product.name}


@router.get("/id_from_name")
async def id_from_name(
    name: str,
    db: Session = Depends(get_sapna_db)
):
    """Return sapna ID given the product name"""
    sapna_product = db.query(sapna).filter(sapna.name == name).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"name": name, "id": sapna_product.id}


@router.post("/stock_by_id")
async def stock_by_id(
    id: str,
    db: Session = Depends(get_sapna_db)
):
    """Tell me how much stock you have for this book id — I want it all!"""
    sapna_product = db.query(sapna).filter(sapna.id == id).first()
    if not sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    total_stock = random.randint(5, 100)    
    return total_stock

@router.post("/delivery_status")
async def delivery_status(
    pincode: str,
    db: Session = Depends(get_sapna_db)
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
    db: Session = Depends(get_sapna_db)
):
    if not name and not id:
        raise HTTPException(status_code=400, detail="Either 'name' or 'id' must be provided")

    # Get product
    if name:
        product = db.query(sapna).filter(sapna.name == name).first()
    else:
        product = db.query(sapna).filter(sapna.id == id).first()

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