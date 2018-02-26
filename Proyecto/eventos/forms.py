from .models import Evento
from django import forms

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = (
            'Nombre',
            'Descripcion',

        )