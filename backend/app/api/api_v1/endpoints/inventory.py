from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from decimal import Decimal

from app.core.database import get_db
from app.models.inventory import InventoryItem
from app.models.product import Product
from app.models.location import Location
from app.schemas.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse, InventoryItemWithDetails

router = APIRouter()

@router.get("/", response_model=List[InventoryItemWithDetails])
def get_inventory_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_id: Optional[int] = None,
    location_id: Optional[int] = None,
    low_stock_only: Optional[bool] = None,
    out_of_stock_only: Optional[bool] = None,
    include_details: Optional[bool] = Query(True, description="Include product and location details"),
    db: Session = Depends(get_db)
):
    """Get all inventory items with optional filtering"""
    query = db.query(InventoryItem).options(
        joinedload(InventoryItem.product),
        joinedload(InventoryItem.location)
    )
    
    if product_id:
        query = query.filter(InventoryItem.product_id == product_id)
    if location_id:
        query = query.filter(InventoryItem.location_id == location_id)
    if low_stock_only:
        query = query.filter(InventoryItem.available_quantity <= InventoryItem.reorder_level)
    if out_of_stock_only:
        query = query.filter(InventoryItem.available_quantity <= 0)
    
    inventory_items = query.offset(skip).limit(limit).all()
    
    result = []
    for item in inventory_items:
        # Create a dict with all the item data
        item_dict = {
            "id": item.id,
            "product_id": item.product_id,
            "location_id": item.location_id,
            "quantity": item.quantity,
            "reserved_quantity": item.reserved_quantity,
            "available_quantity": item.available_quantity,
            "reorder_level": item.reorder_level,
            "reorder_quantity": item.reorder_quantity,
            "max_stock_level": item.max_stock_level,
            "storage_location": item.storage_location,
            "storage_zone": item.storage_zone,
            "unit_cost": item.unit_cost,
            "total_value": item.total_value,
            "status": item.status,
            "notes": item.notes,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
            "is_low_stock": item.is_low_stock,
            "stock_status": item.stock_status,
            "product_name": item.product.name if item.product else None,
            "product_sku": item.product.sku if item.product else None,
            "location_name": item.location.name if item.location else None,
            "location_code": item.location.code if item.location else None
        }
        
        item_data = InventoryItemWithDetails(**item_dict)
        result.append(item_data)
    
    return result

@router.get("/summary")
def get_inventory_summary(db: Session = Depends(get_db)):
    """Get inventory summary statistics"""
    try:
        total_items = db.query(InventoryItem).count()
        total_products = db.query(Product).count()
        total_locations = db.query(Location).count()
        
        # Calculate totals using SQLAlchemy func
        from sqlalchemy import func
        
        total_quantity_result = db.query(func.sum(InventoryItem.quantity)).scalar()
        total_quantity = total_quantity_result or 0
        
        total_value_result = db.query(func.sum(InventoryItem.total_value)).scalar()
        total_value = float(total_value_result or 0)
        
        # Low stock items
        low_stock_items = db.query(InventoryItem).filter(
            InventoryItem.available_quantity <= InventoryItem.reorder_level
        ).count()
        
        # Out of stock items
        out_of_stock_items = db.query(InventoryItem).filter(
            InventoryItem.available_quantity <= 0
        ).count()
        
        return {
            "total_items": total_items,
            "total_products": total_products,
            "total_locations": total_locations,
            "total_quantity": total_quantity,
            "total_value": total_value,
            "low_stock_items": low_stock_items,
            "out_of_stock_items": out_of_stock_items
        }
    except Exception as e:
        # Return default values if there's an error
        return {
            "total_items": 0,
            "total_products": 0,
            "total_locations": 0,
            "total_quantity": 0,
            "total_value": 0.0,
            "low_stock_items": 0,
            "out_of_stock_items": 0,
            "error": str(e)
        }

@router.get("/{inventory_id}", response_model=InventoryItemWithDetails)
def get_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    """Get a specific inventory item by ID"""
    inventory_item = db.query(InventoryItem).options(
        joinedload(InventoryItem.product),
        joinedload(InventoryItem.location)
    ).filter(InventoryItem.id == inventory_id).first()
    
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    # Create a dict with all the item data
    item_dict = {
        "id": inventory_item.id,
        "product_id": inventory_item.product_id,
        "location_id": inventory_item.location_id,
        "quantity": inventory_item.quantity,
        "reserved_quantity": inventory_item.reserved_quantity,
        "available_quantity": inventory_item.available_quantity,
        "reorder_level": inventory_item.reorder_level,
        "reorder_quantity": inventory_item.reorder_quantity,
        "max_stock_level": inventory_item.max_stock_level,
        "storage_location": inventory_item.storage_location,
        "storage_zone": inventory_item.storage_zone,
        "unit_cost": inventory_item.unit_cost,
        "total_value": inventory_item.total_value,
        "status": inventory_item.status,
        "notes": inventory_item.notes,
        "created_at": inventory_item.created_at,
        "updated_at": inventory_item.updated_at,
        "is_low_stock": inventory_item.is_low_stock,
        "stock_status": inventory_item.stock_status,
        "product_name": inventory_item.product.name if inventory_item.product else None,
        "product_sku": inventory_item.product.sku if inventory_item.product else None,
        "location_name": inventory_item.location.name if inventory_item.location else None,
        "location_code": inventory_item.location.code if inventory_item.location else None
    }
    
    return InventoryItemWithDetails(**item_dict)

