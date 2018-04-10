from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'eventos'
urlpatterns = [
    path('', views.lista_evento, name='lista_evento'),
    path('crear_evento', views.crear_evento, name= 'crear_evento'),
    path('editar_evento/<int:id>', views.editar_evento, name='editar_evento'),
    # path('delete', eliminar_evento, name='eliminar_evento'),
]
