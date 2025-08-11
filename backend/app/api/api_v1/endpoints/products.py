from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from app.core.database import get_db
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.inventory import InventoryItem
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductWithInventory

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    is_featured: Optional[bool] = None,
    search: Optional[str] = None,
    include_inventory: Optional[bool] = False,
    db: Session = Depends(get_db)
):
    """Get all products with optional filtering"""
    query = db.query(Product)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if supplier_id:
        query = query.filter(Product.supplier_id == supplier_id)
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    if is_featured is not None:
        query = query.filter(Product.is_featured == is_featured)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) |
            (Product.sku.ilike(search_term)) |
            (Product.description.ilike(search_term))
        )
    
    products = query.offset(skip).limit(limit).all()
    
    # If include_inventory is True, return products with inventory data
    if include_inventory:
        result = []
        for product in products:
            # Calculate inventory totals
            inventory_items = db.query(InventoryItem).filter(InventoryItem.product_id == product.id).all()
            
            total_quantity = sum(item.quantity for item in inventory_items)
            total_value = sum(float(item.total_value or 0) for item in inventory_items)
            low_stock_count = sum(1 for item in inventory_items if item.is_low_stock)
            out_of_stock_count = sum(1 for item in inventory_items if (item.available_quantity or 0) <= 0)
            
            # Create a dict with product data and inventory info
            product_dict = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "sku": product.sku,
                "barcode": product.barcode,
                "category_id": product.category_id,
                "specifications": product.specifications,
                "cost_price": product.cost_price,
                "selling_price": product.selling_price,
                "unit": product.unit,
                "is_active": product.is_active,
                "is_featured": product.is_featured,
                "weight": product.weight,
                "length": product.length,
                "width": product.width,
                "height": product.height,
                "supplier_id": product.supplier_id,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
                "total_quantity": total_quantity,
                "total_value": total_value,
                "low_stock_count": low_stock_count,
                "out_of_stock_count": out_of_stock_count
            }
            result.append(product_dict)
        return result
    
    return products

@router.get("/with-inventory", response_model=List[ProductWithInventory])
def get_products_with_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get products with inventory information"""
    products = db.query(Product).offset(skip).limit(limit).all()
    
    result = []
    for product in products:
        # Calculate inventory totals
        inventory_items = db.query(InventoryItem).filter(InventoryItem.product_id == product.id).all()
        
        total_quantity = sum(item.quantity for item in inventory_items)
        total_value = sum(float(item.total_value or 0) for item in inventory_items)
        low_stock_count = sum(1 for item in inventory_items if item.is_low_stock)
        out_of_stock_count = sum(1 for item in inventory_items if (item.available_quantity or 0) <= 0)
        
        product_data = ProductWithInventory(
            **product.__dict__,
            total_quantity=total_quantity,
            total_value=total_value,
            low_stock_count=low_stock_count,
            out_of_stock_count=out_of_stock_count
        )
        result.append(product_data)
    
    return result

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    # Check if category exists
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    
    # Check if supplier exists (if provided)
    if product.supplier_id:
        supplier = db.query(Supplier).filter(Supplier.id == product.supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=400, detail="Supplier not found")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if new SKU already exists (if being updated)
    if product.sku and product.sku != db_product.sku:
        existing_product = db.query(Product).filter(Product.sku == product.sku).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="SKU already exists")
    
    # Check if category exists (if being updated)
    if product.category_id:
        category = db.query(Category).filter(Category.id == product.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
    
    # Check if supplier exists (if being updated)
    if product.supplier_id:
        supplier = db.query(Supplier).filter(Supplier.id == product.supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=400, detail="Supplier not found")
    
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product has inventory
    inventory_items = db.query(InventoryItem).filter(InventoryItem.product_id == product_id).all()
    if inventory_items:
        raise HTTPException(status_code=400, detail="Cannot delete product with existing inventory")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
