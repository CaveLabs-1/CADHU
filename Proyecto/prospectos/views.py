from django.shortcuts import render
from .models import Prospecto, Lugar, Actividad
from django.views import generic
from .forms import FormaActividad, ProspectoForm, LugarForm

def lista_prospecto(request):
    prospectos = Prospecto.objects.all()
    return render(request, 'prospectos/prospectos.html', {'prospectos':prospectos})

# Create your views here.
# def prospecto_crear(request):
#    context = {}
#    NewProspectoForm = ProspectoForm()
#    NewLugarForm = LugarForm()
#
#   if request.method == 'POST':
#        NewProspectoForm = ProspectoForm(request.POST)
#        NewLugarForm = LugarForm(request.POST)
#
#        if NewProspectoForm.is_valid() and NewLugarForm.is_valid():
#            Lugar = NewLugarForm.save()
#            Prospecto = NewProspectoForm.save(commit = False)
#            Prospecto.Direccion = Lugar
#            Prospecto.save()
#            return prospecto_lista(request)
#
#    context = {
#        'NewProspectoForm' = NewProspectoForm,
#        'NewLugarForm' = NewLugarForm,
#    }
#    return render(request, 'prospecto/prospecto_form.html', context)
#

# def prospecto_lista(request):
#    context = {}
#    return render(request, 'prospecto/prospecto_lista.html',context)
#


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
