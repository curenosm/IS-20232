import uuid

import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from ..forms import CustomUserCreationForm
from .test_data import (TEST_EMAIL, TEST_FIRST_NAME, TEST_LAST_NAME,
                        TEST_PASSWORD, TEST_USERNAME)

User = get_user_model()


@pytest.mark.django_db
def test_valid_registration_form():
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


@pytest.mark.django_db
def test_registration_form_invalid_no_data():
    """
    Prueba unitaria para el formulario de registro.
    """

    data = {}
    form = CustomUserCreationForm(data=data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_registration_form_invalid_email():
    """
    Prueba unitaria para el formulario de registro.
    """

    random_password = str(uuid.uuid4())

    data = {
        'username': str(uuid.uuid4()),
        'password1': random_password,
        'password2': random_password,
        'email': ''
    }

    form = CustomUserCreationForm(data=data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_registration_form_invalid_password():
    """
    Prueba unitaria para el formulario de registro.
    """

    random_password = str(uuid.uuid4())

    data = {
        'username': str(uuid.uuid4()),
        'password1': random_password,
        'password2': '',
        'email': str(uuid.uuid4()) + '@50amigos.com'
    }
    form = CustomUserCreationForm(data=data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_registration_form_invalid_username():
    """
    Prueba unitaria para el formulario de registro.
    """

    random_password = str(uuid.uuid4())

    data = {
        'password1': random_password,
        'password2': random_password,
        'email': str(uuid.uuid4()) + '@50amigos.com'
    }
    form = CustomUserCreationForm(data=data)
    assert not form.is_valid()
