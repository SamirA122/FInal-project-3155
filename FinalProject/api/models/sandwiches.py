from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    category = Column(String(50), nullable=True)  # e.g., "vegetarian", "meat", "vegan"
    description = Column(String(500), nullable=True)
    is_available = Column(Boolean, nullable=False, server_default='1')

    recipes = relationship("Recipe", back_populates="sandwich", cascade="all, delete-orphan")
    order_details = relationship("OrderDetail", back_populates="sandwich")
    reviews = relationship("Review", back_populates="sandwich", cascade="all, delete-orphan")
