import pytest
from app import create_app, db
from app.models import User, API, APILog
from datetime import datetime

@pytest.fixture
def app():
    """Create test app"""
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
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_app_creation(app):
    """Test that app is created"""
    assert app is not None
    assert app.config['TESTING'] == True

def test_home_page(client):
    """Test home page redirects"""
    response = client.get('/')
    assert response.status_code in [200, 302]

def test_login_page(client):
    """Test login page loads"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data or b'login' in response.data

def test_register_page(client):
    """Test register page loads"""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data or b'register' in response.data

def test_register_user(app, client):
    """Test user registration"""
    with app.app_context():
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'test@test.com'

def test_login_user(app, client):
    """Test user login"""
    with app.app_context():
        user = User(username='testuser', email='test@test.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200

def test_dashboard_requires_login(client):
    """Test dashboard requires login"""
    response = client.get('/dashboard')
    assert response.status_code == 302  # Redirect to login
