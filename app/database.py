from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# === AMAZON DB Setup ===
AMAZON_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    AMAZON_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# === FLIPKART DB Setup ===
FLIPKART_DATABASE_URL = os.getenv("FLIPKART_DATABASE_URL")

flipkart_engine = create_engine(
    FLIPKART_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)
FlipkartSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=flipkart_engine)

# === SAPNA DB Setup ===
SAPNA_DATABASE_URL = os.getenv("SAPNA_DATABASE_URL")

sapna_engine = create_engine(
    SAPNA_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)
SapnaSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sapna_engine)

# === Common Base ===
Base = declarative_base()

# === DB Getters ===
def get_db():
    """Default getter for Amazon DB (backward compatibility)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_amazon_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_flipkart_db():
    db = FlipkartSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sapna_db():
    db = SapnaSessionLocal()
    try:
        yield db
    finally:
        db.close()
