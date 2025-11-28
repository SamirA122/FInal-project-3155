from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..dependencies.database import Base


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    ONLINE = "online"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False, server_default=PaymentStatus.PENDING.value)
    payment_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    order = relationship("Order", foreign_keys=[order_id], uselist=False)
