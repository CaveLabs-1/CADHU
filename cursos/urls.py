from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'cursos'
urlpatterns = [
    # path('nuevo_curso', views.CreaCurso.as_view(), name= 'nuevo_curso'),
    path('nuevo_curso', views.nuevo_curso, name= 'nuevo_curso'),
    path('lista_cursos', views.cursos, name= 'cursos'),
]
