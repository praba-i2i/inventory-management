from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    
    # Basic product information
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    barcode = Column(String(100), unique=True, index=True)
    
    # Category relationship
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="products")
    
    # Product specifications (stored as JSON for flexibility)
    specifications = Column(JSON)
    
    # Pricing
    cost_price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    selling_price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    unit = Column(String(50), default="piece")  # piece, kg, liter, meter, etc.
    
    # Product status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Product dimensions and weight
    weight = Column(DECIMAL(8, 3))  # in kg
    length = Column(DECIMAL(8, 2))  # in cm
    width = Column(DECIMAL(8, 2))   # in cm
    height = Column(DECIMAL(8, 2))  # in cm
    
    # Supplier information
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    supplier = relationship("Supplier", back_populates="products")
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="product", cascade="all, delete-orphan")
    purchase_order_items = relationship("PurchaseOrderItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"
