#!/usr/bin/env python
"""
Flask CLI management script for database migrations
"""
import os
from app import create_app
from extensions import db
from models import Event, Invitation

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make database and models available in flask shell"""
    return {
        'db': db,
        'Event': Event,
        'Invitation': Invitation
    }

if __name__ == '__main__':
    app.run()
