# Sistema WMS - Universidad Politécnica Estatal del Carchi

Sistema de Gestión de Almacenes (WMS) desarrollado con Django 5.2 LTS para la Carrera de Logística y Transporte.

## Requisitos Previos

- Python 3.13/3.14 (64 bits)
- Git
- Visual Studio Code

## Instalación Rápida

```powershell
# 1. Clonar el repositorio
git clone https://github.com/Andrew-not/wms-upec.git
cd wms-upec

# 2. Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env

# 5. Generar clave secreta y agregarla a .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 6. Crear base de datos y usuario admin
python manage.py migrate
python manage.py createsuperuser

# 7. Levantar servidor
python manage.py runserver