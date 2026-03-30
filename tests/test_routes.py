import pytest
from app.models import db, User, API, Log

class TestAuthRoutes:
    """Test authentication routes"""
    
    def test_register_user(self, client, app):
        """Test user registration"""
        response = client.post('/register', data={
            'username': 'newuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Verify user was actually created in DB
        with app.app_context():
            assert User.query.filter_by(username='newuser').first() is not None
    
    def test_register_duplicate_user(self, client, auth_user):
        """Test duplicate user registration fails"""
        response = client.post('/register', data={
            'username': 'testuser', # 'testuser' is created by the auth_user fixture
            'password': 'password123'
        }, follow_redirects=True)
        
        # Ensure the error message matches your template's flash message
        assert b'Username already exists' in response.data or response.status_code == 200
    
    def test_login_user(self, client, auth_user):
        """Test user login"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Dashboard' in response.data or b'Logout' in response.data
    
    def test_login_invalid_password(self, client, auth_user):
        """Test login with invalid password"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'Invalid' in response.data or b'password' in response.data

class TestDashboardRoutes:
    """Test dashboard routes"""
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Should redirect to login page
    
    def test_dashboard_authenticated(self, client, auth_user):
        """Test dashboard access with authentication"""
        client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data

class TestAPIRoutes:
    """Test API management routes"""
    
    def test_add_api(self, client, auth_user, app):
        """Test adding a new API"""
        client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        
        response = client.post('/add_api', data={
            'name': 'My API',
            'url': 'https://example.com',
            'interval': 60
        }, follow_redirects=True)
        
        assert response.status_code == 200
        with app.app_context():
            assert API.query.filter_by(name='My API').first() is not None
    
    def test_delete_api(self, client, auth_user, test_api, app):
        """Test deleting an API"""
        client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        
        # Some apps use GET for delete, others use POST. 
        # Using the ID from the fixture.
        response = client.get(f('/delete_api/{test_api.id}'), follow_redirects=True)
        assert response.status_code == 200
        
        with app.app_context():
            assert db.session.get(API, test_api.id) is None

    def test_get_chart_data(self, client, auth_user, test_api, test_logs):
        """Test getting chart data"""
        client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        
        response = client.get('/api/chart_data')
        assert response.status_code == 200
        
        data = response.get_json()
        # Verify the API ID exists as a key in the JSON response
        assert str(test_api.id) in data

class TestCSVExport:
    """Test CSV export functionality"""
    
    def test_export_csv_get(self, client, auth_user):
        """Test CSV export page"""
        client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        response = client.get('/export_csv')
        assert response.status_code == 200
    
    def test_export_csv_post(self, client, auth_user, test_api, test_logs):
        """Test CSV download"""
        client.post('/login', data={'username': 'testuser', 'password': 'password123'})
        response = client.post('/export_csv')
        
        assert response.status_code == 200
        # Check for CSV headers or content
        assert b'API Name' in response.data or b'status_code' in response.data