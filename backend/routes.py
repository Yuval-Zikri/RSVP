from flask import Blueprint, request, jsonify, send_from_directory
from extensions import db, mail
from flask_mail import Message
from models import Event, Invitation
import uuid
import os
from datetime import datetime

api_bp = Blueprint('api', __name__)

import requests

# CID Embedding implementation - no mapping needed


@api_bp.route('/search-location', methods=['GET'])
def search_location():
    query = request.args.get('q')
    if not query:
        return jsonify([]), 200
        
    try:
        # Use a session to manage cookies
        session = requests.Session()
        
        # Headers from user's curl command
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.waze.com/he/live-map/directions',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        session.headers.update(headers)
        
        # 1. Visit the main page to get cookies (CSRF, etc.)
        # This is crucial as the user's curl had a _csrf_token cookie
        try:
            session.get('https://www.waze.com/he/live-map', timeout=5)
        except Exception as e:
            print(f"Failed to init session: {e}")

        # Waze Live Map Autocomplete API
        url = "https://www.waze.com/live-map/api/autocomplete/"
        params = {
            'q': query,
            'exp': '8,10,12',
            'geo-env': 'il',
            'lang': 'he',
            'v': '29.500000,34.000000;33.500000,36.000000' # Viewport covering Israel
        }
        
        response = session.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Waze API Error: {response.status_code} - {response.text}")
            return jsonify([]), 200
            
        data = response.json()
        
        results = []
        for item in data:
            if 'name' in item:
                label = item['name']
                # Fix: User output shows 'latLng' with 'lat' and 'lng'
                lat = item.get('latLng', {}).get('lat')
                lon = item.get('latLng', {}).get('lng')
                
                if lat and lon:
                    results.append({
                        'label': label,
                        'x': lon,
                        'y': lat,
                        'raw': item
                    })
            
        return jsonify(results), 200
    except Exception as e:
        print(f"Waze search error: {e}")
        return jsonify([]), 200

@api_bp.route('/backgrounds/<path:filename>')
def serve_background(filename):
    return send_from_directory('/app/backgrounds', filename)

