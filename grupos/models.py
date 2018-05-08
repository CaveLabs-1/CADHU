from django.db import models
from django.contrib.auth.models import User
from cursos.models import Curso
from django.utils import timezone
import datetime


class Grupo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=600, blank=True, null=True)
    costo = models.PositiveIntegerField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    encargado = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
