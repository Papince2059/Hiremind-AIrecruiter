#!/usr/bin/env python3
"""
Simple Connection Test for Voicruit Python Backend
"""

import requests
import sys

def test_backend():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is running on port 8080")
            return True
        else:
            print(f"X Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("X Backend is not running on port 8080")
        print("  Start it with: python main.py")
        return False
    except Exception as e:
        print(f"X Error: {e}")
        return False

def test_api_docs():
    """Test if API docs are accessible"""
    try:
        response = requests.get("http://localhost:8080/docs", timeout=5)
        if response.status_code == 200:
            print("✓ API documentation is accessible")
            return True
        else:
            print(f"X API docs returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"X API docs error: {e}")
        return False

def test_cors():
    """Test CORS configuration"""
    try:
        headers = {
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'GET'
        }
        response = requests.options("http://localhost:8080/api/interviews/my", headers=headers, timeout=5)
        
        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        if cors_origin:
            print(f"✓ CORS configured for: {cors_origin}")
            return True
        else:
            print("X CORS not configured")
            return False
    except Exception as e:
        print(f"X CORS test error: {e}")
        return False

def main():
    print("Voicruit Backend Connection Test")
    print("=" * 40)
    
    # Test backend
    print("\n1. Testing backend...")
    backend_ok = test_backend()
    
    if not backend_ok:
        print("\nBackend is not running. Please start it first:")
        print("  cd Voicruiter/python-backend")
        print("  python main.py")
        sys.exit(1)
    
    # Test API docs
    print("\n2. Testing API documentation...")
    docs_ok = test_api_docs()
    
    # Test CORS
    print("\n3. Testing CORS...")
    cors_ok = test_cors()
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print(f"Backend: {'PASS' if backend_ok else 'FAIL'}")
    print(f"API Docs: {'PASS' if docs_ok else 'FAIL'}")
    print(f"CORS: {'PASS' if cors_ok else 'FAIL'}")
    
    if backend_ok and docs_ok and cors_ok:
        print("\n✓ All tests passed! Backend is ready.")
        print("\nNext steps:")
        print("1. Start frontend: cd Voicruiter/userpanel && npm run dev")
        print("2. Visit: http://localhost:5173")
        print("3. Test the full application")
    else:
        print("\nX Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
