from django.contrib import admin
from .models import Prospecto, Lugar, Actividad, Empresa, ProspectoGrupo

# Register your models here.
admin.site.register(Prospecto)
admin.site.register(Lugar)
admin.site.register(Actividad)
admin.site.register(Empresa)
admin.site.register(ProspectoGrupo)
