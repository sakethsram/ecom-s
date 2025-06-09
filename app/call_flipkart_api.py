import random
import requests

BASE_URL = "http://localhost:8001/flipkart"

def get_id_and_name(name: str = None, id: int = None):
    params = {}
    if name:
        params["name"] = name
    elif id:
        params["id"] = id
    else:
        raise ValueError("Provide at least 'name' or 'id'")

    response = requests.get(f"{BASE_URL}/id_or_name", params=params)
    response.raise_for_status()
    return response.json()

def get_stock(product_id):
    response = requests.post(
        "http://localhost:8001/flipkart/stock_by_id",
        params={"id": product_id},
        data=""
    )
    response.raise_for_status()
    return response.json()
def get_price(product_id):
    response = requests.post(
        "http://localhost:8001/flipkart/get_price",
        params={"id": product_id},
        data=""
    )
    response.raise_for_status()
    return response.json()

def get_discount(id: int, quantity: int):
    response = requests.post(
        f"{BASE_URL}/get_discount",
        params={"id": id, "quantity": quantity},  # ✅ Correct way
        data={}  # add an empty body for POST if needed
    )
    response.raise_for_status()
    return response.json()


def main():
    product_info = get_id_and_name(id=1)
    product_id = product_info["id"]
    product_name = product_info["name"]
    print(f"✅ Book Info: ID={product_id}, Name={product_name}")

    stock = get_stock(product_id)
    print(f"✅ Stock Available: {stock}")

    price_info = get_price(product_id)
    print(f"✅ Unit Price: {price_info['unit_price']}")

    quantity_to_buy = min(stock, random.randint(1, stock))
    discount_info = get_discount(product_id, quantity_to_buy)
    print(f"✅ Discount Details for {quantity_to_buy} items:\n{discount_info}")

if __name__ == "__main__":
    main()
