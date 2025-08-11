#!/usr/bin/env python3
"""
Script to check database tables and their data
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
import traceback

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.app.core.config import settings

def check_database_tables():
    """Check database tables and their data"""
    
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    inspector = inspect(engine)
    
    print("🔍 Checking database tables and data...")
    print(f"Database URL: {settings.DATABASE_URL}")
    print()
    
    # Get all existing tables
    existing_tables = inspector.get_table_names()
    print(f"Existing tables: {existing_tables}")
    print()
    
    # Check each table
    for table_name in existing_tables:
        print(f"📋 Table: {table_name}")
        
        # Get column information
        columns = inspector.get_columns(table_name)
        print(f"   Columns: {[col['name'] for col in columns]}")
        
        # Count rows
        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                print(f"   Row count: {count}")
                
                # Show sample data if table has rows
                if count > 0:
                    result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 1"))
                    sample = result.fetchone()
                    if sample:
                        print(f"   Sample row keys: {list(sample._mapping.keys())}")
        except Exception as e:
            print(f"   Error checking table: {e}")
        
        print()

if __name__ == "__main__":
    check_database_tables()
