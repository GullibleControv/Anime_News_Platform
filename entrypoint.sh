#!/bin/bash
# ============================================================
# Entrypoint Script for Anime News Platform
# ============================================================
# This script runs when the container starts, BEFORE the main
# application. It's useful for:
#   - Waiting for database to be ready
#   - Running migrations
#   - Any other startup tasks
# ============================================================

set -e  # Exit immediately if any command fails

# ------------------------------------------------------------
# WAIT FOR DATABASE (if using PostgreSQL)
# ------------------------------------------------------------
# When using docker-compose, the database container might take
# a few seconds to start. This loop waits until PostgreSQL is
# ready to accept connections.
# ------------------------------------------------------------
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for PostgreSQL to be ready..."
    
    # Extract host and port from DATABASE_URL
    # Example: postgresql://user:pass@db:5432/dbname
    # We need to check if 'db:5432' is accepting connections
    
    # Simple wait loop (max 30 seconds)
    for i in {1..30}; do
        python << END
import sys
import dj_database_url
import psycopg2

db_config = dj_database_url.parse("$DATABASE_URL")
try:
    conn = psycopg2.connect(
        host=db_config['HOST'],
        port=db_config['PORT'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        dbname=db_config['NAME']
    )
    conn.close()
    sys.exit(0)
except psycopg2.OperationalError:
    sys.exit(1)
END
        if [ $? -eq 0 ]; then
            echo "PostgreSQL is ready!"
            break
        fi
        echo "PostgreSQL not ready yet... waiting ($i/30)"
        sleep 1
    done
fi

# ------------------------------------------------------------
# RUN DATABASE MIGRATIONS
# ------------------------------------------------------------
# Apply any pending database migrations.
# This ensures your database schema is up to date.
# ------------------------------------------------------------
echo "Running database migrations..."
python manage.py migrate --noinput

# ------------------------------------------------------------
# EXECUTE MAIN COMMAND
# ------------------------------------------------------------
# "$@" passes all arguments to this script to the next command.
# This allows docker-compose to override the default CMD.
#
# Example:
#   CMD ["gunicorn", ...] in Dockerfile
#   becomes the $@ here
# ------------------------------------------------------------
echo "Starting application..."
exec "$@"
