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
                    
                    if not apis:
                        time.sleep(30)
                        continue
                    
                    for api in apis:
                        try:
                            # Make HTTP request to the API with timeout
                            start_time = time.time()
                            try:
                                response = requests.get(api.url, timeout=10, allow_redirects=True)
                                response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                                status_code = response.status_code
                                
                                # Create log entry
                                log = APILog(
                                    api_id=api.id,
                                    status_code=status_code,
                                    response_time=response_time,
                                    timestamp=datetime.utcnow()
                                )
                            
                            except requests.exceptions.Timeout:
                                # Request timed out
                                log = APILog(
                                    api_id=api.id,
                                    status_code=0,
                                    response_time=None,
                                    timestamp=datetime.utcnow()
                                )
                            
                            except requests.exceptions.ConnectionError:
                                # Connection error
                                log = APILog(
                                    api_id=api.id,
                                    status_code=None,
                                    response_time=None,
                                    timestamp=datetime.utcnow()
                                )
                            
                            except Exception as e:
                                # Any other request error
                                log = APILog(
                                    api_id=api.id,
                                    status_code=None,
                                    response_time=None,
                                    timestamp=datetime.utcnow()
                                )
                            
                            db.session.add(log)
                        
                        except Exception as e:
                            # Skip this API if there's an error
                            continue
                    
                    # Commit all logs with error handling
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
            
            # Wait before next check
            time.sleep(30)
            
        except Exception as e:
            # Silently handle errors to keep monitor running
            try:
                db.session.rollback()
            except:
                pass
            time.sleep(30)

def start_monitor(app):
    """Start the background monitor thread"""
    global _app
    _app = app
    monitor_thread = threading.Thread(target=monitor_apis, daemon=True)
    monitor_thread.start()
    print("✅ Background API Monitor started")
