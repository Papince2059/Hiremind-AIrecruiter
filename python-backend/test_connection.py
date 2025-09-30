#!/usr/bin/env python3
"""
Test script to verify backend connection and endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_backend_connection():
    """Test basic backend connectivity"""
    try:
        print("Testing backend connection...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Backend is running")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 8080")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False
    
    return True

def test_health_endpoint():
    """Test health check endpoint"""
    try:
        print("\nTesting health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False
    
    return True

def test_user_endpoint():
    """Test user endpoint"""
    try:
        print("\nTesting user endpoint...")
        response = requests.get(f"{BASE_URL}/api/user")
        if response.status_code == 200:
            print("✅ User endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ User endpoint returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing user endpoint: {e}")
        return False
    
    return True

def test_interviews_endpoint():
    """Test interviews endpoint"""
    try:
        print("\nTesting interviews endpoint...")
        response = requests.get(f"{BASE_URL}/api/interviews/my")
        if response.status_code == 200:
            print("✅ Interviews endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Interviews endpoint returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing interviews endpoint: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting backend connection tests...\n")
    
    tests = [
        test_backend_connection,
        test_health_endpoint,
        test_user_endpoint,
        test_interviews_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready for frontend connection.")
    else:
        print("⚠️  Some tests failed. Check the backend setup.")
    
    return passed == total

if __name__ == "__main__":
    main()