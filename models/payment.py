from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Numeric
from datetime import datetime, timezone
from decimal import Decimal
from .base import Base
class Payment(Base):
    __tablename__ = "payment"
    #FIELDS
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  # Buyer making the payment
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)  # Amount paid
    transaction_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)   
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")  # Payment status
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    #RELATESIES
    user: Mapped["User"] = relationship("User", back_populates="payments") #one user many payments
    order: Mapped["Order"] = relationship("Order", back_populates="payment", uselist=False) #one payment one order
    payout: Mapped["Payout"] = relationship("Payout", back_populates="payment", uselist=False)