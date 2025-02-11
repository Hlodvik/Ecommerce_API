from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime
from datetime import datetime, timezone
from typing import Optional
from .base import Base
if TYPE_CHECKING:
    from models import Storefront

    
class BusinessInfo(Base):
    __tablename__ = "business_info"

    id: Mapped[int] = mapped_column(primary_key=True)   
    business_name: Mapped[str] = mapped_column(String(150), nullable=False)
    license_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True)  # Business license
    industry: Mapped[str] = mapped_column(String(100), nullable=False)  # Industry for trade laws/tariffs
    tax_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)  # EIN or equivalent
    tax_status: Mapped[str] = mapped_column(String(50), nullable=False)  # Tax-exempt status or equivalent
    compliance_docs: Mapped[Optional[str]] = mapped_column(String(255))  # URLs for required compliance documents
    business_phone: Mapped[Optional[str]] = mapped_column(String(20))  # Business contact
    business_email: Mapped[Optional[str]] = mapped_column(String(150))  
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    #SHIPS
    storefront: Mapped["Storefront"] = relationship("Storefront", back_populates="business_info", uselist=False)