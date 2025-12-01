# How to Add Data to the Database

There are several ways to add data to your database:

## Method 1: Using the Populate Script 

I've created a script that will automatically add sample data:

```bash
cd /Users/yousef/Desktop/Software_Engineering/Yousef_SamirProject/FinalProject
source venv/bin/activate
python populate_database.py
```

This will add:
- 10 sample ingredients (resources)
- 5 sample sandwiches (menu items)
- Recipes linking ingredients to sandwiches
- 3 promotional codes

## Method 2: Using Swagger UI (Interactive) 🌐

1. Open http://127.0.0.1:8000/docs in your browser
2. Find the endpoint you want to use (e.g., `POST /resources`)
3. Click "Try it out"
4. Fill in the JSON data
5. Click "Execute"

### Example: Adding a Resource

1. Go to `POST /resources`
2. Click "Try it out"
3. Enter:
```json
{
  "item": "Bread",
  "amount": 100
}
```
4. Click "Execute"

### Example: Adding a Sandwich

1. Go to `POST /sandwiches`
2. Click "Try it out"
3. Enter:
```json
{
  "sandwich_name": "Cheese Sandwich",
  "price": 5.99,
  "category": "vegetarian",
  "description": "A delicious cheese sandwich",
  "is_available": true
}
```
4. Click "Execute"

## Method 3: Using cURL (Command Line) 💻

### Add a Resource
```bash
curl -X POST "http://127.0.0.1:8000/resources" \
  -H "Content-Type: application/json" \
  -d '{
    "item": "Bread",
    "amount": 100
  }'
```

### Add a Sandwich
```bash
curl -X POST "http://127.0.0.1:8000/sandwiches" \
  -H "Content-Type: application/json" \
  -d '{
    "sandwich_name": "Cheese Sandwich",
    "price": 5.99,
    "category": "vegetarian",
    "description": "A delicious cheese sandwich",
    "is_available": true
  }'
```

### Add a Recipe (Link Ingredient to Sandwich)
```bash
curl -X POST "http://127.0.0.1:8000/recipes" \
  -H "Content-Type: application/json" \
  -d '{
    "sandwich_id": 1,
    "resource_id": 1,
    "amount": 2
  }'
```

### Add a Promotional Code
```bash
curl -X POST "http://127.0.0.1:8000/promotional-codes" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SAVE10",
    "discount_percent": 10.0,
    "expiration_date": "2024-12-31T23:59:59",
    "is_active": true
  }'
```

## Method 4: Using Python Requests 🐍

Create a Python script:

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Add a resource
response = requests.post(f"{BASE_URL}/resources", json={
    "item": "Bread",
    "amount": 100
})
print(response.json())

# Add a sandwich
response = requests.post(f"{BASE_URL}/sandwiches", json={
    "sandwich_name": "Cheese Sandwich",
    "price": 5.99,
    "category": "vegetarian",
    "is_available": True
})
print(response.json())

# Add a recipe
response = requests.post(f"{BASE_URL}/recipes", json={
    "sandwich_id": 1,
    "resource_id": 1,
    "amount": 2
})
print(response.json())
```

## Recommended Order for Adding Data

1. **Resources (Ingredients)** - Add all ingredients first
2. **Sandwiches (Menu Items)** - Add all menu items
3. **Recipes** - Link ingredients to sandwiches
4. **Promotional Codes** (Optional) - Add discount codes
5. **Orders** - Create orders (this will use the data above)
6. **Payments** - Add payment information for orders
7. **Reviews** - Add customer reviews

## Quick Start Example

```bash
# 1. Add an ingredient
curl -X POST "http://127.0.0.1:8000/resources" \
  -H "Content-Type: application/json" \
  -d '{"item": "Bread", "amount": 100}'

# 2. Add a sandwich
curl -X POST "http://127.0.0.1:8000/sandwiches" \
  -H "Content-Type: application/json" \
  -d '{"sandwich_name": "Cheese Sandwich", "price": 5.99, "category": "vegetarian", "is_available": true}'

# 3. Link them (recipe)
curl -X POST "http://127.0.0.1:8000/recipes" \
  -H "Content-Type: application/json" \
  -d '{"sandwich_id": 1, "resource_id": 1, "amount": 2}'

# 4. Create an order
curl -X POST "http://127.0.0.1:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "order_type": "takeout",
    "order_details": [{"sandwich_id": 1, "amount": 2}]
  }'
```

## Viewing Your Data

After adding data, you can view it:

```bash
# View all resources
curl http://127.0.0.1:8000/resources

# View all sandwiches
curl http://127.0.0.1:8000/sandwiches

# View all orders
curl http://127.0.0.1:8000/orders
```

Or use the Swagger UI at http://127.0.0.1:8000/docs and use the GET endpoints!

