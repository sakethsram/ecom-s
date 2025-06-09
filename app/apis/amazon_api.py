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
        product = db.query(Amazon).filter(Amazon.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product.id, "name": product.name}

    if name:
        product = db.query(Amazon).filter(Amazon.name == name).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product.id, "name": product.name}
@router.post("/get_price")
async def get_price(
    id: Optional[int] = None,  # Use int, as `Amazon.id` is Integer
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

    price_count = db.query(AmazonPrice).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    # Deterministic mapping of product to price (as in your logic)
    price_id = (product.id % price_count) + 1
    price_obj = db.query(AmazonPrice).filter(AmazonPrice.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    return {
        "amazon_id": product.amazon_id,
        "name": product.name,
        "unit_price": price_obj.price
    }

@router.post("/stock_by_id")
async def stock_by_id(
    id: str,
    db: Session = Depends(get_db)
):
    amazon_product = db.query(Amazon).filter(Amazon.id == id).first()
    if not amazon_product:
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
    product = db.query(Amazon).filter(Amazon.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Fetch unit price for the book
    price_count = db.query(AmazonPrice).count()
    if price_count == 0:
        raise HTTPException(status_code=404, detail="No prices available")

    # Determine the price_id (same logic as earlier)
    price_id = (product.id % price_count) + 1
    price_obj = db.query(AmazonPrice).filter(AmazonPrice.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    unit_price = price_obj.price
    total_price = unit_price * quantity

    # Find applicable discount
    discount = db.query(AmazonDiscount).filter(
        AmazonDiscount.cost_from <= total_price,
        AmazonDiscount.cost_to > total_price
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

# @router.get("/get_books_from_amazon")
# def get_books_from_amazon():
#     return {
#         "amz_1": {
#             "name": "Clean Code",
#             "publisher": "Prentice Hall",
#             "genre": "Programming",
#             "subject_code": "CS101",
#             "serial_number": 1001
#         },
#         "amz_2": {
#             "name": "Python Crash Course",
#             "publisher": "No Starch Press",
#             "genre": "Programming",
#             "subject_code": "PY202",
#             "serial_number": 1002
#         },
#         "amz_3": {
#             "name": "Design Patterns",
#             "publisher": "Addison-Wesley",
#             "genre": "Software Engineering",
#             "subject_code": "CS305",
#             "serial_number": 1003
#         },
#         "amz_4": {
#             "name": "AWS Guide",
#             "publisher": "Amazon Publishing",
#             "genre": "Cloud Computing",
#             "subject_code": "CC401",
#             "serial_number": 1004
#         },
#         "amz_5": {
#             "name": "Amazon Exclusive Book",
#             "publisher": "AWS Press",
#             "genre": "Technology",
#             "subject_code": "AMZ501",
#             "serial_number": 1005
#         }
#     }