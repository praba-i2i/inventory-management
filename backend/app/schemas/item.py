from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from .category import CategoryResponse

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None
    quantity: int = Field(0, ge=0)
    unit_price: Decimal = Field(0.00, ge=0)
    reorder_level: int = Field(0, ge=0)
    location: Optional[str] = Field(None, max_length=255)
    supplier: Optional[str] = Field(None, max_length=255)

class ItemCreate(ItemBase):
    @validator('sku')
    def validate_sku(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('SKU cannot be empty if provided')
        return v

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)
    category_id: Optional[int] = None
    quantity: Optional[int] = Field(None, ge=0)
    unit_price: Optional[Decimal] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=255)
    supplier: Optional[str] = Field(None, max_length=255)

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    
    class Config:
        from_attributes = True
