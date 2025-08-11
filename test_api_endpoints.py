#!/usr/bin/env python3
"""
Test script to verify API endpoints are working correctly
"""
import requests
import json

BASE_URL = "https://inventory-management-production-82d5.up.railway.app"

def test_endpoint(endpoint, expected_status=200):
    """Test a specific endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        print(f"Testing: {url}")
        response = requests.get(url, allow_redirects=True)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        print(f"Headers: {dict(response.headers)}")
        print("-" * 50)
        return response.status_code == expected_status
    except Exception as e:
        print(f"Error: {e}")
        print("-" * 50)
        return False

def main():
    print("Testing API Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    test_endpoint("/")
    test_endpoint("/health")
    test_endpoint("/test")
    test_endpoint("/api-test")
    test_endpoint("/debug")
    
    # Test API v1 endpoints
    test_endpoint("/api/v1/products")
    test_endpoint("/api/v1/categories")
    test_endpoint("/api/v1/suppliers")
    test_endpoint("/api/v1/locations")
    test_endpoint("/api/v1/inventory")
    
    print("API Testing Complete")

if __name__ == "__main__":
    main()
