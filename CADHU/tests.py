from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationViewTests(TestCase):

    def setUp(self):
        usuario1 = User.objects.create_user(username='testuser1', password='12345')
        usuario1.save()

    def test_no_login(self):
        """
        Si no ha iniciado sesión, lo manda a la pantalla de log in.
        """
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertRedirects(response, '/login/?next=/prospectos/crear/')

    def test_login(self):
        """
        Iniciar sesión y comprobar que el usuario está adentro del sistema.
        """
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertEqual(str(response.context['user']), 'testuser1')

    def test_logout(self):
        """
        Inicia sesión, se cierra sesión y se comprueba que la sesión se cerró.
        """
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.client.logout()
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertRedirects(response, '/login/?next=/prospectos/crear/')
