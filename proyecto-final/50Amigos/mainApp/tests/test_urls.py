from django.test import TestCase
from django.urls import reverse, resolve

from ..views import (
    CarritoView,
    OrdenView,
    index,
    inicio_comensal,
    get_lista_helados,
    contacto,
    menu,
    registro,
    votacion
)


class TestUrls(TestCase):
    """
    Clase de pruebas que se asegura de que
    las rutas funcionen como se esperaría.
    """

    def setUp(self):
        """
        Función para configurar el estado antes de cada prueba.
        """

        pass

    def test_index_url(self):
        """
        Función para probar que la url del index funcione correctamente.
        """

        url = reverse('mainApp:index')
        res = resolve(url)
        assert res.func.__name__ == index.__name__

    def test_carrito_url(self):
        """
        Función para probar que la url del carrito funcione correctamente.
        """

        url = reverse('mainApp:carrito')
        res = resolve(url)
        assert res.func.view_class == CarritoView

    def test_orden_url(self):
        """
        Función para probar que la url del carrito funcione correctamente.
        """

        url = reverse('mainApp:orden')
        res = resolve(url)
        assert res.func.view_class == OrdenView

    def test_contacto_url(self):
        """
        Función para probar que la url del contacto funcione correctamente.
        """

        url = reverse('mainApp:contacto')
        res = resolve(url)
        assert res.func.__name__ == contacto.__name__

    def test_helados_url(self):
        """
        Función para probar que la url de la lista de helados
        funcione correctamente.
        """

        url = reverse('mainApp:lista_helados')
        res = resolve(url)
        assert res.func.__name__ == get_lista_helados.__name__

    def test_inicio_comensal_url(self):
        """
        Función para probar que la url del inicio de los comensales
        funcione correctamente.
        """

        url = reverse('mainApp:inicio')
        res = resolve(url)
        assert res.func.__name__ == inicio_comensal.__name__

    def test_menu_url(self):
        """
        Función para probar que la url del menú funcione correctamente.
        """

        url = reverse('mainApp:menu')
        res = resolve(url)
        assert res.func.__name__ == menu.__name__

    def test_registro_url(self):
        """
        Función para probar que la url del registro funcione correctamente
        """

        url = reverse('mainApp:registro')
        res = resolve(url)
        assert res.func.__name__ == registro.__name__

    def test_votacion_url(self):
        """
        Función para probar que la url de la votación funcione correctamente
        """

        url = reverse('mainApp:votacion')
        res = resolve(url)
        assert res.func.__name__ == votacion.__name__
