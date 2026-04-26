from backend.database import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(150), nullable=True)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Signal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    signal_strength = db.Column(db.Integer, nullable=True)
    signal_quality = db.Column(db.String(50), nullable=True)
    district = db.Column(db.String(100), nullable=True, default='Unknown')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    predicted_quality = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Retained existing fields to ensure backwards compatibility with UI
    distance = db.Column(db.Float, nullable=True)
    obstacles = db.Column(db.Integer, nullable=True)
    frequency = db.Column(db.Float, nullable=True)
    power = db.Column(db.Float, nullable=True)

    @property
    def quality(self):
        return self.predicted_quality

class UserLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region_type = db.Column(db.String(50), nullable=False) # State, District, Village
    parent_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=True)

class SignalTower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tower_id = db.Column(db.String(50), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    signal_strength = db.Column(db.Float, nullable=False)
    signal_type = db.Column(db.String(50), nullable=False) # Strong, Medium, Weak
    region_name = db.Column(db.String(100), nullable=True)
