import pytest

from django.test import TestCase


from ..models import (
    Anuncio,
    Carrito,
    Categoria,
    Cupon,
    Orden,
    Pedido,
    Platillo,
    Promocion,
    Role,
    Subcategoria,
    User,
)

from .test_data import (
    create_test_data
)


@pytest.mark.django_db
class TestModels(TestCase):
    """
    Clase de prueba encargada de probar todos los modelos de nuestra aplicacion
    """

    def setUp(self):
        """
        Función que se ejecuta antes de cada prueba unitaria.
        """

        [
            self.user,
            self.categoria,
            self.subcategoria,
            self.platillo,
            self.role,
            self.orden,
            self.pedido,
            self.carrito,
            self.promocion,
            self.cupon,
            self.anuncio
        ] = create_test_data()

        self.id_prueba = 9999

    def test_encrypted_password(self):
        """
        Función para probar la contraseña guardada durante el metodo de setup
        se guarde cifrada correctamente en la base de datos.
        """

        assert self.user.password != "password"

    def test_categoria_nombre(self):
        """
        Función para probar el modelo de las categorias.
        """

        categoria = Categoria.objects.get(id=self.id_prueba)
        self.assertEqual(categoria.nombre, self.categoria.nombre)

    def test_subcategoria_nombre(self):
        """
        Función para probar el modelo de las categorias.
        """

        subcategoria = Subcategoria.objects.get(id=self.id_prueba)
        self.assertEqual(subcategoria.nombre, self.subcategoria.nombre)

    def test_helado(self):
        """
        Función para probar el modelo de los helados.
        """

        platillo = Platillo.objects.get(id=self.id_prueba)
        self.assertEqual(platillo.nombre, self.platillo.nombre)

    def test_orden(self):
        """
        Función para probar el modelo de las ordenes.
        """

        orden = Orden.objects.get(id=self.id_prueba)
        self.assertEqual(orden.usuario.username, self.user.username)

    def test_pedido(self):
        """
        Función para probar el modelo de los pedidos.
        """

        pedido = Pedido.objects.get(id=self.id_prueba)
        self.assertEqual(pedido.orden, self.orden)

    def test_anuncio(self):
        """
        Función para probar el modelo de los anuncios.
        """

        anuncio = Anuncio.objects.get(id=self.id_prueba)
        self.assertEqual(anuncio, self.anuncio)

    def test_user(self):
        """
        Función para probar el modelo de los usuarios.
        """

        user = User.objects.get(id=self.id_prueba)
        self.assertEqual(user, self.user)

    def test_role(self):
        """
        Función para probar el modelo de los roles.
        """

        role = Role.objects.get(id=self.id_prueba)
        self.assertEqual(role, self.role)

    def test_promocion(self):
        """
        Función para probar el modelo de las promociones.
        """

        promocion = Promocion.objects.get(id=self.id_prueba)
        self.assertEqual(promocion, self.promocion)

    def test_cupon(self):
        """
        Función para probar el modelo de los cupones de descuento.
        """

        cupon = Cupon.objects.get(id=self.id_prueba)
        self.assertEqual(cupon, self.cupon)

    def test_carrito(self):
        """
        Función para probar el modelo del carrito de compras.
        """

        carrito = Carrito.objects.get(id=self.id_prueba)
        self.assertEqual(carrito, self.carrito)
