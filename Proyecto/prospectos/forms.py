from .models import Prospecto, Lugar
from django.forms import ModelForm
from . import models


class ProspectoForm(ModelForm):
    class Meta:
        model = Prospecto
        fields = (
            'Nombre',
            'Apellido_Paterno',
            'Apellido_Materno',
            'Telefono_Casa',
            'Telefono_Celular',
            'Email',
            'Metodo_Captacion',
            'Interes',
            'Estado_Civil',
            'Ocupacion',
            'Hijos',
        )


class LugarForm(ModelForm):
    class Meta:
        model = Lugar
        fields = (
            'Calle',
            'Numero_Interior',
            'Numero_Exterior',
            'Colonia',
            'Ciudad',
            'Estado',
            'Pais',
            'Codigo_Postal',
        )


class FormaActividad(ModelForm):
    class Meta:
        model = models.Actividad
        fields = [
            'nombre',
            'fecha',
            'hora',
            'notas',
        ]
        help_texts = {
            'fecha': 'Para agendar una actividad en un futuro, seleccione la fecha a realizarla.',
            'hora': 'Este campo es opcional.',
        }
