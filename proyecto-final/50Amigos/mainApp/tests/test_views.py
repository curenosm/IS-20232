import pytest
import json

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import (
    reverse,
    resolve
)

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import (
    APIRequestFactory,
    APIClient,
    force_authenticate,
    RequestsClient,
)

from ..views import *

User = get_user_model()


@pytest.mark.django_db
class TestViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.admin_password = 'password'
        self.admin = User.objects.create_user(
            username='admin', password=self.admin_password)

    def test_login_and_logout_views(self):
        url = reverse('login')
        data = {
            "username": self.admin.username,
            "password": self.admin_password
        }

        res = self.client.login(username=self.admin.username, password=self.admin_password)
        self.assertTrue(res)

        response = self.client.post(url, data)
        assert response.status_code == 302
        self.assertRedirects(response, '/inicio')

    def test_login_not_valid_data(self):
        res = self.client.login(username=self.admin.username, password="wrong_password")
        self.assertFalse(res)
    
    def test_logout_not_logged_in(self):
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == 302
        self.assertRedirects(response, '/')

    def test_logout_fails_if_not_logged(self):
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == 302
        self.assertRedirects(response, '/')

    def test_contacto_GET(self):
        url = reverse('mainApp:contacto')
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'contacto.html')

    def test_index_GET(self):
        url = reverse('mainApp:index')
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'index.html')

    def test_login_GET(self):
        url = reverse('login')
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_registro_GET(self):
        url = reverse('mainApp:registro')
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_votacion_GET_no_login(self):
        url = reverse('mainApp:votacion')
        response = self.client.get(url)
        assert response.status_code == 302
        self.assertRedirects(response, '/accounts/login/?next=/votacion')

    def test_get_lista_helados_GET_no_login(self):
        url = reverse('mainApp:lista_helados')
        response = self.client.get(url)
        assert response.status_code == 302
        self.assertRedirects(response, '/accounts/login/?next=/helados')

    def test_menu_GET_no_login(self):
        url = reverse('mainApp:menu')
        response = self.client.get(url)
        assert response.status_code == 302
        self.assertRedirects(response, '/accounts/login/?next=/menu')

    def test_carrito_GET_no_login(self):
        url = reverse('mainApp:carrito')
        response = self.client.get(url)
        assert response.status_code == 302
        self.assertRedirects(response, '/accounts/login/?next=/carrito')

    def test_inicio_comensal_GET_no_login(self):
        url = reverse('mainApp:inicio')
        response = self.client.get(url)
        assert response.status_code == 302
        self.assertRedirects(response, '/accounts/login/?next=/inicio')
