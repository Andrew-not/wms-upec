"""
Comando: python manage.py crear_usuarios_sistema

Crea los 10 usuarios del sistema con jerarquía:
- 1 Admin (ya existe)
- 1 Jefe de Bodega
- 5 Operarios (uno por módulo)
- 1 Técnico
- 1 Vendedor
- 1 Cliente
"""
from django.core.management.base import BaseCommand
from apps.usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Crea los usuarios del sistema con jerarquía'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== CREANDO USUARIOS DEL SISTEMA ===\n'
        ))

        usuarios = [
            {
                'username': 'jefe_bodega',
                'password': 'jefe123',
                'first_name': 'Jefe',
                'last_name': 'Bodega',
                'email': 'jefe@ctech.com',
                'rol': 'JEFE',
                'cargo': 'Jefe de Bodega',
                'is_staff': True,
            },
            {
                'username': 'operario_catalogo',
                'password': 'operario123',
                'first_name': 'Operario',
                'last_name': 'Catalogo',
                'email': 'op.catalogo@ctech.com',
                'rol': 'OPERARIO',
                'cargo': 'Operario de Catálogo',
                'is_staff': True,
            },
            {
                'username': 'operario_almacen',
                'password': 'operario123',
                'first_name': 'Operario',
                'last_name': 'Almacen',
                'email': 'op.almacen@ctech.com',
                'rol': 'OPERARIO',
                'cargo': 'Operario de Almacén',
                'is_staff': True,
            },
            {
                'username': 'operario_inventario',
                'password': 'operario123',
                'first_name': 'Operario',
                'last_name': 'Inventario',
                'email': 'op.inventario@ctech.com',
                'rol': 'OPERARIO',
                'cargo': 'Operario de Inventario',
                'is_staff': True,
            },
            {
                'username': 'operario_recepcion',
                'password': 'operario123',
                'first_name': 'Operario',
                'last_name': 'Recepcion',
                'email': 'op.recepcion@ctech.com',
                'rol': 'OPERARIO',
                'cargo': 'Operario de Recepción',
                'is_staff': True,
            },
            {
                'username': 'operario_despacho',
                'password': 'operario123',
                'first_name': 'Operario',
                'last_name': 'Despacho',
                'email': 'op.despacho@ctech.com',
                'rol': 'OPERARIO',
                'cargo': 'Operario de Despacho',
                'is_staff': True,
            },
            {
                'username': 'tecnico',
                'password': 'tecnico123',
                'first_name': 'Tecnico',
                'last_name': 'CTech',
                'email': 'tecnico@ctech.com',
                'rol': 'OPERARIO',
                'cargo': 'Técnico de Servicio',
                'is_staff': True,
            },
            {
                'username': 'vendedor',
                'password': 'vendedor123',
                'first_name': 'Vendedor',
                'last_name': 'CTech',
                'email': 'vendedor@ctech.com',
                'rol': 'OPERARIO',
                'cargo': 'Vendedor',
                'is_staff': True,
            },
            {
                'username': 'cliente',
                'password': 'cliente123',
                'first_name': 'Cliente',
                'last_name': 'Demo',
                'email': 'cliente@ctech.com',
                'rol': 'CONSULTA',
                'cargo': 'Cliente',
                'is_staff': False,
            },
        ]

        for data in usuarios:
            user, created = Usuario.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'rol': data['rol'],
                    'cargo': data['cargo'],
                    'is_staff': data['is_staff'],
                    'is_active': True,
                }
            )
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f"  OK {data['username']:25} | {data['rol']:10} | {data['password']}"
                ))
            else:
                self.stdout.write(f"  -> {data['username']:25} ya existia")

        self.stdout.write(self.style.SUCCESS(
            '\nUsuarios del sistema creados correctamente.\n'
        ))
        self.stdout.write('Credenciales:')
        self.stdout.write('  jefe_bodega        / jefe123')
        self.stdout.write('  operario_catalogo  / operario123')
        self.stdout.write('  operario_almacen   / operario123')
        self.stdout.write('  operario_inventario/ operario123')
        self.stdout.write('  operario_recepcion / operario123')
        self.stdout.write('  operario_despacho  / operario123')
        self.stdout.write('  tecnico            / tecnico123')
        self.stdout.write('  vendedor           / vendedor123')
        self.stdout.write('  cliente            / cliente123\n')