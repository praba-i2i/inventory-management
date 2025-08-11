from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

class Supplier(BaseModel):
    __tablename__ = "suppliers"
    
    # Basic supplier information
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Contact information
    email = Column(String(255), index=True)
    phone = Column(String(50))
    website = Column(String(255))
    
    # Address information
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    
    # Business information
    tax_id = Column(String(100))
    payment_terms = Column(String(100))  # e.g., "Net 30", "Net 60"
    credit_limit = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_preferred = Column(Boolean, default=False)
    
    # Relationships
    products = relationship("Product", back_populates="supplier")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}', code='{self.code}')>"
