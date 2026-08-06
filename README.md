# djblog

Blog application built with Django 2.2, fully containerized for production deployment.

## Environment Variables

Configuration is loaded dynamically via container environment variables or `.env`:

| Variable | Description | Default |
| --- | --- | --- |
| `SECRET_KEY` | Django Secret Key | Required when `DEBUG=False` |
| `DEBUG` | Debug mode (`True`/`False`) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Configurable / empty in prod |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | Configurable |
| `PORT` | Container HTTP binding port | `8000` |
| `DATABASE_URL` | Full database connection URL | Optional |
| `DB_HOST` | Database host | Unset (uses SQLite if unset) |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `blogdb` |
| `DB_USER` | Database user | `djblogger` |
| `DB_PASSWORD` | Database password | `tulisanrahasia` |
| `DB_CONN_MAX_AGE` | Connection pooling age (seconds) | `600` |
| `REDIS_URL` | Redis URL for session & cache | Optional |
| `REDIS_HOST` | Redis host | Unset |
| `REDIS_PORT` | Redis port | `6379` |
| `RUN_MIGRATIONS` | Auto-run DB migrations on start | `true` (`false` for replicas) |
| `RUN_COLLECTSTATIC` | Auto-collect static files on start | `true` |

## Building the Container Image

```bash
docker build -t djblog:latest .
```

## Running the Container

### Standalone (with SQLite default)
```bash
docker run -d -p 8000:8000 --name djblog djblog:latest
```

### Connected to External PostgreSQL & Redis
```bash
docker run -d -p 8000:8000 \
  -e DB_HOST=postgres-host \
  -e DB_PORT=5432 \
  -e DB_NAME=blogdb \
  -e DB_USER=djblogger \
  -e DB_PASSWORD=secret \
  -e REDIS_HOST=redis-host \
  -e REDIS_PORT=6379 \
  -e SECRET_KEY=your-production-secret-key \
  -e DEBUG=False \
  --name djblog djblog:latest
```

## Container Probes

- **Liveness Probe**: `GET /healthz` (returns HTTP 200 `{"status": "live"}`)
- **Readiness Probe**: `GET /readyz` (verifies PostgreSQL DB and Redis session store connectivity)
