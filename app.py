import sys
import os
import threading

# Ensures Python can find the 'app' folder regardless of how you run it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_login import LoginManager
from app.models import db
from app.routes import main
from app.monitor import monitor_task

def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    
    app.config['SECRET_KEY'] = 'your_secret_key'
    os.makedirs(app.instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register the routes
    app.register_blueprint(main)

    with app.app_context():
        # Always drop and recreate to ensure schema is up to date
        db.drop_all()
        db.create_all()
        print("Database recreated with fresh schema")
        
        # Start the Monitoring Engine in a background thread (only once)
        threading.Thread(target=monitor_task, args=(app,), daemon=True).start()
        print("Background monitor started")

    return app

if __name__ == "__main__":
    app = create_app()
    # Run the server
    print("🌐 Dashboard available at: http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False, port=5000)