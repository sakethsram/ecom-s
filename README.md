# E-Commerce Multi-Store Management System

A FastAPI-based multi-store management system that supports Amazon, flipkart, and sapna bookstores with separate database management.

## Features

- **Multi-Store Support**: Amazon, flipkart, and sapna bookstores
- **Separate Databases**: Each store has its own MySQL/MariaDB database
- **Auto Database Creation**: Automatically creates databases and tables if they don't exist
- **RESTful APIs**: Complete CRUD operations for each store
- **Price Management**: Dynamic pricing system
- **Delivery Management**: Pincode-based delivery status
- **Discount System**: Quantity-based discount calculations
- **Stock Management**: Real-time stock availability

## Project Structure

```
ecom-s/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main FastAPI application
│   ├── database.py             # Database configuration and connections
│   ├── apis/                   # API endpoints
│   │   ├── amazon_api.py
│   │   ├── flipkart_api.py
│   │   └── sapna_api.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── amazon_models.py
│   │   ├── flipkart_models.py
│   │   └── sapna_models.py
│   └── schemas/                # Pydantic schemas and seed data
│       ├── amazon_schemas.py
│       ├── flipkart_schemas.py
│       └── sapna_schemas.py
├── requirements.txt
├── run.py                      # Application runner
└── README.md
```

## Database Configuration

The system uses three separate MariaDB/MySQL databases:

- `amazon_bookstore` - Amazon store data
- `flipkart_bookstore` - flipkart store data
- `sapna_bookstore` - sapna store data

### Database Tables (per store):

- `{store}_books` - Main product information
- `{store}_prices` - Pricing data
- `{store}_deliverables` - Delivery information by pincode
- `{store}_discounts` - Discount tiers

## Installation & Setup

### Prerequisites

- Python 3.8+
- MariaDB/MySQL Server
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ecom-s
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Make sure MariaDB/MySQL is running. The application will automatically:

- Create databases if they don't exist
- Create tables if they don't exist
- Seed initial data

### 4. Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost/amazon_bookstore
flipkart_DATABASE_URL=mysql+pymysql://root:your_password@localhost/flipkart_bookstore
sapna_DATABASE_URL=mysql+pymysql://root:your_password@localhost/sapna_bookstore
```

If not provided, defaults to `root:jnjnuh@localhost`

### 5. Run the Application

```bash
# Using run.py
python run.py

# Or directly with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Common Endpoints (Available for all stores: /amazon, /flipkart, /sapna)

#### Product Information

- `GET /{store}/name_from_id?id={id}` - Get product name by ID
- `GET /{store}/id_from_name?name={name}` - Get product ID by name

#### Pricing

- `POST /{store}/get_price` - Get product price by ID or name
- `POST /{store}/discount` - Calculate discount based on quantity

#### Inventory

- `POST /{store}/stock_by_id` - Get stock quantity by product ID

#### Delivery

- `POST /{store}/delivery_status` - Check delivery status by pincode

### Example Usage

```bash
# Get Amazon product price
curl -X POST "http://localhost:8000/amazon/get_price" \
  -H "Content-Type: application/json" \
  -d '{"book_name": "Python Crash Course"}'

# Check flipkart delivery status
curl -X POST "http://localhost:8000/flipkart/delivery_status" \
  -H "Content-Type: application/json" \
  -d '{"pincode": "110001"}'

# Calculate sapna discount
curl -X POST "http://localhost:8000/sapna/discount" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 3, "name": "Effective Java"}'
```

## Seed Data

Each store comes pre-loaded with:

- **12 Books** across categories (Python, Java, DSA, AI/ML)
- **Price tiers** from ₹599 to ₹2899
- **Delivery zones** with different delivery times
- **Discount slabs** based on order value

## Development

### Adding New Stores

1. Create new model file in `app/models/`
2. Create new schema file in `app/schemas/`
3. Create new API file in `app/apis/`
4. Add database configuration in `app/database.py`
5. Include router in `app/main.py`

### Database Schema Updates

- Models automatically create tables on first run
- For schema changes, consider using Alembic for migrations

## Troubleshooting

### Common Issues

1. **Database Connection Error**

   - Ensure MariaDB/MySQL is running
   - Check credentials in database.py or .env file
   - Verify database user has CREATE privileges

2. **Port Already in Use**

   - Change port in run.py or use: `uvicorn app.main:app --port 8001`

3. **Module Import Errors**
   - Ensure you're in the project root directory
   - Check Python path: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`

### Logs

Application logs are displayed in console with INFO level by default.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes.
