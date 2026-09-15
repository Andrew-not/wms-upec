"""
Comando: python manage.py crear_usuarios_modulos

Crea 5 usuarios operarios (uno por módulo) + 1 cliente.
Cada operario solo puede ver/modificar su módulo en el admin.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Crea usuarios operarios por módulo y un cliente'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== CREANDO USUARIOS POR MODULO ===\n'
        ))

        # Definir módulos y sus modelos
        modulos = {
            'catalogo': {
                'nombre': 'Catalogo',
                'modelos': ['Categoria', 'Marca', 'UnidadMedida', 'Proveedor', 'Producto'],
            },
            'almacen': {
                'nombre': 'Almacen',
                'modelos': ['Bodega', 'Zona', 'Ubicacion', 'MovimientoUbicacion'],
            },
            'inventario': {
                'nombre': 'Inventario',
                'modelos': ['Existencia', 'Movimiento'],
            },
            'recepcion': {
                'nombre': 'Recepcion',
                'modelos': ['OrdenRecepcion', 'LineaRecepcion'],
            },
            'despacho': {
                'nombre': 'Despacho',
                'modelos': ['Cliente', 'Pedido', 'LineaPedido'],
            },
        }

        # Crear grupos y usuarios para cada módulo
        for modulo, config in modulos.items():
            # 1. Crear grupo del módulo
            grupo, _ = Group.objects.get_or_create(
                name=f'Operario {config["nombre"]}'
            )

            # 2. Obtener permisos de los modelos del módulo
            permisos = []
            for model_name in config['modelos']:
                try:
                    ct = ContentType.objects.get(
                        app_label=modulo,
                        model=model_name.lower()
                    )
                    permisos.extend(
                        Permission.objects.filter(content_type=ct)
                    )
                except ContentType.DoesNotExist:
                    pass

            grupo.permissions.set(permisos)

            # 3. Crear usuario
            username = f'operario_{modulo}'
            user, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': config['nombre'],
                    'last_name': 'Operario',
                    'email': f'{username}@upec.edu.ec',
                    'rol': 'OPERARIO',
                    'is_staff': True,
                    'is_active': True,
                }
            )
            if created:
                user.set_password('operario123')
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'  OK Usuario {username} (clave: operario123)'
                ))
            else:
                self.stdout.write(f'  -> Usuario {username} ya existia')

            user.groups.clear()
            user.groups.add(grupo)
            self.stdout.write(self.style.SUCCESS(
                f'     Grupo: Operario {config["nombre"]} ({len(permisos)} permisos)'
            ))

        # 4. Crear usuario cliente
        cliente, created = Usuario.objects.get_or_create(
            username='cliente',
            defaults={
                'first_name': 'Cliente',
                'last_name': 'Demo',
                'email': 'cliente@upec.edu.ec',
                'rol': 'CONSULTA',
                'is_staff': False,
                'is_active': True,
            }
        )
        if created:
            cliente.set_password('cliente123')
            cliente.save()
            self.stdout.write(self.style.SUCCESS(
                '\n  OK Usuario cliente (clave: cliente123)'
            ))
        else:
            self.stdout.write('\n  -> Usuario cliente ya existia')

        # 5. Resumen
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== RESUMEN ==='
        ))
        self.stdout.write(f'  Grupos: {Group.objects.count()}')
        for g in Group.objects.all():
            self.stdout.write(f'    - {g.name}: {g.permissions.count()} permisos')
        self.stdout.write(f'\n  Usuarios totales: {Usuario.objects.count()}')

        self.stdout.write(self.style.SUCCESS(
            '\nUsuarios creados correctamente.'
        ))
        self.stdout.write('\nCredenciales:')
        for modulo in modulos.keys():
            self.stdout.write(f'  operario_{modulo} / operario123')
        self.stdout.write('  cliente / cliente123')