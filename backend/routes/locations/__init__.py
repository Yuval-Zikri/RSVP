"""Location routes - Location search and background image serving."""
from flask import Blueprint, request, jsonify, send_from_directory
from services.locations import search_location


locations_bp = Blueprint('locations', __name__, url_prefix='/api')


@locations_bp.route('/search-location', methods=['GET'])
def search_location_route():
    """Search for a location"""
    query = request.args.get('q')
    if not query:
        return jsonify([]), 200
    
    results = search_location(query)
    
    from flask import current_app
    if hasattr(current_app, 'metrics'):
        current_app.metrics['location_searches'].inc()
        
    return jsonify(results), 200


@locations_bp.route('/backgrounds/<path:filename>')
def serve_background(filename):
    """Serve background images"""
    return send_from_directory('/app/backgrounds', filename)
