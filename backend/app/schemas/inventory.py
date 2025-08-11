from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime

class InventoryItemBase(BaseModel):
    product_id: int
    location_id: int
    quantity: int = Field(..., ge=0)
    reserved_quantity: int = Field(0, ge=0)
    available_quantity: int = Field(0, ge=0)
    reorder_level: int = Field(0, ge=0)
    reorder_quantity: int = Field(0, ge=0)
    max_stock_level: Optional[int] = Field(None, ge=0)
    storage_location: Optional[str] = Field(None, max_length=255)
    storage_zone: Optional[str] = Field(None, max_length=100)
    unit_cost: Decimal = Field(0.00, ge=0)
    total_value: Decimal = Field(0.00, ge=0)
    status: str = "active"
    notes: Optional[str] = None

    @validator('available_quantity')
    def validate_available_quantity(cls, v, values):
        if 'quantity' in values and 'reserved_quantity' in values:
            if v > values['quantity'] - values['reserved_quantity']:
                raise ValueError('Available quantity cannot exceed quantity minus reserved quantity')
        return v

    @validator('reserved_quantity')
    def validate_reserved_quantity(cls, v, values):
        if 'quantity' in values and v > values['quantity']:
            raise ValueError('Reserved quantity cannot exceed total quantity')
        return v

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=0)
    reserved_quantity: Optional[int] = Field(None, ge=0)
    available_quantity: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    reorder_quantity: Optional[int] = Field(None, ge=0)
    max_stock_level: Optional[int] = Field(None, ge=0)
    storage_location: Optional[str] = Field(None, max_length=255)
    storage_zone: Optional[str] = Field(None, max_length=100)
    unit_cost: Optional[Decimal] = Field(None, ge=0)
    total_value: Optional[Decimal] = Field(None, ge=0)
    status: Optional[str] = None
    notes: Optional[str] = None

class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_low_stock: bool
    stock_status: str
    
    class Config:
        from_attributes = True

class InventoryItemWithDetails(InventoryItemResponse):
    product_name: Optional[str] = None
    product_sku: Optional[str] = None
    location_name: Optional[str] = None
    location_code: Optional[str] = None
