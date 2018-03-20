from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'clientes'
urlpatterns = [
    # path('lista_pagos/<int:id>/', views.lista_pagos, name='lista_pagos'),
    # path('nuevo_pago', views.nuevo_pago, name='nuevo_pago'),
]
