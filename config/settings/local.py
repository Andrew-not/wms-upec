"""
Configuración para entorno de desarrollo local
"""

from .base import *

DEBUG = True

# Mostrar errores detallados
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Base de datos SQLite (por defecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email en consola (no envía correos reales)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug Toolbar (solo en desarrollo)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# IPs internas para Debug Toolbar
INTERNAL_IPS = ['127.0.0.1']

# Configuración de archivos estáticos en desarrollo
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Configuración de archivos multimedia en desarrollo
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'