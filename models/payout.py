from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Numeric
from datetime import datetime, timezone
from decimal import Decimal
from .base import Base
if TYPE_CHECKING:
    from models import Order, Storefront

class Payout(Base):
    __tablename__ = "payout"
    #fields
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False, unique=True)
    storefront_id: Mapped[int] = mapped_column(ForeignKey("storefront.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transaction_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # relationships
    order: Mapped["Order"] = relationship("Order", back_populates="payout", uselist=False)
    storefront: Mapped["Storefront"] = relationship("Storefront", back_populates="payouts")