from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine, SessionLocal
from app.models import flipkart_models
from app.models.flipkart_models import Flipkart, Price , Deliverable, Discount
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


@router.get("/id_or_name")
async def id_or_name_lookup(
    id: Optional[int] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Return product name given the ID, or ID given the name.
    At least one of the parameters ('id' or 'name') is required.
    """
    if not id and not name:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'name'")

    if id:
        product = db.query(Flipkart).filter(Flipkart.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product.id, "name": product.name}

    if name:
        product = db.query(Flipkart).filter(Flipkart.name == name).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product.id, "name": product.name}
@router.post("/get_price")
async def get_price(
    id: Optional[int] = None,  # Use int, as `Flipkart.id` is Integer
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

    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    # Deterministic mapping of product to price (as in your logic)
    price_id = (product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    return {
        "Flipkart_id": product.flipkart_id,
        "name": product.name,
        "unit_price": price_obj.price
    }

@router.post("/stock_by_id")
async def stock_by_id(
    id: str,
    db: Session = Depends(get_db)
):
    Flipkart_product = db.query(Flipkart).filter(Flipkart.id == id).first()
    if not Flipkart_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_stock = random.randint(5, 100)
    return total_stock


@router.post("/get_discount")
async def get_discount(
    id: int,  # Book ID is required
    quantity: int,  # Quantity is required
    db: Session = Depends(get_db)
):
    # Fetch the book by ID
    product = db.query(Flipkart).filter(Flipkart.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Fetch unit price for the book
    price_count = db.query(Price).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    # Determine the price_id (same logic as earlier)
    price_id = (product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    unit_price = price_obj.price
    total_price = unit_price * quantity

    # Find applicable discount
    discount = db.query(Discount).filter(
        Discount.cost_from <= total_price,
        Discount.cost_to > total_price
    ).first()

    percent = discount.percent_off if discount else 0
    reduced_amount = (percent / 100) * total_price
    payable_amount = total_price - reduced_amount

    return {
        "book_id": id,
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "total_price": round(total_price, 2),
        "discount_percent": percent,
        "reduced_amount": round(reduced_amount, 2),
        "payable_amount": round(payable_amount, 2)
    }


# @router.get("/get_books_from_flipakart")
# def get_books_from_flipakart():
#     return {
#         "flip_1": {
#             "name": "Clean Code",
#             "publisher": "Prentice Hall",
#             "genre": "Programming",
#             "subject_code": "CS101",
#             "serial_number": 3001
#         },
#         "flip_2": {
#             "name": "Python Crash Course",
#             "publisher": "No Starch Press",
#             "genre": "Programming",
#             "subject_code": "PY202",
#             "serial_number": 3002
#         },
#         "flip_3": {
#             "name": "Flipkart Daily Deal Book",
#             "publisher": "Flipkart Press",
#             "genre": "Special Offer",
#             "subject_code": "FD301",
#             "serial_number": 3003
#         },
#         "flip_4": {
#             "name": "E-commerce Strategies",
#             "publisher": "Digital Marketing Press",
#             "genre": "Business",
#             "subject_code": "EC401",
#             "serial_number": 3004
#         },
#         "flip_5": {
#             "name": "Budget Coding Books",
#             "publisher": "Affordable Press",
#             "genre": "Programming",
#             "subject_code": "BC501",
#             "serial_number": 3005
#         }
#     }