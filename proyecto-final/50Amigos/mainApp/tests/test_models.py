import pytest

from django.test import TestCase

from django.contrib.auth.hashers import make_password

from ..models import (
    Carrito,
    Platillo,
    Pedido,
    Categoria,
    Subcategoria,
    Orden,
    User,
    Role,
    Promocion,
    Anuncio,
    Cupon
)

from .test_data import (
    USUARIOS,
    CATEGORIAS,
    SUBCATEGORIAS,
    PLATILLOS,
    ROLES,
    ANUNCIOS,
    CUPONES,
    PROMOCIONES,
    ORDENES,
    PEDIDOS,
    CARRITOS
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

        self.id_prueba = 9999
        self.user_password = 'password'

        self.usuario = None
        for usuario in USUARIOS:
            self.usuario = User.objects.create(
                id=usuario.get('id'),
                username=usuario.get('username'),
                password=make_password(usuario.get('password')),
                email=usuario.get('email'))

        self.categoria = None
        for categoria in CATEGORIAS:
            self.categoria = Categoria.objects.create(
                id=categoria.get('id'),
                nombre=categoria.get('nombre'))

        self.subcategoria = None
        for subcategoria in SUBCATEGORIAS:
            self.subcategoria = Subcategoria.objects.create(
                id=subcategoria.get('id'),
                nombre=subcategoria.get('nombre'))

        self.platillo = None
        for platillo in PLATILLOS:
            self.platillo = Platillo.objects.create(
                id=platillo.get('id'),
                nombre=platillo.get('nombre'),
                descripcion=platillo.get('descripcion'),
                imagen=platillo.get('imagen'),
                categoria=self.categoria,
                subcategoria=self.subcategoria,
                precio=platillo.get('precio'),
                ingredientes=platillo.get('ingredientes'))

        self.role = None
        for role in ROLES:
            self.role = Role.objects.create(usuario=self.usuario)

        self.orden = None
        for orden in ORDENES:
            self.orden = Orden.objects.create(
                id=orden.get('id'),
                usuario=self.usuario,
                total=orden.get('total'),
                comentarios=orden.get('comentarios'),
                active=orden.get('active'),
                helado_escogido=self.platillo)

        self.pedido = None
        for pedido in PEDIDOS:
            self.pedido = Pedido.objects.create(
                id=pedido.get('id'),
                orden=self.orden,
                platillo=self.platillo,
                cantidad=pedido.get('cantidad'))

        self.carrito = None
        for carrito in CARRITOS:
            self.carrito = Carrito.objects.create(
                id=carrito.get('id'),
                orden=self.orden)

        self.promocion = None
        for promocion in PROMOCIONES:
            self.promocion = Promocion.objects.create(
                id=promocion.get('id'),
                codigo=promocion.get('codigo'),
                platillo=self.platillo,
                valido_hasta=promocion.get('valido_hasta'),
                imagen=promocion.get('imagen'))

        self.cupon = None
        for cupon in CUPONES:
            self.cupon = Cupon.objects.create(
                id=cupon.get('id'),
                codigo=cupon.get('codigo'),
                promocion=self.promocion)

        self.anuncio = None
        for anuncio in ANUNCIOS:
            self.anuncio = Anuncio.objects.create(
                id=anuncio.get('id'),
                nombre=anuncio.get('nombre'),
                anunciante=anuncio.get('anunciante'),
                valido_hasta=anuncio.get('valido_hasta'),
                imagen=anuncio.get('imagen'),
                active=anuncio.get('active'))

    def test_encrypted_password(self):
        """
        Función para probar la contraseña guardada durante el metodo de setup
        se guarde cifrada correctamente en la base de datos.
        """

        assert self.usuario.password != "password"

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
        self.assertEqual(orden.usuario.username, self.usuario.username)

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
