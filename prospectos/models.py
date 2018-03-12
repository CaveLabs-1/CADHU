from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import datetime
from cursos.models import Curso

# Create your models here.

METODO_CAPTACION = (
    ('Facebook', 'Facebook'),
    ('Buscador', 'Buscador'),
    ('Sitio Web', 'Sitio Web'),
    ('Email', 'Email'),
    ('Triptico/Cartel', 'Triptico/Cartel'),
    ('Radio', 'Radio'),
    ('Recomendacion', 'Recomendacion'),
    ('Otro', 'Otro'),
)

TIPOS_INTERES = (
    ('BAJO', 'BAJO'),
    ('MEDIO', 'MEDIO'),
    ('ALTO', 'ALTO'),
    ('MUY ALTO', 'MUY ALTO'),
)

ESTADO_CIVIL = (
    ('SOLTERO', 'SOLTERO'),
    ('CASADO', 'CASADO'),
    ('DIVORCIADO', 'DIVORCIADO'),
    ('UNION LIBRE', 'UNION LIBRE'),
)

class Empresa(models.Model):
    Nombre = models.CharField(max_length=50, blank=False, null=False)
    Telefono = PhoneNumberField(blank=True, null=True)
    Email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    Direccion = models.ForeignKey('Lugar', on_delete=models.CASCADE)
    Razon_Social = models.CharField(max_length=50, blank=False, null=True)

class Prospecto(models.Model):
    Nombre = models.CharField(max_length=50, blank=False, null=False)
    Apellido_Paterno = models.CharField(max_length=50, blank=False, null=False)
    Apellido_Materno = models.CharField(max_length=50, blank=False, null=False)
    Telefono_Casa = PhoneNumberField(blank=True, null=True)
    Telefono_Celular = PhoneNumberField(blank=True, null=True)
    Email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    Direccion = models.ForeignKey('Lugar', on_delete=models.CASCADE)
    Metodo_Captacion = models.CharField(max_length=50, blank=True, null=True, choices=METODO_CAPTACION)
    Estado_Civil = models.CharField(max_length=15, blank=True, null=True, choices=ESTADO_CIVIL)
    Ocupacion = models.CharField(max_length=15, blank=True, null=True)
    Hijos = models.PositiveIntegerField(blank=True, null=True, default=0)
    Recomendacion = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.Nombre + ' ' + self.Apellido_Paterno + ' ' + self.Apellido_Materno


class Lugar(models.Model):
    Calle = models.CharField(max_length=50, blank=True, null=True)
    Numero_Interior = models.CharField(max_length=6, blank=True, null=True)
    Numero_Exterior = models.CharField(max_length=6, blank=True, null=True)
    Colonia = models.CharField(max_length=50, blank=True, null=True)
    Ciudad = models.CharField(max_length=50, blank=True, null=True)
    Estado = models.CharField(max_length=50, blank=True, null=True)
    Pais = models.CharField(max_length=50, blank=True, null=True, )
    Codigo_Postal = models.CharField(max_length=5, blank=True, null=True)


class Actividad(models.Model):
    # Id_Seguimiento es la relacion Prospecto evento
    # Id_Seguimiento =
    titulo = models.CharField(verbose_name='Actividad', max_length=500)
    fecha = models.DateField(verbose_name='Fecha de la actividad')
    hora = models.TimeField(verbose_name='Hora de la actividad', blank=True, null=True)
    notas = models.CharField(verbose_name='Notas de la actividad', max_length=4000, blank=True, null=True)
    # vendedor = fk

    def __str__(self):
        return self.titulo

    def agenda_futuro(self):
        ahora = timezone.now()
        return ahora - datetime.timedelta(days=1) <= datetime.datetime.combine(self.fecha, self.hora) <= ahora

    def agenta_pasado(self):
        ahora = timezone.now()
        return ahora + datetime.timedelta(days=1) <= datetime.datetime.combine(self.fecha, self.hora) <= ahora


class ProspectoEvento(models.Model):
    Prospecto = models.ForeignKey(Prospecto, on_delete=models.CASCADE, null=True)
    Curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    Fecha = models.DateField(null=True, blank=True)
    Interes = models.CharField(max_length=50, blank=True, null=True, choices=TIPOS_INTERES)
    FlagCADHU = models.NullBooleanField(default=False, null=True, verbose_name='Bandera de interes')