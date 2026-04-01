"""Analytics and Health Score Calculations"""
from datetime import datetime, timedelta
from .models import Log, HealthScore, db

def calculate_health_score(api_id):
    """Calculate API health score based on uptime, speed, and failure rate"""
    logs = Log.query.filter_by(api_id=api_id).all()
    
    if not logs:
        return 100.0, 100.0, 100.0, "excellent"
    
    # Uptime percentage (200 status = success)
    successful = len([l for l in logs if l.status_code == 200])
    total = len(logs)
    uptime_percentage = (successful / total * 100) if total > 0 else 100.0
    
    # Average response time
    avg_response_time = sum(l.response_time for l in logs) / len(logs) if logs else 0
    
    # Success rate
    success_rate = (successful / total * 100) if total > 0 else 100.0
    
    # Calculate overall health score (0-100)
    # 40% uptime, 40% success rate, 20% speed
    health_score = (uptime_percentage * 0.4) + (success_rate * 0.4) + (max(0, 100 - (avg_response_time / 10)) * 0.2)
    health_score = max(0, min(100, health_score))
    
    # Determine status
    if health_score >= 90:
        status = "excellent"
    elif health_score >= 70:
        status = "good"
    else:
        status = "poor"
    
    return uptime_percentage, avg_response_time, success_rate, health_score, status

def update_api_health_scores(api_id):
    """Update or create health score record for an API"""
    uptime, avg_time, success, score, status = calculate_health_score(api_id)
    
    health_record = HealthScore.query.filter_by(api_id=api_id).first()
    
    if health_record:
        health_record.uptime_percentage = uptime
        health_record.avg_response_time = avg_time
        health_record.success_rate = success
        health_record.health_score = score
        health_record.status = status
        health_record.updated_at = datetime.utcnow()
    else:
        health_record = HealthScore(
            api_id=api_id,
            uptime_percentage=uptime,
            avg_response_time=avg_time,
            success_rate=success,
            health_score=score,
            status=status
        )
        db.session.add(health_record)
    
    db.session.commit()
    return health_record

def get_analytics_data(api_id, time_range_hours=24):
    """Get analytics data for a specific time range"""
    since = datetime.utcnow() - timedelta(hours=time_range_hours)
    logs = Log.query.filter_by(api_id=api_id).filter(Log.timestamp >= since).order_by(Log.timestamp.asc()).all()
    
    success_count = len([l for l in logs if l.status_code == 200])
    failure_count = len([l for l in logs if l.status_code != 200])
    
    return {
        'total_requests': len(logs),
        'success_count': success_count,
        'failure_count': failure_count,
        'success_rate': (success_count / len(logs) * 100) if logs else 0,
        'avg_response_time': sum(l.response_time for l in logs) / len(logs) if logs else 0,
        'min_response_time': min(l.response_time for l in logs) if logs else 0,
        'max_response_time': max(l.response_time for l in logs) if logs else 0,
        'logs': logs
    }

def get_status_distribution(api_id, time_range_hours=24):
    """Get distribution of status codes"""
    since = datetime.utcnow() - timedelta(hours=time_range_hours)
    logs = Log.query.filter_by(api_id=api_id).filter(Log.timestamp >= since).all()
    
    status_dist = {}
    for log in logs:
        status = log.status_code
        status_dist[status] = status_dist.get(status, 0) + 1
    
    return status_dist

def predict_downtime(api_id, lookback_hours=72):
    """Simple prediction: if API has been failing in the last hour, it might go down"""
    since = datetime.utcnow() - timedelta(hours=lookback_hours)
    logs = Log.query.filter_by(api_id=api_id).filter(Log.timestamp >= since).order_by(Log.timestamp.desc()).limit(100).all()
    
    if not logs:
        return {"risk": "low", "prediction": "No data available"}
    
    # Check recent failures
    recent_logs = logs[:20]  # Last 20 logs
    recent_failures = len([l for l in recent_logs if l.status_code != 200])
    
    if recent_failures >= 15:
        return {"risk": "high", "prediction": "API is failing frequently - possible downtime soon"}
    elif recent_failures >= 10:
        return {"risk": "medium", "prediction": "API showing instability - monitor closely"}
    else:
        return {"risk": "low", "prediction": "API is stable"}
