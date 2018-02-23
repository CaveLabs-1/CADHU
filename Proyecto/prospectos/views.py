from django.shortcuts import render
from .models import Actividad
from django.views import generic
from .forms import FormaActividad

# Create your views here.


class CreaActividad(generic.CreateView):
    model = Actividad
    form_class = FormaActividad
    template_name = ''

    def get_success_url(self):
        return render(request, '')

    def get_context_data(self, **kwargs):
        context = super(CreaActividad, self).get_context_data(**kwargs)
        context['titulo'] = 'Agregar actividad.'
        return context
