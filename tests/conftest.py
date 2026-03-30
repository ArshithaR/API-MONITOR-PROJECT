import pytest
from app import create_app
from app.models import db, User

@pytest.fixture
def app():
    app = create_app()
    # ... setup code ...
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_user(db_session):
    user = User(username="testuser", password="password")
    db.session.add(user)
    db.session.commit()
    return user