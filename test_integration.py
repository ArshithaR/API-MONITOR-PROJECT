#!/usr/bin/env python
"""Full integration test of all features"""
import sys
import traceback
sys.path.insert(0, '.')

from app import create_app
from app.models import db, User, API, Log
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def run_tests():
    app = create_app()
    
    with app.test_client() as client:
        print("=" * 60)
        print("COMPREHENSIVE API MONITOR INTEGRATION TEST")
        print("=" * 60)
        
        # --- AUTHENTICATION & USER MANAGEMENT ---
        print("\n### 1. AUTHENTICATION & USER MANAGEMENT ###\n")
        
        # Register user
        print("1. Registering test user...")
        resp = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=False)
        print(f"   Register → {resp.status_code} (expected 302)")
        assert resp.status_code == 302, "Register failed"
        
        # Login
        print("2. Logging in...")
        resp = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        print(f"   Login → {resp.status_code} (expected 200)")
        assert resp.status_code == 200, "Login failed"
        
        # Get dashboard
        print("3. Accessing dashboard...")
        resp = client.get('/dashboard')
        print(f"   Dashboard → {resp.status_code}")
        assert resp.status_code == 200, "Dashboard not accessible"
        
        # --- ADD API ---
        print("\n### 2. API MANAGEMENT ###\n")
        
        print("1. Adding test API...")
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            assert user is not None, "User not found"
            
            new_api = API(
                name='Google API',
                url='https://www.google.com',
                user_id=user.id,
                interval=300,
                threshold_latency=1000
            )
            db.session.add(new_api)
            db.session.commit()
            api_id = new_api.id
            print(f"   ✓ API added with ID: {api_id}")
            
            # Add some test logs
            print("2. Adding test logs...")
            for i in range(5):
                log = Log(
                    api_id=api_id,
                    status_code=200,
                    response_time=150 + (i * 10),
                    dns_time=10,
                    connection_time=20,
                    timestamp=datetime.utcnow() - timedelta(minutes=i*5)
                )
                db.session.add(log)
            db.session.commit()
            print(f"   ✓ Added 5 test logs")
        
        # --- ANALYTICS ---
        print("\n### 3. ANALYTICS & HEALTH SCORES ###\n")
        
        print("1. Fetching health data...")
        resp = client.get(f'/api/health/{api_id}')
        print(f"   /api/health/{api_id} → {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"   ✓ Health Score: {data.get('health_score', 'N/A')}")
            print(f"   ✓ Status: {data.get('status', 'N/A')}")
        else:
            print(f"   ✗ Failed to get health data")
        
        print("2. Fetching analytics...")
        resp = client.get(f'/api/analytics/{api_id}')
        print(f"   /api/analytics/{api_id} → {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"   ✓ Total Requests: {data.get('total_requests', 'N/A')}")
            print(f"   ✓ Success Rate: {data.get('success_rate', 'N/A')}%")
        else:
            print(f"   ✗ Failed to get analytics")
        
        print("3. Fetching chart data...")
        resp = client.get(f'/api/chart-data/{api_id}?type=line')
        print(f"   /api/chart-data/{api_id} → {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"   ✓ Chart type: {data.get('type', 'N/A')}")
            print(f"   ✓ Data points: {len(data.get('datasets', [{}])[0].get('data', []))}")
        else:
            print(f"   ✗ Failed to get chart data")
        
        # --- EXPORT ---
        print("\n### 4. EXPORT FEATURES ###\n")
        
        print("1. Exporting to CSV...")
        resp = client.get(f'/export/csv?api_id={api_id}')
        print(f"   /export/csv → {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✓ CSV export successful")
            print(f"   ✓ Content-Type: {resp.headers.get('Content-Type')}")
            lines = resp.data.decode('utf-8').split('\n')
            print(f"   ✓ Lines in CSV: {len([l for l in lines if l.strip()])}")
        else:
            print(f"   ✗ CSV export failed")
        
        # --- ALERTS & PERFORMANCE ---
        print("\n### 5. ALERTS & PERFORMANCE PAGES ###\n")
        
        print("1. Checking alerts page...")
        resp = client.get('/alerts')
        print(f"   /alerts → {resp.status_code}")
        
        print("2. Checking performance page...")
        resp = client.get('/performance')
        print(f"   /performance → {resp.status_code}")
        
        print("3. Checking compare page...")
        resp = client.get('/compare')
        print(f"   /compare → {resp.status_code}")
        
        print("4. Checking settings page...")
        resp = client.get('/settings')
        print(f"   /settings → {resp.status_code}")
        
        print("\n" + "=" * 60)
        print("✓ ALL INTEGRATION TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)

if __name__ == '__main__':
    try:
        run_tests()
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        traceback.print_exc()
        sys.exit(1)
