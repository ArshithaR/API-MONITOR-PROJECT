from app import db
from app.models import User

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_dashboard_access_unauthorized(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

def test_dashboard_access_authorized(app, client, auth):
    with app.app_context():
        # Using a dummy hash for testing
        user = User(username='testuser', password_hash='pbkdf2:sha256:...') 
        db.session.add(user)
        db.session.commit()
        
    auth.login(username='testuser', password='password')
    response = client.get('/dashboard')
    assert response.status_code == 200