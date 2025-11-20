from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class PromotionalCode(Base):
    __tablename__ = "promotional_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)  # e.g., 10.00 for 10%
    expiration_date = Column(DATETIME, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default='1')
    created_at = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    orders = relationship("Order", back_populates="promo_code")
