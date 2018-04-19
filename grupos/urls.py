from django.urls import path
from .views import nuevo_grupo, grupos, eliminar_grupo, info_grupo, editar_grupo, grupos_inactivos

app_name = 'grupos'
urlpatterns = [
    # Lista de grupos
    path('', grupos, name='grupos'),

    # Lista de grupos
    path('inactivos', grupos_inactivos, name='grupos_inactivos'),

    # Crear nuevo grupo
    path('nuevo_grupo', nuevo_grupo, name='nuevo_grupo'),

    # Editar un grupo
    path('editar_grupo/<int:pk>', editar_grupo, name='editar_grupo'),

    # Eliminar un grupo
    path('eliminar_grupo/<int:pk>', eliminar_grupo, name='eliminar_grupo'),

    # Informacion de un grupo
    path('<int:pk>/info', info_grupo, name='info_grupo'),
]
