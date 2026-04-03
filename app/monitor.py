import threading
import time
import requests
from datetime import datetime
from app import db
from app.models import API, APILog

_app = None


def monitor_apis():
    """Background task that monitors APIs periodically."""
    while True:
        try:
            if _app:
                with _app.app_context():
                    apis = API.query.all()

                    if not apis:
                        time.sleep(30)
                        continue

                    for api in apis:
                        try:
                            start_time = time.time()
                            try:
                                response = requests.get(api.url, timeout=10, allow_redirects=True)
                                response_time = (time.time() - start_time) * 1000
                                status_code = response.status_code

                                log = APILog(
                                    api_id=api.id,
                                    status_code=status_code,
                                    response_time=response_time,
                                    timestamp=datetime.utcnow()
                                )

                            except requests.exceptions.Timeout:
                                log = APILog(
                                    api_id=api.id,
                                    status_code=0,
                                    response_time=None,
                                    timestamp=datetime.utcnow()
                                )

                            except requests.exceptions.ConnectionError:
                                log = APILog(
                                    api_id=api.id,
                                    status_code=None,
                                    response_time=None,
                                    timestamp=datetime.utcnow()
                                )

                            except Exception:
                                log = APILog(
                                    api_id=api.id,
                                    status_code=None,
                                    response_time=None,
                                    timestamp=datetime.utcnow()
                                )

                            db.session.add(log)

                        except Exception:
                            continue

                    try:
                        db.session.commit()
                    except Exception:
                        db.session.rollback()

            time.sleep(30)

        except Exception:
            try:
                db.session.rollback()
            except Exception:
                pass
            time.sleep(30)


def start_monitor(app):
    """Start the background monitor thread."""
    global _app
    _app = app
    monitor_thread = threading.Thread(target=monitor_apis, daemon=True)
    monitor_thread.start()
    print("Background API Monitor started")
