import pytest
from app import create_app
from app.models import db, User

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        # This line helps prevent DetachedInstanceErrors
        "SQLALCHEMY_SESSION_OPTIONS": {"expire_on_commit": False}
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def db_session(app):
    with app.app_context():
        # Force session to not expire objects automatically
        db.session.expire_on_commit = False
        yield db.session
        db.session.rollback()
        db.session.close()