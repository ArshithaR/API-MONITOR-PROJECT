"""Alert and Notification Management"""
from datetime import datetime
from .models import Alert, Notification, API, Log, db

def create_alert(api_id, user_id, alert_type, message, severity='warning'):
    """Create a new alert"""
    alert = Alert(
        api_id=api_id,
        user_id=user_id,
        alert_type=alert_type,
        message=message,
        severity=severity,
        created_at=datetime.utcnow()
    )
    db.session.add(alert)
    db.session.commit()
    
    # Create notification
    create_notification(user_id, alert.id, 'in_app', message)
    
    return alert

def create_notification(user_id, alert_id, notification_type, message):
    """Create a notification"""
    notification = Notification(
        user_id=user_id,
        alert_id=alert_id,
        notification_type=notification_type,
        message=message,
        is_sent=False
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def check_api_health(api):
    """Check if API is down or slow, create alerts if needed"""
    recent_logs = Log.query.filter_by(api_id=api.id).order_by(Log.timestamp.desc()).limit(5).all()
    
    if not recent_logs:
        return
    
    # Check if API is down (all recent requests failed)
    failed_requests = [l for l in recent_logs if l.status_code not in [200, 201, 202, 204]]
    
    if len(failed_requests) == len(recent_logs):  # All failed
        if not api.is_down:
            api.is_down = True
            api.down_since = datetime.utcnow()
            db.session.commit()
            
            create_alert(
                api.id,
                api.user_id,
                'down',
                f'🔴 API "{api.name}" is DOWN',
                'critical'
            )
    else:
        if api.is_down:
            api.is_down = False
            api.down_since = None
            db.session.commit()
            
            create_alert(
                api.id,
                api.user_id,
                'recovered',
                f'🟢 API "{api.name}" has RECOVERED',
                'info'
            )
    
    # Check if API is slow
    avg_response_time = sum(l.response_time for l in recent_logs) / len(recent_logs)
    threshold = api.threshold_latency or 1000  # Default to 1000ms if not set
    if avg_response_time > threshold:
        create_alert(
            api.id,
            api.user_id,
            'slow',
            f'🟡 API "{api.name}" is SLOW (Avg: {avg_response_time:.0f}ms)',
            'warning'
        )

def get_unread_alerts(user_id):
    """Get unread alerts for a user"""
    return Alert.query.filter_by(user_id=user_id, is_read=False).order_by(Alert.created_at.desc()).all()

def mark_alert_as_read(alert_id):
    """Mark an alert as read"""
    alert = Alert.query.get(alert_id)
    if alert:
        alert.is_read = True
        db.session.commit()
    return alert

def send_email_alert(email, subject, message):
    """Send email alert (stub - implement with SMTP)"""
    # TODO: Implement email sending with Flask-Mail or smtplib
    print(f"[EMAIL] To: {email} | Subject: {subject} | Message: {message}")
    return True

def send_desktop_notification(user_id, message):
    """Send desktop notification"""
    # TODO: Implement with WebSocket or service worker
    print(f"[DESKTOP NOTIFICATION] User {user_id}: {message}")
    return True
