from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime
from datetime import datetime, timezone
from .base import Base
from models.associations import user_storefront
if TYPE_CHECKING:
    from models import Address, Storefront, Order, Cart, Payment, Payout


class User(Base):
    __tablename__ = "user"
    #FIELDS
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    #SHIPS
    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="user")
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False)
    

class Seller(User):
    __tablename__ = "seller"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    storefronts: Mapped[list["Storefront"]] = relationship("Storefront", secondary=user_storefront, back_populates="admins")
    payouts: Mapped[list["Payout"]] = relationship("Payout", back_populates="seller")