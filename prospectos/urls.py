from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prospectos'
urlpatterns = [
    # Lista de actividades
    path('actividades/', views.ListaActividades.as_view(), name='actividades'),

    # Crear actividad
    path('actividades/crear', views.crearActividad, name='crear_actividad'),

    #Lista prospectos
    path('', views.lista_prospecto, name='lista_prospectos'),

    #Lista empresas
    path('empresas/', views.lista_empresa, name='lista_empresas'),

    #Crear Prospecto
    path('crear/', views.prospecto_crear, name='crear_prospecto'),

    #Crear Empresa
    path('empresa_crear/', views.empresa_crear, name='empresa_crear'),

]
