from django import forms

from .models import Curso

# class CursosForm(forms.ModelForm):
#
#     class Meta:
#         model = Curso
#         fields = ('Nombre', 'Evento', 'Fecha', 'Direccion', 'Descripcion', 'Hora', 'Costo')
#         widgets = {
#             'Fecha': forms.DateInput(),
#             'Hora': forms.TimeInput()
#
#         }

class FormaCurso(forms.ModelForm):

    class Meta:
        model = Curso
        fields = [
            'Nombre',
            'Evento',
            'Fecha',
            'Direccion',
            'Descripcion',
            # 'Hora',
            'Costo',
        ]
        widgets = {
            'Fecha': forms.DateInput(),
            # 'Hora': forms.TimeInput()

        }
