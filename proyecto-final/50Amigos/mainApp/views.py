import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, QueryDict
from django.core.mail import send_mail
from django.contrib import messages

from .models import *
from .forms import *
from .decorators import anonymous_required

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


@anonymous_required
def index(request):
    """
    Pagina de inicio 
    """
    return render(request, 'index.html')


@anonymous_required
def registro(request):
    """
    Vista encargada de manejar el registro de nuevos usuarios
    """

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

            return redirect(to="login")

        data['form'] = formulario

    return render(request, 'registration/registration.html', data)


def contacto(request):
    """
    Página de contacto, muestra un formulario para suscribirse
    a nuestras noticias via email.
    """

    if request.method == 'POST':
        # Se envío el formulario de suscripción a nuestras noticas

        messages.info(
            request, 'The has suscrito exitosamente a nuestras noticicas.')

        pass

    return render(request, 'contacto.html')


@login_required
def votacion(request):
    """
    Página donde se puede realizar la votación por el sabor de helado 
    que se servirá al final de la comida.
    """

    if request.method == 'POST':
        print(request)

        # Obten el resultado de la votacion y asigna el sabor de helado de la orden activa
        orden = get_current_orden(request.user)
        orden.helado = Platillo.objects.filter(
            id=request.POST.get('helado', 1))
        orden.save()

        messages.success(request, 'La votación concluyó exitosamente!')

        return render(request, 'votacion.html', context={orden: orden})

    elif request.method == 'GET':

        messages.warning(
            request, 'Recuerda que en caso de empate elegiremos nosotros.')

        return render(request, 'votacion.html')


@login_required
def get_lista_helados(request):
    """
    Funcion que nos sirve para mostrar todos los sabores de helado disponibles
    de entre los cuales se puede escoger
    """
    if request.method == 'GET':
        helados = Platillo.objects.filter(nombre__icontains='helado')
        return JsonResponse(list(helados), safe=False)


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
        "promociones": Promocion.objects.filter(active=True),
        # Carga los anuncios de terceros que quieran aparecer en el sitio web
        "anuncios": Anuncio.objects.filter(active=True)
    }

    messages.info(
        request, 'Bienvenido a 50Amigos, no olvide hacer la votación por el sabor de helado')

    return render(request, 'inicio.html', context=data)


@login_required
def menu(request):
    """
    Devuelve el template con los platillos disponibles en el menú
    """

    if request.method == 'GET':

        categorias = Categoria.objects.all()

        return render(request, 'menu.html', context={
            "categorias": categorias
        })


@login_required
def carrito(request):
    """
    Vista que se encarga de manejar los procesos relacionados al carrito
    de compras: ordenes, pedidos, total.
    """

    if request.method == 'GET':
        orden = get_current_orden(request.user)
        data = {
            "orden": orden,
            "carrito": orden
        }
        print('Imprimiendo orden actual')
        print(orden)
        print(orden.pedidos.all())
        return render(request, 'carrito.html', context=data)
    elif request.method == 'POST':
        # TODO: Cierra la cuenta actual, genera el ticket y muestra el resumen
        # de la cuenta, incluyendo IVA etc.

        orden = get_current_orden(request.user)

        orden.active = False
        messages.success(
            request, 'La orden fue cerrada, la cuenta puede ser consultada')

        return render(request, 'carrito.html', context={orden: orden})
    elif request.method == 'PUT':
        # TODO: Estamos agregando un pedido a la orden (cuenta)
        # hay que obtenerlo del cuerpo de la peticion y cuardarlo asociarlo
        # a la orden actual, para despues guardarlo

        orden = get_current_orden(request.user)

        data = QueryDict(request.body)
        pedido = Pedido()
        pedido.platillo = Platillo.objects.get(id=data.get('platillo'))
        pedido.cantidad = data.get('cantidad')
        pedido.orden = orden
        pedido.save()
        print(pedido)

        messages.success(request, 'El pedido fue agregado a tu orden')
        return HttpResponse('Success')
