from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import (
    reverse,
)

from rest_framework import status
from django.test import Client

from .test_data import (
    REDIRECT_LOGIN_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
    TEST_USERNAME,
    TEST_HELADO,
    TEMPLATES,
    create_test_data
)

User = get_user_model()


class TestAPIs_GET(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo GET.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Función para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """
        cls.client = Client()

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

        cls.client = Client()

    def test_get_lista_helados_no_login(self):
        """
        Función para probar que la api devuelva el listado de helados
        correctamente.
        """

        url = reverse('mainApp:lista_helados')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, REDIRECT_LOGIN_URL + url)

    def test_get_lista_helados_login(self):
        """
        Función para probar que la api devuelva el listado de helados
        correctamente.
        """

        self.client.force_login(user=self.users[0])
        url = reverse('mainApp:lista_helados')
        res = self.client.get(url)
        assert res.status_code == status.HTTP_200_OK


class TestViews_GET(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo GET.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Función para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """
        cls.client = Client()

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

        cls.client = Client()

    def test_login_not_valid_data(self):
        """
        Función para probar que el login no funcione si se utilizan
        credenciales invalidas para iniciar sesión.
        """

        res = self.client.login(username='error', password='error')
        self.assertFalse(res)

    def test_contacto_no_login(self):
        """
        Función para probar que la página de contacto sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('mainApp:contacto')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['contacto'])

    def test_index_no_login(self):
        """
        Función para probar que la página del index sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('mainApp:index')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['index'])

    def test_login_no_login(self):
        """
        Función para probar que la página de login sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('login')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['login'])

    def test_registro_no_login(self):
        """
        Función para probar que la página de registro sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['registro'])

    def test_votacion_no_login(self):
        """
        Función para probar que la página de votacion no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, REDIRECT_LOGIN_URL + url)

    def test_lista_helados_no_login(self):
        """
        Función para probar que el listado de helados no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:lista_helados')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response,
            REDIRECT_LOGIN_URL + url)

    def test_carrito_no_login(self):
        """
        Función para probar que la página del carrito no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, REDIRECT_LOGIN_URL + url)

    def test_inicio_comensal_no_login(self):
        """
        Función para probar que la página del comensale no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, REDIRECT_LOGIN_URL + url)

    def test_orden_no_login_405(self):
        """
        Funcion para probar que el metodo no está permitido
        en caso de solicitar una petición a la vista de las ordenes sin
        haberse autenticado.
        """

        url = reverse('mainApp:orden')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, REDIRECT_LOGIN_URL + url)

    # PRUEBAS QUE REQUIEREN AUTENTICACION
    def test_registro_login(self):
        """
        Función para probar que la página de registro no sea
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_carrito_login(self):
        """
        Función para probar que la página de carrito sea
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['carrito'])

    def test_inicio_comensal_login(self):
        """
        Función para probar que la página de inicio sea correctamente
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['inicio'])

    def test_votacion_login(self):
        """
        Función para probar que la página de votación sea correctamente
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['votacion'])

    def test_menu_login(self):
        """
        Función para probar que la página de menú sea correctamente
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:menu')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['menu'])

    def test_orden_login_405(self):
        """
        Funcion para probar que el metodo no está permitido
        en caso de solicitar una petición a la vista de las ordenes.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:orden')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestViews_POST(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo POST.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Función para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """
        cls.client = Client()

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

        cls.client = Client()

    def test_logout_no_login(self):
        """
        Función para probar que el logout falle en caso de que no hayamos
        iniciado sesión.
        """

        url = reverse('logout')
        response = self.client.post(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, reverse('mainApp:index'))

    def test_login_no_login(self):
        """
        Función para probar que el login funcione en caso de que no hayamos
        iniciado sesión.
        """

        url = reverse('login')
        data = {"username": "admin", "password": "admin"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_contacto_no_login(self):
        """
        Función para probar que la suscripción a la lista de noticias
        del restaurante funcione en caso de que no hayamos iniciado sesión.
        """

        url = reverse('mainApp:contacto')
        data = {}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['contacto'])

    def test_registro_no_login_200(self):
        """
        Función para probar que el registro de cuentas
        funcione en caso de que no hayamos iniciado sesión.
        """

        url = reverse('mainApp:registro')
        data = {
            'username': 'oiuyiuyqwiuey98798123',
            'password1': 'm97612934kjnbvzkx',
            'password2': 'm97612934kjnbvzkx',
            'email': 'this_is_just@anexample.com'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, reverse('login'))

    def test_registro_no_login_400(self):
        """
        Función para probar que el registro no funcione en caso
        de que se introduzca un nombre de usuario que ya está usado.
        """

        url = reverse('mainApp:registro')
        data = {
            'username': TEST_USERNAME,
            'password1': TEST_PASSWORD,
            'password2': TEST_PASSWORD,
            'email': TEST_EMAIL
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_votacion_no_login(self):
        """
        Función para probar que no se pueda votar sin haber iniciado sesión.
        """

        url = reverse('mainApp:votacion')
        data = {}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, REDIRECT_LOGIN_URL + url)

    def test_orden_no_login_302(self):
        """
        Funcion para probar que el metodo no está permitido
        en caso de solicitar una petición a la vista de las ordenes sin
        haberse autenticado.
        """

        url = reverse('mainApp:orden')
        response = self.client.post(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, REDIRECT_LOGIN_URL + url)

    def test_carrito_login(self):
        """
        Función para probar que no podamos agregar un pedido del carrito
        a la orden en caso de que no hayamos iniciado sesión.
        """

        self.client.force_login(user=self.users[0])
        data = {}
        url = reverse('mainApp:carrito')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['carrito'])

    def test_votacion_login(self):
        """
        Función para probar que podamos votar correctamente si ya iniciamos
        sesión.
        """

        self.client.force_login(user=self.users[0])
        data_str = f'platilloId={TEST_HELADO.get("id")}'
        url = reverse('mainApp:votacion')
        response = self.client.post(
            url,
            data_str,
            content_type='application/x-www-form-urlencoded')
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['votacion'])

    def test_votacion_login_404(self):
        """
        Función para probar que podamos votar correctamente si ya iniciamos
        sesión.
        """

        self.client.force_login(user=self.users[0])
        data = {
            'platilloId': 7812736817
        }
        url = reverse('mainApp:votacion')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_registro_login(self):
        """
        Función para probar que podamos no podamos registrar una cuenta
        si hemos iniciado sesión.
        """

        self.client.force_login(user=self.users[0])
        data = {}
        url = reverse('mainApp:registro')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_orden_login_202(self):
        """
        Funcion para probar que el metodo está permitido
        en caso de solicitar una petición a la vista de las ordenes una
        vez autenticados.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:orden')
        response = self.client.post(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestViews_PUT(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo PUT.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Función para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """
        cls.client = Client()

        [
            cls.users,
            cls.categorias,
            cls.subcategoria,
            cls.platillo,
            cls.role,
            cls.ordenes,
            cls.pedido,
            cls.carrito,
            cls.promociones,
            cls.cupones,
            cls.anuncios
        ] = create_test_data()

        cls.client = Client()

    def test_carrito_login(self):
        """
        Función para probar que podemos agregar pedidos al carrito de compras
        correctamente una vez tengamos sesión iniciada.
        """

        self.client.force_login(user=self.users[0])
        data_str = "platillo=1&cantidad=1"
        url = reverse('mainApp:carrito')
        response = self.client.put(
            url,
            data_str,
            content_type='application/x-www-form-urlencoded')
        assert response.status_code == status.HTTP_200_OK
        self.assertContains(response, 'Success')

    def test_carrito_login_404(self):
        """
        Función para probar que no podemos agregar pedidos al carrito de
        compras si no tenemos un platillo indicado.
        """

        self.client.force_login(user=self.users[0])
        data_str = "platillo=2&cantidad=1"
        url = reverse('mainApp:carrito')
        response = self.client.put(
            url,
            data_str,
            content_type='application/x-www-form-urlencoded')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_orden_login_204(self):
        """
        Funcion para probar que el metodo no está permitido
        en caso de solicitar una petición a la vista de las ordenes sin
        haberse autenticado.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:orden')
        response = self.client.put(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_orden_no_login_302(self):
        """
        Funcion para probar que el metodo no está permitido
        en caso de solicitar una petición a la vista de las ordenes sin
        haberse autenticado.
        """

        url = reverse('mainApp:orden')
        response = self.client.put(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, REDIRECT_LOGIN_URL + url)


class TestViews_DELETE(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo DELETE.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Función para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """
        cls.client = Client()

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

        cls.client = Client()

    def test_carrito_login(self):
        """
        Función para probar que podamos eliminar un pedido del carrito antes
        de haberlo enviado a la orden.
        """

        self.client.force_login(user=self.users[0])
        data = {
            "platillo": 1
        }
        url = reverse('mainApp:carrito')
        response = self.client.delete(url, data)
        assert response.status_code == status.HTTP_202_ACCEPTED

    def test_orden_login_405(self):
        """
        Funcion para probar que el metodo no está permitido
        en caso de solicitar una petición a la vista de las ordenes sin
        haberse autenticado.
        """

        self.client.force_login(user=self.users[0])

        url = reverse('mainApp:orden')
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_orden_no_login_302(self):
        """
        Funcion para probar que el metodo no está permitido
        en caso de solicitar una petición a la vista de las ordenes sin
        haberse autenticado.
        """

        url = reverse('mainApp:orden')
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, REDIRECT_LOGIN_URL + url)
