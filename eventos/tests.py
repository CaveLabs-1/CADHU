from django.test import TestCase
from eventos.models import Evento
# Create your tests here.

class EventoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')

    def test_Nombre_label(self):
        evento=Evento.objects.get(id=1)
        field_label = evento._meta.get_field('Nombre').verbose_name
        self.assertEquals(field_label,'Nombre')

    # def test_get_absolute_url(self):
    #     evento = Evento.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEquals(evento.get_absolute_url(), '/eventos/1')