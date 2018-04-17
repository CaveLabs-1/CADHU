from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import nuevo_curso, cursos, eliminar_grupo, info_grupo, editar_grupo

app_name = 'cursos'
urlpatterns = [
    # path('nuevo_curso', views.CreaCurso.as_view(), name= 'nuevo_curso'),

    #Crear nuevo grupo
    path('nuevo_curso', nuevo_curso, name='nuevo_curso'),

    #Lista de grupos
    path('lista_cursos', cursos, name='cursos'),

    #Eliminar un grupo
    path('eliminar_grupo/<int:id>', eliminar_grupo, name='eliminar_grupo'),

    #Editar un grupo
    path('editar_grupo/<int:id>', editar_grupo, name='editar_grupo'),

    # Informacion de un curso
    path('<int:id>/info', info_grupo, name='info_grupo'),
]
