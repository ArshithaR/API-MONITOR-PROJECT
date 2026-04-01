from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True)
    apis = db.relationship('API', backref='owner', lazy=True)
    alerts = db.relationship('Alert', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class API(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interval = db.Column(db.Integer, default=300)  # Default interval: 5 minutes
    threshold_latency = db.Column(db.Integer, default=1000)  # ms - slow threshold
    is_down = db.Column(db.Boolean, default=False)
    down_since = db.Column(db.DateTime)
    logs = db.relationship('Log', backref='api', lazy=True, cascade='all, delete-orphan')
    health_scores = db.relationship('HealthScore', backref='api', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='api', lazy=True, cascade='all, delete-orphan')

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)
    dns_time = db.Column(db.Float, default=0)
    connection_time = db.Column(db.Float, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    api_id = db.Column(db.Integer, db.ForeignKey('api.id'), nullable=False)

class HealthScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api.id'), nullable=False)
    uptime_percentage = db.Column(db.Float, default=100.0)
    avg_response_time = db.Column(db.Float, default=0.0)
    success_rate = db.Column(db.Float, default=100.0)
    health_score = db.Column(db.Float, default=100.0)  # 0-100
    status = db.Column(db.String(20), default='excellent')  # excellent, good, poor
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    alert_type = db.Column(db.String(50))  # 'down', 'slow', 'recovered'
    message = db.Column(db.String(500))
    severity = db.Column(db.String(20))  # 'critical', 'warning', 'info'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    is_resolved = db.Column(db.Boolean, default=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    alert_id = db.Column(db.Integer, db.ForeignKey('alert.id'))
    notification_type = db.Column(db.String(50))  # 'email', 'desktop', 'in_app'
    message = db.Column(db.String(500))
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)