#!/usr/bin/env python
"""API Monitor - Main Application"""

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    print("\n" + "="*70)
    print("✅ API MONITOR STARTED SUCCESSFULLY")
    print("="*70)
    print("🌐 Access at: http://127.0.0.1:5000")
    print("="*70 + "\n")
    app.run(debug=True, use_reloader=False, port=5000)
