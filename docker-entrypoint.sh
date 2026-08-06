#!/bin/sh
set -e

# Wait for DB connection if DB_HOST is set
if [ -n "$DB_HOST" ]; then
    DB_P="${DB_PORT:-5432}"
    echo "[entrypoint] Checking database availability at $DB_HOST:$DB_P..."
    while ! python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(2); s.connect(('$DB_HOST', int('$DB_P')))" 2>/dev/null; do
        echo "[entrypoint] Waiting for database connection..."
        sleep 2
    done
    echo "[entrypoint] Database connection verified!"
fi

# Wait for Redis connection if REDIS_HOST is set
if [ -n "$REDIS_HOST" ]; then
    R_P="${REDIS_PORT:-6379}"
    echo "[entrypoint] Checking Redis availability at $REDIS_HOST:$R_P..."
    while ! python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(2); s.connect(('$REDIS_HOST', int('$R_P')))" 2>/dev/null; do
        echo "[entrypoint] Waiting for Redis connection..."
        sleep 2
    done
    echo "[entrypoint] Redis connection verified!"
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
THREADS="${GUNICORN_THREADS:-2}"
TIMEOUT="${GUNICORN_TIMEOUT:-30}"
KEEPALIVE="${GUNICORN_KEEPALIVE:-5}"
MAX_REQUESTS="${GUNICORN_MAX_REQUESTS:-1000}"
MAX_REQUESTS_JITTER="${GUNICORN_MAX_REQUESTS_JITTER:-50}"

echo "[entrypoint] Launching Gunicorn WSGI server on 0.0.0.0:$PORT ($WORKERS workers, $THREADS threads)..."
exec gunicorn djblog.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers "$WORKERS" \
    --threads "$THREADS" \
    --timeout "$TIMEOUT" \
    --keep-alive "$KEEPALIVE" \
    --max-requests "$MAX_REQUESTS" \
    --max-requests-jitter "$MAX_REQUESTS_JITTER" \
    --access-logfile - \
    --error-logfile -
