from django.test import TestCase
from django.urls import reverse, resolve

from ..views import *


class TestUrls(TestCase):
    """
    Clase de pruebas que se asegura de que 
    las rutas funcionen como se esperaría.
    """

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
    
    def test_inicio_url(self):
        url = reverse('mainApp:inicio')
        res = resolve(url)
        assert res.func.__name__ == inicio_comensal.__name__
    
    def test_menu_url(self):
        url = reverse('mainApp:menu')
        res = resolve(url)
        assert res.func.__name__ == menu.__name__
    
    def test_carrito_url(self):
        url = reverse('mainApp:carrito')
        res = resolve(url)
        assert res.func.__name__ == carrito.__name__
    
    def test_menu_url(self):
        url = reverse('mainApp:votacion')
        res = resolve(url)
        assert res.func.__name__ == votacion.__name__
    
    def test_menu_url(self):
        url = reverse('mainApp:lista_helados')
        res = resolve(url)
        assert res.func.__name__ == get_lista_helados.__name__
