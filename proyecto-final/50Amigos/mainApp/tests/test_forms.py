import pytest

from django.contrib.auth import get_user_model

from ..forms import CustomUserCreationForm
from .test_data import (
    TEST_USERNAME,
    TEST_PASSWORD,
    TEST_EMAIL,
    TEST_FIRST_NAME,
    TEST_LAST_NAME,
)

User = get_user_model()


@pytest.mark.django_db
def test_valid_login_form():
    """
    Prueba unitaria para el formulario de registro.
    """

    data = {
        'username': TEST_USERNAME,
        'password1': TEST_PASSWORD,
        'password2': TEST_PASSWORD,
        'email': TEST_EMAIL,
        'last_name': TEST_LAST_NAME,
        'first_name': TEST_FIRST_NAME,
    }

    form = CustomUserCreationForm(data=data)
    assert form.is_valid()
