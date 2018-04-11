from .models import Evento
from django import forms

#ID US32 Forma
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = (
            'Nombre',
            'Descripcion',
            'Activo'
        )
