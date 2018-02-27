from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prospectos'
urlpatterns = [
    path('crear/', views.prospecto_crear, name='crear_prospecto'),

]
