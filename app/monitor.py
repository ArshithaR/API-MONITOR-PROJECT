import threading
import time
import requests
from datetime import datetime
from app import db
from app.models import API, APILog

_app = None

def monitor_apis():
    """Background task that monitors APIs periodically"""
    while True:
        try:
            if _app:
                with _app.app_context():
                    # Get all APIs from database
                    apis = API.query.all()
                    
                    for api in apis:
                        try:
                            # Make HTTP request to the API
                            start_time = time.time()
                            response = requests.get(api.url, timeout=10)
                            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                            
                            # Create log entry
                            log = APILog(
                                api_id=api.id,
                                status_code=response.status_code,
                                response_time=response_time,
                                timestamp=datetime.utcnow()
                            )
                            db.session.add(log)
                            
                        except requests.exceptions.ConnectTimeout:
                            # Timeout - mark as failed
                            log = APILog(
                                api_id=api.id,
                                status_code=0,
                                response_time=None,
                                timestamp=datetime.utcnow()
                            )
                            db.session.add(log)
                            
                        except requests.exceptions.RequestException as e:
                            # Other request errors
                            log = APILog(
                                api_id=api.id,
                                status_code=None,
                                response_time=None,
                                timestamp=datetime.utcnow()
                            )
                            db.session.add(log)
                            
                        except Exception as e:
                            # Any other error
                            print(f"Error checking API {api.id}: {str(e)}")
                            continue
                    
                    # Commit all logs
                    db.session.commit()
                
        except Exception as e:
            print(f"Error in monitor_apis: {str(e)}")
            try:
                db.session.rollback()
            except:
                pass
        
        # Wait before next check (check every 30 seconds by default)
        time.sleep(30)

def start_monitor(app):
    """Start the background monitor thread"""
    global _app
    _app = app
    monitor_thread = threading.Thread(target=monitor_apis, daemon=True)
    monitor_thread.start()
    print("✅ Background API Monitor started")
