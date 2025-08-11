from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import BaseModel

class AlertType(enum.Enum):
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    OVERSTOCK = "overstock"
    EXPIRY_WARNING = "expiry_warning"
    REORDER_REMINDER = "reorder_reminder"

class AlertStatus(enum.Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"

class StockAlert(BaseModel):
    __tablename__ = "stock_alerts"
    
    # Alert information
    alert_type = Column(String(50), nullable=False)
    status = Column(String(50), default="active", nullable=False)
    
    # Product and location relationships
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    
    # Alert details
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Threshold information
    current_quantity = Column(Integer, nullable=False)
    threshold_quantity = Column(Integer, nullable=False)
    
    # Notification settings
    is_email_sent = Column(Boolean, default=False)
    is_sms_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime)
    sms_sent_at = Column(DateTime)
    
    # Resolution information
    resolved_by = Column(String(255))
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)
    
    # Relationships
    product = relationship("Product")
    location = relationship("Location")
    
    def __repr__(self):
        return f"<StockAlert(id={self.id}, type='{self.alert_type.value}', status='{self.status.value}')>"
    
    @property
    def is_active(self):
        """Check if alert is still active"""
        return self.status == AlertStatus.ACTIVE
    
    @property
    def requires_attention(self):
        """Check if alert requires immediate attention"""
        return self.severity in ["high", "critical"] and self.status == AlertStatus.ACTIVE
