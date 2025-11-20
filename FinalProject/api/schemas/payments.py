from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    amount: float
    payment_method: str  # "cash", "credit_card", "debit_card", "online"
    payment_status: Optional[str] = "pending"


class PaymentCreate(PaymentBase):
    order_id: int


class PaymentUpdate(BaseModel):
    payment_status: Optional[str] = None  # "pending", "completed", "failed", "refunded"


class Payment(PaymentBase):
    id: int
    order_id: int
    payment_date: datetime

    class ConfigDict:
        from_attributes = True
