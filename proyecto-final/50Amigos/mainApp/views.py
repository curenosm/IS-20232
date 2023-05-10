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

def get_current_orden(user):
    """
    Función que obtiene la orden actual para el usuario indicado
    """
    orden = Orden.objects.filter(usuario=user, active=True) \
        .order_by('-fecha') \
        .first()

    return orden


def index(request):
    """
    Pagina de inicio 
    """
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


def contacto(request):
    """
    Página de contacto, muestra un formulario para suscribirse
    a nuestras noticias via email.
    """

    if request.method == 'GET':
        return render(request, 'contacto.html')
    elif request.method == 'POST':
        # Se envío el formulario de suscripción a nuestras noticas
        pass


@login_required
def votacion(request):
    """
    Página donde se puede realizar la votación por el sabor de helado 
    que se servirá al final de la comida.
    """
    if request.method == 'POST':
        print(request)

        # Obten el resultado de la votacion y asigna el sabor de helado de la orden activa
        orden = get_current_orden()
        orden.helado = Platillo.objects.filter(id=request.data['helado'])
        orden.save()

        return render(request, 'votacion.html', context={orden: orden})

    elif request.method == 'GET':
        return render(request, 'votacion.html')


@login_required
def get_lista_helados(request):
    """
    Funcion que nos sirve para mostrar todos los sabores de helado disponibles
    de entre los cuales se puede escoger
    """
    if request.method == 'GET':
        helados = Platillo.objects.filter(string__icontains='helado')
        return helados


@login_required
def agregar_pedido_a_orden(request):
    """
    Funcion que obtiene la orden actual del usuario, para posteriormente 
    agregar el pedido a la misma
    """

    if request.method == 'POST':
        print(request)

        # Todo lo que esté en el carrito actualmente va a pasar a una orden
        # que se irá a la cocina para ser preparada
        pedido = Pedido()

        return render(request, 'carrito.html')


@login_required
def solicitar_cuenta(request):
    """
    Funcion que cierra la orden actual, obtiene todos los pedidos asociados
    a la misma durante la merienda y calcula el total a pagar.
    """

    if request.method == 'GET':
        return render(request, 'resumen-ordenes.html')
    elif request.method == 'POST':
        # TODO: Cierra la cuenta actual, genera el ticket y muestra el resumen
        # de la cuenta, incluyendo IVA etc.
        return render(request, 'resumen-ordenes.html')


@login_required
def inicio_comensal(request):
    """
    Vista que maneja el template que se muestra una vez iniciada la sesión,
    el inicio mostrará un carrusel de imagenes con promociones actuales
    que se tengan en exhibición. Y otro carrusel para mostrar los anuncios
    pagados por terceros para ser exhibidos en las tabletas. 
    """
    
    data = {
        # Carga en el contexto las promociones actuales del restaurante
        "promociones": Promocion.objects.filter(active = True),
        # Carga los anuncios de terceros que quieran aparecer en el sitio web
        "anuncios": Anuncio.objects.filter(active=True)
    }

    return render(request, 'inicio.html', context=data)


@login_required
def menu(request):
    """
    Devuelve el template con los platillos disponibles en el menú
    """

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
    """
    Vista que se encarga de manejar los procesos relacionados al carrito
    de compras: ordenes, pedidos, total.
    """

    if request.method == 'GET':
        if len(Orden.objects.filter(usuario=request.user, active=True)) == 0:
            orden = Orden()
            orden.usuario = request.user
            orden.save()
            print(orden)
        
        data = {orden: orden}
        return render(request, 'carrito.html', context=data)
    elif request.method == 'POST':

        # TODO: Cierra la cuenta actual, genera el ticket y muestra el resumen
        # de la cuenta, incluyendo IVA etc.

        orden = get_current_orden(request.user)

        return render(request, 'resumen-ordenes.html', context={orden: orden})
    elif request.method == 'PUT':
        # TODO: Estamos agregando un pedido a la orden (cuenta)
        # hay que obtenerlo del cuerpo de la peticion y cuardarlo asociarlo 
        # a la orden actual, para despues guardarlo

        orden = get_current_orden(request.user)

        return render(request, 'resumen-ordenes.html', context={orden: orden})

