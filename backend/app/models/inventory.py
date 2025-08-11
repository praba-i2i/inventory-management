from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"
    
    # Product and location relationships
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    
    # Stock information
    quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, default=0)  # Quantity reserved for orders
    available_quantity = Column(Integer, default=0)  # Available for sale
    
    # Stock thresholds
    reorder_level = Column(Integer, default=0)
    reorder_quantity = Column(Integer, default=0)
    max_stock_level = Column(Integer)
    
    # Storage information
    storage_location = Column(String(255))  # Specific shelf/rack location
    storage_zone = Column(String(100))      # Zone within the location
    
    # Cost and valuation
    unit_cost = Column(DECIMAL(10, 2), default=0.00)
    total_value = Column(DECIMAL(12, 2), default=0.00)
    
    # Status
    status = Column(String(50), default="active")  # active, inactive, discontinued
    notes = Column(Text)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_items")
    location = relationship("Location", back_populates="inventory_items")
    
    def __repr__(self):
        return f"<InventoryItem(id={self.id}, product_id={self.product_id}, location_id={self.location_id}, quantity={self.quantity})>"
    
    @property
    def is_low_stock(self):
        """Check if stock is below reorder level"""
        available = self.available_quantity or 0
        reorder = self.reorder_level or 0
        return available <= reorder
    
    @property
    def stock_status(self):
        """Get stock status string"""
        available = self.available_quantity or 0
        if available <= 0:
            return "out_of_stock"
        elif self.is_low_stock:
            return "low_stock"
        elif self.max_stock_level and available >= self.max_stock_level:
            return "overstocked"
        else:
            return "normal"
