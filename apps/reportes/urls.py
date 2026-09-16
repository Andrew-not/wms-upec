from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.reportes_inicio, name='inicio'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar/word/', views.exportar_word, name='exportar_word'),
]