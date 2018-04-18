from django.db import models

# Create your models here.

class Curso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=300, blank=True)
    activo = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.nombre
