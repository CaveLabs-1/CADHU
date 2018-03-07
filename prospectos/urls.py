from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prospectos'
urlpatterns = [
    # Lista de actividades
    path('actividades/<int:id>/', views.lista_actividades, name='lista_actividades'),

    # Crear actividad
    path('actividades/<int:id>/crear', views.crear_actividad, name='crear_actividad'),

    #Lista prospectos
    path('', views.lista_prospectos, name='lista_prospectos'),

    #Lista empresas
    path('empresas/', views.lista_empresa, name='lista_empresas'),

    #Crear Prospecto
    path('crear_prospecto', views.crear_prospecto, name='crear_prospecto'),

    # Editar Prospecto
    path('editar_prospecto/<int:id>/', views.editar_prospecto, name='editar_prospecto'),

    #Crear Empresa
    path('empresa_crear/', views.empresa_crear, name='empresa_crear'),

]
