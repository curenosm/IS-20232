import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, QueryDict

from rest_framework import status

from .models import (
    Categoria,
    Platillo,
    Pedido,
    Orden,
    Promocion,
    Anuncio
)

from .forms import CustomUserCreationForm
from .serializers import PlatilloSerializer
from .decorators import anonymous_required

User = get_user_model()

logger = logging.getLogger(__name__)

# Password de los comensales (mesa1, mesa2, mesa3): restaurante123


def get_current_carrito(user):
    """
    Función que obtiene la orden actual para el usuario indicado
    """
    orden = Orden.objects.filter(usuario=user, active=True) \
        .order_by('-fecha') \
        .first()

    if not orden:
        orden = Orden.objects.create(usuario=user, active=True)

    return orden


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

        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            usuario = form.save()
            usuario.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)

            messages.success(request, 'Registro exitoso, iniciar sesión')
            return redirect(to="login")
        else:
            if not form.cleaned_data.get('username', False):
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        data['form'] = form

    return render(request, 'registration/registration.html', data)


def contacto(request):
    """
    Página de contacto, muestra un formulario para suscribirse
    a nuestras noticias via email.
    """

    if request.method == 'POST':
        messages.info(
            request,
            'The has suscrito exitosamente a nuestras noticicas.')

    return render(request, 'contacto.html')


@login_required
def votacion(request):
    """
    Página donde se puede realizar la votación por el sabor de helado
    que se servirá al final de la comida.
    """

    if request.method == 'POST':
        # Obten el resultado de la votacion y asigna el sabor de helado de la
        # orden activa
        orden = get_current_carrito(request.user)
        orden.helado = Platillo.objects.filter(
            id=request.POST.get('helado', 1))
        orden.save()

        messages.success(request, 'La votación concluyó exitosamente!')
        return render(request, 'votacion.html', context={orden: orden})

    elif request.method == 'GET':

        messages.warning(
            request,
            'Recuerda que en caso de empate elegiremos nosotros.')
        return render(request, 'votacion.html')


@login_required
def get_lista_helados(request):
    """
    Funcion que nos sirve para mostrar todos los sabores de helado disponibles
    de entre los cuales se puede escoger
    """

    if request.method == 'GET':

        platillos = Platillo.objects.filter(nombre__icontains='helado')
        platilloSerializer = PlatilloSerializer(platillos, many=True)

        return JsonResponse(
            platilloSerializer.data,
            safe=False
        )


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
        request,
        """
        Bienvenido a 50Amigos, no olvide hacer la votación por el
        sabor de helado.
        """
    )

    return render(request, 'inicio.html', context=data)


@login_required
def menu(request):
    """
    Devuelve el template con los platillos disponibles en el menú
    """

    if request.method == 'GET':
        return render(request, 'menu.html', context={
            "categorias": Categoria.objects.all()
        })


@login_required
def carrito(request):
    """
    Vista que se encarga de manejar los procesos relacionados al carrito
    de compras: ordenes, pedidos, total.
    """

    if request.method == 'GET':
        carrito = get_current_carrito(request.user)
        data = {
            "orden": carrito,
            "carrito": carrito
        }

        return render(request, 'carrito.html', context=data)
    elif request.method == 'POST':
        # Cierra la cuenta actual, genera el ticket y muestra el resumen
        # de la cuenta, incluyendo IVA etc.

        carrito = get_current_carrito(request.user)
        carrito.active = False

        messages.success(
            request,
            'La orden fue cerrada, la cuenta puede ser consultada')
        return render(request, 'carrito.html', context={carrito: carrito})
    elif request.method == 'PUT':
        # Estamos agregando un pedido al carrito

        # Todavía no pasa a la orden que es de donde extraemos la cuenta
        # a la orden actual, para despues guardarlo
        carrito = get_current_carrito(request.user)
        data = QueryDict(request.body)
        pedido = None

        # Intenta encontrar un pedido que tenga el mismo platillo
        for p in carrito.pedidos.all():
            if int(p.platillo.id) == int(data.get('platillo')):
                pedido = p

        if pedido is None:
            pedido = Pedido()
            pedido.platillo = get_object_or_404(
                Platillo, id=data.get('platillo'))
            pedido.cantidad = data.get('cantidad')
            pedido.orden = carrito
        else:
            pedido.cantidad = int(data.get('cantidad'))

        pedido.save()

        messages.success(request, 'Tu carrito fue actualizado')
        return HttpResponse('Success')

    elif request.method == 'DELETE':
        # El pedido indicado va a ser elininado del carrito de compras
        carrito = get_current_carrito(request.user)
        data = QueryDict(request.body)

        for p in carrito.pedidos.all():
            if int(data.get('platillo')) == int(p.platillo.id):
                print('si entro')
                p.orden = None
                p.save()

        messages.warning(request, 'El elemento fue retirado de su carrito')
        return HttpResponse('Deleted', status=status.HTTP_202_ACCEPTED)
