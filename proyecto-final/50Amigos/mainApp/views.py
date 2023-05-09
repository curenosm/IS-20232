import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

User = get_user_model()

logger = logging.getLogger(__name__)

# Password de los comensales (mesa1, mesa2, mesa3): restaurante123
def index(request):
    return render(request, 'index.html')


def contacto(request):
    if request.method == 'GET':
        return render(request, 'contacto.html')
    elif request.method == 'POST':
        # Se envío el formulario de suscripción a nuestras noticas
        pass


def votacion(request):
    if request.method == 'POST':
        print(request)
    elif request.method == 'GET':
        return render(request, 'votacion.html')


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

    data = {
        'categorias': [
            {
                "nombre":"Platos fuertes",
                "subcategorias" : [
                    {
                        "nombre": "Pollos",
                        "platillos": [
                            {   
                                "id": 1,
                                "nombre": "Pollo kfc",
                                "imagen": "https://recetinas.com/wp-content/uploads/2018/04/pollo-kentucky.jpg",
                                "descripcion": "Descripcion generica 1",
                                "ingredientes": [
                                    {
                                        "id": 1,
                                        "nombre": "queso"
                                    },
                                    {
                                        "id": 2,
                                        "nombre": "tomate"
                                    }
                                ]
                            },
                            {
                                "id": 2,
                                "nombre": "Pollo adobado",
                                "imagen": "https://storage.googleapis.com/avena-recipes/2019/10/1571782331514.jpeg",
                                "descripcion": "Pollo azado y sazonado con salsa picante",
                                "ingredientes": [
                                    {
                                        "id": 1,
                                        "nombre": "pollo"
                                    },
                                    {
                                        "id": 2,
                                        "nombre": "salsa ultra picante"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    if request.method == 'GET':
        return render(request, 'menu.html', context=data)


@login_required
def carrito(request):

    if request.method == 'GET':
        return render(request, 'carrito.html')
    elif request.method == 'POST':

        # Se esta haciendo una inserción de orden en el carrito

        

        return 

