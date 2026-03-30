import pytest
from app import create_app, db
from app.models import User, API

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_user(app):
    with app.app_context():
        user = User(username='testuser', password='password123')
        db.session.add(user)
        db.session.commit()
        # Refresh to keep the object available outside the session
        db.session.refresh(user)
        return user