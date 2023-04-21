from django.test import TestCase
from django.urls import reverse, resolve

from ..views import *


class TestUrls(TestCase):

    def setUp(self):
        pass

    def test_login_url(self):
        url = reverse('login_url')
        res = resolve(url)

        assert res.func.__name__ == login_view.__name__

    def test_logout_url(self):
        url = reverse('logout_url')
        res = resolve(url)

        assert res.func.__name__ == logout_view.__name__
