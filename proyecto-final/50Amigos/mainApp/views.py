import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

User = get_user_model()

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def registro(request):
    data = {'form': CustomUserCreationForm()}

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            usuario.save()
            user = authenticate(username=formulario.cleaned_data['username'],
                                password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'Registro exitoso, iniciar sesión')
            return redirect(to="mainApp:inicio")
        data['form'] = formulario

    return render(request, 'registration/registration.html', data)


@login_required
def inicio_comensal(request):
    return render(request, 'inicio.html')


@login_required
def menu(request):
    return render(request, 'menu.html')


@login_required
def carrito(request):
    return render(request, 'carrito.html')
