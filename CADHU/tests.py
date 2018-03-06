from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class NoAuthenticationViewTests(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()


    def test_no_login(self):
        """
        Si no ha iniciado sesión, lo manda a la pantalla de log in.
        """
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertRedirects(response, '/login/?next=/prospectos/crear_prospecto')


class AuthenticationViewTests(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    def test_login(self):
        """
        Iniciar sesión y comprobar que el usuario está adentro del sistema.
        """
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertEqual(str(response.context['user']), 'testuser1')

    def test_logout(self):
        """
        Inicia sesión, se cierra sesión y se comprueba que la sesión se cerró.
        """
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.client.logout()
        response = self.client.get(reverse('prospectos:crear_prospecto'))
        self.assertRedirects(response, '/login/?next=/prospectos/crear_prospecto')
