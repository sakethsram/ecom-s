"""
Combined Database Initialization Script for Amazon, Sapna, and Flipkart
Run this after creating your database to set up tables and seed initial data
"""

from app.database import Base, engine, SessionLocal

# Amazon imports
from app.models.amazon_models import Amazon, AmazonPrice, AmazonDeliverable, AmazonDiscount
from app.schemas.amazon_schemas import (
    AMAZON_SEED_DATA,
    AMAZON_PRICE_SEED_DATA,
    AMAZON_DELIVERABLE_SEED_DATA,
    AMAZON_DISCOUNT_SEED_DATA
)

# # Sapna imports
# from app.models.sapna_models import sapna, Price as SapnaPrice, Deliverable as SapnaDeliverable, Discount as SapnaDiscount
# from app.schemas.sapna_schemas import (
#     sapna_SEED_DATA,
#     PRICE_SEED_DATA as SAPNA_PRICE_SEED_DATA,
#     DELIVERABLE_SEED_DATA as SAPNA_DELIVERABLE_SEED_DATA,
#     DISCOUNT_SEED_DATA as SAPNA_DISCOUNT_SEED_DATA
# )

# Flipkart imports
from app.models.flipkart_models import flipkart, Price as FlipkartPrice, Deliverable as FlipkartDeliverable, Discount as FlipkartDiscount
from app.schemas.flipkart_schemas import (
    FLIPKART_SEED_DATA,
    PRICE_SEED_DATA as FLIPKART_PRICE_SEED_DATA,
    DELIVERABLE_SEED_DATA as FLIPKART_DELIVERABLE_SEED_DATA,
    DISCOUNT_SEED_DATA as FLIPKART_DISCOUNT_SEED_DATA
)

def create_all_tables():
    """Create all database tables"""
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

    print("\nCreated tables:")
    print("- amazon_books")
    print("- amazon_prices") 
    print("- amazon_deliverables")
    print("- amazon_discounts")

    # print("- sapna_books")
    # print("- sapna_prices")
    # print("- sapna_deliverables")
    # print("- sapna_discounts")

    print("- flipkart_books")
    print("- flipkart_prices")
    print("- flipkart_deliverables")
    print("- flipkart_discounts")


def seed_all_data():
    """Seed all database tables"""
    db = SessionLocal()
    try:
        print("\nSeeding all databases...")

        # Amazon seeding
        if db.query(Amazon).count() == 0:
            print("Seeding Amazon products...")
            for item in AMAZON_SEED_DATA:
                db.add(Amazon(**item))
            print(f"✅ Added {len(AMAZON_SEED_DATA)} Amazon products")

        if db.query(AmazonPrice).count() == 0:
            print("Seeding Amazon prices...")
            for item in AMAZON_PRICE_SEED_DATA:
                db.add(AmazonPrice(**item))
            print(f"✅ Added {len(AMAZON_PRICE_SEED_DATA)} Amazon prices")

        if db.query(AmazonDeliverable).count() == 0:
            print("Seeding Amazon deliverables...")
            for item in AMAZON_DELIVERABLE_SEED_DATA:
                db.add(AmazonDeliverable(**item))
            print(f"✅ Added {len(AMAZON_DELIVERABLE_SEED_DATA)} Amazon deliverables")

        if db.query(AmazonDiscount).count() == 0:
            print("Seeding Amazon discounts...")
            for item in AMAZON_DISCOUNT_SEED_DATA:
                db.add(AmazonDiscount(**item))
            print(f"✅ Added {len(AMAZON_DISCOUNT_SEED_DATA)} Amazon discounts")

        # # Sapna seeding
        # if db.query(sapna).count() == 0:
        #     print("Seeding Sapna products...")
        #     for item in sapna_SEED_DATA:
        #         db.add(sapna(**item))
        #     print(f"✅ Added {len(sapna_SEED_DATA)} Sapna products")

        # if db.query(SapnaPrice).count() == 0:
        #     print("Seeding Sapna prices...")
        #     for item in SAPNA_PRICE_SEED_DATA:
        #         db.add(SapnaPrice(**item))
        #     print(f"✅ Added {len(SAPNA_PRICE_SEED_DATA)} Sapna prices")

        # if db.query(SapnaDeliverable).count() == 0:
        #     print("Seeding Sapna deliverables...")
        #     for item in SAPNA_DELIVERABLE_SEED_DATA:
        #         db.add(SapnaDeliverable(**item))
        #     print(f"✅ Added {len(SAPNA_DELIVERABLE_SEED_DATA)} Sapna deliverables")

        # if db.query(SapnaDiscount).count() == 0:
        #     print("Seeding Sapna discounts...")
        #     for item in SAPNA_DISCOUNT_SEED_DATA:
        #         db.add(SapnaDiscount(**item))
        #     print(f"✅ Added {len(SAPNA_DISCOUNT_SEED_DATA)} Sapna discounts")

        # Flipkart seeding
        if db.query(flipkart).count() == 0:
            print("Seeding Flipkart products...")
            for item in FLIPKART_SEED_DATA:
                db.add(flipkart(**item))
            print(f"✅ Added {len(FLIPKART_SEED_DATA)} Flipkart products")

        if db.query(FlipkartPrice).count() == 0:
            print("Seeding Flipkart prices...")
            for item in FLIPKART_PRICE_SEED_DATA:
                db.add(FlipkartPrice(**item))
            print(f"✅ Added {len(FLIPKART_PRICE_SEED_DATA)} Flipkart prices")

        if db.query(FlipkartDeliverable).count() == 0:
            print("Seeding Flipkart deliverables...")
            for item in FLIPKART_DELIVERABLE_SEED_DATA:
                db.add(FlipkartDeliverable(**item))
            print(f"✅ Added {len(FLIPKART_DELIVERABLE_SEED_DATA)} Flipkart deliverables")

        if db.query(FlipkartDiscount).count() == 0:
            print("Seeding Flipkart discounts...")
            for item in FLIPKART_DISCOUNT_SEED_DATA:
                db.add(FlipkartDiscount(**item))
            print(f"✅ Added {len(FLIPKART_DISCOUNT_SEED_DATA)} Flipkart discounts")

        db.commit()
        print("\n✅ All databases seeded successfully!")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise e
    finally:
        db.close()


def main():
    """Main initializer"""
    try:
        create_all_tables()
        seed_all_data()
        print("\n🎉 All databases initialized and seeded successfully!")
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        raise e


if __name__ == "__main__":
    main()
