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


@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.REDIRECT_LOGIN_URL = '/accounts/login/?next='
        self.username = 'prueba'
        self.password = 'prueba'
        self.email = 'prueba@prueba.com'

        self.user = User.objects.create(
            username=self.username,
            password=make_password(self.password)
        )

        self.factory = APIRequestFactory()
        self.client = Client()

    def test_logout_POST_no_login(self):
        url = reverse('login')
        response = self.client.post(url, {})
        assert response.status_code == status.HTTP_200_OK

    def test_login_POST_no_login(self):
        url = reverse('login')
        data = {
            "username": "admin",
            "password": "admin"}
        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK

    def test_login_not_valid_data(self):
        res = self.client.login(
            username='administrador',
            password="wrong_password")
        self.assertFalse(res)

    def test_logout_not_logged_in(self):
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, '/')

    def test_logout_fails_if_not_logged(self):
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(response, '/')

    def test_contacto_GET_no_login(self):
        url = reverse('mainApp:contacto')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'contacto.html')

    def test_contacto_POST_no_login(self):
        url = reverse('mainApp:contacto')
        data = {}
        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'contacto.html')

    def test_index_GET_no_login(self):
        url = reverse('mainApp:index')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'index.html')

    def test_login_GET_no_login(self):
        url = reverse('login')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_registro_GET_no_login(self):
        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_registro_POST_no_login(self):
        url = reverse('mainApp:registro')
        data = {
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
            'email': self.email
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_votacion_GET_no_login(self):
        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:votacion'))

    def test_votacion_POST_no_login(self):
        url = reverse('mainApp:votacion')
        data = {}
        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:votacion'))

    def test_get_lista_helados_GET_no_login(self):
        url = reverse('mainApp:lista_helados')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:lista_helados'))

    def test_carrito_GET_no_login(self):
        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:carrito'))

    def test_inicio_comensal_GET_no_login(self):
        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND
        self.assertRedirects(
            response, self.REDIRECT_LOGIN_URL + reverse('mainApp:inicio'))

    def test_get_lista_helados_GET_no_login(self):
        url = reverse('mainApp:lista_helados')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_302_FOUND

    # PRUEBAS QUE REQUIEREN AUTENTICACION
    def test_registro_GET_login(self):

        self.client.force_login(user=self.user)

        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_registro_POST_login(self):

        self.client.force_login(user=self.user)

        url = reverse('mainApp:registro')
        response = self.client.post(url, data={})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_carrito_GET_login(self):

        self.client.force_login(user=self.user)

        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'carrito.html')

    def test_inicio_comensal_GET_login(self):

        self.client.force_login(user=self.user)

        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'inicio.html')

    def test_votacion_GET_login(self):

        self.client.force_login(user=self.user)

        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'votacion.html')

    def test_votacion_POST_login(self):

        self.client.force_login(user=self.user)

        url = reverse('mainApp:votacion')
        response = self.client.post(url, data={})
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'votacion.html')

    def test_menu_GET_login(self):

        self.client.force_login(user=self.user)

        url = reverse('mainApp:menu')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        self.assertTemplateUsed(response, 'menu.html')
