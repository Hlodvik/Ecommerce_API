from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Numeric
from datetime import datetime, timezone
from decimal import Decimal
from .base import Base

class Payout(Base):
    __tablename__ = "payout"
    #FIELDS
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), unique=True, nullable=False)  # one to one with order
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"), unique=True, nullable=False)  # one to one with payment
    seller_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  # seller receiving payout
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)  # Amount being paid out
    transaction_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)   
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")  # pending, complete etc
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    # SHIPS
    order: Mapped["Order"] = relationship("Order", back_populates="payout", uselist=False)  # one to one
    payment: Mapped["Payment"] = relationship("Payment", back_populates="payout", uselist=False)  # one to one
    seller: Mapped["Seller"] = relationship("Seller", back_populates="payouts")
