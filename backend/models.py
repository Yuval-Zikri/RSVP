from datetime import datetime
from extensions import db
import uuid

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True) # e.g. "Hila & Ido"
    type = db.Column(db.String(50), nullable=False) # wedding, birthday, etc.
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500), nullable=True) # Full address from map search
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    background_theme = db.Column(db.String(50), default='default')
    email_background_url = db.Column(db.String(500), nullable=True)  # Unsplash URL for emails
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invitations = db.relationship('Invitation', backref='event', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'type': self.type,
            'date': self.date.isoformat(),
            'location': self.location,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'background_theme': self.background_theme,
            'email_background_url': self.email_background_url
        }

class Invitation(db.Model):
    __tablename__ = 'invitations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, attending, not_attending
    guests_count = db.Column(db.Integer, default=0)
    token = db.Column(db.String(64), unique=True, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'email': self.email,
            'name': self.name,
            'status': self.status,
            'guests_count': self.guests_count,
            'token': self.token
        }
