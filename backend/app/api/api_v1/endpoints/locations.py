from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse

router = APIRouter()

@router.get("/", response_model=List[LocationResponse])
def get_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all locations with pagination"""
    locations = db.query(Location).offset(skip).limit(limit).all()
    return locations

@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Get a specific location by ID"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.post("/", response_model=LocationResponse)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    """Create a new location"""
    # Check if location code already exists
    existing_location = db.query(Location).filter(Location.code == location.code).first()
    if existing_location:
        raise HTTPException(status_code=400, detail="Location code already exists")
    
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int, 
    location: LocationUpdate, 
    db: Session = Depends(get_db)
):
    """Update a location"""
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Check if new code conflicts with existing location
    if location.code and location.code != db_location.code:
        existing_location = db.query(Location).filter(Location.code == location.code).first()
        if existing_location:
            raise HTTPException(status_code=400, detail="Location code already exists")
    
    # Update fields
    update_data = location.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_location, field, value)
    
    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a location"""
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Check if location has associated inventory items
    if db_location.inventory_items:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete location with associated inventory items"
        )
    
    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully"}
