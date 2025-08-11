#!/usr/bin/env python3
"""
Simple script to test environment variables
"""
import os

print("=== Environment Variables Test ===")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
print(f"PORT: {os.getenv('PORT', 'NOT SET')}")
print(f"PYTHONPATH: {os.getenv('PYTHONPATH', 'NOT SET')}")

# List all environment variables
print("\n=== All Environment Variables ===")
for key, value in os.environ.items():
    if 'DATABASE' in key.upper() or 'PORT' in key.upper():
        print(f"{key}: {value}")
