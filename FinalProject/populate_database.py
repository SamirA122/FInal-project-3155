"""
Script to populate the database with sample data.
Run this after starting the server to add initial data.

Usage:
    python populate_database.py
"""
import requests
import json
from datetime import datetime, timedelta


BASE_URL = "http://127.0.0.1:8000"


def print_response(title, response):
    """Helper function to print API responses"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    if response.status_code in [200, 201]:
        print(f"✅ Success! Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")
    return response.status_code in [200, 201]


def populate_resources():
    """Add sample ingredients/resources"""
    print("\n📦 Adding Resources (Ingredients)...")
    
    resources = [
        {"item": "Bread", "amount": 100},
        {"item": "Cheese", "amount": 50},
        {"item": "Lettuce", "amount": 30},
        {"item": "Tomato", "amount": 40},
        {"item": "Chicken", "amount": 25},
        {"item": "Beef", "amount": 20},
        {"item": "Bacon", "amount": 30},
        {"item": "Mayonnaise", "amount": 15},
        {"item": "Mustard", "amount": 20},
        {"item": "Pickles", "amount": 35},
    ]
    
    created_resources = []
    for resource in resources:
        response = requests.post(f"{BASE_URL}/resources", json=resource)
        if print_response(f"Creating Resource: {resource['item']}", response):
            created_resources.append(response.json())
    
    return created_resources


def populate_sandwiches():
    """Add sample menu items (sandwiches)"""
    print("\n🥪 Adding Sandwiches (Menu Items)...")
    
    sandwiches = [
        {
            "sandwich_name": "Classic Cheese",
            "price": 5.99,
            "category": "vegetarian",
            "description": "A simple and delicious cheese sandwich",
            "is_available": True
        },
        {
            "sandwich_name": "Veggie Delight",
            "price": 6.99,
            "category": "vegetarian",
            "description": "Fresh vegetables with lettuce and tomato",
            "is_available": True
        },
        {
            "sandwich_name": "Chicken Club",
            "price": 8.99,
            "category": "meat",
            "description": "Grilled chicken with bacon and cheese",
            "is_available": True
        },
        {
            "sandwich_name": "Beef Burger",
            "price": 9.99,
            "category": "meat",
            "description": "Juicy beef patty with all the fixings",
            "is_available": True
        },
        {
            "sandwich_name": "BLT",
            "price": 7.99,
            "category": "meat",
            "description": "Bacon, lettuce, and tomato classic",
            "is_available": True
        },
    ]
    
    created_sandwiches = []
    for sandwich in sandwiches:
        response = requests.post(f"{BASE_URL}/sandwiches", json=sandwich)
        if print_response(f"Creating Sandwich: {sandwich['sandwich_name']}", response):
            created_sandwiches.append(response.json())
    
    return created_sandwiches


def populate_recipes(resources, sandwiches):
    """Link ingredients to sandwiches (create recipes)"""
    print("\n📝 Adding Recipes (Linking Ingredients to Sandwiches)...")
    
    # Map resource names to IDs
    resource_map = {r['item']: r['id'] for r in resources}
    
    recipes = [
        # Classic Cheese Sandwich
        {"sandwich_id": 1, "resource_id": resource_map["Bread"], "amount": 2},
        {"sandwich_id": 1, "resource_id": resource_map["Cheese"], "amount": 2},
        {"sandwich_id": 1, "resource_id": resource_map["Mayonnaise"], "amount": 1},
        
        # Veggie Delight
        {"sandwich_id": 2, "resource_id": resource_map["Bread"], "amount": 2},
        {"sandwich_id": 2, "resource_id": resource_map["Lettuce"], "amount": 2},
        {"sandwich_id": 2, "resource_id": resource_map["Tomato"], "amount": 2},
        {"sandwich_id": 2, "resource_id": resource_map["Pickles"], "amount": 1},
        
        # Chicken Club
        {"sandwich_id": 3, "resource_id": resource_map["Bread"], "amount": 2},
        {"sandwich_id": 3, "resource_id": resource_map["Chicken"], "amount": 1},
        {"sandwich_id": 3, "resource_id": resource_map["Bacon"], "amount": 2},
        {"sandwich_id": 3, "resource_id": resource_map["Cheese"], "amount": 1},
        {"sandwich_id": 3, "resource_id": resource_map["Lettuce"], "amount": 1},
        
        # Beef Burger
        {"sandwich_id": 4, "resource_id": resource_map["Bread"], "amount": 2},
        {"sandwich_id": 4, "resource_id": resource_map["Beef"], "amount": 1},
        {"sandwich_id": 4, "resource_id": resource_map["Cheese"], "amount": 1},
        {"sandwich_id": 4, "resource_id": resource_map["Lettuce"], "amount": 1},
        {"sandwich_id": 4, "resource_id": resource_map["Tomato"], "amount": 1},
        {"sandwich_id": 4, "resource_id": resource_map["Pickles"], "amount": 1},
        
        # BLT
        {"sandwich_id": 5, "resource_id": resource_map["Bread"], "amount": 2},
        {"sandwich_id": 5, "resource_id": resource_map["Bacon"], "amount": 3},
        {"sandwich_id": 5, "resource_id": resource_map["Lettuce"], "amount": 1},
        {"sandwich_id": 5, "resource_id": resource_map["Tomato"], "amount": 2},
        {"sandwich_id": 5, "resource_id": resource_map["Mayonnaise"], "amount": 1},
    ]
    
    for recipe in recipes:
        response = requests.post(f"{BASE_URL}/recipes", json=recipe)
        print_response(f"Creating Recipe: Sandwich {recipe['sandwich_id']} -> Resource {recipe['resource_id']}", response)


def populate_promotional_codes():
    """Add sample promotional codes"""
    print("\n🎟️ Adding Promotional Codes...")
    
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S")
    
    promo_codes = [
        {
            "code": "SAVE10",
            "discount_percent": 10.0,
            "expiration_date": future_date,
            "is_active": True
        },
        {
            "code": "WELCOME20",
            "discount_percent": 20.0,
            "expiration_date": future_date,
            "is_active": True
        },
        {
            "code": "STUDENT15",
            "discount_percent": 15.0,
            "expiration_date": future_date,
            "is_active": True
        },
    ]
    
    for promo in promo_codes:
        response = requests.post(f"{BASE_URL}/promotional-codes", json=promo)
        print_response(f"Creating Promo Code: {promo['code']}", response)


def main():
    """Main function to populate all data"""
    print("\n" + "="*60)
    print("🚀 Starting Database Population")
    print("="*60)
    print("\nMake sure the server is running at http://127.0.0.1:8000")
    
    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code != 200:
            print(f"\n❌ Error: Cannot connect to server at {BASE_URL}")
            print("Please make sure the server is running:")
            print("  uvicorn api.main:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Cannot connect to server at {BASE_URL}")
        print("Please make sure the server is running:")
        print("  uvicorn api.main:app --reload")
        return
    
    # Populate in order
    resources = populate_resources()
    sandwiches = populate_sandwiches()
    populate_recipes(resources, sandwiches)
    populate_promotional_codes()
    
    print("\n" + "="*60)
    print("✅ Database Population Complete!")
    print("="*60)
    print("\nYou can now:")
    print("  - View all resources: GET /resources")
    print("  - View all sandwiches: GET /sandwiches")
    print("  - Create orders: POST /orders")
    print("  - View analytics: GET /analytics/*")


if __name__ == "__main__":
    main()

