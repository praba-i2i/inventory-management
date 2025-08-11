from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem
from app.models.supplier import Supplier
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse, PurchaseOrderWithItems

router = APIRouter()

@router.get("/", response_model=List[PurchaseOrderResponse])
def get_purchase_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    supplier_id: Optional[int] = None,
    status: Optional[str] = None,
    include_items: Optional[bool] = Query(False, description="Include purchase order items"),
    db: Session = Depends(get_db)
):
    """Get all purchase orders with pagination"""
    query = db.query(PurchaseOrder)
    
    if supplier_id:
        query = query.filter(PurchaseOrder.supplier_id == supplier_id)
    if status:
        # Handle enum status filtering
        try:
            from app.models.purchase_order import PurchaseOrderStatus
            status_enum = PurchaseOrderStatus(status)
            query = query.filter(PurchaseOrder.status == status_enum)
        except ValueError:
            # If status is not a valid enum value, return empty list
            return []
    
    purchase_orders = query.offset(skip).limit(limit).all()
    return purchase_orders

@router.get("/{purchase_order_id}", response_model=PurchaseOrderWithItems)
def get_purchase_order(purchase_order_id: int, db: Session = Depends(get_db)):
    """Get a specific purchase order by ID with items"""
    purchase_order = db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()
    if not purchase_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return purchase_order

@router.post("/", response_model=PurchaseOrderResponse)
def create_purchase_order(purchase_order: PurchaseOrderCreate, db: Session = Depends(get_db)):
    """Create a new purchase order"""
    # Check if supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == purchase_order.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=400, detail="Supplier not found")
    
    db_purchase_order = PurchaseOrder(**purchase_order.dict())
    db.add(db_purchase_order)
    db.commit()
    db.refresh(db_purchase_order)
    return db_purchase_order

@router.put("/{purchase_order_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(
    purchase_order_id: int, 
    purchase_order: PurchaseOrderUpdate, 
    db: Session = Depends(get_db)
):
    """Update a purchase order"""
    db_purchase_order = db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()
    if not db_purchase_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    # Check if supplier exists (if being updated)
    if purchase_order.supplier_id:
        supplier = db.query(Supplier).filter(Supplier.id == purchase_order.supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=400, detail="Supplier not found")
    
    update_data = purchase_order.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_purchase_order, field, value)
    
    db.commit()
    db.refresh(db_purchase_order)
    return db_purchase_order

@router.delete("/{purchase_order_id}")
def delete_purchase_order(purchase_order_id: int, db: Session = Depends(get_db)):
    """Delete a purchase order"""
    db_purchase_order = db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()
    if not db_purchase_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    db.delete(db_purchase_order)
    db.commit()
    return {"message": "Purchase order deleted successfully"}
