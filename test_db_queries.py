#!/usr/bin/env python3
"""
Script to test database queries directly
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import traceback

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.app.core.config import settings
from backend.app.models import Location, InventoryItem, PurchaseOrder, StockAlert

def test_database_queries():
    """Test database queries directly"""
    
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    print("🧪 Testing database queries directly...")
    print(f"Database URL: {settings.DATABASE_URL}")
    print()
    
    try:
        db = SessionLocal()
        
        # Test locations query
        print("Testing locations query...")
        try:
            locations = db.query(Location).limit(5).all()
            print(f"✅ Found {len(locations)} locations")
            if locations:
                print(f"   First location: {locations[0].name}")
        except Exception as e:
            print(f"❌ Error querying locations: {e}")
            traceback.print_exc()
        
        # Test inventory items query
        print("\nTesting inventory items query...")
        try:
            inventory_items = db.query(InventoryItem).limit(5).all()
            print(f"✅ Found {len(inventory_items)} inventory items")
            if inventory_items:
                print(f"   First item: {inventory_items[0].id}")
        except Exception as e:
            print(f"❌ Error querying inventory items: {e}")
            traceback.print_exc()
        
        # Test purchase orders query
        print("\nTesting purchase orders query...")
        try:
            purchase_orders = db.query(PurchaseOrder).limit(5).all()
            print(f"✅ Found {len(purchase_orders)} purchase orders")
            if purchase_orders:
                print(f"   First order: {purchase_orders[0].po_number}")
        except Exception as e:
            print(f"❌ Error querying purchase orders: {e}")
            traceback.print_exc()
        
        # Test stock alerts query
        print("\nTesting stock alerts query...")
        try:
            stock_alerts = db.query(StockAlert).limit(5).all()
            print(f"✅ Found {len(stock_alerts)} stock alerts")
            if stock_alerts:
                print(f"   First alert: {stock_alerts[0].title}")
        except Exception as e:
            print(f"❌ Error querying stock alerts: {e}")
            traceback.print_exc()
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_database_queries()
