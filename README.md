# djblog

Blog application built with Django 2.2, fully containerized with full-stack observability (Metrics, Logs, Traces).

## Observability Features

The application implements the **Three Pillars of Observability**:

1. **Metrics (Prometheus)**:
   - Exposes `/metrics` endpoint via `django-prometheus`.
   - Tracks HTTP request counts, latency histograms, database query execution times, and Redis cache hits/misses.

2. **Logs (Loki)**:
   - Outputs structured JSON logs to stdout (`{"timestamp": "...", "level": "...", "trace_id": "...", "span_id": "...", ...}`).
   - Automatically injects OpenTelemetry `trace_id` and `span_id` into every log line for 1-click log-to-trace navigation in Grafana.

3. **Tracing (OpenTelemetry)**:
   - Auto-instruments Django HTTP handlers, PostgreSQL database queries, and Redis commands.
   - Exports OTLP spans via HTTP to Grafana Tempo, OpenTelemetry Collector, or Jaeger via `OTEL_EXPORTER_OTLP_ENDPOINT`.

## Environment Variables

Configuration is loaded dynamically via container environment variables or `.env`:

| Variable | Description | Default |
| --- | --- | --- |
| `SECRET_KEY` | Django Secret Key | Required when `DEBUG=False` |
| `DEBUG` | Debug mode (`True`/`False`) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Configurable / empty in prod |
| `PORT` | Container HTTP binding port | `8000` |
| `DATABASE_URL` | Full database connection URL | Optional |
| `DB_HOST` | Database host | Unset (uses SQLite if unset) |
| `REDIS_HOST` | Redis host | Unset |
| `OTEL_SERVICE_NAME` | OpenTelemetry Service Name | `djblog` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP Exporter Endpoint URL | Unset (disabled if unset) |

## Container Probes & Endpoints

- **Liveness Probe**: `GET /healthz` (returns HTTP 200 `{"status": "live"}`)
- **Readiness Probe**: `GET /readyz` (verifies PostgreSQL DB and Redis session store connectivity)
- **Prometheus Metrics**: `GET /metrics`

## Building & Running

```bash
docker build -t djblog:latest .

docker run -d -p 8000:8000 \
  -e DB_HOST=postgres-host \
  -e REDIS_HOST=redis-host \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318/v1/traces \
  -e SECRET_KEY=your-production-secret-key \
  -e DEBUG=False \
  --name djblog djblog:latest
```

## Development with Docker Compose

A development `docker-compose.yaml` is provided for local laptop usage.

```bash
cp .env.example .env
docker compose up --build
```

The compose setup includes:
- `web` service built from the repository Dockerfile
- `db` service using PostgreSQL
- `redis` service using Redis

The development web service mounts the project source code and a named staticfiles volume so changes are reflected immediately.

## Kubernetes Deployment

A Helm chart for the application is available at `charts/djblog`.

The chart deploys the Django application as a `Deployment` and exposes it through a `Service`. External dependencies like PostgreSQL, Redis, and an optional OpenTelemetry collector must be provided separately.

Example install:

```bash
helm install djblog ./charts/djblog \
  --set image.repository=your-registry/djblog \
  --set image.tag=latest \
  --set env.SECRET_KEY=your-production-secret-key \
  --set env.DB_HOST=postgres-host \
  --set env.DB_USER=djblogger \
  --set env.DB_PASSWORD=your-db-password \
  --set env.REDIS_HOST=redis-host \
  --set env.REDIS_PASSWORD=your-redis-password \
  --set env.ALLOWED_HOSTS=your.host.example.com
```

For secret values, you can enable the chart-managed Kubernetes Secret or provide your own existing secret name:

```bash
helm install djblog ./charts/djblog \
  --set secret.enabled=true \
  --set secret.djangoSecretKey=your-production-secret-key \
  --set secret.dbPassword=your-db-password \
  --set secret.redisPassword=your-redis-password
```

To deploy a bundled Redis instance for the application, enable Redis in the chart and let the chart wire the host automatically:

```bash
helm install djblog ./charts/djblog \
  --set redis.enabled=true \
  --set image.repository=your-registry/djblog \
  --set image.tag=latest \
  --set env.SECRET_KEY=your-production-secret-key \
  --set env.DB_HOST=postgres-host \
  --set env.DB_PASSWORD=your-db-password
```

To use an existing Redis service instead, leave `redis.enabled` disabled and provide the Redis host and optional password via environment values:

```bash
helm install djblog ./charts/djblog \
  --set env.REDIS_HOST=redis.my-namespace.svc.cluster.local \
  --set env.REDIS_PASSWORD=your-redis-password
```

## GitHub Actions

This repository includes GitHub Actions workflows for CI and CD.

- `/.github/workflows/ci.yml` runs on push and pull request and executes dependency installation, Django system checks, and application tests.
- `/.github/workflows/cd.yml` runs on push to `master`/`main` and builds/pushes a container image to GitHub Container Registry. When `KUBE_CONFIG_DATA` is configured as a repository secret, it also deploys the Helm chart to the target Kubernetes cluster.

### Required repository secrets for CD

- `GITHUB_TOKEN` (provided automatically by GitHub Actions)
- `KUBE_CONFIG_DATA` (base64-encoded kubeconfig file)
- Optional secrets for Helm values when deploying:
  - `DJANGO_SECRET_KEY`
  - `DB_PASSWORD`
  - `REDIS_PASSWORD`
  - `DB_HOST`
  - `REDIS_HOST`

A base64-encoded kubeconfig can be generated locally with:

```bash
cat $HOME/.kube/config | base64 | tr -d '\n'
```
