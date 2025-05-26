from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class flipkartBase(BaseModel):
    name: str
    publisher: str
    genre: str
    subject_code: str
    serial_number: int

class flipkartCreate(flipkartBase):
    flipkart_id: str

class flipkart(flipkartBase):
    id: int
    flipkart_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class PriceBase(BaseModel):
    price: float

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DeliverableBase(BaseModel):
    pincode: str
    delivery_time: int

class DeliverableCreate(DeliverableBase):
    pass

class Deliverable(DeliverableBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DiscountBase(BaseModel):
    cost_from: float
    cost_to: float
    percent_off: float

class DiscountCreate(DiscountBase):
    pass

class Discount(DiscountBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
# Seeding data - Insert only once
flipkart_SEED_DATA = [
    # Python books
    {'flipkart_id': 'py_001', 'name': 'Python Crash Course', 'publisher': 'No Starch Press', 'genre': 'python', 'subject_code': 'py', 'serial_number': 1, 'price': 579.99},
    {'flipkart_id': 'py_002', 'name': 'Automate the Boring Stuff with Python', 'publisher': 'No Starch Press', 'genre': 'python', 'subject_code': 'py', 'serial_number': 2, 'price': 759.99},
    {'flipkart_id': 'py_003', 'name': 'Effective Python', 'publisher': 'Addison-Wesley', 'genre': 'python', 'subject_code': 'py', 'serial_number': 3, 'price': 949.99},

    # Java books
    {'flipkart_id': 'java_001', 'name': 'Java: The Complete Reference', 'publisher': 'Oracle Press', 'genre': 'java', 'subject_code': 'java', 'serial_number': 1, 'price': 1249.99},
    {'flipkart_id': 'java_002', 'name': 'Effective Java', 'publisher': 'Addison-Wesley', 'genre': 'java', 'subject_code': 'java', 'serial_number': 2, 'price': 1429.99},
    {'flipkart_id': 'java_003', 'name': 'Head First Java', 'publisher': "O'Reilly Media", 'genre': 'java', 'subject_code': 'java', 'serial_number': 3, 'price': 1629.99},

    # Data Structures and Algorithms books
    {'flipkart_id': 'dsa_001', 'name': 'Introduction to Algorithms', 'publisher': 'MIT Press', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 1, 'price': 1819.99},
    {'flipkart_id': 'dsa_002', 'name': 'Algorithms Unlocked', 'publisher': 'MIT Press', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 2, 'price': 2019.99},
    {'flipkart_id': 'dsa_003', 'name': 'Data Structures and Algorithms in Python', 'publisher': 'Wiley', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 3, 'price': 2219.99},

    # Artificial Intelligence and Machine Learning books
    {'flipkart_id': 'aiml_001', 'name': 'Hands-On Machine Learning', 'publisher': "O'Reilly Media", 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 1, 'price': 2399.99},
    {'flipkart_id': 'aiml_002', 'name': 'Pattern Recognition and Machine Learning', 'publisher': 'Springer', 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 2, 'price': 2599.99},
    {'flipkart_id': 'aiml_003', 'name': 'Deep Learning', 'publisher': 'MIT Press', 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 3, 'price': 2799.99},
]

PRICE_SEED_DATA = [
    {'id': 1, 'price': 579.99},
    {'id': 2, 'price': 759.99},
    {'id': 3, 'price': 949.99},
    {'id': 4, 'price': 1249.99},
    {'id': 5, 'price': 1429.99},
    {'id': 6, 'price': 1629.99},
    {'id': 7, 'price': 1819.99},
    {'id': 8, 'price': 2019.99},
    {'id': 9, 'price': 2219.99},
    {'id': 10, 'price': 2399.99},
    {'id': 11, 'price': 2599.99},
    {'id': 12, 'price': 2799.99},
]

DELIVERABLE_SEED_DATA = [
    {'pincode': '110001', 'delivery_time': 1},  # Same day
    {'pincode': '400001', 'delivery_time': 2},  # 2 days
    {'pincode': '560001', 'delivery_time': 3},  # 3 days
    {'pincode': '700001', 'delivery_time': 4},  # 4 days
    {'pincode': '600001', 'delivery_time': 2},  # 2 days
    {'pincode': '110002', 'delivery_time': 1},  # Same day delivery
    {'pincode': '400002', 'delivery_time': 1},  # Same day delivery
    {'pincode': '560002', 'delivery_time': 2},  # 2 days
    {'pincode': '700002', 'delivery_time': 3},  # 3 days
    {'pincode': '600002', 'delivery_time': 2},  # 2 days
]

DISCOUNT_SEED_DATA = [
    {'cost_from': 0.0, 'cost_to': 750.0, 'percent_off': 0.0},
    {'cost_from': 750.0, 'cost_to': 1150.0, 'percent_off': 7.0},
    {'cost_from': 1150.0, 'cost_to': 1750.0, 'percent_off': 12.0},
    {'cost_from': 1750.0, 'cost_to': 2400.0, 'percent_off': 18.0},
    {'cost_from': 2400.0, 'cost_to': 10000.0, 'percent_off': 25.0},
]