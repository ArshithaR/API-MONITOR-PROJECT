"""Unit Tests for API Monitor"""
import pytest
from datetime import datetime, timedelta
from app import db, create_app
from app.models import User, API, Log, HealthScore, Alert, Notification
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create test user"""
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash=generate_password_hash('password123')
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def test_api(app, test_user):
    """Create test API"""
    api = API(
        name='Test API',
        url='https://api.example.com',
        user_id=test_user.id,
        interval=300,
        threshold_latency=1000
    )
    db.session.add(api)
    db.session.commit()
    return api


class TestAuthentication:
    """Test authentication routes"""
    
    def test_index_redirect_authenticated(self, client, test_user):
        """Test that authenticated users are redirected from index"""
        with client:
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = client.get('/')
            assert response.status_code == 302  # Redirect
    
    def test_register_new_user(self, client):
        """Test user registration"""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        assert b'Account created' in response.data
        
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'new@example.com'
    
    def test_duplicate_username(self, client, test_user):
        """Test that duplicate usernames are rejected"""
        response = client.post('/register', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        assert b'already exists' in response.data
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Dashboard' in response.data or b'dashboard' in response.data
    
    def test_login_failure(self, client):
        """Test login with wrong password"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert b'Unsuccessful' in response.data


class TestDashboard:
    """Test dashboard functionality"""
    
    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires authentication"""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
    
    def test_dashboard_loads(self, client, test_user):
        """Test dashboard loads for authenticated user"""
        with client:
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = client.get('/dashboard')
            assert response.status_code == 200
    
    def test_add_api(self, client, test_user):
        """Test adding an API"""
        with client:
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = client.post('/add_api', data={
                'name': 'My API',
                'url': 'https://myapi.example.com',
                'interval': 60,
                'threshold': 500
            }, follow_redirects=True)
            
            api = API.query.filter_by(name='My API').first()
            assert api is not None
            assert api.url == 'https://myapi.example.com'
            assert api.interval == 60
            assert api.threshold_latency == 500


class TestModels:
    """Test database models"""
    
    def test_user_model(self, test_user):
        """Test User model"""
        assert test_user.username == 'testuser'
        assert test_user.email == 'test@example.com'
    
    def test_api_model(self, test_api):
        """Test API model"""
        assert test_api.name == 'Test API'
        assert test_api.url == 'https://api.example.com'
        assert test_api.interval == 300
        assert test_api.threshold_latency == 1000
    
    def test_log_model(self, test_api):
        """Test Log model"""
        log = Log(
            api_id=test_api.id,
            status_code=200,
            response_time=125.5,
            dns_time=10.0,
            connection_time=15.0
        )
        db.session.add(log)
        db.session.commit()
        
        retrieved_log = Log.query.first()
        assert retrieved_log.status_code == 200
        assert retrieved_log.response_time == 125.5
    
    def test_health_score_model(self, test_api):
        """Test HealthScore model"""
        health = HealthScore(
            api_id=test_api.id,
            uptime_percentage=99.5,
            avg_response_time=150.0,
            success_rate=98.0,
            health_score=98.5,
            status='excellent'
        )
        db.session.add(health)
        db.session.commit()
        
        retrieved_health = HealthScore.query.first()
        assert retrieved_health.health_score == 98.5
        assert retrieved_health.status == 'excellent'
    
    def test_alert_model(self, test_api, test_user):
        """Test Alert model"""
        alert = Alert(
            api_id=test_api.id,
            user_id=test_user.id,
            alert_type='down',
            message='API is down',
            severity='critical'
        )
        db.session.add(alert)
        db.session.commit()
        
        retrieved_alert = Alert.query.first()
        assert retrieved_alert.alert_type == 'down'
        assert retrieved_alert.severity == 'critical'


class TestAnalytics:
    """Test analytics functions"""
    
    def test_health_score_calculation(self, test_api):
        """Test health score calculation"""
        from app.analytics import calculate_health_score
        
        # Add logs
        for i in range(5):
            log = Log(
                api_id=test_api.id,
                status_code=200,
                response_time=100.0 + i * 10
            )
            db.session.add(log)
        db.session.commit()
        
        uptime, avg_time, success, score, status = calculate_health_score(test_api.id)
        assert uptime == 100.0
        assert score > 0
        assert status in ['excellent', 'good', 'poor']
    
    def test_analytics_data(self, test_api):
        """Test analytics data retrieval"""
        from app.analytics import get_analytics_data
        
        # Add test logs
        for i in range(10):
            log = Log(
                api_id=test_api.id,
                status_code=200 if i % 2 == 0 else 500,
                response_time=100.0 + i * 5
            )
            db.session.add(log)
        db.session.commit()
        
        data = get_analytics_data(test_api.id, 24)
        assert data['total_requests'] == 10
        assert data['success_count'] == 5
        assert data['failure_count'] == 5
        assert data['success_rate'] == 50.0


class TestExport:
    """Test export functionality"""
    
    def test_csv_export(self, client, test_user, test_api):
        """Test CSV export"""
        # Add test logs
        for i in range(3):
            log = Log(
                api_id=test_api.id,
                status_code=200,
                response_time=100.0 + i
            )
            db.session.add(log)
        db.session.commit()
        
        with client:
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = client.get(f'/export/csv?api_id={test_api.id}')
            
            assert response.status_code == 200
            assert b'API Name' in response.data
            assert b'Test API' in response.data


class TestAPI:
    """Test API endpoints"""
    
    def test_analytics_endpoint(self, client, test_user, test_api):
        """Test analytics API endpoint"""
        # Add logs
        for i in range(5):
            log = Log(
                api_id=test_api.id,
                status_code=200,
                response_time=100.0 + i * 10
            )
            db.session.add(log)
        db.session.commit()
        
        with client:
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = client.get(f'/api/analytics/{test_api.id}')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'success_rate' in data
            assert 'avg_response_time' in data
    
    def test_health_endpoint(self, client, test_user, test_api):
        """Test health API endpoint"""
        health = HealthScore(
            api_id=test_api.id,
            health_score=95.0,
            status='excellent',
            uptime_percentage=99.5,
            avg_response_time=150.0,
            success_rate=98.0
        )
        db.session.add(health)
        db.session.commit()
        
        with client:
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = client.get(f'/api/health/{test_api.id}')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['health_score'] == 95.0
            assert data['status'] == 'excellent'
