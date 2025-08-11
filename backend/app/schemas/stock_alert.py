from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    OVERSTOCK = "overstock"
    EXPIRY_WARNING = "expiry_warning"
    REORDER_REMINDER = "reorder_reminder"

class AlertStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"

class StockAlertBase(BaseModel):
    alert_type: AlertType
    product_id: int
    location_id: int
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    severity: str = Field("medium", pattern="^(low|medium|high|critical)$")
    current_quantity: int = Field(..., ge=0)
    threshold_quantity: int = Field(..., ge=0)

class StockAlertCreate(StockAlertBase):
    pass

class StockAlertUpdate(BaseModel):
    status: Optional[AlertStatus] = None
    is_email_sent: Optional[bool] = None
    is_sms_sent: Optional[bool] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None

class StockAlertResponse(StockAlertBase):
    id: int
    status: AlertStatus
    is_email_sent: bool
    is_sms_sent: bool
    email_sent_at: Optional[datetime] = None
    sms_sent_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    requires_attention: bool
    
    class Config:
        from_attributes = True

class StockAlertWithDetails(StockAlertResponse):
    product_name: Optional[str] = None
    product_sku: Optional[str] = None
    location_name: Optional[str] = None
    location_code: Optional[str] = None
