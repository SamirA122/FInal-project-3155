# Import all models to ensure relationships are properly resolved
from . import resources
from . import recipes
from . import sandwiches
from . import orders
from . import order_details
from . import reviews
from . import promotional_codes
from . import payments

# Ensure all models are loaded
__all__ = [
    "resources",
    "recipes", 
    "sandwiches",
    "orders",
    "order_details",
    "reviews",
    "promotional_codes",
    "payments"
]
