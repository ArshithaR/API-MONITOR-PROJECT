#!/usr/bin/env python
"""Diagnose JSON serialization error"""
import sys
import traceback
import json
sys.path.insert(0, '.')

from app import create_app
from app.models import db, User, API, Log
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Check what's in the database after app creation
    user = User.query.first()
    if not user:
        # Create a test user
        user = User(username='testuser', email='test@example.com', password_hash='hash')
        db.session.add(user)
        db.session.commit()
        print(f"Created test user: {user.id}")
    else:
        print(f"Found existing user: {user.id}")
    
    # Create an API
    api = API(name='Test API', url='https://test.com', user_id=user.id)
    db.session.add(api)
    db.session.commit()
    print(f"Created test API: {api.id}")
    
    # Add logs
    for i in range(3):
        log = Log(
            api_id=api.id,
            status_code=200,
            response_time=100 + i*10,
            dns_time=5,
            connection_time=10,
            timestamp=datetime.utcnow() - timedelta(minutes=i*5)
        )
        db.session.add(log)
    db.session.commit()
    print(f"Added 3 logs")

with app.test_client() as client:
    print("\n--- Testing health endpoint ---")
    try:
        resp = client.get(f'/api/health/{api.id}')
        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('Content-Type')}")
        if resp.status_code == 200:
            print(f"Response: {resp.data}")
        else:
            print(f"Error: {resp.data}")
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()
    
    print("\n--- Testing analytics endpoint ---")
    try:
        resp = client.get(f'/api/analytics/{api.id}')
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"Analytics: {data}")
        else:
            print(f"Error: {resp.data}")
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()
    
    print("\n--- Testing chart-data endpoint ---")
    try:
        resp = client.get(f'/api/chart-data/{api.id}?type=line')
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"Chart data: {data}")
        else:
            print(f"Error: {resp.data}")
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()
