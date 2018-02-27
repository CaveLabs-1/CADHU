from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'prospectos'
urlpatterns = [
    # Lista de actividades
    path('actividades/', views.ListaActividades.as_view(), name='actividades'),
    # Crear actividad
    path('actividades/crear', views.CreaActividad.as_view(), name='crear_actividad'),
    #Lista prospectos
    path('', views.lista_prospecto, name='lista_prospectos'),

]
