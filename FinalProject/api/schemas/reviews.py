from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .sandwiches import Sandwich


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    order_id: int
    sandwich_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review_text: Optional[str] = None


class Review(ReviewBase):
    id: int
    order_id: int
    sandwich_id: int
    created_at: datetime
    sandwich: Optional[Sandwich] = None

    class ConfigDict:
        from_attributes = True
