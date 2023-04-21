import logging

from django.contrib.auth import get_user_model
from django.shortcuts import render, HttpResponse

from .models import *

User = get_user_model()

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')
