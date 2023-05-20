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


class TestModels(TestCase):
    """
    Clase de prueba encargada de probar todos los modelos de nuestra aplicacion
    """

    @classmethod
    def setUpTestData(cls):
        """
        Función para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """

        [
            cls.users,
            cls.categorias,
            cls.subcategorias,
            cls.platillos,
            cls.roles,
            cls.ordenes,
            cls.pedidos,
            cls.carritos,
            cls.promociones,
            cls.cupones,
            cls.anuncios
        ] = create_test_data()

        cls.id_prueba = 9999

    def test_encrypted_password(self):
        """
        Función para probar la contraseña guardada durante el metodo de setup
        se guarde cifrada correctamente en la base de datos.
        """

        assert self.users[0].password != "password"

    def test_categoria_nombre(self):
        """
        Función para probar el modelo de las categorias.
        """

        for c in self.categorias:
            categoria = Categoria.objects.get(id=self.id_prueba)
            self.assertEqual(categoria.nombre, c.nombre)

    def test_subcategoria_nombre(self):
        """
        Función para probar el modelo de las categorias.
        """

        for s in self.subcategorias:
            subcategoria = Subcategoria.objects.get(id=self.id_prueba)
            self.assertEqual(subcategoria.nombre, s.nombre)

    def test_helado(self):
        """
        Función para probar el modelo de los helados.
        """

        for p in self.platillos:
            platillo = Platillo.objects.get(id=p.id)
            self.assertEqual(platillo.nombre, p.nombre)

    def test_orden(self):
        """
        Función para probar el modelo de las ordenes.
        """

        for o in self.ordenes:
            orden = Orden.objects.get(id=o.id)
            self.assertEqual(orden.usuario.username, o.usuario.username)

    def test_pedido(self):
        """
        Función para probar el modelo de los pedidos.
        """

        for p in self.pedidos:
            pedido = Pedido.objects.get(id=p.id)
            self.assertEqual(pedido.carrito.orden, self.ordenes[0])

    def test_anuncio(self):
        """
        Función para probar el modelo de los anuncios.
        """
        for a in self.anuncios:
            anuncio = Anuncio.objects.get(id=a.id)
            self.assertEqual(anuncio, a)

    def test_user(self):
        """
        Función para probar el modelo de los usuarios.
        """

        for u in self.users:
            user = User.objects.get(id=u.id)
            self.assertEqual(user, u)

    def test_role(self):
        """
        Función para probar el modelo de los roles.
        """

        for r in self.roles:
            role = Role.objects.get(id=r.id)
            self.assertEqual(role, r)

    def test_promocion(self):
        """
        Función para probar el modelo de las promociones.
        """

        for p in self.promociones:
            promocion = Promocion.objects.get(id=self.id_prueba)
            self.assertEqual(promocion, p)

    def test_cupon(self):
        """
        Función para probar el modelo de los cupones de descuento.
        """

        for c in self.cupones:
            cupon = Cupon.objects.get(id=self.id_prueba)
            self.assertEqual(cupon, c)

    def test_carrito(self):
        """
        Función para probar el modelo del carrito de compras.
        """
        for c in self.carritos:
            carrito = Carrito.objects.get(id=self.id_prueba)
            self.assertEqual(carrito, c)


class TestModelString(TestCase):
    """
    Clase para probar los metodos __str__ de los modelos
    """

    @classmethod
    def setUpTestData(cls):
        """
        Función para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """

        [
            cls.users,
            cls.categorias,
            cls.subcategorias,
            cls.platillos,
            cls.roles,
            cls.ordenes,
            cls.pedidos,
            cls.carritos,
            cls.promociones,
            cls.cupones,
            cls.anuncios
        ] = create_test_data()

        cls.id_prueba = 9999

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

        assert self.pedidos[0].get_subtotal() == '200.00'

    def test_carrito_total(self):
        """
        Prueba unitaria para el subtotal de un carrito
        """

        assert str(self.carritos[0].get_total()) == '200.00'

    def test_orden_total(self):
        """
        Prueba unitaria para el subtotal de un carrito
        """

        assert str(self.ordenes[0].get_total()) == '0'

    def test_user_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo User
        """

        for u in self.users:
            assert 'Username: ' in str(u)
            assert 'First name: ' in str(u)
            assert 'Last name: ' in str(u)
            assert 'Email: ' in str(u)

    def test_categoria_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Categoria
        """

        for c in self.categorias:
            assert 'Id: ' in str(c)
            assert 'Nombre: ' in str(c)

    def test_subcategoria_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Subcategoria
        """

        for s in self.subcategorias:
            assert 'Id: ' in str(s)
            assert 'Nombre: ' in str(s)
            assert 'Categoria: ' in str(s)

    def test_platillo_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Platillo
        """

        for p in self.platillos:
            assert 'Id: ' in str(p)
            assert 'Nombre: ' in str(p)
            assert 'Categoria: ' in str(p)

    def test_role_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Role
        """

        for r in self.roles:
            assert 'Id: ' in str(r)
            assert 'Usuario: ' in str(r)
            assert 'Grupo: ' in str(r)

    def test_orden_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Orden
        """

        for o in self.ordenes:
            assert 'Id: ' in str(o)
            assert 'Usuario: ' in str(o)
            assert 'Fecha: ' in str(o)

    def test_orden_get_pedidos(self):
        """
        Prueba unitaria para el metodo get_pedidos del modelo Orden
        """

        assert len(self.ordenes[0].get_pedidos()) == 0

    def test_carrito_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Carrito
        """

        for c in self.carritos:
            assert 'Id: ' in str(c)
            assert 'Orden: ' in str(c)

    def test_pedido_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Pedido
        """

        for p in self.pedidos:
            assert 'Id: ' in str(p)
            assert 'Orden: ' in str(p)
            assert 'Platillo: ' in str(p)

    def test_promocion_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Promocion
        """

        for p in self.promociones:
            assert 'Id: ' in str(p)
            assert 'Platillo: ' in str(p)
            assert 'Expiracion: ' in str(p)

    def test_cupon_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Cupon
        """

        for c in self.cupones:
            assert 'Id: ' in str(c)
            assert 'Codigo: ' in str(c)
            assert 'Promocion: ' in str(c)

    def test_anuncio_str(self):
        """
        Prueba unitaria para el metodo __str__ del modelo Anuncio
        """

        for a in self.anuncios:
            assert 'Id: ' in str(a)
            assert 'Anunciante: ' in str(a)
            assert 'Nombre: ' in str(a)
