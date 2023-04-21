from django.test import TestCase
from mixer.backend.django import mixer
import pytest

from ..models import *


@pytest.mark.django_db
class TestModels(TestCase):
    pass
