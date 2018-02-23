from django.forms import ModelForm
from . import models


class FormaActividad(ModelForm):
    class Meta:
        model = models.Actividad
        fields = ['nombre', 'fecha', 'hora', 'notas']
        help_texts = {
            'fecha': 'Para agendar una actividad en un futuro, seleccione la fecha a realizarla.',
            'hora': 'Este campo es opcional.',
        }
