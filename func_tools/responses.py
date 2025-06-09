
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Tool,
    FunctionDeclaration
)
def get_book_search_tool():
    functions = declare_functions()
    book_search_tool = Tool(function_declarations=functions)
    return book_search_tool


def simulate_flipkart_api_response(book_title):
    """Simulate Flipkart API response - hardcoded response"""
    flipkart_books = {
        "flip_1": {
            "name": "Mastering Java",
            "publisher": "Prentice Hall",
            "genre": "Programming",
            "subject_code": "CS111",
            "serial_number": 3001
        },
        "flip_2": {
            "name": "The Algorithm Design Book",
            "publisher": "No Starch Press",
            "genre": "Programming",
            "subject_code": "AL202",
            "serial_number": 3002
        },
        "flip_3": {
            "name": "Flipkart Daily Deal Book",
            "publisher": "Flipkart Press",
            "genre": "Special Offer",
            "subject_code": "FD301",
            "serial_number": 3003
        },
        "flip_4": {
            "name": "E-commerce Strategies",
            "publisher": "Digital Marketing Press",
            "genre": "Business",
            "subject_code": "EC401",
            "serial_number": 3004
        },
        "flip_5": {
            "name": "Budget Coding Books",
            "publisher": "Affordable Press",
            "genre": "Programming",
            "subject_code": "BC501",
            "serial_number": 3005
        }
    }
    
    book_found = any(book_title.lower() in book["name"].lower() for book in flipkart_books.values())

    return {
        "status": "found" if book_found else "not_found",
        "message": f"Book '{book_title}' {'found' if book_found else 'not available'} on Flipkart",
        "books": flipkart_books
    }

def simulate_amazon_api_response(book_title):
    """Simulate Amazon API response - hardcoded response"""
    amazon_books = {
        "amz_1": {
            "name": "Clean Code",
            "publisher": "Prentice Hall",
            "genre": "Programming",
            "subject_code": "CS101",
            "serial_number": 1001
        },
        "amz_2": {
            "name": "Python Crash Course",
            "publisher": "No Starch Press",
            "genre": "Programming",
            "subject_code": "PY202",
            "serial_number": 1002
        },
        "amz_3": {
            "name": "Design Patterns",
            "publisher": "Addison-Wesley",
            "genre": "Software Engineering",
            "subject_code": "CS305",
            "serial_number": 1003
        },
        "amz_4": {
            "name": "AWS Guide",
            "publisher": "Amazon Publishing",
            "genre": "Cloud Computing",
            "subject_code": "CC401",
            "serial_number": 1004
        },
        "amz_5": {
            "name": "Amazon Exclusive Book",
            "publisher": "AWS Press",
            "genre": "Technology",
            "subject_code": "AMZ501",
            "serial_number": 1005
        }
    }

    book_found = any(book_title.lower() in book["name"].lower() for book in amazon_books.values())

    return {
        "status": "found" if book_found else "not_found",
        "message": f"Book '{book_title}' {'found' if book_found else 'not available'} on Amazon",
        "books": amazon_books
    }

def simulate_sapna_api_response(book_title):
    """Simulate Sapna API response - hardcoded response"""
    sapna_books = {
        "sapna_1": {
            "name": "The Art of Debugging",
            "publisher": "Prentice Hall",
            "genre": "Programming",
            "subject_code": "CS151",
            "serial_number": 2001
        },
        "sapna_2": {
            "name": "JavaScript Essentials",
            "publisher": "No Starch Press",
            "genre": "Programming",
            "subject_code": "JS202",
            "serial_number": 2002
        },
        "sapna_3": {
            "name": "Kannada Programming Book",
            "publisher": "Sapna House",
            "genre": "Regional",
            "subject_code": "KN401",
            "serial_number": 2003
        },
        "sapna_4": {
            "name": "SAPNA Special Edition",
            "publisher": "Sapna Publications",
            "genre": "Collection",
            "subject_code": "SP501",
            "serial_number": 2004
        },
        "sapna_5": {
            "name": "Regional Coding Patterns",
            "publisher": "Local Tech Press",
            "genre": "Programming",
            "subject_code": "RP601",
            "serial_number": 2005
        }
    }

    book_found = any(book_title.lower() in book["name"].lower() for book in sapna_books.values())

    return {
        "status": "found" if book_found else "not_found",
        "message": f"Book '{book_title}' {'found' if book_found else 'not available'} on Sapna",
        "books": sapna_books
    }

def declare_functions():
    get_books_from_amazon = FunctionDeclaration(
        name="get_books_from_amazon",
        description="Tell user to call @router.get('/get_books_from_amazon') - PRIMARY store, check first",
        parameters={
            "type": "object",
            "properties": {
                "book_title": {"type": "string", "description": "Title of the book to search"}
            },
            "required": ["book_title"]
        },
    )

    get_books_from_flipkart = FunctionDeclaration(
        name="get_books_from_flipkart", 
        description="Tell user to call @router.get('/get_books_from_flipkart') - SECONDARY store, only if Amazon fails",
        parameters={
            "type": "object",
            "properties": {
                "book_title": {"type": "string", "description": "Title of the book to search"}
            },
            "required": ["book_title"]
        },
    )

    get_books_from_sapna = FunctionDeclaration(
        name="get_books_from_sapna",
        description="Tell user to call @router.get('/get_books_from_sapna') - LAST RESORT store only",
        parameters={
            "type": "object", 
            "properties": {
                "book_title": {"type": "string", "description": "Title of the book to search"}
            },
            "required": ["book_title"]
        },
    )

    return [get_books_from_amazon, get_books_from_flipkart, get_books_from_sapna]