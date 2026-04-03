from app import db
from app.models import User


def test_app_creation(app):
    """Test that app is created."""
    assert app is not None
    assert app.config["TESTING"] is True


def test_home_page(client):
    """Test home page redirects."""
    response = client.get("/")
    assert response.status_code in [200, 302]


def test_login_page(client):
    """Test login page loads."""
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data or b"login" in response.data


def test_register_page(client):
    """Test register page loads."""
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b"Register" in response.data or b"register" in response.data


def test_register_user(app, client):
    """Test user registration."""
    with app.app_context():
        client.post("/auth/register", data={
            "username": "testuser",
            "email": "test@test.com",
            "password": "password123"
        }, follow_redirects=True)

        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.email == "test@test.com"


def test_login_user(app, client):
    """Test user login."""
    with app.app_context():
        user = User(username="testuser", email="test@test.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)

    assert response.status_code == 200


def test_dashboard_requires_login(client):
    """Test dashboard requires login."""
    response = client.get("/dashboard")
    assert response.status_code == 302


def test_metrics_endpoint_exposes_prometheus_text(client):
    """Test Prometheus metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"api_monitor_http_requests_total" in response.data


def test_devops_page_loads_after_login(app, client):
    """Test devops page after login."""
    with app.app_context():
        user = User(username="devops", email="devops@test.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/auth/login", data={
        "username": "devops",
        "password": "secret123"
    }, follow_redirects=True)

    assert response.status_code == 200

    devops_response = client.get("/devops")
    assert devops_response.status_code == 200
