from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prospectos'
urlpatterns = [
    # Lista de actividades para una relación Prospecto - Evento
    path('actividades/<int:id>/', views.lista_actividades, name='lista_actividades'),

    # Crear actividad para una relación Prospecto - Evento
    path('actividades/crear/<int:id>/', views.crear_actividad, name='crear_actividad'),

    #Lista prospectos
    path('', views.lista_prospectos, name='lista_prospectos'),

    # Carga masiva
    path('carga', views.carga_masiva, name='carga'),

    #Lista empresas
    path('empresas/', views.lista_empresa, name='lista_empresas'),

    #ID_US32 Crear Prospecto
    path('crear_prospecto', views.crear_prospecto, name='crear_prospecto'),

    # Editar Prospecto
    path('editar_prospecto/<int:id>/', views.editar_prospecto, name='editar_prospecto'),

    #Crear Empresa
    path('crear_empresa/', views.crear_empresa, name='crear_empresa'),

]
