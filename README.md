# Sistema WMS TechStock

Sistema de Gestión de Almacenes (WMS) con Django 5.2 LTS.

Universidad Politécnica Estatal del Carchi - Carrera de Logística y Transporte.

## Módulos

- Catálogo
- Almacén
- Inventario
- Recepción
- Despacho
- Usuarios

## Requisitos previos

- Python 3.13+
- Git
- Node.js LTS
- VS Code

## Instalación

    git clone https://github.com/Andrew-not/wms-upec.git
    cd wms-upec
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    npm install
    copy .env.example .env

Generar SECRET_KEY:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Pegar el resultado en .env

    python manage.py migrate
    python manage.py cargar_datos_demo
    python manage.py createsuperuser
    python manage.py configurar_permisos

## Ejecutar (2 terminales)

Terminal 1 - Tailwind:

    npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch

Terminal 2 - Django:

    .\.venv\Scripts\Activate.ps1
    python manage.py runserver

Abrir: http://127.0.0.1:8000/

## URLs

| URL | Módulo |
|-----|--------|
| / | Dashboard |
| /catalogo/productos/ | Catálogo |
| /almacen/ubicaciones/ | Almacén |
| /almacen/mapa/ | Mapa |
| /inventario/kardex/ | Kardex |
| /recepcion/ordenes/ | Recepción |
| /despacho/pedidos/ | Despacho |
| /admin/ | Admin |

## Credenciales

- Admin: tu superusuario
- Operario: operario / operario123

## Documentación

- docs/ARQUITECTURA.md
- docs/MODULO_INVENTARIO.md
- docs/MODULO_CATALOGO.md
- docs/MODULO_ALMACEN.md
- docs/MODULO_RECEPCION.md
- docs/MODULO_DESPACHO.md