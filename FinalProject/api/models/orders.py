from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..dependencies.database import Base


class OrderType(str, enum.Enum):
    TAKEOUT = "takeout"
    DELIVERY = "delivery"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    tracking_number = Column(String(50), unique=True, nullable=True, index=True)
    order_type = Column(Enum(OrderType), nullable=False, server_default=OrderType.TAKEOUT.value)
    order_status = Column(Enum(OrderStatus), nullable=False, server_default=OrderStatus.PENDING.value)
    total_price = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    promo_code_id = Column(Integer, ForeignKey("promotional_codes.id"), nullable=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="order", cascade="all, delete-orphan")
    promo_code = relationship("PromotionalCode", back_populates="orders")
    payment = relationship("Payment", back_populates="order")