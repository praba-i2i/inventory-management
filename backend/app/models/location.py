from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel

class Location(BaseModel):
    __tablename__ = "locations"
    
    # Basic location information
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Location type
    type = Column(String(50), nullable=False, default="warehouse")  # warehouse, store, office, etc.
    
    # Address information
    address = Column(Text)
    
    # Contact information
    contact_person = Column(String(255))
    contact_phone = Column(String(50))
    
    # Location details
    status = Column(String(50), default="active")  # active, inactive
    
    # Capacity and storage information
    capacity = Column(Integer)  # Total storage capacity
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="location")
    
    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}', code='{self.code}')>"
