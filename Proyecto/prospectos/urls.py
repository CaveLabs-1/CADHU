from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import lista_prospecto

app_name = 'prospectos'
urlpatterns = [
    path('', lista_prospecto, name='lista_prospectos'),
] 
