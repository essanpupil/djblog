"""djblog URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection

def healthz(request):
    """Liveness probe: returns 200 OK fast if container is running."""
    return JsonResponse({'status': 'live'})

def readyz(request):
    """Readiness probe: verifies database connection is active."""
    try:
        connection.ensure_connection()
        return JsonResponse({'status': 'ready', 'database': 'ok'})
    except Exception as exc:
        return JsonResponse({'status': 'not_ready', 'database': str(exc)}, status=503)

urlpatterns = [
    path('healthz', healthz, name='healthz'),
    path('readyz', readyz, name='readyz'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
