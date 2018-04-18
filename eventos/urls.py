from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import lista_cursos, crear_curso, eliminar_curso, editar_curso

app_name = 'eventos'
urlpatterns = [
    path('', lista_cursos, name='lista_cursos'),
    path('crear_curso', crear_curso, name= 'crear_curso'),
    path('eliminar_curso/<int:id>', eliminar_curso, name='eliminar_curso'),
    path('editar_curso/<int:id>', editar_curso, name='editar_curso'),
]
