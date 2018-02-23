from django.db import models

# Create your models here.


class Actividad(models.Model):
    Id_Seguimiento = models.ForeignKey()
    nombre = models.CharField(verbose_name='Actividad')
    fecha = models.DateField(verbose_name='Fecha de la actividad')
    hora = models.TimeField(verbose_name='Hora de la actividad')
    notas = models.CharField(verbose_name='Notas de la actividad')
    vendedor = models.ForeignKey()
