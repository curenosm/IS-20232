from django.test import TestCase
from django.urls import reverse, resolve

from ..views import *


class TestUrls(TestCase):

    def setUp(self):
        pass

    def test_contacto_url(self):
        url = reverse('mainApp:contacto')
        res = resolve(url)

        assert res.func.__name__ == contacto.__name__

    def test_registro_url(self):
        url = reverse('mainApp:registro')
        res = resolve(url)

        assert res.func.__name__ == registro.__name__
