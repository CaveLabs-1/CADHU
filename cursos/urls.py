from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import nuevo_curso, cursos, eliminar_grupo

app_name = 'cursos'
urlpatterns = [
    # path('nuevo_curso', views.CreaCurso.as_view(), name= 'nuevo_curso'),
    path('nuevo_curso', nuevo_curso, name='nuevo_curso'),
    path('lista_cursos', cursos, name='cursos'),
    path('eliminar_grupo/<int:id>', eliminar_grupo, name='eliminar_grupo'),
]
