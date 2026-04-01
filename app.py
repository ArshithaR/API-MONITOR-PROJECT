#!/usr/bin/env python
"""API Monitor - Main Application Entry Point"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app import create_app
    
    app = create_app()
    print("\n" + "="*60)
    print("🚀 API MONITOR - STARTING APPLICATION")
    print("="*60)
    print("📍 Server running at: http://127.0.0.1:5000")
    print("🔧 Features: Monitoring • Analytics • Charts • Alerts • Export")
    print("="*60 + "\n")
    app.run(debug=True, use_reloader=False, port=5000, host='127.0.0.1')