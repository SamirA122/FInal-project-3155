from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import TYPE_CHECKING
from ..dependencies.database import Base

if TYPE_CHECKING:
    from .recipes import Recipe


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(100), unique=True, nullable=False)
    amount = Column(Integer, index=True, nullable=False, server_default='0.0')

    recipes = relationship("Recipe", back_populates="resource", lazy="select")
