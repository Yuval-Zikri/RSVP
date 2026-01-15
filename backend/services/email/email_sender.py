"""Email sending functions for invitations and reminders."""
from flask_mail import Message
from extensions import mail
from .template_generator import generate_email_html
from .attachment_handler import attach_background_image


def send_invitation_email(event, guest, base_url):
    """Send invitation email to a guest
    
    Args:
        event: Event object
        guest: Dict with 'name' and 'email'
        base_url: Base URL for RSVP link
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        rsvp_link = f"{base_url}/rsvp/{guest['token']}"
        
        html_body, attachment_cid = generate_email_html(event, guest['name'], rsvp_link)
        
        msg = Message(
            subject=f"Invitation to {event.title}",
            recipients=[guest['email']],
            html=html_body
        )
        
        # Attach the background image if we have a CID
        attach_background_image(msg, attachment_cid)
        
        mail.send(msg)
        print(f"Email sent to {guest['email']}")
        return True
    except Exception as e:
        from flask import current_app
        if hasattr(current_app, 'metrics'):
            current_app.metrics['email_errors'].inc()
        print(f"Failed to send email to {guest['email']}: {e}")
        return False


def send_reminder_email(event, invitation, base_url):
    """Send reminder email to a guest
    
    Args:
        event: Event object
        invitation: Invitation object with token, name, email
        base_url: Base URL for RSVP link
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        rsvp_link = f"{base_url}/rsvp/{invitation.token}"
        html_body, attachment_cid = generate_email_html(event, invitation.name, rsvp_link)
        
        msg = Message(
            subject=f"Reminder: RSVP for {event.title}",
            recipients=[invitation.email],
            html=html_body
        )
        
        # Attach background image if needed
        attach_background_image(msg, attachment_cid)
        
        mail.send(msg)
        print(f"Reminder sent to {invitation.email}")
        return True
    except Exception as e:
        from flask import current_app
        if hasattr(current_app, 'metrics'):
            current_app.metrics['email_errors'].inc()
        print(f"Failed to send reminder to {invitation.email}: {e}")
        return False


def send_updated_invitation_email(event, invitation, base_url):
    """Send updated invitation email (e.g., when event date changes)
    
    Args:
        event: Event object
        invitation: Invitation object with token, name, email
        base_url: Base URL for RSVP link
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        rsvp_link = f"{base_url}/rsvp/{invitation.token}"
        
        html_body, attachment_cid = generate_email_html(event, invitation.name, rsvp_link)
        
        msg = Message(
            subject=f"Updated: Invitation to {event.title}",
            recipients=[invitation.email],
            html=html_body
        )
        
        # Attach background image if needed
        attach_background_image(msg, attachment_cid)
        
        mail.send(msg)
        print(f"Resent invitation to {invitation.email}")
        return True
    except Exception as e:
        from flask import current_app
        if hasattr(current_app, 'metrics'):
            current_app.metrics['email_errors'].inc()
        print(f"Failed to resend email to {invitation.email}: {e}")
        return False
