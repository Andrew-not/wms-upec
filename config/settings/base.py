"""
Configuración base del proyecto WMS
Compartida entre todos los entornos (desarrollo y producción)
"""

from pathlib import Path
import os
import environ

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Inicializar django-environ
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Leer el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Seguridad
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicaciones de terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'import_export',
    'rest_framework',
    'django_extensions',
    
    # Aplicaciones del proyecto
    'apps.core',
    'apps.usuarios',
    'apps.catalogo',
    'apps.almacen',
    'apps.inventario',
    'apps.recepcion',
    'apps.despacho',
    'apps.reportes',
]

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'usuarios.Usuario'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Base de datos (por defecto SQLite)
DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3')
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalización
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos subidos por usuarios
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de formularios
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login y logout
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Tipo de campo por defecto para llaves primarias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'