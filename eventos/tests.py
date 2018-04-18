from django.test import TestCase
from .models import Curso
from cursos.models import Curso as Grupo
from django.urls import reverse
from django.contrib.auth.models import User, Group
# Create your tests here.

class CursoModelTest(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        self.usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        self.usuario1.save()
        login = self.client.login(username='testuser1', password='12345')


    #Prueba que la url para lista curso exista.
    def test_view_url_exists_lista_curso(self):
        resp = self.client.get('/eventos/')
        self.assertEqual(resp.status_code, 200)

    #Prueba que se utilice el template sea el correcto.
    def test_view_uses_correct_template_lista_curso(self):
        resp = self.client.get(reverse('eventos:lista_cursos'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'eventos/cursos.html')

    #Prueba que la url para crear curso exista.
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/eventos/crear_curso')
        self.assertEqual(resp.status_code, 200)

    #Prueba que se utilice el template sea el correcto.
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('eventos:crear_curso'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'eventos/crear_curso.html')

    #Prueba que el post a la base de datos sea correcto.
    def test_view_crear_curso(self):
        resp = self.client.post(reverse('eventos:crear_curso'), {
            'nombre': 'Taller',
            'descripcion': 'Este es el curso de pruebas automoatizadas.'})
        self.assertEqual(resp.status_code, 302)
        cant= Curso.objects.count()
        self.assertEqual(cant,1)

    #ACCEPTANCE CRITERIA 33.1 33.2
    def test_view_editar(self):
        curso = Curso.objects.create(
            id=1,
            nombre='Descodificación',
            descripcion='DBI'
        )
        resp = self.client.post(reverse('eventos:editar_curso', kwargs={'id': curso.id}), {
            'nombre': 'Taller', 'descripcion': 'Este es el curso de pruebas automoatizadas.'
            },follow=True)
        actualizado = Curso.objects.get(id=curso.id)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(actualizado, 'Descodificación')

class BorrarCursoTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.curso = Curso.objects.create(nombre='Curso 1', descripcion='Curso para desactivar')
        cls.curso2 = Curso.objects.create(nombre='Curso 2', descripcion='Curso para borrar')
        cls.grupo = Grupo.objects.create(Nombre='Curso', Evento= cls.curso, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16', Direccion='Calle', Descripcion='Curso de marzo', Costo=1000)

    def test_ac_35_1(self):
        resp = self.client.get(reverse('eventos:eliminar_curso', kwargs={'id': self.curso2.id}))
        deleted_event = Curso.objects.filter(nombre="Curso 2").count()
        self.assertEqual(deleted_event, 0)

    def test_ac_35_2(self):
        resp = self.client.get(reverse('eventos:eliminar_curso', kwargs={'id': self.curso.id}))
        curso_actualizado = Curso.objects.get(id=self.curso.id)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(curso_actualizado.activo, False)
