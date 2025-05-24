from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine, SessionLocal
from app.models import amazon_models
from app.models.amazon_models import Amazon, Price, Deliverable, Discount
from app.schemas.amazon_schemas import (
    AMAZON_SEED_DATA, 
    PRICE_SEED_DATA, 
    DELIVERABLE_SEED_DATA, 
    DISCOUNT_SEED_DATA
)
from typing import Optional
import random

router = APIRouter()

def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Amazon).count() == 0:
            # Seed Amazon products
            for item in AMAZON_SEED_DATA:
                amazon_product = Amazon(**item)
                db.add(amazon_product)
            
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
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

# Create database tables and seed data
amazon_models.Base.metadata.create_all(bind=engine)
seed_database()

@router.get("/")
async def amazon_root():
    return {"message": "Amazon Management System API - All endpoints ready!"}

async def get_price_from_amazon(
    amazon_id: str,
    quantity: int = 1,
    db: Session = Depends(get_db)
):
    """Get price for a specific Amazon product"""
    # Find the amazon product
    amazon_product = db.query(Amazon).filter(Amazon.amazon_id == amazon_id).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get price based on product ID (for demo, using amazon.id % price_count)
    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")
    
    price_id = (amazon_product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()
    
    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")
    
    total_price = price_obj.price * quantity
    
    return {
        "amazon_id": amazon_id,
        "product_name": amazon_product.name,
        "unit_price": price_obj.price,
        "quantity": quantity,
        "total_price": total_price,
        "currency": "INR"
    }

@router.post("/get_price_from_amazon_by_bookid")
async def get_price_from_amazon_by_bookid(
    amazon_id: str,
    quantity: int = 1,
    db: Session = Depends(get_db)
):
    """Get price for a specific Amazon product by book ID"""
    amazon_product = db.query(Amazon).filter(Amazon.amazon_id == amazon_id).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")
    
    price_id = (amazon_product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()
    
    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")
    
    total_price = price_obj.price * quantity
    
    return {
        "amazon_id": amazon_id,
        "product_name": amazon_product.name,
        "unit_price": price_obj.price,
        "quantity": quantity,
        "total_price": total_price,
        "currency": "INR"
    }

@router.post("/get_price_from_amazon_by_bookname")
async def get_price_from_amazon_by_bookname(
    book_name: str,
    quantity: int = 1,
    db: Session = Depends(get_db)
):
    """Get price for a specific Amazon product by book name"""
    amazon_product = db.query(Amazon).filter(Amazon.name == book_name).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")
    
    price_id = (amazon_product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()
    
    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")
    
    total_price = price_obj.price * quantity
    
    return {
        "amazon_id": amazon_product.amazon_id,
        "product_name": book_name,
        "unit_price": price_obj.price,
        "quantity": quantity,
        "total_price": total_price,
        "currency": "INR"
    }

@router.post("/stock_by_name")
async def stock_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    """Tell me how much stock you have for this book name — I want it all!"""
    amazon_product = db.query(Amazon).filter(Amazon.name == name).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    total_stock = random.randint(5, 100)  # Simulated stock
    
    return {
        "message": f"Hey! For '{name}', we have {total_stock} in stock. Take it all!"
    }


@router.post("/stock_by_id")
async def stock_by_id(
    amazon_id: str,
    db: Session = Depends(get_db)
):
    """Tell me how much stock you have for this book id — I want it all!"""
    amazon_product = db.query(Amazon).filter(Amazon.amazon_id == amazon_id).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    total_stock = random.randint(5, 100)  # Simulated stock
    
    return {
        "message": f"Hey! For book ID '{amazon_id}', we have {total_stock} in stock. Take it all!"
    }

@router.post("/delivery_status_by_name")
async def delivery_status_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    amazon_product = db.query(Amazon).filter(Amazon.name == name).first()
    if not amazon_product:
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
    amazon_id: str,
    db: Session = Depends(get_db)
):
    amazon_product = db.query(Amazon).filter(Amazon.amazon_id == amazon_id).first()
    if not amazon_product:
        raise HTTPException(status_code=404, detail="Product not found")

    status = random.choice([1, 0, -1])

    messages = {
        1: "Can be delivered today",
        0: "Deliverable",
        -1: "Not deliverable"
    }

    return {
        "message": f"Delivery status for book ID '{amazon_id}': {messages[status]}",
        "status_code": status
    }