# --- Events ---
@api_bp.route('/events', methods=['POST'])
def create_event():
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
            
            # Ensure we have a valid URL for the email background
            bg_url = event.email_background_url
            print(f"DEBUG: Raw email_background_url: {bg_url}")
            print(f"DEBUG: BASE_URL env var: {os.getenv('BASE_URL')}")
            
            attachment_cid = None
            
            if bg_url and not bg_url.startswith('http'):
                 # It's a local filename, try to attach it
                 file_path = os.path.join('/app/backgrounds', bg_url)
                 if os.path.exists(file_path):
                     attachment_cid = bg_url # Use filename as CID
                     bg_url = f"cid:{attachment_cid}"
                     print(f"DEBUG: Attaching local file: {file_path} as CID: {attachment_cid}")
                 else:
                     print(f"DEBUG: Local file not found: {file_path}")
                     # Fallback to a default Unsplash image if file not found
                     bg_url = 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
            elif not bg_url:
                # Fallback to a default Unsplash image if no valid URL is present
                bg_url = 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
            
            print(f"DEBUG: Final bg_url: {bg_url}")

            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ margin: 0; padding: 0; width: 100% !important; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; background-color: #f0f0f0; }}
                    img {{ border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }}
                    .btn-primary {{ 
                        background-color: #007bff; 
                        color: #ffffff; 
                        padding: 14px 28px; 
                        text-decoration: none; 
                        border-radius: 50px; 
                        font-weight: bold; 
                        display: inline-block;
                        mso-padding-alt: 0;
                        text-underline-color: #007bff;
                    }}
                    .btn-nav {{
                        background-color: #ffffff;
                        color: #007bff;
                        border: 1px solid #007bff;
                        padding: 8px 16px;
                        text-decoration: none;
                        border-radius: 50px;
                        font-size: 14px;
                        display: inline-block;
                        margin: 0 5px;
                    }}
                </style>
            </head>
            <body style="margin: 0; padding: 0; background-color: #f0f0f0;">
                <!-- Main Table Container (Full Width Gray Background) -->
                <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%" style="min-height: 100vh; background-color: #f0f0f0;">
                    <tr>
                        <td align="center" valign="top" style="padding: 40px 0;">
                            
                            <!-- Phone Container (Centered, Fixed Width) -->
                            <!-- Using max-width 500px to match mobile preview -->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px; width: 100%; margin: 0 auto; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.2);">
                                <tr>
                                    <td align="center" valign="middle" background="{bg_url}" style="padding: 0; background-image: url('{bg_url}'); background-size: cover; background-position: center; background-repeat: no-repeat; background-color: #e6f7ff; height: 640px;">
                                        <!--[if gte mso 9]>
                                        <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:500px;height:640px;">
                                        <v:fill type="frame" src="{bg_url}" color="#e6f7ff" />
                                        <v:textbox inset="0,0,0,0">
                                        <![endif]-->
                                        
                                        <!-- Content Wrapper (to center the card vertically if needed, or just padding) -->
                                        <div style="padding: 20px;">
                                            <!-- Card Container -->
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: rgba(255, 255, 255, 0.95); border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); backdrop-filter: blur(10px);">
                                                <tr>
                                                    <td align="center" style="padding: 30px 20px;">
                                                        
                                                        <!-- Event Type -->
                                                        <div style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; color: #666; margin-bottom: 10px; font-weight: bold; font-family: Helvetica, Arial, sans-serif;">
                                                            {event.type.upper()}
                                                        </div>

                                                        <!-- Event Title -->
                                                        <h1 style="margin: 10px 0; font-size: 28px; font-weight: 700; color: #1a1a1a; line-height: 1.2; font-family: Helvetica, Arial, sans-serif;">
                                                            {event.title}
                                                        </h1>

                                                        <!-- Subtitle -->
                                                        {f'<div style="font-size: 18px; color: #4a4a4a; margin-bottom: 20px; font-family: Georgia, serif; font-style: italic;">{event.subtitle}</div>' if event.subtitle else ''}

                                                        <!-- Details -->
                                                        <table border="0" cellpadding="0" cellspacing="0" style="margin: 20px auto; text-align: left;">
                                                            <tr>
                                                                <td style="padding: 5px 0; font-size: 14px; color: #333; font-family: Helvetica, Arial, sans-serif;">
                                                                    <span style="margin-right: 8px; font-size: 16px;">📅</span>
                                                                    {event.date.strftime('%A, %B %d, %Y')} at {event.date.strftime('%I:%M %p')}
                                                                </td>
                                                            </tr>
                                                            <tr>
                                                                <td style="padding: 5px 0; font-size: 14px; color: #333; font-family: Helvetica, Arial, sans-serif;">
                                                                    <span style="margin-right: 8px; font-size: 16px;">📍</span>
                                                                    {event.location}
                                                                </td>
                                                            </tr>
                                                        </table>

                                                        <!-- RSVP Button -->
                                                        <div style="margin-top: 20px; margin-bottom: 20px;">
                                                            <!--[if mso]>
                                                            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{rsvp_link}" style="height:40px;v-text-anchor:middle;width:160px;" arcsize="50%" stroke="f" fillcolor="#007bff">
                                                            <w:anchorlock/>
                                                            <center>
                                                            <![endif]-->
                                                                <a href="{rsvp_link}" class="btn-primary" style="color: #ffffff; font-family: Helvetica, Arial, sans-serif; padding: 10px 24px; font-size: 14px;">RSVP Now</a>
                                                            <!--[if mso]>
                                                            </center>
                                                            </v:roundrect>
                                                            <![endif]-->
                                                        </div>

                                                        <!-- Navigation Buttons -->
                                                        {f'''
                                                        <table border="0" cellpadding="0" cellspacing="0" style="margin: 15px auto 0 auto;">
                                                            <tr>
                                                                <td style="padding: 0 5px;">
                                                                    <!--[if mso]>
                                                                    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://waze.com/ul?ll={event.latitude},{event.longitude}&navigate=yes" style="height:32px;v-text-anchor:middle;width:100px;" arcsize="50%" strokecolor="#007bff" fillcolor="#ffffff">
                                                                    <w:anchorlock/>
                                                                    <center style="color:#007bff;font-family:Helvetica, Arial,sans-serif;font-size:12px;font-weight:bold;">Waze</center>
                                                                    </v:roundrect>
                                                                    <![endif]-->
                                                                    <a href="https://waze.com/ul?ll={event.latitude},{event.longitude}&navigate=yes" style="background-color: #ffffff; color: #007bff; border: 1px solid #007bff; padding: 8px 20px; text-decoration: none; border-radius: 50px; font-size: 12px; font-weight: bold; display: inline-block; font-family: Helvetica, Arial, sans-serif; mso-hide:all;">🚗 Waze</a>
                                                                </td>
                                                                <td style="padding: 0 5px;">
                                                                    <!--[if mso]>
                                                                    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://www.google.com/maps/search/?api=1&query={event.latitude},{event.longitude}" style="height:32px;v-text-anchor:middle;width:100px;" arcsize="50%" strokecolor="#007bff" fillcolor="#ffffff">
                                                                    <w:anchorlock/>
                                                                    <center style="color:#007bff;font-family:Helvetica, Arial,sans-serif;font-size:12px;font-weight:bold;">Maps</center>
                                                                    </v:roundrect>
                                                                    <![endif]-->
                                                                    <a href="https://www.google.com/maps/search/?api=1&query={event.latitude},{event.longitude}" style="background-color: #ffffff; color: #007bff; border: 1px solid #007bff; padding: 8px 20px; text-decoration: none; border-radius: 50px; font-size: 12px; font-weight: bold; display: inline-block; font-family: Helvetica, Arial, sans-serif; mso-hide:all;">🗺️ Maps</a>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                        ''' if event.latitude and event.longitude else ''}

                                                        <!-- Footer -->
                                                        <div style="margin-top: 20px; font-size: 10px; color: #888; border-top: 1px solid #eee; padding-top: 15px; font-family: Helvetica, Arial, sans-serif;">
                                                            <p style="margin: 3px 0;">Hello {guest['name']}, we can't wait to see you!</p>
                                                            <p style="margin: 3px 0;">If the button doesn't work: <br><a href="{rsvp_link}" style="color: #007bff; text-decoration: none;">Link</a></p>
                                                        </div>

                                                    </td>
                                                </tr>
                                            </table>
                                        </div>

                                        <!--[if gte mso 9]>
                                        </v:textbox>
                                        </v:rect>
                                        <![endif]-->
                                    </td>
                                </tr>
                            </table>

                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            
            msg = Message(
                subject=f"Invitation to {event.title}",
                recipients=[guest['email']],
                html=html_body
            )
            
            # Attach the background image if we have a CID
            if attachment_cid:
                try:
                    file_path = os.path.join('/app/backgrounds', attachment_cid)
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                        # Guess content type based on extension
                        content_type = 'image/jpeg'
                        if attachment_cid.lower().endswith('.png'):
                            content_type = 'image/png'
                            
                        msg.attach(
                            filename=attachment_cid,
                            content_type=content_type,
                            data=file_data,
                            disposition='inline',
                            headers=[['Content-ID', f'<{attachment_cid}>']]
                        )
                        print(f"DEBUG: Attached {attachment_cid} to email")
                except Exception as e:
                    print(f"ERROR: Failed to attach file {attachment_cid}: {e}")

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
