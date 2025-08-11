#!/usr/bin/env python3
"""
Simple test to check just the locations API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_locations_api():
    """Test the locations API specifically"""
    url = f"{BASE_URL}/api/v1/locations/"
    print(f"🧪 Testing Locations API")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data)} locations")
            if data:
                print(f"   First location: {json.dumps(data[0], indent=2, default=str)}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_locations_api()
