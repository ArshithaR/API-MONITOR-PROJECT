import requests
import time
from .models import db, API, Log
from datetime import datetime, timedelta

def monitor_task(app):
    with app.app_context():
        while True:
            apis = API.query.all()
            now = datetime.utcnow()
            for api in apis:
                last_log = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).first()
                if last_log is None or (now - last_log.timestamp) > timedelta(seconds=api.interval):
                    try:
                        start = time.time()
                        r = requests.get(api.url, timeout=5)
                        latency = (time.time() - start) * 1000
                        log = Log(api_id=api.id, status_code=r.status_code, response_time=round(latency, 2))
                    except:
                        log = Log(api_id=api.id, status_code=0, response_time=0)
                    
                    db.session.add(log)
                    db.session.commit()
            time.sleep(10) # Checks every 10 seconds