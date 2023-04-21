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
        self.admin_password = 'qwerty123'
        self.admin = User.objects.create_user(username='admin', password=self.admin_password)

    def test_login_and_logout_views(self):
        url = reverse('login_url')
        data = {
            "username": self.admin.username,
            "password": self.admin_password
        }
        response = self.client.post(url, data)
        assert response.status_code == 200
        url = reverse('logout_url')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_logout_fails_if_not_logged(self):
        url = reverse('logout_url')
        response = self.client.get(url)
        assert response.status_code == 400

    def test_post_user_viewset(self):
        url = reverse('user_list')
        data = {
            "username": "nuevo",
            "email": "nuevo@correo.com",
            "first_name": "first",
            "last_name": "last",
            "password": "Password123",
            "password2": "Password123",
        }
        response = self.client.post(url, data)
        assert response.status_code == 201
