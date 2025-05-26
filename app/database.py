from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_if_not_exists(database_url, db_name):
    """Create database if it doesn't exist"""
    try:
        # Extract connection details without database name
        base_url = database_url.rsplit('/', 1)[0]
        # Create engine without database name
        temp_engine = create_engine(base_url, echo=False)
        with temp_engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
            if not result.fetchone():
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                logger.info(f"Database '{db_name}' created successfully")
            else:
                logger.info(f"Database '{db_name}' already exists")
        temp_engine.dispose()
    except Exception as e:
        logger.error(f"Error creating database '{db_name}': {e}")

# Database names
AMAZON_DB_NAME = "amazon_bookstore"
flipkart_DB_NAME = "flipkart_bookstore"
sapna_DB_NAME = "sapna_bookstore"

# === AMAZON DB Setup ===
AMAZON_DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+pymysql://root:jnjnuh@mysql/{AMAZON_DB_NAME}")
create_database_if_not_exists(AMAZON_DATABASE_URL, AMAZON_DB_NAME)
amazon_engine = create_engine(
    AMAZON_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)
AmazonSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=amazon_engine)

# === flipkart DB Setup ===
flipkart_DATABASE_URL = os.getenv("flipkart_DATABASE_URL", f"mysql+pymysql://root:jnjnuh@mysql/{flipkart_DB_NAME}")
create_database_if_not_exists(flipkart_DATABASE_URL, flipkart_DB_NAME)
flipkart_engine = create_engine(
    flipkart_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)
flipkartsessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=flipkart_engine)

# === sapna DB Setup ===
sapna_DATABASE_URL = os.getenv("sapna_DATABASE_URL", f"mysql+pymysql://root:jnjnuh@mysql/{sapna_DB_NAME}")
create_database_if_not_exists(sapna_DATABASE_URL, sapna_DB_NAME)
sapna_engine = create_engine(
    sapna_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)
sapnaSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sapna_engine)

# === Common Base ===
Base = declarative_base()

# === DB Getters ===
def get_db():
    """Default getter for Amazon DB (backward compatibility)"""
    db = AmazonSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_amazon_db():
    db = AmazonSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_flipkart_db():
    db = flipkartsessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_sapna_db():
    db = sapnaSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Export engines for use in model files
__all__ = ['Base', 'amazon_engine', 'flipkart_engine', 'sapna_engine',
           'get_db', 'get_amazon_db', 'get_flipkart_db', 'get_sapna_db',
           'AmazonSessionLocal', 'flipkartsessionlocal', 'sapnaSessionLocal']