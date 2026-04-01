import pytest
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

def test_index_page(client):
    """Checks if the home page loads."""
    response = client.get('/')
    assert response.status_code == 200

def test_login_page(client):
    """Checks if the login page loads."""
    response = client.get('/login')
    assert response.status_code == 200

def test_dashboard_access_unauthorized(client):
    """Ensures logged-out users are redirected to login/index."""
    # follow_redirects=True ensures we see the final page after the redirect
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    # Check for "Login" text to confirm we were sent to the login/index page
    assert b"Login" in response.data

def test_dashboard_access_authorized(app, client, auth):
    """Tests if a registered user can reach the dashboard."""
    with app.app_context():
        # Correctly hash the password so auth.login actually works
        hashed_pw = generate_password_hash('password')
        user = User(username='testuser', password_hash=hashed_pw) 
        db.session.add(user)
        db.session.commit()
        
    # Trigger the login fixture
    auth.login(username='testuser', password='password')
    
    response = client.get('/dashboard')
    assert response.status_code == 200
    # Optional: Check if the dashboard title or a specific UI element is present
    assert b"Dashboard" in response.data