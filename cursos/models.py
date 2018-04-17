from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Curso(models.Model):
    Evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=25, blank=True, null=True)
    Fecha_Inicio = models.DateField(blank=True, null=True)
    Fecha_Fin = models.DateField(blank=True, null=True)
    Direccion = models.CharField(max_length=100, blank=True, null=True)
    Descripcion = models.CharField(max_length=600, blank=True, null=True)
    Costo = models.PositiveIntegerField(blank=True, null=True)
    Activo = models.BooleanField(default=True)
    Encargado = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Nombre
