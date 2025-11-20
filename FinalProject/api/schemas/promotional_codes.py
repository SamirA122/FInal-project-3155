from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PromotionalCodeBase(BaseModel):
    code: str
    discount_percent: float = Field(..., ge=0, le=100)
    expiration_date: Optional[datetime] = None
    is_active: bool = True


class PromotionalCodeCreate(PromotionalCodeBase):
    pass


class PromotionalCodeUpdate(BaseModel):
    code: Optional[str] = None
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    expiration_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class PromotionalCode(PromotionalCodeBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
