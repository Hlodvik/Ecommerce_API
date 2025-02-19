from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, Numeric, Integer, DateTime
from typing import Optional
from decimal import Decimal
from .base import Base
from models.associations import cart_product, order_product
if TYPE_CHECKING:
    from models import Storefront, Order, Cart


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    storefront_id: Mapped[int] = mapped_column(ForeignKey("storefront.id"), nullable=False)  # Link to storefront 
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)#found numeric quite handy. we dont trade in goods costing more than 999,999.99 in this hypothetical. someone spending that much probably wont mind calling to make the deal, eh?
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hs_code: Mapped[str] = mapped_column(String(20), nullable=True)  #  harmonized system code, see readme tariffs
    restricted: Mapped[bool] = mapped_column(Boolean, default=False) 
    restriction_reason: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships
    storefront: Mapped["Storefront"] = relationship("Storefront", back_populates="products")
    carts: Mapped[list["Cart"]] = relationship("Cart", secondary=cart_product, back_populates="products")
    orders: Mapped[list["Order"]] = relationship("Order", secondary=order_product, back_populates="products")