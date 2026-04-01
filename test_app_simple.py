#!/usr/bin/env python
"""Test the actual Flask app routes with better error handling"""
import sys
import traceback
sys.path.insert(0, '.')

try:
    from app import create_app
    print("✓ create_app imported successfully")
    
    app = create_app()
    print("✓ App created successfully")
    
    with app.test_client() as client:
        print("\n--- Testing routes ---")
        
        # Test 1: Home without login
        print("\n1. GET / (Home)")
        try:
            response = client.get('/')
            print(f"   Status: {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
            traceback.print_exc()
        
        # Test 2: Login page
        print("\n2. GET /login")
        try:
            response = client.get('/login')
            print(f"   Status: {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
            traceback.print_exc()
        
        # Test 3: Register 
        print("\n3. POST /register")
        try:
            response = client.post('/register', data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }, follow_redirects=False)
            print(f"   Status: {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
            traceback.print_exc()
        
        # Test 4: Export CSV (should redirect to login)
        print("\n4. GET /export/csv (should redirect)")
        try:
            response = client.get('/export/csv', follow_redirects=False)
            print(f"   Status: {response.status_code}")
            print(f"   Location: {response.headers.get('Location', 'N/A')}")
        except Exception as e:
            print(f"   Error: {e}")
            traceback.print_exc()

except Exception as e:
    print(f"✗ Fatal error: {e}")
    traceback.print_exc()
    sys.exit(1)
