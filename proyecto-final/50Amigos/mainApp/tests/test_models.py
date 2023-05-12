from django.test import TestCase
from mixer.backend.django import mixer
import pytest

from ..models import *


@pytest.mark.django_db
class TestModels(TestCase):
    """
    Clase de prueba encargada de probar todos los modelos de nuestra aplicacion
    """

    def setUp(self):
        self.usuario = User.objects.create(
            username='prueba', email='prueba@50amigos.com', password='password')
        self.categoria = Categoria.objects.create(nombre="categoria prueba 1")
        self.subcategoria = Subcategoria.objects.create(
            nombre="Subcategoria prueba 1", categoria=self.categoria)
        self.helado = Platillo.objects.create(
            nombre="helado", categoria=self.categoria, subcategoria=self.subcategoria, precio="100")
        self.orden = Orden.objects.create(
            usuario=self.usuario, total="100.00", comentarios="Ninguno", active=False, helado_escogido=self.helado)

    def test_categoria_nombre(self):
        categoria = Categoria.objects.get(id=1)
        self.assertEqual(categoria.nombre, self.categoria.nombre)

    def test_subcategoria_nombre(self):
        subcategoria = Subcategoria.objects.get(id=1)
        self.assertEqual(subcategoria.nombre, self.subcategoria.nombre)

    def test_helado(self):
        platillo = Platillo.objects.get(id=1)
        self.assertEqual(platillo.nombre, self.helado.nombre)

    def test_orden(self):
        orden = Orden.objects.get(id=1)
        self.assertEqual(orden.usuario.username, self.usuario.username)
