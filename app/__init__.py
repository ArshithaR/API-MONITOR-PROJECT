from flask import Flask
from .models import db 
from .routes import main

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    db.init_app(app) 
    app.register_blueprint(main)
    
    return app