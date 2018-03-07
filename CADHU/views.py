from django.http import HttpResponseRedirect
from django.urls import reverse

def redireccionar(request):
        return HttpResponseRedirect(reverse('login'))
