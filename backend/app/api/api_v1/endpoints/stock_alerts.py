from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.stock_alert import StockAlert
from app.models.product import Product
from app.models.location import Location
from app.schemas.stock_alert import StockAlertCreate, StockAlertUpdate, StockAlertResponse, StockAlertWithDetails

router = APIRouter()

@router.get("/", response_model=List[StockAlertResponse])
def get_stock_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    alert_type: Optional[str] = None,
    severity: Optional[str] = None,
    product_id: Optional[int] = None,
    location_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all stock alerts with pagination"""
    query = db.query(StockAlert)
    
    if status:
        # Handle enum status filtering
        try:
            from app.models.stock_alert import AlertStatus
            status_enum = AlertStatus(status)
            query = query.filter(StockAlert.status == status_enum)
        except ValueError:
            # If status is not a valid enum value, return empty list
            return []
    if alert_type:
        # Handle enum alert_type filtering
        try:
            from app.models.stock_alert import AlertType
            alert_type_enum = AlertType(alert_type)
            query = query.filter(StockAlert.alert_type == alert_type_enum)
        except ValueError:
            # If alert_type is not a valid enum value, return empty list
            return []
    if severity:
        query = query.filter(StockAlert.severity == severity)
    if product_id:
        query = query.filter(StockAlert.product_id == product_id)
    if location_id:
        query = query.filter(StockAlert.location_id == location_id)
    
    stock_alerts = query.offset(skip).limit(limit).all()
    return stock_alerts

@router.get("/{alert_id}", response_model=StockAlertWithDetails)
def get_stock_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get a specific stock alert by ID"""
    stock_alert = db.query(StockAlert).filter(StockAlert.id == alert_id).first()
    if not stock_alert:
        raise HTTPException(status_code=404, detail="Stock alert not found")
    return stock_alert

@router.post("/", response_model=StockAlertResponse)
def create_stock_alert(stock_alert: StockAlertCreate, db: Session = Depends(get_db)):
    """Create a new stock alert"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == stock_alert.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    
    # Check if location exists
    location = db.query(Location).filter(Location.id == stock_alert.location_id).first()
    if not location:
        raise HTTPException(status_code=400, detail="Location not found")
    
    db_stock_alert = StockAlert(**stock_alert.dict())
    db.add(db_stock_alert)
    db.commit()
    db.refresh(db_stock_alert)
    return db_stock_alert

@router.put("/{alert_id}", response_model=StockAlertResponse)
def update_stock_alert(
    alert_id: int, 
    stock_alert: StockAlertUpdate, 
    db: Session = Depends(get_db)
):
    """Update a stock alert"""
    db_stock_alert = db.query(StockAlert).filter(StockAlert.id == alert_id).first()
    if not db_stock_alert:
        raise HTTPException(status_code=404, detail="Stock alert not found")
    
    update_data = stock_alert.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_stock_alert, field, value)
    
    db.commit()
    db.refresh(db_stock_alert)
    return db_stock_alert

@router.delete("/{alert_id}")
def delete_stock_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete a stock alert"""
    db_stock_alert = db.query(StockAlert).filter(StockAlert.id == alert_id).first()
    if not db_stock_alert:
        raise HTTPException(status_code=404, detail="Stock alert not found")
    
    db.delete(db_stock_alert)
    db.commit()
    return {"message": "Stock alert deleted successfully"}

@router.put("/{alert_id}/acknowledge", response_model=StockAlertResponse)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge a stock alert"""
    db_stock_alert = db.query(StockAlert).filter(StockAlert.id == alert_id).first()
    if not db_stock_alert:
        raise HTTPException(status_code=404, detail="Stock alert not found")
    
    db_stock_alert.status = "acknowledged"
    db_stock_alert.acknowledged_at = db_stock_alert.updated_at
    db.commit()
    db.refresh(db_stock_alert)
    return db_stock_alert

@router.put("/{alert_id}/resolve", response_model=StockAlertResponse)
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """Resolve a stock alert"""
    db_stock_alert = db.query(StockAlert).filter(StockAlert.id == alert_id).first()
    if not db_stock_alert:
        raise HTTPException(status_code=404, detail="Stock alert not found")
    
    db_stock_alert.status = "resolved"
    db_stock_alert.resolved_at = db_stock_alert.updated_at
    db.commit()
    db.refresh(db_stock_alert)
    return db_stock_alert
