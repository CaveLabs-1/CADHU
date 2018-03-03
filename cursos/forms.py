from django import forms

from .models import Curso

class CursosForm(forms.ModelForm):

    class Meta:
        model = Curso
        fields = ('Nombre', 'Fecha', 'Direccion', 'Descripcion', 'Hora', 'Costo', 'Evento')
        widgets = {
            'Fecha': forms.DateInput(),
            'Hora': forms.TimeInput()

        }
