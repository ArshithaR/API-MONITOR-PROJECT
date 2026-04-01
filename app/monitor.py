import requests
import time
from .models import db, API, Log
from .analytics import update_api_health_scores
from .alerts import check_api_health
from datetime import datetime, timedelta

def monitor_task(app):
    with app.app_context():
        while True:
            apis = API.query.all()
            now = datetime.utcnow()
            for api in apis:
                interval = api.interval if api.interval else 300  # Default to 5 minutes
                last_log = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).first()
                if last_log is None or (now - last_log.timestamp) > timedelta(seconds=interval):
                    try:
                        start = time.time()
                        r = requests.get(api.url, timeout=5)
                        latency = (time.time() - start) * 1000
                        log = Log(api_id=api.id, status_code=r.status_code, response_time=round(latency, 2))
                    except:
                        log = Log(api_id=api.id, status_code=0, response_time=0)
                    
                    db.session.add(log)
                    db.session.commit()
                    
                    # Update health scores
                    update_api_health_scores(api.id)
                    
                    # Check for alerts
                    check_api_health(api)
            
            time.sleep(10)  # Checks every 10 seconds