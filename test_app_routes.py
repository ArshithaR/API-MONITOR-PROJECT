#!/usr/bin/env python
"""Test the actual Flask app routes"""
import sys
sys.path.insert(0, '.')

from app import create_app

app = create_app()

with app.test_client() as client:
    # Test export/csv without login (should redirect or 404)
    print("Testing /export/csv without login...")
    response = client.get('/export/csv')
    print(f"  Status: {response.status_code}")
    print(f"  Location header: {response.headers.get('Location', 'N/A')}")
    
    # Test performance without login
    print("\nTesting /performance without login...")
    response = client.get('/performance')
    print(f"  Status: {response.status_code}")
    print(f"  Location header: {response.headers.get('Location', 'N/A')}")
    
    # Test login page
    print("\nTesting /login...")
    response = client.get('/login')
    print(f"  Status: {response.status_code}")
    
    # Test home
    print("\nTesting /...")
    response = client.get('/')
    print(f"  Status: {response.status_code}")
    
    # First, register a user
    print("\n--- Registering test user ---")
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    print(f"Register response: {response.status_code}")
    
    # Now login
    print("\n--- Logging in ---")
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)
    print(f"Login response: {response.status_code}")
    
    # Now test export/csv with login
    print("\n--- Testing /export/csv after login ---")
    response = client.get('/export/csv')
    print(f"  Status: {response.status_code}")
    print(f"  Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"  First 100 chars: {response.data[:100]}")
    
    # Test performance after login
    print("\n--- Testing /performance after login ---")
    response = client.get('/performance')
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        print(f"  Content preview: {response.data[:200]}")
