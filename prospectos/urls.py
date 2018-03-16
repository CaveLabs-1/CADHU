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

    # Lista prospectos activos
    path('', views.lista_prospectos, name='lista_prospectos'),

    # Lista prospectos inactivos
    path('inactivo', views.lista_prospectos_inactivo, name='lista_prospectos_inactivo'),

    path('<int:id>/baja_prospecto', views.baja_prospecto, name='baja_prospecto'),

    # Carga masiva de prospectos
    path('carga', views.carga_masiva, name='carga'),

    # Lista empresas
    path('empresas/', views.lista_empresa, name='lista_empresas'),

    # Crear Prospecto
    path('crear_prospecto', views.crear_prospecto, name='crear_prospecto'),

    # Registrar Cursos a Prospecto
    path('<int:id>/registrar_cursos', views.registrar_cursos, name='registrar_cursos'),

    # Editar Prospecto
    path('editar_prospecto/<int:id>/', views.editar_prospecto, name='editar_prospecto'),

    # Crear Empresa
    path('crear_empresa/', views.crear_empresa, name='crear_empresa'),

]
