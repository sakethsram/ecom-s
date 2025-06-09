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
        print("sapna database seeded successfully!")

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
    return {"message": "sapna Management System API - All endpoints ready!"}


@router.get("/id_or_name")
async def id_or_name_lookup(
    id: Optional[int] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_sapna_db)
):
    """
    Return product name given the ID, or ID given the name.
    At least one of the parameters ('id' or 'name') is required.
    """
    if not id and not name:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'name'")

    if id:
        product = db.query(sapna).filter(sapna.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product.id, "name": product.name}

    if name:
        product = db.query(sapna).filter(sapna.name == name).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product.id, "name": product.name}
@router.post("/get_price")
async def get_price(
    id: Optional[int] = None,  # Use int, as `sapna.id` is Integer
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

    # Deterministic mapping of product to price (as in your logic)
    price_id = (product.id % price_count) + 1
    price_obj = db.query(Price).filter(Price.id == price_id).first()

    if not price_obj:
        raise HTTPException(status_code=404, detail="Price not found")

    return {
        "sapna_id": product.sapna_id,
        "name": product.name,
        "unit_price": price_obj.price
    }

@router.post("/stock_by_id")
async def stock_by_id(
    id: str,
    db: Session = Depends(get_sapna_db)
):
    Sapna_product = db.query(sapna).filter(sapna.id == id).first()
    if not Sapna_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_stock = random.randint(5, 100)
    return total_stock


@router.post("/get_discount")
async def get_discount(
    id: int,  # Book ID is required
    quantity: int,  # Quantity is required
    db: Session = Depends(get_sapna_db)
):
    # Fetch the book by ID
    product = db.query(sapna).filter(sapna.id == id).first()
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


# @router.get("/get_books_from_sapna")
# def get_books_from_sapna():
#     return {
#         "sapna_1": {
#             "name": "Clean Code",
#             "publisher": "Prentice Hall",
#             "genre": "Programming",
#             "subject_code": "CS101",
#             "serial_number": 2001
#         },
#         "sapna_2": {
#             "name": "Python Crash Course",
#             "publisher": "No Starch Press",
#             "genre": "Programming",
#             "subject_code": "PY202",
#             "serial_number": 2002
#         },
#         "sapna_3": {
#             "name": "Kannada Programming Book",
#             "publisher": "sapna House",
#             "genre": "Regional",
#             "subject_code": "KN401",
#             "serial_number": 2003
#         },
#         "sapna_4": {
#             "name": "SAPNA Special Edition",
#             "publisher": "sapna Publications",
#             "genre": "Collection",
#             "subject_code": "SP501",
#             "serial_number": 2004
#         },
#         "sapna_5": {
#             "name": "Regional Coding Patterns",
#             "publisher": "Local Tech Press",
#             "genre": "Programming",
#             "subject_code": "RP601",
#             "serial_number": 2005
#         }
#     }