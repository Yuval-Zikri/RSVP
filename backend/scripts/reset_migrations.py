#!/usr/bin/env python
"""Reset migration history in the database"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Get database connection details from environment
# Get database connection details from environment
database_url = os.getenv('DATABASE_URL')
if database_url:
    from urllib.parse import urlparse
    url = urlparse(database_url)
    db_config = {
        'host': url.hostname,
        'port': url.port or 5432,
        'database': url.path[1:],
        'user': url.username,
        'password': url.password
    }
else:
    db_config = {
        'host': os.getenv('DB_HOST', 'postgres'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'event_manager'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres')
    }

try:
    # Connect to database
    conn = psycopg2.connect(**db_config)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Connected to database successfully")
    
    # Drop the alembic_version table if it exists
    cursor.execute("DROP TABLE IF EXISTS alembic_version CASCADE;")
    print("✓ Cleared migration history (dropped alembic_version table)")
    
    # Optionally, you can also drop all tables to start completely fresh
    # Uncomment the following lines if you want to reset the entire database
    """
    cursor.execute("DROP TABLE IF EXISTS event CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS rsvp CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS gift CASCADE;")
    print("✓ Dropped all application tables")
    """
    
    cursor.close()
    conn.close()
    
    print("\n✓ Migration history cleared successfully!")
    print("You can now run migrations again.")
    
except Exception as e:
    print(f"Error: {e}")
    exit(1)
