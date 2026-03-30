from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .routes import main

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # FIX 1: Add a secret key for sessions/logins
    app.config['SECRET_KEY'] = 'dev-key-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    # FIX 2: Prevent the "DetachedInstanceError" in tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # FIX 3: Set up the Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    
    return app