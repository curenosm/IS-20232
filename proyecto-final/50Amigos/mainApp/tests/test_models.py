from django.test import TestCase
import pytest

from django.contrib.auth.hashers import make_password

from ..models import (
    Platillo,
    Pedido,
    Categoria,
    Subcategoria,
    Orden,
    User,
    Role
)


@pytest.mark.django_db
class TestModels(TestCase):
    """
    Clase de prueba encargada de probar todos los modelos de nuestra aplicacion
    """

    def setUp(self):
        self.user_password = 'password'
        self.usuario = User.objects.create(
            username='prueba',
            email='prueba@50amigos.com',
            password=make_password(self.user_password)
        )
        self.role = Role.objects.create(usuario=self.usuario)
        self.categoria = Categoria.objects.create(
            id=9999,
            nombre="categoria prueba 1")
        self.subcategoria = Subcategoria.objects.create(
            id=9999,
            nombre="Subcategoria prueba 1",
            categoria=self.categoria
        )
        self.helado = Platillo.objects.create(
            id=9999,
            nombre="helado",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            precio="100"
        )
        self.orden = Orden.objects.create(
            id=9999,
            usuario=self.usuario,
            total="100.00",
            comentarios="Ninguno",
            active=False,
            helado_escogido=self.helado
        )
        self.pedido = Pedido.objects.create(
            id=9999,
            orden=self.orden,
            platillo=self.helado,
            cantidad=1
        )

    def test_encrypted_password(self):
        """
        Funcion para probar la contraseña guardada durante el metodo de setup
        se guarde cifrada correctamente en la base de datos.
        """

        assert self.usuario.password != "password"

    def test_categoria_nombre(self):
        """
        Funcion para probar el modelo de las categorias.
        """

        categoria = Categoria.objects.get(id=9999)
        self.assertEqual(categoria.nombre, self.categoria.nombre)

    def test_subcategoria_nombre(self):
        """
        Funcion para probar el modelo de las categorias.
        """

        subcategoria = Subcategoria.objects.get(id=9999)
        self.assertEqual(subcategoria.nombre, self.subcategoria.nombre)

    def test_helado(self):
        """
        Funcion para probar el modelo de los helados.
        """

        platillo = Platillo.objects.get(id=9999)
        self.assertEqual(platillo.nombre, self.helado.nombre)

    def test_orden(self):
        """
        Funcion para probar el modelo de las ordenes.
        """

        orden = Orden.objects.get(id=9999)
        self.assertEqual(orden.usuario.username, self.usuario.username)

    def test_pedido(self):
        """
        Funcion para probar el modelo de los pedidos.
        """

        pedido = Pedido.objects.get(id=9999)
        self.assertEqual(pedido.orden, self.orden)
