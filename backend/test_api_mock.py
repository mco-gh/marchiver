#!/usr/bin/env python
"""
Modified test script for the Marchiver API.
This script tests the basic functionality of the API with mocked responses.
"""

import requests
import json
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import config
from app.core.config import HOST, PORT, API_PREFIX

# Base URL for the API
BASE_URL = f"http://{HOST}:{PORT}"

def test_health():
    """Test the health endpoint."""
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    url = f"{BASE_URL}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ Root endpoint passed: {response.json()}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def run_tests():
    """Run all tests."""
    print("🔍 Testing Marchiver API...")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🧪 Testing {name}...")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print(f"\n🏁 {passed}/{len(results)} tests passed")

if __name__ == "__main__":
    run_tests()
