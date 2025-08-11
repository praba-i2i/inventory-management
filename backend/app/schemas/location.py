from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    type: str = "warehouse"  # warehouse, store, office, other
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    capacity: Optional[int] = None
    status: str = "active"  # active, inactive

    @validator('type')
    def validate_type(cls, v):
        allowed_types = ['warehouse', 'store', 'office', 'other']
        if v not in allowed_types:
            raise ValueError(f'Type must be one of: {allowed_types}')
        return v

    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['active', 'inactive']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None

    @validator('type')
    def validate_type(cls, v):
        if v is not None:
            allowed_types = ['warehouse', 'store', 'office', 'other']
            if v not in allowed_types:
                raise ValueError(f'Type must be one of: {allowed_types}')
        return v

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['active', 'inactive']
            if v not in allowed_statuses:
                raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v

class LocationResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
