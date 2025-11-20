from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    order_type: Optional[str] = "takeout"  # "takeout" or "delivery"
    promo_code: Optional[str] = None  # Promo code string for validation


class OrderDetailItem(BaseModel):
    sandwich_id: int
    amount: int

class OrderCreate(OrderBase):
    order_details: list[OrderDetailItem]  # List of {sandwich_id, amount}


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    order_type: Optional[str] = None
    order_status: Optional[str] = None  # "pending", "preparing", "ready", "completed"


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    order_details: Optional[list[OrderDetail]] = None

    class ConfigDict:
        from_attributes = True
