import sys
import os
import threading

# FIX: Ensures Python can find the 'app' folder regardless of how you run it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_login import LoginManager
from app.models import db
from app.routes import main
from app.monitor import monitor_task

def create_app():
    app = Flask(__name__, instance_relative_config=True)
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
        try:
            db.create_all()
            print("Database initialized")
        except Exception as e:
            print("Database initialize failed", e)
            try:
                db.drop_all()
                db.create_all()
                print("Database re-created after drop")
            except Exception as e2:
                print("Database recreate failed", e2)

        # Start the Monitoring Engine in a background thread (only once)
        # This pings your APIs while the website is running
        threading.Thread(target=monitor_task, args=(app,), daemon=True).start()
        print("Background monitor started")

    return app

if __name__ == "__main__":
    app = create_app()
    # Run the server
    print("🌐 Dashboard available at: http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False, port=5000) # use_reloader=False prevents double-starting the monitor