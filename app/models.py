from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    apis = db.relationship('API', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class API(db.Model):
    """API Endpoint model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interval = db.Column(db.Integer, default=60)  # seconds
    threshold_latency = db.Column(db.Integer, default=1000)  # ms
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs = db.relationship('APILog', backref='api', lazy=True, cascade='all, delete-orphan')
    
    def get_last_log(self):
        return APILog.query.filter_by(api_id=self.id).order_by(APILog.timestamp.desc()).first()
    
    def get_avg_response_time(self, hours=24):
        """Get average response time for last N hours"""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        logs = APILog.query.filter(
            APILog.api_id == self.id,
            APILog.timestamp >= cutoff
        ).all()
        if not logs:
            return 0
        # Filter out None values to avoid TypeError
        response_times = [l.response_time for l in logs if l.response_time is not None]
        if not response_times:
            return 0
        return sum(response_times) / len(response_times)

class APILog(db.Model):
    """API monitoring log"""
    __tablename__ = 'api_log'
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api.id'), nullable=False)
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)  # milliseconds
    is_success = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<APILog {self.api_id} - {self.status_code} - {self.response_time}ms>'
