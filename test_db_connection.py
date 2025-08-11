#!/usr/bin/env python3
"""
Simple script to test database connection
"""
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, 'backend')

try:
    from app.core.config import settings
    from app.core.database import test_db_connection
    
    print("=== Database Connection Test ===")
    print(f"Database URL: {settings.DATABASE_URL[:20]}..." if settings.DATABASE_URL else "NOT SET")
    print(f"Port: {settings.PORT}")
    print(f"Debug: {settings.DEBUG}")
    
    if test_db_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
        
except Exception as e:
    print(f"❌ Error testing database connection: {e}")
    import traceback
    traceback.print_exc()
