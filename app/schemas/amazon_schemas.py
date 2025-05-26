from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AmazonBase(BaseModel):
    name: str
    publisher: str
    genre: str
    subject_code: str
    serial_number: int

class AmazonCreate(AmazonBase):
    amazon_id: str

class Amazon(AmazonBase):
    id: int
    amazon_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class AmazonPriceBase(BaseModel):  # Added Amazon prefix
    price: float

class AmazonPriceCreate(AmazonPriceBase):  # Added Amazon prefix
    pass

class AmazonPrice(AmazonPriceBase):  # Added Amazon prefix
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AmazonDeliverableBase(BaseModel):  # Added Amazon prefix
    pincode: str
    delivery_time: int

class AmazonDeliverableCreate(AmazonDeliverableBase):  # Added Amazon prefix
    pass

class AmazonDeliverable(AmazonDeliverableBase):  # Added Amazon prefix
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AmazonDiscountBase(BaseModel):  # Added Amazon prefix
    cost_from: float
    cost_to: float
    percent_off: float

class AmazonDiscountCreate(AmazonDiscountBase):  # Added Amazon prefix
    pass

class AmazonDiscount(AmazonDiscountBase):  # Added Amazon prefix
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Amazon Seeding data - Insert only once
AMAZON_SEED_DATA = [
    # Python books
    {'amazon_id': 'amazon_py_001', 'name': 'Python Crash Course', 'publisher': 'No Starch Press', 'genre': 'python', 'subject_code': 'py', 'serial_number': 1},
    {'amazon_id': 'amazon_py_002', 'name': 'Automate the Boring Stuff with Python', 'publisher': 'No Starch Press', 'genre': 'python', 'subject_code': 'py', 'serial_number': 2},
    {'amazon_id': 'amazon_py_003', 'name': 'Effective Python', 'publisher': 'Addison-Wesley', 'genre': 'python', 'subject_code': 'py', 'serial_number': 3},

    # Java books
    {'amazon_id': 'amazon_java_001', 'name': 'Java: The Complete Reference', 'publisher': 'Oracle Press', 'genre': 'java', 'subject_code': 'java', 'serial_number': 1},
    {'amazon_id': 'amazon_java_002', 'name': 'Effective Java', 'publisher': 'Addison-Wesley', 'genre': 'java', 'subject_code': 'java', 'serial_number': 2},
    {'amazon_id': 'amazon_java_003', 'name': 'Head First Java', 'publisher': "O'Reilly Media", 'genre': 'java', 'subject_code': 'java', 'serial_number': 3},

    # Data Structures and Algorithms books
    {'amazon_id': 'amazon_dsa_001', 'name': 'Introduction to Algorithms', 'publisher': 'MIT Press', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 1},
    {'amazon_id': 'amazon_dsa_002', 'name': 'Algorithms Unlocked', 'publisher': 'MIT Press', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 2},
    {'amazon_id': 'amazon_dsa_003', 'name': 'Data Structures and Algorithms in Python', 'publisher': 'Wiley', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 3},

    # Artificial Intelligence and Machine Learning books
    {'amazon_id': 'amazon_aiml_001', 'name': 'Hands-On Machine Learning', 'publisher': "O'Reilly Media", 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 1},
    {'amazon_id': 'amazon_aiml_002', 'name': 'Pattern Recognition and Machine Learning', 'publisher': 'Springer', 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 2},
    {'amazon_id': 'amazon_aiml_003', 'name': 'Deep Learning', 'publisher': 'MIT Press', 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 3},
]

AMAZON_PRICE_SEED_DATA = [  # Added Amazon prefix
    {'id': 1, 'price': 599.99},
    {'id': 2, 'price': 799.99},
    {'id': 3, 'price': 999.99},
    {'id': 4, 'price': 1299.99},
    {'id': 5, 'price': 1499.99},
    {'id': 6, 'price': 1699.99},
    {'id': 7, 'price': 1899.99},
    {'id': 8, 'price': 2099.99},
    {'id': 9, 'price': 2299.99},
    {'id': 10, 'price': 2499.99},
    {'id': 11, 'price': 2699.99},
    {'id': 12, 'price': 2899.99},
]

AMAZON_DELIVERABLE_SEED_DATA = [  # Added Amazon prefix
    {'pincode': '110001', 'delivery_time': 2},  # 2 days
    {'pincode': '400001', 'delivery_time': 3},  # 3 days
    {'pincode': '560001', 'delivery_time': 4},  # 4 days
    {'pincode': '700001', 'delivery_time': 5},  # 5 days
    {'pincode': '600001', 'delivery_time': 3},  # 3 days
]

AMAZON_DISCOUNT_SEED_DATA = [  # Added Amazon prefix
    {'cost_from': 0.0, 'cost_to': 800.0, 'percent_off': 0.0},
    {'cost_from': 800.0, 'cost_to': 1200.0, 'percent_off': 5.0},
    {'cost_from': 1200.0, 'cost_to': 1800.0, 'percent_off': 10.0},
    {'cost_from': 1800.0, 'cost_to': 2500.0, 'percent_off': 15.0},
    {'cost_from': 2500.0, 'cost_to': 10000.0, 'percent_off': 20.0},
]