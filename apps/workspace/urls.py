from django.urls import path
from . import views

app_name = 'workspace'

urlpatterns = [
    # Mi Espacio principal
    path('', views.mi_espacio, name='mi_espacio'),
    
    # Tareas
    path('tareas/', views.tarea_lista, name='tarea_lista'),
    path('tareas/crear/', views.tarea_crear, name='tarea_crear'),
    path('tareas/<int:pk>/editar/', views.tarea_editar, name='tarea_editar'),
    path('tareas/<int:pk>/completar/', views.tarea_completar, name='tarea_completar'),
    path('tareas/<int:pk>/eliminar/', views.tarea_eliminar, name='tarea_eliminar'),
    
    # Eventos
    path('eventos/', views.evento_lista, name='evento_lista'),
    path('eventos/crear/', views.evento_crear, name='evento_crear'),
    path('eventos/<int:pk>/editar/', views.evento_editar, name='evento_editar'),
    path('eventos/<int:pk>/eliminar/', views.evento_eliminar, name='evento_eliminar'),
    
    # Notas
    path('notas/', views.nota_lista, name='nota_lista'),
    path('notas/crear/', views.nota_crear, name='nota_crear'),
    path('notas/<int:pk>/editar/', views.nota_editar, name='nota_editar'),
    path('notas/<int:pk>/eliminar/', views.nota_eliminar, name='nota_eliminar'),
    
    # Metas
    path('metas/', views.meta_lista, name='meta_lista'),
    path('metas/crear/', views.meta_crear, name='meta_crear'),
    path('metas/<int:pk>/editar/', views.meta_editar, name='meta_editar'),
    path('metas/<int:pk>/eliminar/', views.meta_eliminar, name='meta_eliminar'),
    
    # Mensajes
    path('mensajes/', views.mensaje_lista, name='mensaje_lista'),
    path('mensajes/crear/', views.mensaje_crear, name='mensaje_crear'),
    path('mensajes/<int:pk>/', views.mensaje_ver, name='mensaje_ver'),
    
    # Notificaciones
    path('notificaciones/', views.notificacion_lista, name='notificacion_lista'),
    path('notificaciones/<int:pk>/leer/', views.notificacion_marcar_leida, name='notificacion_marcar_leida'),
    path('notificaciones/leer-todas/', views.notificacion_marcar_todas_leidas, name='notificacion_marcar_todas_leidas'),
]