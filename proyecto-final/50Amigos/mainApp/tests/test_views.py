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
        self.admin = User.objects.create_user(username='admin', password=self.admin_password)

    def test_login_and_logout_views(self):
        url = reverse('login')
        data = {
            "username": self.admin.username,
            "password": self.admin_password
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == 302

    def test_logout_fails_if_not_logged(self):
        url = reverse('logout')
        response = self.client.get(url)
        assert response.status_code == 302
