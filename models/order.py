from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime
from datetime import datetime, timezone
from .base import Base
from models.associations import order_product
if TYPE_CHECKING():
    from models import User, Address, Product, Payment, Payout


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    shipping_address_id: Mapped[int] = mapped_column(ForeignKey("address.id"), nullable=False)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"), unique=True, nullable=False)

    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")  # Order status
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    products: Mapped[list["Product"]] = relationship("Product", secondary=order_product, back_populates="orders")  # many to many
    user: Mapped["User"] = relationship("User", back_populates="orders")  # one to many
    payment: Mapped["Payment"] = relationship("Payment", back_populates="order", uselist=False)  # one to one
    shipping_address: Mapped["Address"] = relationship("Address", back_populates="orders")  # one to one
    payout: Mapped["Payout"] = relationship("Payout", back_populates="order", uselist=False) #one to one