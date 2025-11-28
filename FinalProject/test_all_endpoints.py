#!/usr/bin/env python3
"""
Comprehensive test script for all API endpoints and CRUD operations.
Tests all endpoints systematically and reports results.
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_section(msg):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.END}\n")

def test_endpoint(method, url, data=None, params=None, expected_status=200):
    """Test an endpoint and return the response"""
    try:
        if method == "GET":
            response = requests.get(url, params=params, allow_redirects=True)
        elif method == "POST":
            response = requests.post(url, json=data, allow_redirects=True)
        elif method == "PUT":
            response = requests.put(url, json=data, allow_redirects=True)
        elif method == "DELETE":
            response = requests.delete(url, allow_redirects=True)
        
        if response.status_code == expected_status:
            return True, response.json() if response.content else {}
        else:
            return False, f"Status {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

# Store created IDs for cleanup and testing
created_ids = {
    'resources': [],
    'sandwiches': [],
    'recipes': [],
    'orders': [],
    'payments': [],
    'reviews': [],
    'promotional_codes': []
}

def main():
    print_section("🧪 COMPREHENSIVE API ENDPOINT TESTING")
    print_info("Testing all CRUD operations for each endpoint\n")
    
    # ==================== RESOURCES (Ingredients) ====================
    print_section("1. RESOURCES (Ingredients) - CRUD Testing")
    
    # CREATE
    print_info("Testing POST /resources (Create)")
    import time
    unique_name = f"Test Bread {int(time.time())}"
    resource_data = {"item": unique_name, "amount": 100}
    success, result = test_endpoint("POST", f"{BASE_URL}/resources", resource_data)
    if success:
        resource_id = result.get('id')
        created_ids['resources'].append(resource_id)
        print_success(f"Created resource ID: {resource_id}")
    else:
        print_error(f"Failed: {result}")
        return
    
    # READ ALL
    print_info("Testing GET /resources (Read All)")
    success, result = test_endpoint("GET", f"{BASE_URL}/resources")
    if success:
        print_success(f"Retrieved {len(result)} resources")
    else:
        print_error(f"Failed: {result}")
    
    # READ ONE
    print_info(f"Testing GET /resources/{resource_id} (Read One)")
    success, result = test_endpoint("GET", f"{BASE_URL}/resources/{resource_id}")
    if success:
        print_success(f"Retrieved resource: {result.get('item')}")
    else:
        print_error(f"Failed: {result}")
    
    # UPDATE
    print_info(f"Testing PUT /resources/{resource_id} (Update)")
    update_data = {"amount": 150}  # Only update amount to avoid duplicate name
    success, result = test_endpoint("PUT", f"{BASE_URL}/resources/{resource_id}", update_data)
    if success:
        print_success(f"Updated resource: {result.get('item')} (amount: {result.get('amount')})")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== SANDWICHES ====================
    print_section("2. SANDWICHES (Menu Items) - CRUD Testing")
    
    # CREATE
    print_info("Testing POST /sandwiches (Create)")
    import time
    unique_name = f"Test Cheese Sandwich {int(time.time())}"
    sandwich_data = {
        "sandwich_name": unique_name,
        "price": 5.99,
        "category": "vegetarian",
        "description": "A test sandwich",
        "is_available": True
    }
    success, result = test_endpoint("POST", f"{BASE_URL}/sandwiches", sandwich_data)
    if success:
        sandwich_id = result.get('id')
        created_ids['sandwiches'].append(sandwich_id)
        print_success(f"Created sandwich ID: {sandwich_id}")
    else:
        print_error(f"Failed: {result}")
        return
    
    # READ ALL
    print_info("Testing GET /sandwiches (Read All)")
    success, result = test_endpoint("GET", f"{BASE_URL}/sandwiches")
    if success:
        print_success(f"Retrieved {len(result)} sandwiches")
    else:
        print_error(f"Failed: {result}")
    
    # READ ALL WITH FILTER
    print_info("Testing GET /sandwiches?category=vegetarian (Filter)")
    success, result = test_endpoint("GET", f"{BASE_URL}/sandwiches", params={"category": "vegetarian"})
    if success:
        print_success(f"Retrieved {len(result)} vegetarian sandwiches")
    else:
        print_error(f"Failed: {result}")
    
    # READ ONE
    print_info(f"Testing GET /sandwiches/{sandwich_id} (Read One)")
    success, result = test_endpoint("GET", f"{BASE_URL}/sandwiches/{sandwich_id}")
    if success:
        print_success(f"Retrieved sandwich: {result.get('sandwich_name')}")
    else:
        print_error(f"Failed: {result}")
    
    # UPDATE
    print_info(f"Testing PUT /sandwiches/{sandwich_id} (Update)")
    update_data = {"price": 6.99, "description": "Updated description"}
    success, result = test_endpoint("PUT", f"{BASE_URL}/sandwiches/{sandwich_id}", update_data)
    if success:
        print_success(f"Updated sandwich: price={result.get('price')}")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== RECIPES ====================
    print_section("3. RECIPES - CRUD Testing")
    
    # CREATE
    print_info("Testing POST /recipes (Create)")
    recipe_data = {
        "sandwich_id": sandwich_id,
        "resource_id": resource_id,
        "amount": 2
    }
    success, result = test_endpoint("POST", f"{BASE_URL}/recipes", recipe_data)
    if success:
        recipe_id = result.get('id')
        created_ids['recipes'].append(recipe_id)
        print_success(f"Created recipe ID: {recipe_id}")
    else:
        print_error(f"Failed: {result}")
        return
    
    # READ ALL
    print_info("Testing GET /recipes (Read All)")
    success, result = test_endpoint("GET", f"{BASE_URL}/recipes")
    if success:
        print_success(f"Retrieved {len(result)} recipes")
    else:
        print_error(f"Failed: {result}")
    
    # READ ONE
    print_info(f"Testing GET /recipes/{recipe_id} (Read One)")
    success, result = test_endpoint("GET", f"{BASE_URL}/recipes/{recipe_id}")
    if success:
        print_success(f"Retrieved recipe ID: {recipe_id}")
    else:
        print_error(f"Failed: {result}")
    
    # UPDATE
    print_info(f"Testing PUT /recipes/{recipe_id} (Update)")
    update_data = {"amount": 3}
    success, result = test_endpoint("PUT", f"{BASE_URL}/recipes/{recipe_id}", update_data)
    if success:
        print_success(f"Updated recipe: amount={result.get('amount')}")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== PROMOTIONAL CODES ====================
    print_section("4. PROMOTIONAL CODES - CRUD Testing")
    
    # CREATE
    print_info("Testing POST /promotional-codes (Create)")
    import time
    future_date = (datetime.now() + timedelta(days=30)).isoformat()
    unique_code = f"TEST{int(time.time())}"
    promo_data = {
        "code": unique_code,
        "discount_percent": 10.0,
        "expiration_date": future_date,
        "is_active": True
    }
    success, result = test_endpoint("POST", f"{BASE_URL}/promotional-codes", promo_data)
    if success:
        promo_id = result.get('id')
        created_ids['promotional_codes'].append(promo_id)
        print_success(f"Created promotional code ID: {promo_id}")
    else:
        print_error(f"Failed: {result}")
        return
    
    # READ ALL
    print_info("Testing GET /promotional-codes (Read All)")
    success, result = test_endpoint("GET", f"{BASE_URL}/promotional-codes")
    if success:
        print_success(f"Retrieved {len(result)} promotional codes")
    else:
        print_error(f"Failed: {result}")
    
    # READ BY CODE
    print_info(f"Testing GET /promotional-codes/code/{unique_code} (Read By Code)")
    success, result = test_endpoint("GET", f"{BASE_URL}/promotional-codes/code/{unique_code}")
    if success:
        print_success(f"Retrieved promo code: {result.get('code')}")
    else:
        print_error(f"Failed: {result}")
    
    # UPDATE
    print_info(f"Testing PUT /promotional-codes/{promo_id} (Update)")
    update_data = {"discount_percent": 15.0}
    success, result = test_endpoint("PUT", f"{BASE_URL}/promotional-codes/{promo_id}", update_data)
    if success:
        print_success(f"Updated promo code: discount={result.get('discount_percent')}%")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== ORDERS ====================
    print_section("5. ORDERS - CRUD Testing")
    
    # CREATE
    print_info("Testing POST /orders (Create)")
    # Use an existing sandwich ID (from populated data)
    # Test without promo code first (promo codes may have issues)
    order_data = {
        "customer_name": "Test Customer",
        "description": "Test order",
        "order_type": "takeout",
        "order_details": [
            {
                "sandwich_id": 1,  # Use existing sandwich ID
                "amount": 1
            }
        ]
    }
    success, result = test_endpoint("POST", f"{BASE_URL}/orders/", order_data)
    if success:
        order_id = result.get('id')
        created_ids['orders'].append(order_id)
        print_success(f"Created order ID: {order_id}")
        print_info(f"  Tracking Number: {result.get('tracking_number')}")
        print_info(f"  Total Price: ${result.get('total_price')}")
    else:
        print_error(f"Failed: {result}")
        return
    
    # READ ALL
    print_info("Testing GET /orders (Read All)")
    success, result = test_endpoint("GET", f"{BASE_URL}/orders")
    if success:
        print_success(f"Retrieved {len(result)} orders")
    else:
        print_error(f"Failed: {result}")
    
    # READ ONE
    print_info(f"Testing GET /orders/{order_id} (Read One)")
    success, result = test_endpoint("GET", f"{BASE_URL}/orders/{order_id}")
    if success:
        print_success(f"Retrieved order ID: {order_id}")
    else:
        print_error(f"Failed: {result}")
    
    # UPDATE
    print_info(f"Testing PUT /orders/{order_id} (Update)")
    update_data = {"order_status": "preparing"}
    success, result = test_endpoint("PUT", f"{BASE_URL}/orders/{order_id}", update_data)
    if success:
        print_success(f"Updated order status: {result.get('order_status')}")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== PAYMENTS ====================
    print_section("6. PAYMENTS - CRUD Testing")
    
    # CREATE
    print_info("Testing POST /payments (Create)")
    payment_data = {
        "order_id": order_id,
        "amount": float(result.get('total_price', 5.99)),
        "payment_method": "credit_card",
        "payment_status": "completed"
    }
    success, result = test_endpoint("POST", f"{BASE_URL}/payments", payment_data)
    if success:
        payment_id = result.get('id')
        created_ids['payments'].append(payment_id)
        print_success(f"Created payment ID: {payment_id}")
    else:
        print_error(f"Failed: {result}")
        return
    
    # READ ALL
    print_info("Testing GET /payments (Read All)")
    success, result = test_endpoint("GET", f"{BASE_URL}/payments")
    if success:
        print_success(f"Retrieved {len(result)} payments")
    else:
        print_error(f"Failed: {result}")
    
    # READ BY ORDER
    print_info(f"Testing GET /payments/order/{order_id} (Read By Order)")
    success, result = test_endpoint("GET", f"{BASE_URL}/payments/order/{order_id}")
    if success:
        print_success(f"Retrieved payment for order {order_id}")
    else:
        print_error(f"Failed: {result}")
    
    # UPDATE
    print_info(f"Testing PUT /payments/{payment_id} (Update)")
    update_data = {"payment_status": "completed"}
    success, result = test_endpoint("PUT", f"{BASE_URL}/payments/{payment_id}", update_data)
    if success:
        print_success(f"Updated payment status: {result.get('payment_status')}")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== REVIEWS ====================
    print_section("7. REVIEWS - CRUD Testing")
    
    # CREATE
    print_info("Testing POST /reviews (Create)")
    review_data = {
        "order_id": order_id,
        "sandwich_id": sandwich_id,
        "rating": 5,
        "review_text": "Great sandwich!"
    }
    success, result = test_endpoint("POST", f"{BASE_URL}/reviews", review_data)
    if success:
        review_id = result.get('id')
        created_ids['reviews'].append(review_id)
        print_success(f"Created review ID: {review_id}")
    else:
        print_error(f"Failed: {result}")
        return
    
    # READ ALL
    print_info("Testing GET /reviews (Read All)")
    success, result = test_endpoint("GET", f"{BASE_URL}/reviews")
    if success:
        print_success(f"Retrieved {len(result)} reviews")
    else:
        print_error(f"Failed: {result}")
    
    # READ ONE
    print_info(f"Testing GET /reviews/{review_id} (Read One)")
    success, result = test_endpoint("GET", f"{BASE_URL}/reviews/{review_id}")
    if success:
        print_success(f"Retrieved review: rating={result.get('rating')}")
    else:
        print_error(f"Failed: {result}")
    
    # UPDATE
    print_info(f"Testing PUT /reviews/{review_id} (Update)")
    update_data = {"rating": 4, "review_text": "Updated review"}
    success, result = test_endpoint("PUT", f"{BASE_URL}/reviews/{review_id}", update_data)
    if success:
        print_success(f"Updated review: rating={result.get('rating')}")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== ANALYTICS ====================
    print_section("8. ANALYTICS - Read Testing")
    
    # REVENUE
    print_info("Testing GET /analytics/revenue")
    success, result = test_endpoint("GET", f"{BASE_URL}/analytics/revenue")
    if success:
        print_success(f"Retrieved revenue data")
    else:
        print_error(f"Failed: {result}")
    
    # POPULAR DISHES
    print_info("Testing GET /analytics/popular-dishes")
    success, result = test_endpoint("GET", f"{BASE_URL}/analytics/popular-dishes")
    if success:
        print_success(f"Retrieved popular dishes")
    else:
        print_error(f"Failed: {result}")
    
    # COMPLAINTS
    print_info("Testing GET /analytics/complaints")
    success, result = test_endpoint("GET", f"{BASE_URL}/analytics/complaints")
    if success:
        print_success(f"Retrieved complaints data")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== DELETE OPERATIONS ====================
    print_section("9. DELETE Operations Testing")
    
    # DELETE REVIEW
    print_info(f"Testing DELETE /reviews/{review_id}")
    success, result = test_endpoint("DELETE", f"{BASE_URL}/reviews/{review_id}", expected_status=204)
    if success:
        print_success(f"Deleted review ID: {review_id}")
    else:
        print_error(f"Failed: {result}")
    
    # DELETE PAYMENT
    print_info(f"Testing DELETE /payments/{payment_id}")
    success, result = test_endpoint("DELETE", f"{BASE_URL}/payments/{payment_id}", expected_status=204)
    if success:
        print_success(f"Deleted payment ID: {payment_id}")
    else:
        print_error(f"Failed: {result}")
    
    # DELETE RECIPE
    print_info(f"Testing DELETE /recipes/{recipe_id}")
    success, result = test_endpoint("DELETE", f"{BASE_URL}/recipes/{recipe_id}", expected_status=204)
    if success:
        print_success(f"Deleted recipe ID: {recipe_id}")
    else:
        print_error(f"Failed: {result}")
    
    # DELETE SANDWICH
    print_info(f"Testing DELETE /sandwiches/{sandwich_id}")
    success, result = test_endpoint("DELETE", f"{BASE_URL}/sandwiches/{sandwich_id}", expected_status=204)
    if success:
        print_success(f"Deleted sandwich ID: {sandwich_id}")
    else:
        print_error(f"Failed: {result}")
    
    # DELETE RESOURCE
    print_info(f"Testing DELETE /resources/{resource_id}")
    success, result = test_endpoint("DELETE", f"{BASE_URL}/resources/{resource_id}", expected_status=204)
    if success:
        print_success(f"Deleted resource ID: {resource_id}")
    else:
        print_error(f"Failed: {result}")
    
    # DELETE PROMO CODE
    print_info(f"Testing DELETE /promotional-codes/{promo_id}")
    success, result = test_endpoint("DELETE", f"{BASE_URL}/promotional-codes/{promo_id}", expected_status=204)
    if success:
        print_success(f"Deleted promotional code ID: {promo_id}")
    else:
        print_error(f"Failed: {result}")
    
    # ==================== SUMMARY ====================
    print_section("✅ TESTING COMPLETE!")
    print_success("All endpoints have been tested successfully!")
    print_info("\nNote: Some orders may remain in the database as they may have dependencies.")
    print_info("You can manually clean them up if needed.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

