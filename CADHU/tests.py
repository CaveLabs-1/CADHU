from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class NoAuthenticationViewTests(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()

    #Acceptance Criteria: 1.1
    def test_1_2(self):
        response = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertRedirects(response, '/login/?next=/prospectos/')


class AuthenticationViewTests(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    #Acceptance Criteria: 1.1
    def test_1_1(self):
        response = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(str(response.context['user']), 'testuser1')

    #Acceptance Criteria: 2.1
    def test_2_1(self):
        response = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.client.logout()
        response = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertRedirects(response, '/login/?next=/prospectos/')
