from django.shortcuts import render

from .models import Prospecto, Lugar

from .forms import ProspectoForm, LugarForm

# Create your views here.
def prospecto_crear(request):
    context = {}
    NewProspectoForm = ProspectoForm()
    NewLugarForm = LugarForm()

    if request.method == 'POST':
        NewProspectoForm = ProspectoForm(request.POST)
        NewLugarForm = LugarForm(request.POST)
        ProspectoValid = NewProspectoForm.is_valid()
        LugarValid = NewLugarForm.is_valid()

        if ProspectoValid and LugarValid:
            Lugar = NewLugarForm.save()
            Prospecto = NewProspectoForm.save(commit = False)
            Prospecto.Direccion = Lugar
            Prospecto.save()
            return prospecto_lista(request)

    context = {
        'NewProspectoForm' = NewProspectoForm,
        'NewLugarForm' = NewLugarForm,
    }
    return render(request, 'prospecto/prospecto_form.html', context)

def prospecto_lista(request):
    context = {}
    return render(request, 'prospecto/prospecto_lista.html',context)

