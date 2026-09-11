"""
Comando personalizado: python manage.py configurar_permisos

Crea grupos de permisos según la rúbrica:
- Administradores: acceso total
- Operarios: solo ver y agregar en inventario/catálogo/almacén
- Consulta: solo ver
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Configura grupos y permisos según la rúbrica'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== CONFIGURANDO PERMISOS ===\n'
        ))

        # Modelos que manejamos
        modelos = [
            ('catalogo', 'Producto'),
            ('catalogo', 'Categoria'),
            ('catalogo', 'Marca'),
            ('catalogo', 'UnidadMedida'),
            ('catalogo', 'Proveedor'),
            ('almacen', 'Bodega'),
            ('almacen', 'Zona'),
            ('almacen', 'Ubicacion'),
            ('inventario', 'Existencia'),
            ('inventario', 'Movimiento'),
        ]

        # ============================================
        # GRUPO: ADMINISTRADORES
        # ============================================
        admin_group, _ = Group.objects.get_or_create(name='Administradores')

        # Todos los permisos de los modelos
        permisos_admin = []
        for app_label, model_name in modelos:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name.lower())
                permisos = Permission.objects.filter(content_type=ct)
                permisos_admin.extend(permisos)
            except ContentType.DoesNotExist:
                pass

        admin_group.permissions.set(permisos_admin)
        self.stdout.write(self.style.SUCCESS(
            f'  OK Grupo "Administradores": {len(permisos_admin)} permisos'
        ))

        # ============================================
        # GRUPO: OPERARIOS
        # ============================================
        operario_group, _ = Group.objects.get_or_create(name='Operarios')

        # Solo ver y agregar
        permisos_operario = []
        for app_label, model_name in modelos:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name.lower())
                for action in ['view', 'add']:
                    try:
                        p = Permission.objects.get(
                            content_type=ct,
                            codename=f'{action}_{model_name.lower()}'
                        )
                        permisos_operario.append(p)
                    except Permission.DoesNotExist:
                        pass
            except ContentType.DoesNotExist:
                pass

        operario_group.permissions.set(permisos_operario)
        self.stdout.write(self.style.SUCCESS(
            f'  OK Grupo "Operarios": {len(permisos_operario)} permisos (ver + agregar)'
        ))

        # ============================================
        # GRUPO: CONSULTA
        # ============================================
        consulta_group, _ = Group.objects.get_or_create(name='Consulta')

        # Solo ver
        permisos_consulta = []
        for app_label, model_name in modelos:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name.lower())
                try:
                    p = Permission.objects.get(
                        content_type=ct,
                        codename=f'view_{model_name.lower()}'
                    )
                    permisos_consulta.append(p)
                except Permission.DoesNotExist:
                    pass
            except ContentType.DoesNotExist:
                pass

        consulta_group.permissions.set(permisos_consulta)
        self.stdout.write(self.style.SUCCESS(
            f'  OK Grupo "Consulta": {len(permisos_consulta)} permisos (solo ver)'
        ))

        # ============================================
        # ASIGNAR USUARIOS A GRUPOS
        # ============================================
        self.stdout.write('\n  Asignando usuarios a grupos...')

        for user in Usuario.objects.all():
            # Limpiar grupos anteriores
            user.groups.clear()

            if user.is_superuser or user.rol == 'ADMIN':
                user.groups.add(admin_group)
                self.stdout.write(f'    {user.username} → Administradores')
            elif user.rol == 'OPERARIO' or user.rol == 'JEFE_BODEGA':
                user.groups.add(operario_group)
                self.stdout.write(f'    {user.username} → Operarios')
            else:  # CONSULTA
                user.groups.add(consulta_group)
                self.stdout.write(f'    {user.username} → Consulta')

        # ============================================
        # RESUMEN
        # ============================================
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== RESUMEN ==='
        ))
        self.stdout.write(f'  Grupos: {Group.objects.count()}')
        for g in Group.objects.all():
            self.stdout.write(f'    - {g.name}: {g.permissions.count()} permisos')
        self.stdout.write(f'  Usuarios: {Usuario.objects.count()}')

        self.stdout.write(self.style.SUCCESS(
            '\nPermisos configurados correctamente.\n'
        ))