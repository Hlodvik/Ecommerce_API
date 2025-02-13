from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Table, Column
from datetime import datetime, timezone
from .base import Base
from models.associations import user_storefront
if TYPE_CHECKING:
    from models import  Product, BusinessInfo, User, Order, Payout

class Storefront(Base):
    __tablename__ = "storefront"
    #FIELDS
    id: Mapped[int] = mapped_column(primary_key=True)
    business_info_id: Mapped[int] = mapped_column(ForeignKey("business_info.id"), unique=True, nullable=True) 
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    payout_method: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  

    #SHIPS
    admins: Mapped[list["User"]] = relationship("User", secondary=user_storefront, back_populates="storefronts") #many to many
    business_info: Mapped["BusinessInfo"] = relationship("BusinessInfo", back_populates="storefront", uselist=False)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="storefront", foreign_keys="[Product.storefront_id]")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="storefront")
    payouts: Mapped[list["Payout"]] = relationship("Payout", back_populates="storefront")  # one to many

