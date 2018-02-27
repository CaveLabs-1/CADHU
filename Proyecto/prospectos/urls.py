from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import lista_prospecto

app_name = 'prospectos'
urlpatterns = [
    # Lista de actividades
    path('actividades/', views.ListaActividades.as_view(), name='actividades'),
    # Crear actividad
    path('actividades/crear', views.CreaActividad.as_view(), name='crear_actividad'),

    path('', lista_prospecto, name='lista_prospectos'),

]
