from app import db  # Import the db instance from your app factory
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # Relationship to link APIs to a specific user
    apis = db.relationship('API', backref='owner', lazy=True, cascade="all, delete-orphan")

class API(db.Model):
    __tablename__ = 'api'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    interval = db.Column(db.Integer, default=60) # Interval in seconds
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relationship to link logs to this API
    logs = db.relationship('Log', backref='api', lazy=True, cascade="all, delete-orphan")

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api.id'), nullable=False)
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float) # Stored in milliseconds or seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)