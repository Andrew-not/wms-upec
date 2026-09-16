from django.urls import path
from . import views

app_name = 'servicio'

urlpatterns = [
    path('', views.servicio_inicio, name='servicio_inicio'),
]