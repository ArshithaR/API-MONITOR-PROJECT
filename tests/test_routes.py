import pytest
from flask_login import login_user
from app.models import db, Log

class TestAuthRoutes:
    """Test authentication routes"""
    
    def test_register_user(self, client):
        """Test user registration"""
        response = client.post('/register', data={
            'username': 'newuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Registration successful' in response.data
    
    def test_register_duplicate_user(self, client, auth_user):
        """Test duplicate user registration fails"""
        response = client.post('/register', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert b'Username already exists' in response.data
    
    def test_login_user(self, client, auth_user):
        """Test user login"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'API Performance Dashboard' in response.data
    
    def test_login_invalid_password(self, client, auth_user):
        """Test login with invalid password"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'Invalid username or password' in response.data
    
    def test_logout(self, client, auth_user):
        """Test user logout"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

class TestDashboardRoutes:
    """Test dashboard routes"""
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
    
    def test_dashboard_authenticated(self, client, auth_user):
        """Test dashboard access with authentication"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'API Performance Dashboard' in response.data
    
    def test_performance_page_exists(self, client, auth_user):
        """Test performance analytics page"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/performance')
        assert response.status_code == 200
        assert b'Performance Analytics' in response.data

class TestAPIRoutes:
    """Test API management routes"""
    
    def test_add_api(self, client, auth_user):
        """Test adding a new API"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.post('/add_api', data={
            'name': 'My API',
            'url': 'https://example.com',
            'interval': 60
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'My API' in response.data
    
    def test_delete_api(self, client, auth_user, test_api):
        """Test deleting an API"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get(f'/delete_api/{test_api.id}', follow_redirects=True)
        assert response.status_code == 200
    
    def test_get_chart_data(self, client, auth_user, test_api, test_logs):
        """Test getting chart data"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/api/chart_data')
        assert response.status_code == 200
        
        data = response.get_json()
        assert str(test_api.id) in data

class TestCSVExport:
    """Test CSV export functionality"""
    
    def test_export_csv_get(self, client, auth_user):
        """Test CSV export page"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.get('/export_csv')
        assert response.status_code == 200
    
    def test_export_csv_post(self, client, auth_user, test_api, test_logs):
        """Test CSV download"""
        client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        
        response = client.post('/export_csv')
        assert response.status_code == 200
        assert b'API Name' in response.data
        assert b'Test API' in response.data
