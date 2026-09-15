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
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',

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

# ============================================
# CONFIGURACIÓN DE DJANGO-UNFOLD
# ============================================

from django.templatetags.static import static
from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "TechStock WMS",
    "SITE_HEADER": "TechStock · Sistema de Gestión",
    "SITE_URL": "/",
    "SITE_SYMBOL": "inventory_2",  # Icono de Material Symbols
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "DASHBOARD_CALLBACK": "apps.core.dashboard.dashboard_callback",
    
    "COLORS": {
        "primary": {
            "50":  "240 249 255",
            "100": "224 242 254",
            "200": "186 230 253",
            "300": "125 211 252",
            "400": "56 189 248",
            "500": "14 165 233",   # azul principal
            "600": "2 132 199",
            "700": "3 105 161",
            "800": "7 89 133",
            "900": "12 74 110",
            "950": "8 47 73",
        },
    },
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Operación",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Catálogo",
                        "icon": "category",
                        "link": reverse_lazy("admin:catalogo_producto_changelist"),
                    },
                    {
                        "title": "Almacén",
                        "icon": "warehouse",
                        "link": reverse_lazy("admin:almacen_ubicacion_changelist"),
                    },
                    {
                        "title": "Existencias",
                        "icon": "inventory",
                        "link": reverse_lazy("admin:inventario_existencia_changelist"),
                    },
                    {
                        "title": "Kardex",
                        "icon": "history",
                        "link": reverse_lazy("admin:inventario_movimiento_changelist"),
                    },
                ],
            },
            {
                "title": "Sistema",
                "separator": True,
                "items": [
                    {
                        "title": "Usuarios",
                        "icon": "people",
                        "link": reverse_lazy("admin:usuarios_usuario_changelist"),
                    },
                ],
            },
        ],
    },
}