#!/bin/bash
# ============================================================
# Entrypoint Script for Anime News Platform
# ============================================================

set -e  # Exit immediately if any command fails

# ------------------------------------------------------------
# COLLECT STATIC FILES
# ------------------------------------------------------------
echo "Collecting static files..."
python manage.py collectstatic --noinput

# ------------------------------------------------------------
# WAIT FOR DATABASE (if using PostgreSQL)
# ------------------------------------------------------------
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for PostgreSQL to be ready..."
    
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
echo "Running database migrations..."
python manage.py migrate --noinput

# ------------------------------------------------------------
# EXECUTE MAIN COMMAND
# ------------------------------------------------------------
echo "Starting application..."
exec "$@"
