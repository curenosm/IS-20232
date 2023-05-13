import pytest
import json

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import (
    reverse,
)

from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
)
from django.test import Client

from django.contrib.auth.hashers import make_password


from ..views import *

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

    def setUp(self):
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

        self.factory = APIRequestFactory()
        self.client = Client()

    def test_login_not_valid_data(self):
        res = self.client.login(username='error', password='error')
        self.assertFalse(res)

    def test_logout_not_logged_in(self):
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, reverse('mainApp:index'))

    def test_logout_fails_if_not_logged(self):
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, reverse('mainApp:index'))

    def test_contacto_no_login(self):
        url = reverse('mainApp:contacto')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['contacto'])

    def test_index_no_login(self):
        url = reverse('mainApp:index')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['index'])

    def test_login_no_login(self):
        url = reverse('login')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['login'])

    def test_registro_no_login(self):
        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['registro'])

    def test_votacion_no_login(self):
        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:votacion'))

    def test_lista_helados_no_login(self):
        url = reverse('mainApp:lista_helados')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:lista_helados'))

    def test_carrito_no_login(self):
        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:carrito'))

    def test_inicio_comensal_no_login(self):
        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:inicio'))

    # PRUEBAS QUE REQUIEREN AUTENTICACION
    def test_registro_login(self):
        self.client.force_login(user=self.user)

        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_carrito_login(self):
        self.client.force_login(user=self.user)

        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['carrito'])

    def test_inicio_comensal_login(self):
        self.client.force_login(user=self.user)

        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['inicio'])

    def test_votacion_login(self):
        self.client.force_login(user=self.user)

        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['votacion'])

    def test_menu_login(self):
        self.client.force_login(user=self.user)

        url = reverse('mainApp:menu')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['menu'])


@pytest.mark.django_db
class TestViews_POST(TestCase):

    def setUp(self):
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

        self.factory = APIRequestFactory()
        self.client = Client()

    def test_logout_no_login(self):
        url = reverse('login')
        data = {}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_login_no_login(self):
        url = reverse('login')
        data = {"username": "admin", "password": "admin"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_contacto_no_login(self):
        url = reverse('mainApp:contacto')
        data = {}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['contacto'])

    def test_registro_no_login_200(self):
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
        url = reverse('mainApp:votacion')
        data = {}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:votacion'))

    def test_carrito_login(self):
        self.client.force_login(user=self.user)
        data = {}
        url = reverse('mainApp:carrito')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['carrito'])

    def test_votacion_login(self):
        self.client.force_login(user=self.user)
        data = {}
        url = reverse('mainApp:votacion')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, TEMPLATES['votacion'])

    def test_registro_login(self):
        self.client.force_login(user=self.user)
        data = {}
        url = reverse('mainApp:registro')
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestViews_PUT(TestCase):

    def setUp(self):
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

        self.factory = APIRequestFactory()
        self.client = Client()

    def test_carrito_login(self):
        self.client.force_login(user=self.user)
        data_str = "platillo=1&cantidad=1"
        url = reverse('mainApp:carrito')
        response = self.client.put(url, data_str,
            content_type='application/x-www-form-urlencoded')
        assert response.status_code == status.HTTP_200_OK
        self.assertContains(response, 'Success')

    def test_carrito_login_404(self):
        self.client.force_login(user=self.user)
        data_str = "platillo=2&cantidad=1"
        url = reverse('mainApp:carrito')
        response = self.client.put(url, data_str, 
            content_type='application/x-www-form-urlencoded')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestViews_DELETE(TestCase):

    def setUp(self):
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

        self.factory = APIRequestFactory()
        self.client = Client()
    
    def test_carrito_login(self):
        self.client.force_login(user=self.user)
        data = {
            "platillo": 1
        }
        url = reverse('mainApp:carrito')
        response = self.client.delete(url, data)
        assert response.status_code == status.HTTP_202_ACCEPTED
