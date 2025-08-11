from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import BaseModel

class PurchaseOrderStatus(enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    ORDERED = "ordered"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"
    
    # Order information
    po_number = Column(String(50), unique=True, nullable=False, index=True)
    reference_number = Column(String(100), index=True)
    
    # Supplier relationship
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    supplier = relationship("Supplier", back_populates="purchase_orders")
    
    # Order details
    order_date = Column(DateTime, nullable=False, default=func.now())
    expected_delivery_date = Column(DateTime)
    actual_delivery_date = Column(DateTime)
    
    # Status
    status = Column(String(50), default="draft", nullable=False)
    
    # Financial information
    subtotal = Column(DECIMAL(12, 2), default=0.00)
    tax_amount = Column(DECIMAL(10, 2), default=0.00)
    shipping_amount = Column(DECIMAL(10, 2), default=0.00)
    discount_amount = Column(DECIMAL(10, 2), default=0.00)
    total_amount = Column(DECIMAL(12, 2), default=0.00)
    
    # Notes and terms
    notes = Column(Text)
    terms_and_conditions = Column(Text)
    
    # Approval information
    approved_by = Column(String(255))
    approved_at = Column(DateTime)
    
    # Relationships
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PurchaseOrder(id={self.id}, po_number='{self.po_number}', status='{self.status.value}')>"

class PurchaseOrderItem(BaseModel):
    __tablename__ = "purchase_order_items"
    
    # Relationships
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Item details
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(12, 2), nullable=False)
    
    # Received information
    received_quantity = Column(Integer, default=0)
    remaining_quantity = Column(Integer, default=0)
    
    # Notes
    notes = Column(Text)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product", back_populates="purchase_order_items")
    
    def __repr__(self):
        return f"<PurchaseOrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
