# How to Use the Application

## Prerequisites

1. Make sure MySQL is running on your system
2. Create a database named `sandwich_maker_api` (or update the config)
3. Update database credentials in `api/dependencies/config.py` if needed

## Step 1: Activate Virtual Environment

```bash
cd /Users/yousef/Desktop/Software_Engineering/Yousef_SamirProject/FinalProject
source venv/bin/activate
```

## Step 2: Start the Server

```bash
uvicorn api.main:app --reload
```

The server will start on `http://127.0.0.1:8000`

## Step 3: Access the API Documentation

Open your browser and go to:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

The Swagger UI provides an interactive interface where you can test all endpoints directly!

## Step 4: Populate Initial Data

Before creating orders, you need to set up:
1. **Resources (Ingredients)** - Add ingredients to your inventory
2. **Sandwiches (Menu Items)** - Create menu items
3. **Recipes** - Link ingredients to sandwiches

### Example: Setting Up Data

#### 1. Create Resources (Ingredients)
```bash
POST http://127.0.0.1:8000/resources
{
  "item": "Bread",
  "amount": 100
}
```

```bash
POST http://127.0.0.1:8000/resources
{
  "item": "Cheese",
  "amount": 50
}
```

```bash
POST http://127.0.0.1:8000/resources
{
  "item": "Lettuce",
  "amount": 30
}
```

#### 2. Create Sandwiches (Menu Items)
```bash
POST http://127.0.0.1:8000/sandwiches
{
  "sandwich_name": "Cheese Sandwich",
  "price": 5.99,
  "category": "vegetarian",
  "description": "A delicious cheese sandwich",
  "is_available": true
}
```

```bash
POST http://127.0.0.1:8000/sandwiches
{
  "sandwich_name": "Veggie Delight",
  "price": 6.99,
  "category": "vegetarian",
  "description": "Fresh vegetables on bread",
  "is_available": true
}
```

#### 3. Create Recipes (Link Ingredients to Sandwiches)
```bash
POST http://127.0.0.1:8000/recipes
{
  "sandwich_id": 1,
  "resource_id": 1,
  "amount": 2
}
```

```bash
POST http://127.0.0.1:8000/recipes
{
  "sandwich_id": 1,
  "resource_id": 2,
  "amount": 1
}
```

#### 4. Create Promotional Code (Optional)
```bash
POST http://127.0.0.1:8000/promotional-codes
{
  "code": "SAVE10",
  "discount_percent": 10.0,
  "expiration_date": "2024-12-31T23:59:59",
  "is_active": true
}
```

## Step 5: Create an Order

### Example: Place an Order (Customer)
```bash
POST http://127.0.0.1:8000/orders
{
  "customer_name": "John Doe",
  "description": "Lunch order",
  "order_type": "takeout",
  "promo_code": "SAVE10",
  "order_details": [
    {
      "sandwich_id": 1,
      "amount": 2
    }
  ]
}
```

**Response will include:**
- Order ID
- Tracking number (e.g., "TRK-A1B2C3D4")
- Total price (with discount applied if promo code used)
- Order status

### Track Your Order
```bash
GET http://127.0.0.1:8000/orders/tracking/TRK-A1B2C3D4
```

## Step 6: Make Payment

```bash
POST http://127.0.0.1:8000/payments
{
  "order_id": 1,
  "amount": 10.78,
  "payment_method": "credit_card",
  "payment_status": "completed"
}
```

## Step 7: Add Review

```bash
POST http://127.0.0.1:8000/reviews
{
  "order_id": 1,
  "sandwich_id": 1,
  "rating": 5,
  "review_text": "Excellent sandwich!"
}
```

## Common Use Cases

### Restaurant Staff: View All Orders
```bash
GET http://127.0.0.1:8000/orders
```

### Restaurant Staff: View Orders by Date Range
```bash
GET http://127.0.0.1:8000/orders?start_date=2024-01-01T00:00:00&end_date=2024-01-31T23:59:59
```

### Restaurant Staff: Get Daily Revenue
```bash
GET http://127.0.0.1:8000/analytics/revenue?date=2024-01-15T00:00:00
```

### Restaurant Staff: View Popular Dishes
```bash
GET http://127.0.0.1:8000/analytics/popular-dishes?limit=10
```

### Restaurant Staff: View Complaints
```bash
GET http://127.0.0.1:8000/analytics/complaints?min_rating=2
```

### Customer: Search Vegetarian Options
```bash
GET http://127.0.0.1:8000/sandwiches?category=vegetarian
```

### Customer: View All Available Sandwiches
```bash
GET http://127.0.0.1:8000/sandwiches?is_available=true
```

## Using cURL (Command Line)

If you prefer command line, here are some examples:

```bash
# Create a resource
curl -X POST "http://127.0.0.1:8000/resources" \
  -H "Content-Type: application/json" \
  -d '{"item": "Bread", "amount": 100}'

# Create a sandwich
curl -X POST "http://127.0.0.1:8000/sandwiches" \
  -H "Content-Type: application/json" \
  -d '{"sandwich_name": "Cheese Sandwich", "price": 5.99, "category": "vegetarian", "is_available": true}'

# Get all sandwiches
curl -X GET "http://127.0.0.1:8000/sandwiches"

# Create an order
curl -X POST "http://127.0.0.1:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "order_type": "takeout",
    "order_details": [{"sandwich_id": 1, "amount": 2}]
  }'
```

## Using Python Requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Create a resource
response = requests.post(f"{BASE_URL}/resources", json={
    "item": "Bread",
    "amount": 100
})
print(response.json())

# Create a sandwich
response = requests.post(f"{BASE_URL}/sandwiches", json={
    "sandwich_name": "Cheese Sandwich",
    "price": 5.99,
    "category": "vegetarian",
    "is_available": True
})
print(response.json())

# Create an order
response = requests.post(f"{BASE_URL}/orders", json={
    "customer_name": "John Doe",
    "order_type": "takeout",
    "order_details": [{"sandwich_id": 1, "amount": 2}]
})
order = response.json()
print(f"Order created! Tracking: {order['tracking_number']}")
```

## Testing

Run the test suite:
```bash
pytest api/tests/
```

## Troubleshooting

1. **Database Connection Error**: Make sure MySQL is running and credentials in `config.py` are correct
2. **Port Already in Use**: Change the port in `config.py` or stop the process using port 8000
3. **Module Not Found**: Make sure virtual environment is activated
4. **Insufficient Ingredients Error**: Add more resources to your inventory

## Next Steps

1. Populate your database with initial data
2. Test all endpoints using the Swagger UI
3. Create sample orders to test the full workflow
4. Check analytics endpoints to see revenue and popular dishes

