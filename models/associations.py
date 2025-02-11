from sqlalchemy import Table, Column, ForeignKey, Integer, Numeric
from .base import Base



#sellers / storefronts
user_storefront = Table(
    "user_storefront",
    Base.metadata,
    Column("seller_id", ForeignKey("seller.user_id"), primary_key=True),
    Column("storefront_id", ForeignKey("storefront.id"), primary_key=True)
)

#products BEFORE CHECKOUT
cart_product = Table(
    "cart_product",
    Base.metadata,
    Column("cart_id", ForeignKey("cart.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1)
)

#products AFTER CHECKOUT
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("order.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1),
    Column("export_tax", Numeric(6, 2), nullable=True)  
)



