from django.db import models
# from django.contrib.auth.models import User, Curso
# from django.utils import timezone
# import datetime
#
# class Pago(models.Model):
#
#     # cliente
#     curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE)
#     fecha = models.DateField(blank=True, null=True)
#     monto = models.IntegerField(blank=True, null=True)
#     referencia = models.CharField(max_length=25, blank=True, null=True)
#
#     # Evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE)
#     # Nombre = models.CharField(max_length=25, blank=True, null=True)
#     # Fecha = models.DateField(blank=True, null=True)
#     # Direccion = models.CharField(max_length=100, blank=True, null=True)
#     # Descripcion = models.CharField(max_length=150, blank=True, null=True)
#     # Costo = models.PositiveIntegerField(blank=True, null=True)
#     # Activo = models.BooleanField(default=True)
#     # Encargado = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.Nombre
