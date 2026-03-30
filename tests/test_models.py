import pytest
from app.models import db, User, API, Log
from werkzeug.security import check_password_hash

class TestUserModel:
    """Test User model"""
    
    def test_user_creation(self, app):
        """Test user can be created"""
        with app.app_context():
            user = User(username='john', password='hashed_pass')
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'john'
            assert user.password == 'hashed_pass'
    
    def test_user_unique_username(self, app):
        """Test username must be unique"""
        with app.app_context():
            user1 = User(username='john', password='pass1')
            user2 = User(username='john', password='pass2')
            db.session.add(user1)
            db.session.commit()
            db.session.add(user2)
            
            with pytest.raises(Exception):
                db.session.commit()

class TestAPIModel:
    """Test API model"""
    
    def test_api_creation(self, app, auth_user):
        """Test API can be created"""
        with app.app_context():
            api = API(
                user_id=auth_user.id,
                name='My API',
                url='https://example.com',
                interval=60
            )
            db.session.add(api)
            db.session.commit()
            
            assert api.id is not None
            assert api.name == 'My API'
            assert api.url == 'https://example.com'
            assert api.interval == 60
    
    def test_api_user_relationship(self, app, test_api, auth_user):
        """Test API-User relationship"""
        with app.app_context():
            api = API.query.filter_by(id=test_api.id).first()
            assert api.user_id == auth_user.id

class TestLogModel:
    """Test Log model"""
    
    def test_log_creation(self, app, test_api):
        """Test log can be created"""
        with app.app_context():
            log = Log(api_id=test_api.id, status_code=200, response_time=150.5)
            db.session.add(log)
            db.session.commit()
            
            assert log.id is not None
            assert log.status_code == 200
            assert log.response_time == 150.5
            assert log.api_id == test_api.id
    
    def test_log_cascade_delete(self, app, test_api):
        """Test logs are deleted when API is deleted"""
        with app.app_context():
            # Create logs
            log = Log(api_id=test_api.id, status_code=200, response_time=100)
            db.session.add(log)
            db.session.commit()
            
            log_id = log.id
            
            # Delete API
            db.session.delete(test_api)
            db.session.commit()
            
            # Verify log is deleted
            deleted_log = Log.query.filter_by(id=log_id).first()
            assert deleted_log is None
