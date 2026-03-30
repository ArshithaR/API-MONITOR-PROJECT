from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    apis = db.relationship('API', backref='owner', lazy=True)

class API(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logs = db.relationship('Log', backref='api', cascade="all, delete-orphan", lazy=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    api_id = db.Column(db.Integer, db.ForeignKey('api.id'), nullable=False)