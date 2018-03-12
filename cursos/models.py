from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import datetime

class Curso(models.Model):
    Evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=25, blank=True, null=True)
    Fecha = models.DateField(blank=True, null=True)
    Direccion = models.CharField(max_length=100, blank=True, null=True)
    Descripcion = models.CharField(max_length=150, blank=True, null=True)
    Costo = models.PositiveIntegerField(blank=True, null=True)
    Activo = models.BooleanField(default=True)
