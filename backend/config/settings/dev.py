"""Development settings"""
from .base import *

DEBUG = True

# Add Django Debug Toolbar
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Show toolbar for localhost
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Email backend for development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable caching in development (use local memory cache instead of Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 1,
    }
}

# Allow all CORS in development
CORS_ALLOW_ALL_ORIGINS = True
