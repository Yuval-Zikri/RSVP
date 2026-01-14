import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from prometheus_client import make_wsgi_app, Counter, Histogram
import time
from flask import g
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from extensions import db, mail, migrate
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
    REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency seconds', ['method', 'endpoint'])

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    @app.before_request
    def _prom_before_request():
        g._prom_start_time = time.time()

    @app.after_request
    def _prom_after_request(response):
        try:
            start = getattr(g, '_prom_start_time', None)
            if start is not None:
                latency = time.time() - start
                endpoint = request.endpoint or request.path
                REQUEST_LATENCY.labels(request.method, endpoint).observe(latency)
                REQUEST_COUNT.labels(request.method, endpoint, str(response.status_code)).inc()
        except Exception:
            pass
        return response
    
    
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
    
    # Add ngrok-skip-browser-warning header to all responses
    @app.after_request
    def add_ngrok_header(response):
        response.headers['ngrok-skip-browser-warning'] = 'true'
        return response

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