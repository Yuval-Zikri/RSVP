"""Event actions - Reminders, preview, and RSVP listing."""
from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Invitation
from services.email import send_reminder_email, generate_email_html
import os


# Create blueprint
actions_bp = Blueprint('events_actions', __name__)


@actions_bp.route('/<int:event_id>/remind', methods=['POST'])
def send_reminders(event_id):
    """Send reminder emails to pending guests"""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Get all pending invitations
    pending_invites = Invitation.query.filter_by(
        event_id=event_id,
        status='pending'
    ).all()
    
    if not pending_invites:
        return jsonify({"message": "No pending invitations to remind"}), 200
    
    sent_count = 0
    base_url = os.getenv('BASE_URL', 'http://localhost:3000').rstrip('/')
    
    for invite in pending_invites:
        if send_reminder_email(event, invite, base_url):
            sent_count += 1
    
    return jsonify({
        "message": f"Sent {sent_count} reminders",
        "sent_count": sent_count
    }), 200


@actions_bp.route('/<int:event_id>/preview', methods=['GET'])
def get_email_preview(event_id):
    """Generate HTML preview of invitation email"""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # For preview, convert background URL to HTTP URL (CID doesn't work in iframes)
    bg_url = event.email_background_url
    
    if bg_url and not bg_url.startswith('http'):
        # It's a local filename, convert to HTTP URL
        base_url = os.getenv('BASE_URL', 'http://localhost:3000').rstrip('/')
        bg_url = f"{base_url}/api/backgrounds/{bg_url}"
    elif not bg_url:
        # Fallback to a default Unsplash image
        bg_url = 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    
    # Create a modified event object for preview with HTTP URL
    event_preview = type('obj', (object,), {
        'type': event.type,
        'title': event.title,
        'subtitle': event.subtitle,
        'date': event.date,
        'location': event.location,
        'latitude': event.latitude,
        'longitude': event.longitude,
        'email_background_url': bg_url  # Use HTTP URL instead
    })()
    
    # Generate preview with placeholder
    base_url = os.getenv('BASE_URL', 'http://localhost:3000').rstrip('/')
    sample_rsvp_link = f"{base_url}/rsvp/preview"
    
    # Generate HTML using the modified event with HTTP URL (no CID attachment)
    html_body, _ = generate_email_html(event_preview, "Guest Name", sample_rsvp_link)
    
    return html_body, 200, {'Content-Type': 'text/html; charset=utf-8'}


@actions_bp.route('/<int:event_id>/rsvps', methods=['GET'])
def get_event_rsvps(event_id):
    """Get all RSVPs for an event"""
    invitations = Invitation.query.filter_by(event_id=event_id).all()
    return jsonify([i.to_dict() for i in invitations]), 200
