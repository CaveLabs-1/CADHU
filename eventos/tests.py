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
        self.test_eventoinstance1=Evento.objects.create(Nombre='test_taller',Descripcion='Creacion de test de eventos')


    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')

    #Prueba que la url para crear evento exista.
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/eventos/crear_evento')
        self.assertEqual(resp.status_code, 200)
    #Prueba que se utilice el template sea el correcto.
    def test_view_uses_correct_template(self):
        resp = self.client.get('/eventos/crear_evento')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'eventos/crear_evento.html')
    #Prueba que el post a la base de datos sea correcto.
    def test_view_crear_evento(self):
        resp = self.client.post('/eventos/crear_evento',  {'Nombre':'Taller prueba', 'Desctipcion':'Este es el evento de pruebas automoatizadas.'},follow=True )
        self.assertEqual(resp.status_code, 200)