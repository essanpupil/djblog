from .settings import *

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
DEBUG = False
X_FRAME_OPTIONS = 'DENY'
ALLOWED_HOSTS = ['192.168.33.10']
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "blogdb",
        "USER": "djblogger",
        "PASSWORD": "tulisanrahasia",
        "HOST": "127.0.0.1",
        "PORT": 5432
    }
}