@router.post("/", response_model=InventoryItemResponse)
def create_inventory_item(inventory_item: InventoryItemCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == inventory_item.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    
    # Check if location exists
    location = db.query(Location).filter(Location.id == inventory_item.location_id).first()
    if not location:
        raise HTTPException(status_code=400, detail="Location not found")
    
    # Check if inventory item already exists for this product and location
    existing_item = db.query(InventoryItem).filter(
        InventoryItem.product_id == inventory_item.product_id,
        InventoryItem.location_id == inventory_item.location_id
    ).first()
    
    if existing_item:
        raise HTTPException(status_code=400, detail="Inventory item already exists for this product and location")
    
    # Calculate available quantity
    available_qty = inventory_item.quantity - inventory_item.reserved_quantity
    if available_qty < 0:
        raise HTTPException(status_code=400, detail="Reserved quantity cannot exceed total quantity")
    
    # Calculate total value
    total_value = inventory_item.quantity * inventory_item.unit_cost
    
    db_inventory_item = InventoryItem(
        **inventory_item.dict(),
        available_quantity=available_qty,
        total_value=total_value
    )
    
    db.add(db_inventory_item)
    db.commit()
    db.refresh(db_inventory_item)
    return db_inventory_item

@router.put("/{inventory_id}", response_model=InventoryItemResponse)
def update_inventory_item(inventory_id: int, inventory_item: InventoryItemUpdate, db: Session = Depends(get_db)):
    """Update an inventory item"""
    db_inventory_item = db.query(InventoryItem).filter(InventoryItem.id == inventory_id).first()
    if not db_inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    update_data = inventory_item.dict(exclude_unset=True)
    
    # Handle quantity updates
    if 'quantity' in update_data or 'reserved_quantity' in update_data:
        new_quantity = update_data.get('quantity', db_inventory_item.quantity)
        new_reserved = update_data.get('reserved_quantity', db_inventory_item.reserved_quantity)
        
        if new_reserved > new_quantity:
            raise HTTPException(status_code=400, detail="Reserved quantity cannot exceed total quantity")
        
        # Update available quantity
        update_data['available_quantity'] = new_quantity - new_reserved
    
    # Update total value if quantity or unit cost changed
    if 'quantity' in update_data or 'unit_cost' in update_data:
        new_quantity = update_data.get('quantity', db_inventory_item.quantity)
        new_unit_cost = update_data.get('unit_cost', db_inventory_item.unit_cost)
        update_data['total_value'] = new_quantity * new_unit_cost
    
    for field, value in update_data.items():
        setattr(db_inventory_item, field, value)
    
    db.commit()
    db.refresh(db_inventory_item)
    return db_inventory_item

@router.delete("/{inventory_id}")
def delete_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    """Delete an inventory item"""
    db_inventory_item = db.query(InventoryItem).filter(InventoryItem.id == inventory_id).first()
    if not db_inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    # Check if there's stock before deletion
    if db_inventory_item.quantity > 0:
        raise HTTPException(status_code=400, detail="Cannot delete inventory item with stock")
    
    db.delete(db_inventory_item)
    db.commit()
    return {"message": "Inventory item deleted successfully"}

@router.post("/{inventory_id}/adjust")
def adjust_inventory(
    inventory_id: int,
    quantity_change: int,
    adjustment_type: str = "addition",  # "addition" or "subtraction"
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Adjust inventory quantity"""
    db_inventory_item = db.query(InventoryItem).filter(InventoryItem.id == inventory_id).first()
    if not db_inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    if adjustment_type == "subtraction":
        quantity_change = -quantity_change
    
    new_quantity = db_inventory_item.quantity + quantity_change
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    
    # Update available quantity
    new_available = new_quantity - db_inventory_item.reserved_quantity
    if new_available < 0:
        raise HTTPException(status_code=400, detail="Available quantity cannot be negative")
    
    # Update total value
    new_total_value = new_quantity * db_inventory_item.unit_cost
    
    db_inventory_item.quantity = new_quantity
    db_inventory_item.available_quantity = new_available
    db_inventory_item.total_value = new_total_value
    
    if notes:
        db_inventory_item.notes = notes
    
    db.commit()
    db.refresh(db_inventory_item)
    
    return {
        "message": "Inventory adjusted successfully",
        "new_quantity": new_quantity,
        "new_available_quantity": new_available,
        "adjustment": quantity_change
    }
