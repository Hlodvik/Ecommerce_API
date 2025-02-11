from __future__ import annotations
from typing import TYPE_CHECKING
from extensions import db
from sqlalchemy import Column, Integer, String, Float, Text
from .base import Base

class DMCache(Base):
    __tablename__ = "dm_cache"

    id = Column(Integer, primary_key=True)
    country_name = Column(String(100))
    country = Column(String(2), unique=True, nullable=False)  # ISO-2 Country Code
    de_minimis_value = Column(Float, default=0)
    de_minimis_currency = Column(String(3), default="USD")
    vat_amount = Column(Float, default=0)
    vat_currency = Column(String(3), default="USD")
    notes = Column(Text, default="")


# return values were given on the website which can be found in readme. this is my loop around for not 
# actually having access to the API. if connection fails, get the last successfully loaded data, values default to zero if never.