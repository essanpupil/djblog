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
