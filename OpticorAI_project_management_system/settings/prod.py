"""Production settings."""
from .base import *  # noqa
import os

DEBUG = True

# Read secret from the proper environment variable
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# ✅ Add this to allow your Railway domain
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-60bd4.up.railway.app"
]

# Optional but recommended: Also allow this host in ALLOWED_HOSTS
ALLOWED_HOSTS = [
    "web-production-60bd4.up.railway.app",
    "127.0.0.1",
    "localhost"
]


from django.conf import settings
from django.http import JsonResponse

def show_settings(request):
    return JsonResponse({
        "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
        "CSRF_TRUSTED_ORIGINS": settings.CSRF_TRUSTED_ORIGINS,
    })


# Security hardening
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# WhiteNoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'true').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'false').lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'no-reply@example.com')

# Optional Redis cache (enabled if REDIS_URL is provided)
if os.environ.get('REDIS_URL'):
	CACHES = {
		'default': {
			'BACKEND': 'django.core.cache.backends.redis.RedisCache',
			'LOCATION': os.environ['REDIS_URL'],
		}
	}

# Persistent DB connections for better throughput (safe default; override via env)
try:
	# If DATABASES exists from base, update default
	DATABASES['default']['CONN_MAX_AGE'] = int(os.environ.get('CONN_MAX_AGE', '60'))
except Exception:
	pass























