"""djblog URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings

def healthz(request):
    """Liveness probe: returns 200 OK fast if container is running."""
    return JsonResponse({'status': 'live'})

def readyz(request):
    """Readiness probe: verifies database and redis connectivity."""
    status = {'status': 'ready', 'database': 'ok'}
    errors = {}

    try:
        connection.ensure_connection()
    except Exception as exc:
        errors['database'] = str(exc)

    if getattr(settings, 'SESSION_ENGINE', '') == 'django.contrib.sessions.backends.cache':
        try:
            cache.set('_healthcheck', 'ok', 5)
            if cache.get('_healthcheck') != 'ok':
                errors['redis'] = 'Cache read/write mismatch'
            else:
                status['redis'] = 'ok'
        except Exception as exc:
            errors['redis'] = str(exc)

    if errors:
        status['status'] = 'not_ready'
        status.update(errors)
        return JsonResponse(status, status=503)

    return JsonResponse(status)

urlpatterns = [
    path('healthz', healthz, name='healthz'),
    path('readyz', readyz, name='readyz'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
