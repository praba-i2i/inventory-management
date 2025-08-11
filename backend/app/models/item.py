from sqlalchemy import Column, String, Text, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Item(BaseModel):
    __tablename__ = "items"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    sku = Column(String(100), unique=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    unit_price = Column(Numeric(10, 2), nullable=False, default=0.00)
    reorder_level = Column(Integer, default=0)
    location = Column(String(255))
    supplier = Column(String(255))
    
    # Relationship
    category = relationship("Category", back_populates="items")
    
    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', sku='{self.sku}')>"
