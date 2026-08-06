#!/bin/sh
set -e

# Wait for DB connection if DB_HOST is set or if DATABASE_URL is provided
if [ -n "$DB_HOST" ]; then
    DB_P="${DB_PORT:-5432}"
    echo "[entrypoint] Checking database availability at $DB_HOST:$DB_P..."
    while ! python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(2); s.connect(('$DB_HOST', int('$DB_P')))" 2>/dev/null; do
        echo "[entrypoint] Waiting for database connection..."
        sleep 2
    done
    echo "[entrypoint] Database connection verified!"
fi

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    echo "[entrypoint] Applying database migrations..."
    python manage.py migrate --noinput
fi

if [ "${RUN_COLLECTSTATIC:-true}" = "true" ]; then
    echo "[entrypoint] Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

PORT="${PORT:-8000}"
WORKERS="${GUNICORN_WORKERS:-3}"

echo "[entrypoint] Launching Gunicorn WSGI server on 0.0.0.0:$PORT with $WORKERS workers..."
exec gunicorn djblog.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers "$WORKERS" \
    --access-logfile - \
    --error-logfile -
