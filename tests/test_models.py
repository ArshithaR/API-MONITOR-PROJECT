import pytest
from app import db
from app.models import User, API, Log
from sqlalchemy.exc import IntegrityError

class TestUserModel:
    def test_user_creation(self, app):
        with app.app_context():
            user = User(username='john', password_hash='pass1')
            db.session.add(user)
            db.session.commit()
            assert User.query.filter_by(username='john').first() is not None

    def test_user_unique_username(self, app):
        with app.app_context():
            user1 = User(username='john', password_hash='pass1')
            db.session.add(user1)
            db.session.commit()
            
            user2 = User(username='john', password_hash='pass2')
            db.session.add(user2)
            with pytest.raises(IntegrityError):
                db.session.commit()

class TestAPIModel:
    def test_api_creation(self, app):
        with app.app_context():
            user = User(username='api_owner', password_hash='pass')
            db.session.add(user)
            db.session.commit()
            
            api = API(name='Test API', url='http://test.com', user_id=user.id)
            db.session.add(api)
            db.session.commit()
            assert API.query.filter_by(name='Test API').first() is not None

class TestLogModel:
    def test_log_creation(self, app):
        with app.app_context():
            user = User(username='logger', password_hash='pass')
            db.session.add(user)
            db.session.commit()
            api = API(name='Log API', url='http://log.com', user_id=user.id)
            db.session.add(api)
            db.session.commit()
            
            log = Log(status_code=200, response_time=0.5, api_id=api.id)
            db.session.add(log)
            db.session.commit()
            assert Log.query.filter_by(status_code=200).first() is not None