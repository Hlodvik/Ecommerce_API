from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime 
from datetime import datetime, timezone
from .base import Base
from models.associations import cart_product

# Shopping carts are standard across ecommerce sites, so chose to include 




class Cart(Base):
    __tablename__ = "cart"
    #fields
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    # ̶l̶o̶v̶e̶ ̶t̶r̶i̶a̶n̶g̶l̶e̶  Relationships:
    products: Mapped[list["Product"]] = relationship("Product", secondary=cart_product, back_populates="carts")
    user: Mapped["User"] = relationship("User", back_populates="cart")