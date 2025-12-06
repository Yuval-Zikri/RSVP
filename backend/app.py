import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from extensions import db, mail, migrate

# Initialize Extensions
# db and mail are imported from extensions.py

from config import Config

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(Config)
    
    # Initialize Plugins
    CORS(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # Prometheus Metrics
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    
    
    # Register Blueprints
    from routes.events import events_bp
    from routes.invitations import invitations_bp
    from routes.rsvp import rsvp_bp
    from routes.locations import locations_bp
    
    app.register_blueprint(events_bp)
    app.register_blueprint(invitations_bp)
    app.register_blueprint(rsvp_bp)
    app.register_blueprint(locations_bp)
    
    # Health Check
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    @app.shell_context_processor
    def make_shell_context():
        """Make database and models available in flask shell"""
        from models import Event, Invitation
        return {
            'db': db,
            'Event': Event,
            'Invitation': Invitation
        }
        
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
