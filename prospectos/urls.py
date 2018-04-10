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

    # Modificar el estado de terminacion de una Actividad
    path('actividades/terminado/<int:id>', views.estado_actividad, name='estado_actividad'),

    # Lista prospectos activos
    path('', views.lista_prospectos, name='lista_prospectos'),

    # Lista prospectos inactivos
    path('prospectos/inactivo', views.lista_prospectos_inactivo, name='lista_prospectos_inactivo'),

    path('<int:id>/baja_prospecto', views.baja_prospecto, name='baja_prospecto'),

    # Carga masiva de prospectos
    path('carga', views.carga_masiva, name='carga'),

    # Lista empresas
    path('empresas/', views.lista_empresas, name='lista_empresas'),

    # Lista empresas inactivas
    path('empresas/inactivas', views.lista_empresas_inactivo, name='lista_empresas_inactivo'),

    path('<int:id>/baja_empresas', views.baja_empresas, name='baja_empresas'),

    # Informacion de empresa
    path('empresas/empresa_info/<int:id>', views.empresa_info, name='empresa_info'),
    # Crear Prospecto
    path('crear_prospecto', views.crear_prospecto, name='crear_prospecto'),

    # Info prospecto
    path('informacion/<int:id>', views.info_prospecto, name='info_prospecto'),

    # Info curso-prospecto
    path('interes/<int:rel>', views.info_prospecto_curso, name='info_prospecto_curso'),

    # Registrar Cursos a Prospecto
    path('<int:id>/registrar_cursos', views.registrar_cursos, name='registrar_cursos'),

    #Editar Curso del Prospecto
    path('editar_curso/<int:id>', views.editar_curso, name='editar_curso'),

    #Eliminar Curso de Prospecto
    path('eliminar_curso/<int:id>', views.eliminar_curso, name='eliminar_curso'),

    # Editar Prospecto
    path('<int:id>/editar_prospecto', views.editar_prospecto, name='editar_prospecto'),

    # Crear Empresa
    path('crear_empresa', views.crear_empresa, name='crear_empresa'),

    # Editar Empresa
    path('editar_empresa/<int:id>', views.editar_empresa, name='editar_empresa'),

    #Lista de pagos
    path('lista_pagos/<int:idPE>', views.lista_pagos, name='lista_pagos'),

    #Nuevo pago
    path('nuevo_pago/<int:idPE>', views.nuevo_pago, name='nuevo_pago'),

    # Crear Cliente
    path('crear_cliente/<int:id>/', views.crear_cliente, name='crear_cliente'),

    # Editar Cliente
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),

    # Informacion de cliente
    path('clientes/info_cliente/<int:id>', views.info_cliente, name='info_cliente'),

]
