"""Event CRUD operations - Create, Read, Delete."""
from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Invitation
from datetime import datetime


# Create blueprint
crud_bp = Blueprint('events_crud', __name__)


@crud_bp.route('', methods=['POST'])
def create_event():
    """Create a new event"""
    data = request.json
    try:
        print(f"DEBUG: Creating event with email_bg: {data.get('email_background_url')}")
        new_event = Event(
            title=data['title'],
            subtitle=data.get('subtitle'),
            type=data['type'],
            date=datetime.fromisoformat(data['date']),
            location=data['location'],
            address=data.get('address'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            background_theme=data.get('background_theme', 'default'),
            email_background_url=data.get('email_background_url')
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@crud_bp.route('', methods=['GET'])
def get_events():
    """Get all events"""
    events = Event.query.all()
    return jsonify([e.to_dict() for e in events]), 200


@crud_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event"""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict()), 200


@crud_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Delete associated invitations first
    Invitation.query.filter_by(event_id=event_id).delete()
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully"}), 200


@crud_bp.route('/all', methods=['DELETE'])
def delete_all_events():
    """Delete all events and their invitations"""
    try:
        # Standard approach to delete all
        Invitation.query.delete()
        Event.query.delete()
        db.session.commit()
        return jsonify({"message": "All events and invitations deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
