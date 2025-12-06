#!/bin/sh
# entrypoint.sh - Runs database migrations before starting the server

set -e

# Wait for database to be ready using Python script
python scripts/wait_for_db.py

echo "PostgreSQL is up - executing migrations"

# Check if migrations folder exists, if not initialize it
if [ ! -d "./migrations" ]; then
    echo "Creating migrations folder..."
    echo "Clearing old migration history from database..."
    python scripts/reset_migrations.py || echo "Note: Could not clear migration history (table may not exist)"
    flask db init
fi

# Run database migrations
# We use set +e to allow the command to fail so we can handle the error
set +e
flask db migrate -m "Auto migration"
flask db upgrade
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -ne 0 ]; then
    echo "Migration failed. Attempting to reset database migrations..."
    python scripts/reset_migrations.py
    rm -rf migrations
    flask db init
    flask db migrate -m "Auto migration after reset"
    flask db upgrade
fi

echo "Starting application..."
exec python app.py
