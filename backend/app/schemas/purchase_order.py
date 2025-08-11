from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from enum import Enum

class PurchaseOrderStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    ORDERED = "ordered"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class PurchaseOrderBase(BaseModel):
    po_number: str = Field(..., min_length=1, max_length=50)
    reference_number: Optional[str] = Field(None, max_length=100)
    supplier_id: int
    expected_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None

    @validator('po_number')
    def validate_po_number(cls, v):
        if not v.strip():
            raise ValueError('PO number cannot be empty')
        return v.upper()

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrderUpdate(BaseModel):
    reference_number: Optional[str] = Field(None, max_length=100)
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    status: Optional[PurchaseOrderStatus] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None
    approved_by: Optional[str] = None

class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    order_date: datetime
    actual_delivery_date: Optional[datetime] = None
    status: PurchaseOrderStatus
    subtotal: Decimal
    tax_amount: Decimal
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PurchaseOrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)
    total_price: Decimal = Field(..., ge=0)
    notes: Optional[str] = None

    @validator('total_price')
    def validate_total_price(cls, v, values):
        if 'quantity' in values and 'unit_price' in values:
            expected_total = values['quantity'] * values['unit_price']
            if abs(v - expected_total) > Decimal('0.01'):
                raise ValueError('Total price must equal quantity * unit price')
        return v

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    unit_price: Optional[Decimal] = Field(None, ge=0)
    total_price: Optional[Decimal] = Field(None, ge=0)
    received_quantity: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: int
    purchase_order_id: int
    received_quantity: int
    remaining_quantity: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PurchaseOrderWithItems(PurchaseOrderResponse):
    items: List[PurchaseOrderItemResponse] = []
