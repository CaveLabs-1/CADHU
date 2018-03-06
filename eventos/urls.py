from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import lista_evento, crear_evento

app_name = 'eventos'
urlpatterns = [
    path('', lista_evento, name='lista_eventos'),
    path('crear_evento', crear_evento, name= 'crear_eventos'),
    # path('update', update_evento, name='update_evento'),
    # path('delete', eliminar_evento, name='eliminar_evento'),
]
