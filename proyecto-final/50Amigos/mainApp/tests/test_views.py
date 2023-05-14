import pytest

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import (
    reverse,
)

from rest_framework import status
from django.test import Client

from django.contrib.auth.hashers import make_password


from ..models import (
    Subcategoria,
    Categoria,
    Platillo
)


User = get_user_model()

TEMPLATES = {
    "inicio": 'inicio.html',
    "carrito": 'carrito.html',
    "contacto": 'contacto.html',
    "index": 'index.html',
    "login": 'registration/login.html',
    "menu": 'menu.html',
    "registro": 'registration/registration.html',
    "votacion": 'votacion.html',
}


@pytest.mark.django_db
class TestViews_GET(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo GET.
    """

    def setUp(self):
        """
        Funcion para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """

        self.REDIRECT_LOGIN_URL = '/accounts/login/?next='
        self.USERNAME = 'prueba'
        self.PASSWORD = 'prueba'
        self.EMAIL = 'prueba@prueba.com'

        self.user = User.objects.create(
            username=self.USERNAME,
            password=make_password(self.PASSWORD)
        )
        self.categoria = Categoria.objects.create(nombre="Prueba")
        self.subcategoria = Subcategoria.objects.create(nombre="Prueba")

        self.platillo = Platillo.objects.create(
            id=1,
            nombre='Prueba',
            imagen='noimagen.jpg',
            precio='100.00',
            categoria=self.categoria,
            subcategoria=self.subcategoria
        )

        self.client = Client()

    def test_login_not_valid_data(self):
        """
        Funcion para probar que el login no funcione si se utilizan
        credenciales invalidas para iniciar sesión.
        """

        res = self.client.login(username='error', password='error')
        self.assertFalse(res)

    def test_contacto_no_login(self):
        """
        Funcion para probar que la página de contacto sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('mainApp:contacto')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['contacto'])

    def test_index_no_login(self):
        """
        Funcion para probar que la página del index sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('mainApp:index')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['index'])

    def test_login_no_login(self):
        """
        Funcion para probar que la página de login sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('login')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['login'])

    def test_registro_no_login(self):
        """
        Funcion para probar que la página de registro sea correctamente
        accesible en caso de que no se haya iniciado sesión.
        """

        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['registro'])

    def test_votacion_no_login(self):
        """
        Funcion para probar que la página de votacion no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:votacion'))

    def test_lista_helados_no_login(self):
        """
        Funcion para probar que el listado de helados no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:lista_helados')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response,
            self.REDIRECT_LOGIN_URL + reverse('mainApp:lista_helados'))

    def test_carrito_no_login(self):
        """
        Funcion para probar que la página del carrito no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:carrito'))

    def test_inicio_comensal_no_login(self):
        """
        Funcion para probar que la página del comensale no sea
        accesible en caso de que aún no se haya iniciado sesión.
        """

        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:inicio'))

    # PRUEBAS QUE REQUIEREN AUTENTICACION
    def test_registro_login(self):
        """
        Funcion para probar que la página de registro no sea
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.user)

        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_carrito_login(self):
        """
        Funcion para probar que la página de carrito sea
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.user)

        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['carrito'])

    def test_inicio_comensal_login(self):
        """
        Funcion para probar que la página de inicio sea correctamente
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.user)

        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['inicio'])

    def test_votacion_login(self):
        """
        Funcion para probar que la página de votación sea correctamente
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.user)

        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['votacion'])

    def test_menu_login(self):
        """
        Funcion para probar que la página de menú sea correctamente
        accesible en caso de que ya se haya iniciado sesión.
        """

        self.client.force_login(user=self.user)

        url = reverse('mainApp:menu')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['menu'])


@pytest.mark.django_db
class TestViews_POST(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo POST.
    """

    def setUp(self):
        """
        Funcion para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """

        self.REDIRECT_LOGIN_URL = '/accounts/login/?next='
        self.USERNAME = 'prueba'
        self.PASSWORD = 'prueba'
        self.EMAIL = 'prueba@prueba.com'

        self.user = User.objects.create(
            username=self.USERNAME,
            password=make_password(self.PASSWORD)
        )
        self.categoria = Categoria.objects.create(nombre="Prueba")
        self.subcategoria = Subcategoria.objects.create(nombre="Prueba")

        self.platillo = Platillo.objects.create(
            id=1,
            nombre='Prueba',
            imagen='noimagen.jpg',
            precio='100.00',
            categoria=self.categoria,
            subcategoria=self.subcategoria
        )

        self.client = Client()

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
            'username': 'new-user',
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
            'email': 'new@50amigos.com'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_registro_no_login_400(self):
        """
        Función para probar que el registro no funcione en caso
        de que se introduzca un nombre de usuario que ya está usado.
        """

        url = reverse('mainApp:registro')
        data = {
            'username': self.USERNAME,
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
            'email': self.EMAIL
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
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:votacion'))

    def test_carrito_login(self):
        """
        Función para probar que no podamos agregar un pedido del carrito
        a la orden en caso de que no hayamos iniciado sesión.
        """

        self.client.force_login(user=self.user)
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

        self.client.force_login(user=self.user)
        data = {}
        url = reverse('mainApp:votacion')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['votacion'])

    def test_registro_login(self):
        """
        Función para probar que podamos no podamos registrar una cuenta
        si hemos iniciado sesión.
        """

        self.client.force_login(user=self.user)
        data = {}
        url = reverse('mainApp:registro')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestViews_PUT(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo PUT.
    """

    def setUp(self):
        """
        Funcion para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """

        self.REDIRECT_LOGIN_URL = '/accounts/login/?next='
        self.USERNAME = 'prueba'
        self.PASSWORD = 'prueba'
        self.EMAIL = 'prueba@prueba.com'

        self.user = User.objects.create(
            username=self.USERNAME,
            password=make_password(self.PASSWORD)
        )
        self.categoria = Categoria.objects.create(nombre="Prueba")
        self.subcategoria = Subcategoria.objects.create(nombre="Prueba")

        self.platillo = Platillo.objects.create(
            id=1,
            nombre='Prueba',
            imagen='noimagen.jpg',
            precio='100.00',
            categoria=self.categoria,
            subcategoria=self.subcategoria
        )
        self.client = Client()

    def test_carrito_login(self):
        """
        Funcion para probar que podemos agregar pedidos al carrito de compras
        correctamente una vez tengamos sesión iniciada.
        """

        self.client.force_login(user=self.user)
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
        Funcion para probar que no podemos agregar pedidos al carrito de
        compras si no tenemos un platillo indicado.
        """

        self.client.force_login(user=self.user)
        data_str = "platillo=2&cantidad=1"
        url = reverse('mainApp:carrito')
        response = self.client.put(
            url,
            data_str,
            content_type='application/x-www-form-urlencoded')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestViews_DELETE(TestCase):
    """
    Clase para probar las llamadas a vistas con metodo DELETE.
    """

    def setUp(self):
        """
        Funcion para configurar el estado del sistema antes de cualquier
        prueba unitaria.
        """

        self.REDIRECT_LOGIN_URL = '/accounts/login/?next='
        self.USERNAME = 'prueba'
        self.PASSWORD = 'prueba'
        self.EMAIL = 'prueba@prueba.com'

        self.user = User.objects.create(
            username=self.USERNAME,
            password=make_password(self.PASSWORD)
        )
        self.categoria = Categoria.objects.create(nombre="Prueba")
        self.subcategoria = Subcategoria.objects.create(nombre="Prueba")

        self.platillo = Platillo.objects.create(
            id=1,
            nombre='Prueba',
            imagen='noimagen.jpg',
            precio='100.00',
            categoria=self.categoria,
            subcategoria=self.subcategoria
        )
        self.client = Client()

    def test_carrito_login(self):
        """
        Funcion para probar que podamos eliminar un pedido del carrito antes
        de haberlo enviado a la orden.
        """

        self.client.force_login(user=self.user)
        data = {
            "platillo": 1
        }
        url = reverse('mainApp:carrito')
        response = self.client.delete(url, data)
        assert response.status_code == status.HTTP_202_ACCEPTED
