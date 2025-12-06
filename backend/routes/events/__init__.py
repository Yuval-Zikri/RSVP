"""Events routes - Combines all event-related endpoints."""
from flask import Blueprint
from .crud import crud_bp
from .updates import updates_bp
from .actions import actions_bp


# Create main events blueprint
events_bp = Blueprint('events', __name__, url_prefix='/api/events')

# Register sub-blueprints
events_bp.register_blueprint(crud_bp)
events_bp.register_blueprint(updates_bp)
events_bp.register_blueprint(actions_bp)
