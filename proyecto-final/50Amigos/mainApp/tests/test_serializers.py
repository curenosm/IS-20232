from django.contrib.auth import get_user_model

from ..serializers import PlatilloSerializer
from .test_data import (
    PLATILLOS
)

User = get_user_model()


def test_valid_login_form():
    """
    Prueba unitaria para el formulario de registro.
    """

    data = PLATILLOS[0]
    platilloSerializer = PlatilloSerializer(data=data)
    assert platilloSerializer.is_valid()
