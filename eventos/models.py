from django.db import models
from cursos.models import Curso

# Create your models here.

class Evento(models.Model):
    Nombre = models.CharField(max_length=100, unique=True)
    Descripcion = models.TextField()
    Activo = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.Nombre
