import requests
from datetime import datetime, timezone
import json
local = 0
if local:
    BASE_URL = "http://127.0.0.1:8000"
else:
    BASE_URL = "http://54.237.161.55:8000"

def test_create_stringing_order():
    order_data = {
        "sport": "Tennis",
        "racket_model": "Wilson Pro Staff",
        "string": "Luxilon ALU Power",
        "tension": "55",
        "pickup_date": "2024-10-28T22:07:38.884962+00:00",
        "notes": "Please string at 55 lbs",
        "price": 20.0
    }
    
    response = requests.post(
        f"{BASE_URL}/orders/order_stringing",
        json=order_data
    )
    print("\nCreate stringing order response status:", response.status_code)
    print("Response data:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        return response.json().get('id')
    return None

def test_get_order(order_id="fefc7837-fc6e-49b5-93ce-005d09f5f7a2"):
    response = requests.get(f"{BASE_URL}/orders/orders/{order_id}")
    print("\nGet order response status:", response.status_code)
    print("Response data:")
    print(json.dumps(response.json(), indent=2))

def test_get_all_orders():
    params = {
        "sport": "Tennis",
        "order_status": "pending",
        "skip": 0,
        "limit": 10
    }
    response = requests.get(f"{BASE_URL}/orders", params=params)
    print("\nGet all orders response status:", response.status_code)
    print("Response data:")
    print(json.dumps(response.json(), indent=2))

def test_update_order(order_id="fefc7837-fc6e-49b5-93ce-005d09f5f7a2"):
    update_data = {
        "string": "",
        "tension": "",
        "racket_model": "",
        "notes": "Please deliver between 9 am and 12 pm.",
        "order_status": "pending",
        "updated_at": "2024-09-29T22:11:44",
        "sport": "",
        "pickup_date": "2024-11-29T22:11:44",
        "price": 1,
        "created_at": "2024-09-29T22:11:44"
    }
    
    response = requests.put(
        f"{BASE_URL}/orders/orders/{order_id}",
        json=update_data
    )
    print("\nUpdate order response status:", response.status_code)
    print("Response data:")
    print(json.dumps(response.json(), indent=2))

def test_delete_order(order_id="fefc7837-fc6e-49b5-93ce-005d09f5f7a2"):
    response = requests.delete(f"{BASE_URL}/orders/orders/{order_id}")
    print("\nDelete order response status:", response.status_code)
    print("Response data:")
    print(json.dumps(response.json(), indent=2))

def run_all_tests():
    print("===== Starting API Tests =====")
    order_id = '565c7269-4490-40fa-a45f-f6e27002e844'
    try:
        print("\nTesting Get All Orders...")
        test_get_all_orders()
        
        print("\nTesting Create Stringing Order...")
        new_order_id = test_create_stringing_order()
        
        print("\nTesting Get Specific Order...")
        test_get_order(order_id)
        
        print("\nTesting Update Order...")
        test_update_order(order_id)
        
        print("\nTesting Delete Order...")
        test_delete_order(order_id)
        
    except requests.exceptions.RequestException as e:
        print(f"\nError occurred during testing: {e}")
    
    print("\n===== API Tests Completed =====")

def run_single_test():
    print("===== Starting Single Test =====")
    
    try:
        test_get_order()
        
    except requests.exceptions.RequestException as e:
        print(f"\nError occurred during testing: {e}")
    
    print("\n===== Single Test Completed =====")

if __name__ == "__main__":
    run_all_tests()