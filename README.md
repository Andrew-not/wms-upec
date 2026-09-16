# C.TECH WMS - Sistema de Gestión de Almacenes

Sistema WMS desarrollado con Django 5.2 LTS para **C.TECH - Servicio y Calidad**.

Universidad Politécnica Estatal del Carchi  
Carrera de Logística y Transporte

## 🎯 Módulos implementados

- **Catálogo** — productos, categorías, marcas, proveedores
- **Almacén** — bodegas, zonas, ubicaciones con mapa visual
- **Inventario** — existencias, kardex, servicios transaccionales
- **Recepción** — órdenes de recepción con putaway
- **Despacho** — clientes, pedidos, picking con validación de stock
- **Servicio Técnico** — equipos por IMEI (en desarrollo)
- **Mi Espacio** — tareas, eventos, metas, notas
- **Reportes** — análisis con exportación PDF/Excel/Word

## 👥 Sistema de usuarios

| Usuario | Contraseña | Rol | Acceso |
|---------|-----------|-----|--------|
| `Andrewnot` | (crear) | ADMIN | Todo |
| `jefe_bodega` | `jefe123` | JEFE | Todo menos admin |
| `operario_catalogo` | `operario123` | OPERARIO | Catálogo |
| `operario_almacen` | `operario123` | OPERARIO | Almacén |
| `operario_inventario` | `operario123` | OPERARIO | Inventario |
| `operario_recepcion` | `operario123` | OPERARIO | Recepción |
| `operario_despacho` | `operario123` | OPERARIO | Despacho |
| `tecnico` | `tecnico123` | OPERARIO | Servicio |
| `vendedor` | `vendedor123` | OPERARIO | Despacho |
| `cliente` | `cliente123` | CONSULTA | Solo lectura |

## 📋 Requisitos previos

- Python 3.13+ (marcar "Add python.exe to PATH")
- Git
- Node.js LTS
- Visual Studio Code

## 🚀 Instalación

```powershell
# 1. Clonar repositorio
git clone https://github.com/Andrew-not/wms-upec.git
cd wms-upec

# 2. Entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt
npm install

# 4. Archivo .env
copy .env.example .env

# 5. Generar SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Pegar el resultado en .env

# 6. Base de datos
python manage.py migrate
python manage.py cargar_datos_demo --reset
python manage.py createsuperuser
python manage.py crear_usuarios_sistema

# 7. Servidor (2 terminales)
# Terminal 1:
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch

# Terminal 2:
python manage.py runserver