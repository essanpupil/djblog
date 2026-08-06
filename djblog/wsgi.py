"""
WSGI config for djblog project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djblog.settings')

# OpenTelemetry Distributed Tracing Initialization
otlp_endpoint = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', '')
service_name = os.environ.get('OTEL_SERVICE_NAME', 'djblog')

if otlp_endpoint and os.environ.get('ENABLE_OTEL', 'False').lower() in ('true', '1', 't'):
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.django import DjangoInstrumentor
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
        from opentelemetry.instrumentation.redis import RedisInstrumentor

        resource = Resource.create({"service.name": service_name})
        provider = TracerProvider(resource=resource)
        
        endpoint_url = otlp_endpoint if otlp_endpoint else "http://localhost:4318/v1/traces"
        exporter = OTLPSpanExporter(endpoint=endpoint_url)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        DjangoInstrumentor().instrument()
        Psycopg2Instrumentor().instrument()
        RedisInstrumentor().instrument()
        print(f"[OpenTelemetry] Tracing initialized for service '{service_name}' targeting {endpoint_url}")
    except Exception as exc:
        print(f"[OpenTelemetry] Failed to initialize tracing: {exc}")

application = get_wsgi_application()
