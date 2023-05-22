from django.contrib.auth import get_user_model

from ..models import (Platillo)
from ..serializers import PlatilloSerializer
from .test_data import PLATILLOS

User = get_user_model()


def test_valid_platillo_serializer():
    """
    Prueba unitaria para el formulario de login.
    """

    data = PLATILLOS[0]
    platillo_serializer = PlatilloSerializer(data=data)
    assert platillo_serializer.is_valid()

def test_platillo_serializer_invalid_no_data():
    """
    Prueba unitaria para verificar que le formulario de login falle en caso
    de datos incorrectos.
    """

    data = {}
    platillo_serializer = PlatilloSerializer(data=data)
    assert not platillo_serializer.is_valid()

def test_platillo_serializer_invalid():
    """
    Prueba unitaria para verificar que le formulario de login falle en caso
    de datos incorrectos.
    """

    platillo = Platillo()
    platillo_serializer = PlatilloSerializer(data=platillo)
    assert not platillo_serializer.is_valid()
