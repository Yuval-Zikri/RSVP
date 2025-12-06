"""Event update operations - Update event details and handle date changes."""
from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Invitation
from datetime import datetime
from services.email import send_updated_invitation_email
import os


# Create blueprint
updates_bp = Blueprint('events_updates', __name__)


@updates_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update event details, reset RSVPs and resend if date changed"""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    data = request.json
    try:
        # Store old date for comparison
        old_date = event.date
        new_date = datetime.fromisoformat(data['date'])
        date_changed = old_date != new_date
        
        # Update event fields
        event.title = data['title']
        event.subtitle = data.get('subtitle')
        event.type = data['type']
        event.date = new_date
        event.location = data['location']
        event.address = data.get('address')
        event.latitude = data.get('latitude')
        event.longitude = data.get('longitude')
        event.background_theme = data.get('background_theme', 'default')
        event.email_background_url = data.get('email_background_url')
        
        # If date changed, reset RSVPs and resend invitations
        invitations = []
        if date_changed:
            print(f"Date changed from {old_date} to {new_date}, resetting RSVPs and resending invitations")
            invitations = Invitation.query.filter_by(event_id=event_id).all()
            
            base_url = os.getenv('BASE_URL', 'http://localhost:3000').rstrip('/')
            
            for invite in invitations:
                # Reset status
                invite.status = 'pending'
                invite.guests_count = 0
                
                # Resend invitation email
                send_updated_invitation_email(event, invite, base_url)
        
        db.session.commit()
        return jsonify({
            "message": "Event updated successfully",
            "date_changed": date_changed,
            "invitations_resent": len(invitations) if date_changed else 0,
            "event": event.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
