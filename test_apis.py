#!/usr/bin/env python3
"""
Simple test script to check if the APIs are working on port 8000
"""

import requests
import json

BASE_URL = "http://localhost:8000"  # Backend is now running on port 8000

def test_api(endpoint, description):
    """Test a specific API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🧪 Testing {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Success! Found {len(data)} items")
                if data:
                    print(f"   First item keys: {list(data[0].keys())}")
            else:
                print(f"✅ Success! Response keys: {list(data.keys())}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

def main():
    print("🚀 Testing API Endpoints on Port 8000")
    print("=" * 50)
    
    # Test the previously problematic endpoints
    test_api("/api/v1/purchase-orders/?include_items=true", "Purchase Orders with Items")
    test_api("/api/v1/inventory/?include_details=true", "Inventory with Details")
    test_api("/api/v1/locations/", "Locations")
    test_api("/api/v1/stock-alerts/", "Stock Alerts")
    
    # Test some working endpoints for comparison
    test_api("/api/v1/suppliers/", "Suppliers")
    test_api("/api/v1/products/", "Products")
    test_api("/api/v1/categories/", "Categories")

if __name__ == "__main__":
    main()
