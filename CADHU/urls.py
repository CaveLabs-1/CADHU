"""CADHU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/',  admin.site.urls),
    path('', views.index, name='index'),
    #Ligas del login, logout, reset password.
    #ID: US1
    path('', include('django.contrib.auth.urls')),
    path('prospectos/', include('prospectos.urls', namespace='prospectos')),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('eventos/', include('eventos.urls', namespace='eventos')),
    path('cursos/', include('cursos.urls', namespace='cursos')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
