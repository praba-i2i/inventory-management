#!/usr/bin/env python3
"""
Script to check actual enum values in the database
"""

import os
import sys
from sqlalchemy import create_engine, text

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.app.core.config import settings

def check_enum_values():
    """Check actual enum values in the database"""
    
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    
    print("🔍 Checking enum values in the database...")
    print(f"Database URL: {settings.DATABASE_URL}")
    print()
    
    try:
        with engine.connect() as conn:
            # Check purchase order statuses
            print("📋 Purchase order statuses:")
            result = conn.execute(text("SELECT DISTINCT status FROM purchase_orders"))
            statuses = [row[0] for row in result.fetchall()]
            for status in statuses:
                print(f"   '{status}'")
            
            # Check stock alert types
            print("\n📋 Stock alert types:")
            result = conn.execute(text("SELECT DISTINCT alert_type FROM stock_alerts"))
            alert_types = [row[0] for row in result.fetchall()]
            for alert_type in alert_types:
                print(f"   '{alert_type}'")
            
            # Check stock alert statuses
            print("\n📋 Stock alert statuses:")
            result = conn.execute(text("SELECT DISTINCT status FROM stock_alerts"))
            alert_statuses = [row[0] for row in result.fetchall()]
            for alert_status in alert_statuses:
                print(f"   '{alert_status}'")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_enum_values()
