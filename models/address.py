from __future__ import annotations
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base


class Address(Base):
    __tablename__ = "address"
    #fields
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    street: Mapped[str] = mapped_column(String(125), nullable=False)
    city: Mapped[str] = mapped_column(String(85), nullable=False) #looked up the city with the most characters in the name, which goes to 85 chars long for somewhere in new zealand 
    region: Mapped[str] = mapped_column(String(85), nullable=False)#state/ region / province. let's keep things globally minded, folks
    country: Mapped[str] = mapped_column(String(85), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(10), nullable=False)
    #relationships
    user: Mapped["User"] = relationship("User", back_populates="addresses") #one user many address
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="shipping_address") #one address  many order