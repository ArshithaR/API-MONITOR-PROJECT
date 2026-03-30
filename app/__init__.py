from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Create the instances HERE (outside create_app)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Use a absolute path for the DB to avoid "Instance" folder issues
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the instances with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app