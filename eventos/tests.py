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

    #Prueba que la url para crear evento exista.
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/eventos/crear_evento')
        self.assertEqual(resp.status_code, 200)
    #Prueba que se utilice el template sea el correcto.
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('eventos:crear_evento'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'eventos/crear_evento.html')

    #Prueba que el post a la base de datos sea correcto.
    def test_view_crear_evento(self):
        resp = self.client.post(reverse('eventos:crear_evento'), {
            'Nombre': 'Taller',
            'Descripcion': 'Este es el evento de pruebas automoatizadas.'})
        self.assertEqual(resp.status_code, 302)
        cant= Evento.objects.count()
        self.assertEqual(cant,1)

    # def test_ac_13_2(self):
    #     resp = self.client.post(reverse('prospectos:empresa_crear'), {
    #         'Nombre': 'ITESM',
    #         'Telefono': '+524422232226',
    #         'Email': 'correo@itesm.com',
    #         'Razon_Social': 'Escuela'})
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertQuerysetEqual(resp.context['empresas'], ['<Empresa: ITESM>'])