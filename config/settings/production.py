"""
Configuración para entorno de producción
"""

from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['.upec.edu.ec'])

# Base de datos PostgreSQL (desde .env)
DATABASES = {
    'default': env.db()
}

# Configuración de seguridad para producción
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email real (configurar según proveedor)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Configuración de archivos estáticos para producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'