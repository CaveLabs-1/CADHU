from django.test import TestCase
from .models import Curso
from grupos.models import Grupo
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

    # Prueba que la url para lista grupo exista.
    def test_view_url_exists_lista_curso(self):
        resp = self.client.get('/cursos/')
        self.assertEqual(resp.status_code, 200)

    # Prueba que se utilice el template sea el correcto.
    def test_view_uses_correct_template_lista_curso(self):
        resp = self.client.get(reverse('cursos:lista_cursos'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cursos/cursos.html')

    #Prueba que la url para crear grupo exista.
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/cursos/crear_curso')
        self.assertEqual(resp.status_code, 200)

    #Prueba que se utilice el template sea el correcto.
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('cursos:crear_curso'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cursos/form_curso.html')

    #Prueba que el post a la base de datos sea correcto.
    def test_view_crear_curso(self):
        resp = self.client.post(reverse('cursos:crear_curso'), {
            'nombre': 'Taller',
            'descripcion': 'Este es el grupo de pruebas automoatizadas.'})
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
        resp = self.client.post(reverse('cursos:editar_curso', kwargs={'pk': curso.id}), {
            'nombre': 'Taller', 'descripcion': 'Este es el grupo de pruebas automoatizadas.'
            },follow=True)
        actualizado = Curso.objects.get(pk=curso.id)
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
        cls.grupo = Grupo.objects.create(nombre='Grupo', curso=cls.curso, fecha_inicio='2018-03-16',
                                         fecha_fin='2018-03-16', direccion='Calle', descripcion='Grupo de marzo', costo=1000)

    def test_ac_35_1(self):
        resp = self.client.get(reverse('cursos:eliminar_curso', kwargs={'pk': self.curso2.id}))
        deleted_event = Curso.objects.filter(nombre="Curso 2").count()
        self.assertEqual(deleted_event, 0)

    def test_ac_35_2(self):
        resp = self.client.get(reverse('cursos:eliminar_curso', kwargs={'pk': self.curso.id}))
        curso_actualizado = Curso.objects.get(pk=self.curso.id)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(curso_actualizado.activo, False)
