from django.db import models

# Create your models here.
class Prospecto(models.Model):
    Nombre = models.Charfield(
        max_length=50,
        blank=False,
        null=False,
    )

    Apellido_Paterno = models.Charfield(
        max_length=50,
        blank=False,
        null=False,
    )

    Apellido_Materno = models.Charfield(
        max_length=50,
        blank=False,
        null=False,
    )

    Telefono_Casa = PhoneNumberField(
        blank=True,
        null=True,
    )

    Telefono_Celular = PhoneNumberField(
        blank=True,
        null=True,
    )

    Email = models.Charfield(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )

    Direccion = models.ForeignKey(
        'Lugar',
        on_delete=models.CASCADE,
    )

    Metodo_Captacion = models.Charfield(
        max_length=50,
        blank=True,
        null=True,
    )

    Interes = models.Charfield(
        max_length=50,
        blank=True,
        null=True,
    )

    Estado_Civil = models.Charfield(
        max_length=15,
        blank=True,
        null=True,
    )

    Ocupacion = models.Charfield(
        max_length=15,
        blank=True,
        null=True,
    )

    Hijos = models.BooleanField(
        default=False,
    )

    def  __str__(self):
        return self.Nombre +' '+ self.Apellido_Paterno +' '+ self.Apellido_Materno

class Lugar(models.Model):
    Calle = models.Charfield(
        max_length=50,
        blank=True,
        null=True,
    )

    Numero_Interior = PositiveIntegerField(
        blank=True,
        null=True,
    )

    Numero_Exterior = PositiveIntegerField(
        blank=True,
        null=True,
    )

    Colonia = models.Charfield(
        max_length=50,
        blank=True,
        null=True,
    )

    Ciudad = models.Charfield(
        max_length=50,
        blank=True,
        null=True,
    )

    Estado = models.Charfield(
        max_length=50,
        blank=True,
        null=True,
    )

    Pais = models.Charfield(
        max_length=50,
        blank=True,
        null=True,
    )

    Codigo_Postal = models.Charfield(
        max_length=5,
        blank=True,
        null=True,
    )
