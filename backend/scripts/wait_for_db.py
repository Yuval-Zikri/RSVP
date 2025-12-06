import os
import sys
import time
import psycopg2
from urllib.parse import urlparse

def wait_for_db():
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("DATABASE_URL not set")
        sys.exit(1)

    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    
    print(f"Waiting for database at {hostname}:{port}...")
    
    while True:
        try:
            conn = psycopg2.connect(
                dbname=database,
                user=username,
                password=password,
                host=hostname,
                port=port
            )
            conn.close()
            print("Database is ready!")
            sys.exit(0)
        except psycopg2.OperationalError as e:
            print(f"Database not ready: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()
