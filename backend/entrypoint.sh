#!/bin/sh
# entrypoint.sh - Runs database migrations before starting the server

set -e

# Wait for database to be ready using Python script
python wait_for_db.py

echo "PostgreSQL is up - executing migrations"

# Check if migrations folder exists, if not initialize it
if [ ! -d "./migrations" ]; then
    echo "Creating migrations folder..."
    flask db init
fi

# Run database migrations
flask db migrate -m "Auto migration" || true
flask db upgrade

echo "Starting application..."
exec python app.py
