from django.db import models
from django.conf import settings
from django.utils import timezone


class TareaPersonal(models.Model):
    """Tarea personal del usuario."""
    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('NORMAL', 'Normal'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    CATEGORIAS = [
        ('GENERAL', 'General'),
        ('RECEPCION', 'Recepción'),
        ('DESPACHO', 'Despacho'),
        ('INVENTARIO', 'Inventario'),
        ('SERVICIO', 'Servicio Técnico'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    titulo = models.CharField('Título', max_length=200)
    descripcion = models.TextField('Descripción', blank=True)
    categoria = models.CharField('Categoría', max_length=20, choices=CATEGORIAS, default='GENERAL')
    prioridad = models.CharField('Prioridad', max_length=10, choices=PRIORIDADES, default='NORMAL')
    estado = models.CharField('Estado', max_length=15, choices=ESTADOS, default='PENDIENTE')
    fecha_limite = models.DateTimeField('Fecha límite', null=True, blank=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    fecha_completada = models.DateTimeField('Fecha de completada', null=True, blank=True)

    class Meta:
        verbose_name = 'Tarea personal'
        verbose_name_plural = 'Tareas personales'
        ordering = ['estado', '-prioridad', 'fecha_limite']

    def __str__(self):
        return f'{self.usuario.username} - {self.titulo}'


class EventoCalendario(models.Model):
    """Evento en el calendario del usuario."""
    TIPOS = [
        ('REUNION', 'Reunión'),
        ('ENTREGA', 'Entrega'),
        ('RECEPCION', 'Recepción programada'),
        ('SERVICIO', 'Servicio técnico'),
        ('PERSONAL', 'Personal'),
        ('OTRO', 'Otro'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos'
    )
    titulo = models.CharField('Título', max_length=200)
    descripcion = models.TextField('Descripción', blank=True)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS, default='OTRO')
    fecha_inicio = models.DateTimeField('Fecha de inicio')
    fecha_fin = models.DateTimeField('Fecha de fin')
    todo_el_dia = models.BooleanField('Todo el día', default=False)
    ubicacion = models.CharField('Ubicación', max_length=200, blank=True)
    completado = models.BooleanField('Completado', default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha_inicio']

    def __str__(self):
        return f'{self.usuario.username} - {self.titulo}'


class NotaRapida(models.Model):
    """Nota rápida del usuario."""
    COLORES = [
        ('AMARILLO', 'Amarillo'),
        ('VERDE', 'Verde'),
        ('AZUL', 'Azul'),
        ('ROJO', 'Rojo'),
        ('MORADO', 'Morado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notas'
    )
    titulo = models.CharField('Título', max_length=100)
    contenido = models.TextField('Contenido')
    color = models.CharField('Color', max_length=10, choices=COLORES, default='AMARILLO')
    fijada = models.BooleanField('Fijada', default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nota rápida'
        verbose_name_plural = 'Notas rápidas'
        ordering = ['-fijada', '-fecha_actualizacion']

    def __str__(self):
        return f'{self.usuario.username} - {self.titulo}'


class Notificacion(models.Model):
    """Notificación interna del usuario."""
    TIPOS = [
        ('INFO', 'Información'),
        ('SUCCESS', 'Éxito'),
        ('WARNING', 'Advertencia'),
        ('URGENT', 'Urgente'),
    ]

    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    tipo = models.CharField('Tipo', max_length=10, choices=TIPOS, default='INFO')
    titulo = models.CharField('Título', max_length=200)
    mensaje = models.TextField('Mensaje')
    url_destino = models.CharField('URL destino', max_length=500, blank=True)
    leida = models.BooleanField('Leída', default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.destinatario.username} - {self.titulo}'


class Meta(models.Model):
    """Meta personal del usuario."""
    TIPOS = [
        ('VENTAS', 'Ventas'),
        ('REPARACIONES', 'Reparaciones'),
        ('RECEPCIONES', 'Recepciones'),
        ('CLIENTES', 'Clientes atendidos'),
        ('CUSTOM', 'Personalizada'),
    ]
    PERIODOS = [
        ('DIARIA', 'Diaria'),
        ('SEMANAL', 'Semanal'),
        ('MENSUAL', 'Mensual'),
        ('ANUAL', 'Anual'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='metas'
    )
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS, default='CUSTOM')
    descripcion = models.CharField('Descripción', max_length=200)
    objetivo = models.DecimalField('Objetivo', max_digits=10, decimal_places=2, default=0)
    progreso = models.DecimalField('Progreso', max_digits=10, decimal_places=2, default=0)
    periodo = models.CharField('Período', max_length=15, choices=PERIODOS, default='MENSUAL')
    fecha_inicio = models.DateField('Fecha inicio')
    fecha_fin = models.DateField('Fecha fin')
    activa = models.BooleanField('Activa', default=True)
    completada = models.BooleanField('Completada', default=False)

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        ordering = ['-activa', 'fecha_fin']

    def __str__(self):
        return f'{self.usuario.username} - {self.descripcion}'

    @property
    def porcentaje(self):
        if self.objetivo == 0:
            return 0
        return round((self.progreso / self.objetivo) * 100, 1)


class PreferenciaUsuario(models.Model):
    """Configuración personal del usuario."""
    TEMAS = [
        ('OSCURO', 'Oscuro'),
        ('CLARO', 'Claro'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferencias'
    )
    tema = models.CharField('Tema', max_length=10, choices=TEMAS, default='OSCURO')
    notif_email = models.BooleanField('Notificaciones por email', default=True)
    notif_dashboard = models.BooleanField('Notificaciones en dashboard', default=True)
    mostrar_calendario = models.BooleanField('Mostrar calendario', default=True)
    mostrar_tareas = models.BooleanField('Mostrar tareas', default=True)
    mostrar_metas = models.BooleanField('Mostrar metas', default=True)
    mostrar_notas = models.BooleanField('Mostrar notas', default=True)
    mostrar_kpis = models.BooleanField('Mostrar KPIs', default=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Preferencia'
        verbose_name_plural = 'Preferencias'

    def __str__(self):
        return f'Preferencias de {self.usuario.username}'


class ActividadReciente(models.Model):
    """Log de actividad del usuario."""
    ACCIONES = [
        ('CREAR', 'Crear'),
        ('EDITAR', 'Editar'),
        ('ELIMINAR', 'Eliminar'),
        ('VER', 'Ver'),
        ('PROCESAR', 'Procesar'),
    ]
    MODULOS = [
        ('CATALOGO', 'Catálogo'),
        ('ALMACEN', 'Almacén'),
        ('INVENTARIO', 'Inventario'),
        ('RECEPCION', 'Recepción'),
        ('DESPACHO', 'Despacho'),
        ('SERVICIO', 'Servicio'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actividades'
    )
    accion = models.CharField('Acción', max_length=10, choices=ACCIONES)
    modulo = models.CharField('Módulo', max_length=20, choices=MODULOS)
    descripcion = models.CharField('Descripción', max_length=300)
    url = models.CharField('URL', max_length=500, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Actividad reciente'
        verbose_name_plural = 'Actividades recientes'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.usuario.username} - {self.descripcion}'