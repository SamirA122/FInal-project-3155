from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    review_text = Column(Text, nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    order = relationship("Order", back_populates="reviews")
    sandwich = relationship("Sandwich", back_populates="reviews")
