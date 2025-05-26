from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class sapnaBase(BaseModel):
    name: str
    publisher: str
    genre: str
    subject_code: str
    serial_number: int

class sapnaCreate(sapnaBase):
    sapna_id: str

class sapna(sapnaBase):
    id: int
    sapna_id: str
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
SAPNA_SEED_DATA = [
    # Python books
    {'sapna_id': 'py_001', 'name': 'Python Crash Course', 'publisher': 'No Starch Press', 'genre': 'python', 'subject_code': 'py', 'serial_number': 1},
    {'sapna_id': 'py_002', 'name': 'Automate the Boring Stuff with Python', 'publisher': 'No Starch Press', 'genre': 'python', 'subject_code': 'py', 'serial_number': 2},
    {'sapna_id': 'py_003', 'name': 'Effective Python', 'publisher': 'Addison-Wesley', 'genre': 'python', 'subject_code': 'py', 'serial_number': 3},
    
    # Java books
    {'sapna_id': 'java_001', 'name': 'Java: The Complete Reference', 'publisher': 'Oracle Press', 'genre': 'java', 'subject_code': 'java', 'serial_number': 1},
    {'sapna_id': 'java_002', 'name': 'Effective Java', 'publisher': 'Addison-Wesley', 'genre': 'java', 'subject_code': 'java', 'serial_number': 2},
    {'sapna_id': 'java_003', 'name': 'Head First Java', 'publisher': "O'Reilly Media", 'genre': 'java', 'subject_code': 'java', 'serial_number': 3},
    
    # Data Structures and Algorithms books
    {'sapna_id': 'dsa_001', 'name': 'Introduction to Algorithms', 'publisher': 'MIT Press', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 1},
    {'sapna_id': 'dsa_002', 'name': 'Algorithms Unlocked', 'publisher': 'MIT Press', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 2},
    {'sapna_id': 'dsa_003', 'name': 'Data Structures and Algorithms in Python', 'publisher': 'Wiley', 'genre': 'data_structures_algorithms', 'subject_code': 'dsa', 'serial_number': 3},
    
    # Artificial Intelligence and Machine Learning books
    {'sapna_id': 'aiml_001', 'name': 'Hands-On Machine Learning', 'publisher': "O'Reilly Media", 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 1},
    {'sapna_id': 'aiml_002', 'name': 'Pattern Recognition and Machine Learning', 'publisher': 'Springer', 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 2},
    {'sapna_id': 'aiml_003', 'name': 'Deep Learning', 'publisher': 'MIT Press', 'genre': 'artificial_intelligence_machine_learning', 'subject_code': 'aiml', 'serial_number': 3},
]

PRICE_SEED_DATA = [
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

DELIVERABLE_SEED_DATA = [
    {'pincode': '110001', 'delivery_time': 2},  # 2 days
    {'pincode': '400001', 'delivery_time': 3},  # 3 days
    {'pincode': '560001', 'delivery_time': 4},  # 4 days
    {'pincode': '700001', 'delivery_time': 5},  # 5 days
    {'pincode': '600001', 'delivery_time': 3},  # 3 days
]

DISCOUNT_SEED_DATA = [
    {'cost_from': 0.0, 'cost_to': 800.0, 'percent_off': 0.0},
    {'cost_from': 800.0, 'cost_to': 1200.0, 'percent_off': 5.0},
    {'cost_from': 1200.0, 'cost_to': 1800.0, 'percent_off': 10.0},
    {'cost_from': 1800.0, 'cost_to': 2500.0, 'percent_off': 15.0},
    {'cost_from': 2500.0, 'cost_to': 10000.0, 'percent_off': 20.0},
]
