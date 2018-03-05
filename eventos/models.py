from django.db import models

# Create your models here.

class Evento(models.Model):
    Nombre = models.CharField(max_length=100, unique=True)
    Descripcion = models.TextField()

    def __str__(self):
        return self.Nombre