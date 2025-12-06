"""Email service - Exports all email-related functions."""
from .template_generator import generate_email_html
from .attachment_handler import attach_background_image
from .email_sender import (
    send_invitation_email,
    send_reminder_email,
    send_updated_invitation_email
)

__all__ = [
    'generate_email_html',
    'attach_background_image',
    'send_invitation_email',
    'send_reminder_email',
    'send_updated_invitation_email'
]
