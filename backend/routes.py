from flask import Blueprint, request, jsonify
from extensions import db, mail
from flask_mail import Message
from models import Event, Invitation
import uuid
import os
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
            background_theme=data.get('background_theme', 'default'),
            email_background_url=data.get('email_background_url')
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
    
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
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
        
        # Send Email
        try:
            base_url = os.getenv('BASE_URL', 'http://localhost:3000').rstrip('/')
            rsvp_link = f"{base_url}/rsvp/{token}"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 0; }}
                    .container {{ max-width: 600px; margin: 40px auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
                    .header {{ 
                        background-image: url('{event.email_background_url or event.background_theme}');
                        background-size: cover;
                        background-position: center;
                        padding: 60px 20px; 
                        text-align: center; 
                        color: white; 
                        position: relative;
                    }}
                    .header::before {{
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: rgba(0,0,0,0.5);
                    }}
                    .header h1 {{ position: relative; margin: 0; font-size: 32px; font-weight: 700; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }}
                    .content {{ padding: 40px 30px; text-align: center; color: #2d3748; }}
                    .greeting {{ font-size: 18px; margin-bottom: 20px; }}
                    .event-title {{ font-size: 24px; font-weight: bold; color: #4a5568; margin: 20px 0; }}
                    .details {{ background: #edf2f7; padding: 20px; border-radius: 12px; margin: 30px 0; text-align: left; }}
                    .detail-item {{ margin: 10px 0; font-size: 16px; display: flex; align-items: center; }}
                    .icon {{ margin-right: 10px; font-size: 20px; }}
                    .btn {{ display: inline-block; background: #667eea; color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 16px; margin-top: 20px; transition: transform 0.2s; }}
                    .btn:hover {{ transform: translateY(-2px); background: #5a67d8; }}
                    .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #a0aec0; border-top: 1px solid #e2e8f0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>YOU'RE INVITED!</h1>
                    </div>
                    <div class="content">
                        <p class="greeting">Hello <strong>{guest['name']}</strong>,</p>
                        <p>We are delighted to invite you to our special event:</p>
                        
                        <div class="event-title">{event.title}</div>
                        
                        <div class="details">
                            <div class="detail-item">
                                <span class="icon">📅</span>
                                <span>{event.date.strftime('%A, %B %d, %Y at %I:%M %p')}</span>
                            </div>
                            <div class="detail-item">
                                <span class="icon">📍</span>
                                <span>{event.location}</span>
                            </div>
                        </div>
                        
                        <a href="{rsvp_link}" class="btn">RSVP Now</a>
                        
                        <p style="margin-top: 30px; font-size: 14px; color: #718096;">
                            Please respond by clicking the button above.
                        </p>
                    </div>
                    <div class="footer">
                        <p>If the button doesn't work, copy this link:</p>
                        <p><a href="{rsvp_link}" style="color: #667eea;">{rsvp_link}</a></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(
                subject=f"Invitation to {event.title}",
                recipients=[guest['email']],
                html=html_body
            )
            mail.send(msg)
            print(f"Email sent to {guest['email']}")
        except Exception as e:
            print(f"Failed to send email to {guest['email']}: {e}")

    db.session.commit()
    return jsonify({"message": f"Sent {len(created_invites)} invitations", "invitations": [i.to_dict() for i in created_invites]}), 201

@api_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Delete associated invitations first
    Invitation.query.filter_by(event_id=event_id).delete()
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully"}), 200

@api_bp.route('/events/<int:event_id>/rsvps', methods=['GET'])
def get_event_rsvps(event_id):
    invitations = Invitation.query.filter_by(event_id=event_id).all()
    return jsonify([i.to_dict() for i in invitations]), 200

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
