from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prospectos'
urlpatterns = [
    # Lista de actividades para una relación Prospecto - Evento
    path('actividades/<int:pk>/', views.lista_actividades, name='lista_actividades'),

    # Crear actividad para una relación Prospecto - Evento
    path('actividades/crear/<int:pk>/', views.crear_actividad, name='crear_actividad'),

    # Modificar el estado de terminacion de una Actividad
    path('actividades/terminado/<int:pk>', views.estado_actividad, name='estado_actividad'),

    # Modificar el estado de terminacion de una Actividad
    path('flag/<int:pk>', views.estado_flag, name='estado_flag'),

    # Lista prospectos activos
    path('', views.lista_prospectos, name='lista_prospectos'),

    # Lista prospectos inactivos
    path('prospectos/inactivo', views.lista_prospectos_inactivo, name='lista_prospectos_inactivo'),

    path('<int:pk>/baja_prospecto', views.baja_prospecto, name='baja_prospecto'),

    # Carga masiva de prospectos
    path('carga', views.carga_masiva, name='carga'),

    # Lista empresas
    path('empresas/', views.lista_empresas, name='lista_empresas'),

    # Lista empresas inactivas
    path('empresas/inactivas', views.lista_empresas_inactivo, name='lista_empresas_inactivo'),

    path('<int:pk>/baja_empresas', views.baja_empresas, name='baja_empresas'),

    # Informacion de empresa
    path('empresas/empresa_info/<int:pk>', views.empresa_info, name='empresa_info'),

    # Crear Prospecto
    path('crear_prospecto', views.crear_prospecto, name='crear_prospecto'),

    # Info prospecto
    path('informacion/<int:pk>', views.info_prospecto, name='info_prospecto'),

    # Info grupo-prospecto
    path('interes/<int:rel>', views.info_prospecto_grupo, name='info_prospecto_grupo'),

    # Registrar Cursos a Prospecto
    path('<int:pk>/registrar_cursos', views.registrar_cursos, name='registrar_cursos'),

    #Editar Grupo del Prospecto
    path('editar_curso/<int:pk>', views.editar_curso, name='editar_curso'),

    #Eliminar Grupo de Prospecto
    path('eliminar_curso/<int:pk>', views.eliminar_curso, name='eliminar_curso'),

    # Editar Prospecto
    path('<int:pk>/editar_prospecto', views.editar_prospecto, name='editar_prospecto'),

    # Crear Empresa
    path('crear_empresa', views.crear_empresa, name='crear_empresa'),

    # Editar Empresa
    path('editar_empresa/<int:pk>', views.editar_empresa, name='editar_empresa'),

    # Lista de pagos
    path('lista_pagos/<int:id_pe>', views.lista_pagos, name='lista_pagos'),

    # Nuevo pago
    path('nuevo_pago/<int:id_pe>', views.nuevo_pago, name='nuevo_pago'),

    # Crear Cliente
    path('crear_cliente/<int:pk>/', views.crear_cliente, name='crear_cliente'),

    # Editar Cliente
    path('editar_cliente/<int:pk>/', views.editar_cliente, name='editar_cliente'),

    # Informacion de cliente
    path('clientes/info_cliente/<int:pk>', views.info_cliente, name='info_cliente'),

    # Borrar Cliente
    path('baja_cliente/<int:pk>', views.baja_cliente, name='baja_cliente'),

    # Borrar Cliente
    path('eliminar_cliente/<int:pk>', views.eliminar_cliente, name='eliminar_cliente'),

    # Lista clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),

    # Lista clientes inactivas
    path('clientes/inactivos', views.lista_clientes_inactivos, name='lista_clientes_inactivos'),

    #Autorizar Pago
    path('autorizar_pago/<int:pk>', views.autorizar_pago, name='autorizar_pago'),

    #Inscribir prospectos a empresa
    path('empresa/inscribir/<int:pk>',views.inscribir_empresa, name='inscribir_empresa'),
]
