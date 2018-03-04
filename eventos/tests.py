from django.test import TestCase
from eventos.models import Evento
from django.urls import reverse
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

    def test_Descripcion_label(self):
        evento=Evento.objects.get(id=1)
        field_label = evento._meta.get_field('Descripcion').verbose_name
        self.assertEquals(field_label,'Descripcion')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/eventos/new')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/eventos/new')
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'eventos/crear_evento.html')
    # def test_get_absolute_url(self):
    #     evento = Evento.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEquals(evento.get_absolute_url(), '/eventos/1')
