"""Invitation routes - Managing and sending invitations."""
from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Invitation
from services.email import send_invitation_email
import uuid
import os


invitations_bp = Blueprint('invitations', __name__, url_prefix='/api/invitations')


@invitations_bp.route('', methods=['POST'])
def send_invitations():
    """Send invitations to guests for an event"""
    data = request.json
    event_id = data.get('event_id')
    guests = data.get('guests')  # List of {name, email}
    
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    if not event_id or not guests:
        return jsonify({"error": "Missing event_id or guests list"}), 400
        
    created_invites = []
    base_url = os.getenv('BASE_URL', 'http://localhost:3000').rstrip('/')
    
    for guest in guests:
        token = str(uuid.uuid4())
        new_invite = Invitation(
            event_id=event_id,
            email=guest['email'],
            name=guest['name'],
            token=token
        )
        db.session.add(new_invite)
        created_invites.append(new_invite)
        
        # Send Email
        guest_with_token = {
            'name': guest['name'],
            'email': guest['email'],
            'token': token
        }
        send_invitation_email(event, guest_with_token, base_url)

    from flask import current_app
    db.session.commit()
    
    # Increment metric
    if hasattr(current_app, 'metrics'):
        current_app.metrics['invitations_sent'].inc(len(created_invites))
        
    return jsonify({
        "message": f"Sent {len(created_invites)} invitations",
        "invitations": [i.to_dict() for i in created_invites]
    }), 201
