import sys
import os

# Ensures Python can find the 'app' folder regardless of how you run it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

if __name__ == "__main__":
    app = create_app()
    # Run the server
    print("🌐 Dashboard available at: http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False, port=5000)