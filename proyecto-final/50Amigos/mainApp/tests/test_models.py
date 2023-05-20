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
    PLATILLOS,
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
        self.assertEqual(pedido.carrito.orden, self.orden)

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


class TestModelString(TestCase):
    """
    Clase para probar los metodos __str__ de los modelos
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

    def test_platillo_get_ingredientes_list_empty(self):
        """
        Prueba unitaria para verificar que un platillo sin ingredientes
        devuelva una lista vacía en cado de llamar al método
        get_ingredientes_list.
        """

        platillo = Platillo.objects.filter(**PLATILLOS[-1])[0]
        assert len(platillo.get_ingredientes_list()) == 0

    def test_platillo_get_ingredientes_list__not_empty(self):
        """
        Prueba unitaria para verificar que un platillo sin ingredientes
        devuelva una lista vacía en cado de llamar al método
        get_ingredientes_list.
        """

        platillo = Platillo.objects.filter(**PLATILLOS[0])[0]
        assert len(platillo.get_ingredientes_list()) != 0

    def test_platillo_enabled_if_not_helado(self):
        """
        Prueba unitaria para verificar que los botones de mas/menos y
        agregar al carrito se deshabiliten si el platillo es un helado.
        """

        platillo = Platillo.objects.filter(**PLATILLOS[0])[0]
        assert platillo.disabled_if_helado() == ''

    def test_platillo_disabled_if_helado(self):
        """
        Prueba unitaria para verificar que los botones de mas/menos y
        agregar al carrito se deshabiliten si el platillo es un helado.
        """

        platillo = Platillo.objects.filter(**PLATILLOS[-1])[0]
        assert platillo.disabled_if_helado() == 'disabled'

    def test_pedido_subtotal(self):
        """
        Prueba unitaria para el subtotal de un pedido de cantidad n
        """

        assert self.pedido.get_subtotal() == '100.00'

    def test_user_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo User
        """

        assert 'Username: ' in str(self.user)
        assert 'First name: ' in str(self.user)
        assert 'Last name: ' in str(self.user)
        assert 'Email: ' in str(self.user)

    def test_categoria_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Categoria
        """

        assert 'Id: ' in str(self.categoria)
        assert 'Nombre: ' in str(self.categoria)

    def test_subcategoria_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Subcategoria
        """

        assert 'Id: ' in str(self.subcategoria)
        assert 'Nombre: ' in str(self.subcategoria)
        assert 'Categoria: ' in str(self.subcategoria)

    def test_platillo_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Platillo
        """

        assert 'Id: ' in str(self.platillo)
        assert 'Nombre: ' in str(self.platillo)
        assert 'Categoria: ' in str(self.platillo)

    def test_role_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Role
        """

        assert 'Id: ' in str(self.role)
        assert 'Usuario: ' in str(self.role)
        assert 'Grupo: ' in str(self.role)

    def test_orden_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Orden
        """

        assert 'Id: ' in str(self.orden)
        assert 'Usuario: ' in str(self.orden)
        assert 'Fecha: ' in str(self.orden)

    def test_carrito_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Carrito
        """

        assert 'Id: ' in str(self.carrito)
        assert 'Orden: ' in str(self.carrito)

    def test_pedido_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Pedido
        """

        assert 'Id: ' in str(self.pedido)
        assert 'Orden: ' in str(self.pedido)
        assert 'Platillo: ' in str(self.pedido)

    def test_promocion_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Promocion
        """

        assert 'Id: ' in str(self.promocion)
        assert 'Platillo: ' in str(self.promocion)
        assert 'Expiracion: ' in str(self.promocion)

    def test_cupon_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Cupon
        """

        assert 'Id: ' in str(self.cupon)
        assert 'Codigo: ' in str(self.cupon)
        assert 'Promocion: ' in str(self.cupon)

    def test_anuncio_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Anuncio
        """

        assert 'Id: ' in str(self.anuncio)
        assert 'Anunciante: ' in str(self.anuncio)
        assert 'Nombre: ' in str(self.anuncio)
