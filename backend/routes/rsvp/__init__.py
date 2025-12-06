"""RSVP routes - Handling guest RSVPs."""
from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Invitation


rsvp_bp = Blueprint('rsvp', __name__, url_prefix='/api/rsvp')


@rsvp_bp.route('/<token>', methods=['GET'])
def get_rsvp_status(token):
    """Get RSVP status for a token"""
    invite = Invitation.query.filter_by(token=token).first()
    if not invite:
        return jsonify({"error": "Invalid token"}), 404
    
    event = Event.query.get(invite.event_id)
    return jsonify({
        "invitation": invite.to_dict(),
        "event": event.to_dict()
    }), 200


@rsvp_bp.route('/<token>', methods=['POST'])
def update_rsvp(token):
    """Update RSVP response"""
    invite = Invitation.query.filter_by(token=token).first()
    if not invite:
        return jsonify({"error": "Invalid token"}), 404
        
    data = request.json
    status = data.get('status')  # attending, not_attending
    guests_count = data.get('guests_count', 0)
    
    if status not in ['attending', 'not_attending']:
        return jsonify({"error": "Invalid status"}), 400
        
    invite.status = status
    invite.guests_count = guests_count
    db.session.commit()
    
    return jsonify(invite.to_dict()), 200
