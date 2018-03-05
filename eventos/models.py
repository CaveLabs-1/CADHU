from django.db import models

# Create your models here.

class Evento(models.Model):
    Nombre=models.CharField(max_length=100, unique=True)
    Descripcion= models.TextField()

    def __str__(self):
        return self.Nombre

# class Curso(models.Model):
#     Evento = models.ForeignKey('Evento', on_delete=models.CASCADE)
#     Nombre = models.CharField(max_length=25, blank=True, null=True)
#     Fecha = models.DateField(blank=True, null=True)
#     Direccion = models.CharField(max_length=100, blank=True, null=True)
#     Descripcion = models.CharField(max_length=150, blank=True, null=True)
#     Hora = models.TimeField(blank=True, null=True)
#     Costo = models.PositiveIntegerField(blank=True, null=True)
