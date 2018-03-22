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

    # Lista prospectos
    path('', views.lista_prospectos, name='lista_prospectos'),

    # Carga masiva de prospectos
    path('carga', views.carga_masiva, name='carga'),

    # Lista empresas
    path('empresas/', views.lista_empresa, name='lista_empresas'),

    # Crear Prospecto
    path('crear_prospecto', views.crear_prospecto, name='crear_prospecto'),

    # Registrar Curso a Prospecto
    path('<int:id>/registrar_cursos', views.registrar_cursos, name='registrar_cursos'),

    #Editar Curso del Prospecto
    path('editar_curso/<int:id>', views.editar_curso, name='editar_curso'),

    #Eliminar Curso de Prospecto
    path('eliminar_curso/<int:id>', views.eliminar_curso, name='eliminar_curso'),

    # Editar Prospecto
    path('editar_prospecto/<int:id>/', views.editar_prospecto, name='editar_prospecto'),

    # Crear Empresa
    path('crear_empresa/', views.crear_empresa, name='crear_empresa'),

    # Crear Cliente
    path('crear_cliente/<int:id>/', views.crear_cliente, name='crear_cliente'),

]
