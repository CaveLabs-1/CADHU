from django.test import TestCase
from eventos.models import Evento
from django.urls import reverse
from django.contrib.auth.models import User, Group
# Create your tests here.

class EventoModelTest(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/eventos/nuevo_evento')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/eventos/nuevo_evento')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'eventos/crear_evento.html')

    # def test_get_absolute_url(self):
    #     evento = Evento.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEquals(evento.get_absolute_url(), '/eventos/1')
