"""
Comando personalizado: python manage.py cargar_datos_demo

Carga datos de demostración para el WMS TechStock.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import random

from apps.catalogo.models import (
    Categoria, Marca, UnidadMedida, Proveedor, Producto
)
from apps.almacen.models import Bodega, Zona, Ubicacion
from apps.usuarios.models import Usuario
from apps.inventario.services import (
    registrar_entrada, registrar_salida,
    registrar_traslado, StockInsuficienteError
)
from apps.inventario.models import Existencia, Movimiento


class Command(BaseCommand):
    help = 'Carga datos de demostración para el WMS'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Borra todos los datos antes de cargar'
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Borrando datos existentes...'))
            self._reset_data()

        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== CARGANDO DATOS DEMO ===\n'
        ))

        with transaction.atomic():
            bodega, zonas, ubicaciones = self._crear_almacen()
            categorias, marcas, unidades, proveedores = self._crear_catalogos()
            productos = self._crear_productos(
                categorias, marcas, unidades, proveedores
            )
            admin_user, operario = self._crear_usuarios()
            self._ejecutar_movimientos(productos, ubicaciones, admin_user)

        self._mostrar_resumen()

    def _reset_data(self):
        Movimiento.objects.all().delete()
        Existencia.objects.all().delete()
        try:
            from apps.despacho.models import Pedido, LineaPedido, Cliente
            LineaPedido.objects.all().delete()
            Pedido.objects.all().delete()
            Cliente.objects.all().delete()
        except Exception:
            pass
        try:
            from apps.recepcion.models import OrdenRecepcion, LineaRecepcion
            LineaRecepcion.objects.all().delete()
            OrdenRecepcion.objects.all().delete()
        except Exception:
            pass
        try:
            from apps.almacen.models import MovimientoUbicacion
            MovimientoUbicacion.objects.all().delete()
        except Exception:
            pass
        Ubicacion.objects.all().delete()
        Zona.objects.all().delete()
        Bodega.objects.all().delete()
        Producto.objects.all().delete()
        Proveedor.objects.all().delete()
        UnidadMedida.objects.all().delete()
        Marca.objects.all().delete()
        Categoria.objects.all().delete()

    def _crear_almacen(self):
        self.stdout.write('  -> Creando bodega, zonas y ubicaciones...')

        bodega = Bodega.objects.create(
            codigo='B1',
            nombre='Bodega Principal UPEC',
            direccion='Av. Universitaria s/n',
            ciudad='Tulcan'
        )

        zonas_data = [
            ('Z1', 'Almacenaje', 'ALMACENAJE'),
            ('Z2', 'Picking', 'PICKING'),
            ('Z3', 'Recepcion', 'RECEPCION'),
        ]

        zonas = []
        for codigo, nombre, tipo in zonas_data:
            zona = Zona.objects.create(
                bodega=bodega,
                codigo=codigo,
                nombre=nombre,
                tipo=tipo
            )
            zonas.append(zona)

        ubicaciones = []
        for zona in zonas:
            for i in range(1, 5):
                ubi = Ubicacion.objects.create(
                    codigo=f'B1-{zona.codigo}-E{i}',
                    zona=zona,
                    pasillo=str(i),
                    rack='1',
                    nivel='1',
                    capacidad_maxima=100
                )
                ubicaciones.append(ubi)

        self.stdout.write(self.style.SUCCESS(
            f'    OK 1 bodega, {len(zonas)} zonas, {len(ubicaciones)} ubicaciones'
        ))
        return bodega, zonas, ubicaciones

    def _crear_catalogos(self):
        self.stdout.write('  -> Creando categorias, marcas, unidades y proveedores...')

        categorias = []
        for nombre, desc in [
            ('Smartphone', 'Telefonos inteligentes'),
            ('Tablet', 'Tabletas y iPads'),
            ('Laptop', 'Computadoras portatiles'),
        ]:
            cat = Categoria.objects.create(nombre=nombre, descripcion=desc)
            categorias.append(cat)

        marcas = []
        for nombre, pais in [
            ('Apple', 'EE.UU.'),
            ('Samsung', 'Corea del Sur'),
            ('Xiaomi', 'China'),
            ('Lenovo', 'China'),
        ]:
            mar = Marca.objects.create(nombre=nombre, pais_origen=pais)
            marcas.append(mar)

        unidades = []
        for nombre, abrev in [
            ('Unidad', 'UND'),
            ('Caja', 'CJ'),
            ('Pack x10', 'PACK'),
        ]:
            u = UnidadMedida.objects.create(nombre=nombre, abreviatura=abrev)
            unidades.append(u)

        proveedores = []
        for razon, ruc, tel, email, ciudad in [
            ('Distribuidora Andina S.A.', '1792345678001', '022345678',
             'ventas@andina.com.ec', 'Quito'),
            ('Tech Import Cia. Ltda.', '0998765432001', '042345678',
             'info@techimport.com.ec', 'Guayaquil'),
        ]:
            p = Proveedor.objects.create(
                razon_social=razon,
                numero_documento=ruc,
                telefono=tel,
                email=email,
                ciudad=ciudad
            )
            proveedores.append(p)

        self.stdout.write(self.style.SUCCESS(
            f'    OK {len(categorias)} categorias, {len(marcas)} marcas, '
            f'{len(unidades)} unidades, {len(proveedores)} proveedores'
        ))
        return categorias, marcas, unidades, proveedores

    def _crear_productos(self, categorias, marcas, unidades, proveedores):
        self.stdout.write('  -> Creando 10 productos...')

        cat_smart, cat_tablet, cat_laptop = categorias
        mar_apple, mar_samsung, mar_xiaomi, mar_lenovo = marcas
        und_unidad = unidades[0]
        prov_andina, prov_tech = proveedores

        productos_data = [
            ('APL-IP15-128', 'iPhone 15 128GB', mar_apple, cat_smart, 799.00, prov_tech),
            ('APL-IP15-256', 'iPhone 15 256GB', mar_apple, cat_smart, 899.00, prov_tech),
            ('APL-IPAD10', 'iPad 10ma Gen 64GB', mar_apple, cat_tablet, 449.00, prov_tech),
            ('SAM-S23-256', 'Galaxy S23 256GB', mar_samsung, cat_smart, 699.00, prov_andina),
            ('SAM-S24-512', 'Galaxy S24 512GB', mar_samsung, cat_smart, 999.00, prov_andina),
            ('SAM-TABA9', 'Galaxy Tab A9', mar_samsung, cat_tablet, 279.00, prov_andina),
            ('XIA-RN13', 'Redmi Note 13', mar_xiaomi, cat_smart, 299.00, prov_andina),
            ('XIA-POCOX6', 'POCO X6 Pro', mar_xiaomi, cat_smart, 379.00, prov_andina),
            ('LEN-TPE14', 'ThinkPad E14 i5', mar_lenovo, cat_laptop, 599.00, prov_tech),
            ('LEN-IP3', 'IdeaPad 3 Ryzen 5', mar_lenovo, cat_laptop, 449.00, prov_tech),
        ]

        productos = []
        for sku, nombre, marca, categoria, precio, prov in productos_data:
            p = Producto.objects.create(
                sku=sku,
                nombre=nombre,
                marca=marca,
                categoria=categoria,
                unidad_medida=und_unidad,
                proveedor=prov,
                precio_venta=Decimal(str(precio)),
                stock_minimo=5,
                stock_maximo=100,
                especificaciones='Producto de demostracion'
            )
            productos.append(p)

        self.stdout.write(self.style.SUCCESS(
            f'    OK {len(productos)} productos'
        ))
        return productos

    def _crear_usuarios(self):
        self.stdout.write('  -> Creando usuarios...')

        admin_user = Usuario.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = Usuario.objects.filter(rol='ADMIN').first()
        if not admin_user:
            self.stdout.write(self.style.ERROR(
                '    ERROR: No hay superusuario.'
            ))
            raise SystemExit(1)

        return admin_user, admin_user

    def _crear_movimiento_con_fecha(self, funcion, fecha_mov, **kwargs):
        """Ejecuta una función de service y actualiza la fecha del movimiento."""
        mov = funcion(**kwargs)
        fecha_dt = timezone.datetime.combine(
            fecha_mov,
            timezone.datetime.min.time()
        )
        fecha_aware = timezone.make_aware(fecha_dt)
        Movimiento.objects.filter(pk=mov.pk).update(fecha=fecha_aware)
        return mov

    def _ejecutar_movimientos(self, productos, ubicaciones, admin_user):
        self.stdout.write('  -> Ejecutando movimientos...')

        hoy = timezone.now().date()

        # ============================================
        # 30 ENTRADAS distribuidas en los últimos 30 días
        # ============================================
        for i in range(30):
            fecha_mov = hoy - timedelta(days=random.randint(0, 30))
            prod = random.choice(productos)
            ubi = random.choice(ubicaciones)
            
            try:
                self._crear_movimiento_con_fecha(
                    registrar_entrada,
                    fecha_mov,
                    producto=prod,
                    ubicacion=ubi,
                    cantidad=random.randint(5, 20),
                    usuario=admin_user,
                    documento=f'OC-2026-{i+1:03d}',
                    observacion=f'Entrada #{i+1}'
                )
            except Exception:
                pass

        self.stdout.write('    OK 30 entradas distribuidas')

        # ============================================
        # 20 SALIDAS distribuidas
        # ============================================
        for i in range(20):
            fecha_mov = hoy - timedelta(days=random.randint(0, 30))
            prod = random.choice(productos)
            ubi = random.choice(ubicaciones)
            
            try:
                exist = Existencia.objects.filter(producto=prod, ubicacion=ubi).first()
                if exist and exist.cantidad > 5:
                    self._crear_movimiento_con_fecha(
                        registrar_salida,
                        fecha_mov,
                        producto=prod,
                        ubicacion=ubi,
                        cantidad=random.randint(1, 3),
                        usuario=admin_user,
                        documento=f'PED-2026-{i+1:03d}',
                        observacion=f'Venta #{i+1}'
                    )
            except Exception:
                pass

        self.stdout.write('    OK 20 salidas distribuidas')

        # ============================================
        # 10 TRASLADOS
        # ============================================
        for i in range(10):
            fecha_mov = hoy - timedelta(days=random.randint(0, 25))
            prod = random.choice(productos)
            ubi_origen = random.choice(ubicaciones)
            ubi_destino = random.choice([u for u in ubicaciones if u != ubi_origen])
            
            try:
                exist = Existencia.objects.filter(producto=prod, ubicacion=ubi_origen).first()
                if exist and exist.cantidad > 3:
                    self._crear_movimiento_con_fecha(
                        registrar_traslado,
                        fecha_mov,
                        producto=prod,
                        ubicacion_origen=ubi_origen,
                        ubicacion_destino=ubi_destino,
                        cantidad=random.randint(1, 3),
                        usuario=admin_user,
                        documento=f'TR-2026-{i+1:03d}',
                        observacion=f'Traslado #{i+1}'
                    )
            except Exception:
                pass

        self.stdout.write('    OK 10 traslados distribuidos')

        # ============================================
        # INTENTO FALLIDO
        # ============================================
        try:
            registrar_salida(
                producto=productos[0],
                ubicacion=ubicaciones[4],
                cantidad=99999,
                usuario=admin_user,
                documento='TEST-ERROR',
                observacion='Prueba de stock insuficiente'
            )
        except StockInsuficienteError:
            self.stdout.write(self.style.SUCCESS(
                '    OK Intento fallido rechazado correctamente'
            ))

    def _mostrar_resumen(self):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== RESUMEN ==='
        ))
        self.stdout.write(f'  Productos:     {Producto.objects.count()}')
        self.stdout.write(f'  Ubicaciones:   {Ubicacion.objects.count()}')
        self.stdout.write(f'  Existencias:   {Existencia.objects.count()}')
        self.stdout.write(f'  Movimientos:   {Movimiento.objects.count()}')
        self.stdout.write(f'  Usuarios:      {Usuario.objects.count()}')

        self.stdout.write(self.style.SUCCESS(
            '\nDatos demo cargados correctamente.\n'
        ))