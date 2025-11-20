from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SandwichBase(BaseModel):
    sandwich_name: str
    price: float
    category: Optional[str] = None
    description: Optional[str] = None
    is_available: Optional[bool] = True


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None


class Sandwich(SandwichBase):
    id: int

    class ConfigDict:
        from_attributes = True