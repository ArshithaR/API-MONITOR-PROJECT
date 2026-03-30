import pytest
import os
from app import create_app
from app.models import db, User, API, Log
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create app with test config"""
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
def auth_user(app):
    """Create test user"""
    with app.app_context():
        user = User(username='testuser', password=generate_password_hash('password123'))
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def test_api(app, auth_user):
    """Create test API"""
    with app.app_context():
        api = API(
            user_id=auth_user.id,
            name='Test API',
            url='https://api.example.com',
            interval=60
        )
        db.session.add(api)
        db.session.commit()
        return api

@pytest.fixture
def test_logs(app, test_api):
    """Create test logs"""
    with app.app_context():
        logs = [
            Log(api_id=test_api.id, status_code=200, response_time=100.5),
            Log(api_id=test_api.id, status_code=200, response_time=150.3),
            Log(api_id=test_api.id, status_code=500, response_time=2000.1),
        ]
        for log in logs:
            db.session.add(log)
        db.session.commit()
        return logs
