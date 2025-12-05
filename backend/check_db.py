
from app import create_app
from extensions import db
from models import Event

app = create_app()

with app.app_context():
    event = Event.query.order_by(Event.id.desc()).first()
    if event:
        print(f"Event ID: {event.id}")
        print(f"Title: {event.title}")
        print(f"Email Background URL (DB): '{event.email_background_url}'")
    else:
        print("No events found.")
