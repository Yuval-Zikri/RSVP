from flask import Blueprint, request, jsonify
from app import db
from models import Event, Invitation
import uuid
from datetime import datetime

api_bp = Blueprint('api', __name__)

# --- Events ---
@api_bp.route('/events', methods=['POST'])
def create_event():
    data = request.json
    try:
        new_event = Event(
            title=data['title'],
            type=data['type'],
            date=datetime.fromisoformat(data['date']),
            location=data['location'],
            background_theme=data.get('background_theme', 'default')
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events]), 200

# --- Invitations ---
@api_bp.route('/invitations', methods=['POST'])
def send_invitations():
    data = request.json
    event_id = data.get('event_id')
    guests = data.get('guests') # List of {name, email}
    
    if not event_id or not guests:
        return jsonify({"error": "Missing event_id or guests list"}), 400
        
    created_invites = []
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
        
        # TODO: Integrate Email Service (Mailtrap) here
        print(f"MOCK EMAIL: Sending invite to {guest['email']} with link /rsvp/{token}")

    db.session.commit()
    return jsonify({"message": f"Sent {len(created_invites)} invitations", "invitations": [i.to_dict() for i in created_invites]}), 201

# --- RSVP ---
@api_bp.route('/rsvp/<token>', methods=['GET'])
def get_rsvp_status(token):
    invite = Invitation.query.filter_by(token=token).first()
    if not invite:
        return jsonify({"error": "Invalid token"}), 404
    
    event = Event.query.get(invite.event_id)
    return jsonify({
        "invitation": invite.to_dict(),
        "event": event.to_dict()
    }), 200

@api_bp.route('/rsvp/<token>', methods=['POST'])
def update_rsvp(token):
    invite = Invitation.query.filter_by(token=token).first()
    if not invite:
        return jsonify({"error": "Invalid token"}), 404
        
    data = request.json
    status = data.get('status') # attending, not_attending
    guests_count = data.get('guests_count', 0)
    
    if status not in ['attending', 'not_attending']:
        return jsonify({"error": "Invalid status"}), 400
        
    invite.status = status
    invite.guests_count = guests_count
    db.session.commit()
    
    return jsonify(invite.to_dict()), 200
