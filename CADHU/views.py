from django.http import HttpResponseRedirect
from django.urls import reverse

def redireccionar(request):
        #Redireccionar la liga principal al login.
        return HttpResponseRedirect(reverse('login'))
