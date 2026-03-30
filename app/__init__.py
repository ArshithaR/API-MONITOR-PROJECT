from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    login_manager.init_app(app)
    
    # This tells Flask-Login where to redirect unauthorized users
    login_manager.login_view = 'main.login' 

    # IMPORTANT: You must import and register the blueprint here
    from app.routes import main
    app.register_blueprint(main)

    return app