import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse, QueryDict
from django.views import View
from django.core.mail import EmailMultiAlternatives
from rest_framework import status
from django.conf import settings

from .models import (
    Carrito,
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


def get_current_orden(user):
    """
    Función que obtiene la orden actual para el usuario indicado.
    """
    orden = Orden.objects.filter(usuario=user, active=True) \
        .order_by('-fecha') \
        .first()

    if not orden:
        orden = Orden.objects.create(usuario=user, active=True)

    return orden


def get_current_carrito(user):
    """
    Función que obtiene el carrito actual para el usuario indicado.
    """
    carrito = Carrito.objects.filter(
        usuario=user,
        active=True).order_by('-fecha').first()

    if not carrito:
        carrito = Carrito.objects.create(
            usuario=user,
            active=True,
            orden=get_current_orden(user))
    else:
        carrito.orden = get_current_orden(user)
        carrito.save()

    return carrito


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

    status_response = status.HTTP_200_OK
    if request.method == 'POST':

        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            usuario = form.save()
            usuario.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])

            login(request, user)
            messages.success(request, 'Registro exitoso, iniciar sesión')
            return redirect(to="login")
        else:
            if form.errors.get('username', True):
                status_response = status.HTTP_400_BAD_REQUEST

        data['form'] = form

    return render(
        request,
        'registration/registration.html',
        data,
        status=status_response)


def contacto(request):
    """
    Página de contacto, muestra un formulario para suscribirse
    a nuestras noticias via email.
    """

    if request.method == 'POST':
        data = QueryDict(request.body)
        email = data.get('email')

        if not email:
            messages.error(
                request,
                'Verifica tu correo.')
        else:
            subject = "Suscriptor"
            from_email = settings.EMAIL_HOST_USER
            to = email
            text_content = "This is an important message."
            html_content = """
            <b>Gracias por suscribirte a nuestras noticias.</b>
            """
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                from_email,
                [to])
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send()
                messages.info(
                    request,
                    'The has suscrito exitosamente a nuestras noticicas.')
            except Exception as e:
                logger.error(e)
                messages.error(
                    request,
                    'El servicio no está disponible en este momento.')

    return render(request, 'contacto.html')


@login_required
def votacion(request):
    """
    Página donde se puede realizar la votación por el sabor de helado
    que se servirá al final de la comida.
    """

    if request.method == 'POST':

        data = QueryDict(request.body)
        id = data.get('platilloId')
        print(id)

        # Obten el resultado de la votacion y asigna el sabor de helado de la
        # orden activa
        orden = get_current_orden(request.user)
        orden.helado_escogido = get_object_or_404(Platillo, id=id)
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


@method_decorator(login_required, name='dispatch')
class OrdenView(View):
    """
    Vista basada en clases para manejar las peticiones relacionadas
    con el manejo de la orden de un comensal.
    """

    def post(self, request, *args, **kwargs):
        """
        Metodo para cerrar la orden y generar la cuenta durante la
        estadía en el restaurante.
        """

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        """
        Método para agregar los pedidos del carrito actual a la orden.
        """

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        """
        Método para eliminar un pedido de la orden.
        """

        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@method_decorator(login_required, name='dispatch')
class CarritoView(View):
    """
    Vista basada en clases para manejar las peticiones relacionadas
    con el carrito de compras, incluye agregar pedidos al mismo, eliminarlos,
    editarlos y consultar el estado del carrito.
    """

    def get(self, request, *args, **kwargs):
        """
        Devuelve el template con el carrito y la orden actual en el contexto
        """

        carrito = get_current_carrito(request.user)
        orden = get_current_orden(request.user)
        data = {
            "orden": orden,
            "carrito": carrito
        }
        return render(request, 'carrito.html', context=data)

    def post(self, request, *args, **kwargs):
        """
        Pasa los pedidos del carrito a la orden (cuenta)
        """

        carrito = get_current_carrito(request.user)
        orden = get_current_orden(request.user)

        carrito.active = False
        carrito.save()

        data = {
            "orden": orden,
            "carrito": []
        }
        messages.success(
            request,
            'La orden fue cerrada, la cuenta puede ser consultada')
        return render(request, 'carrito.html', context=data)

    def put(self, request, *args, **kwargs):
        """
        Estamos agregando un pedido al carrito, todavía no pasa a la
        orden que es de donde extraemos la cuenta # a la orden actual,
        para despues guardarlo.
        """

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
            pedido.carrito = carrito
        else:
            pedido.cantidad = int(data.get('cantidad'))

        pedido.save()

        messages.success(request, 'Tu carrito fue actualizado')
        return HttpResponse('Success')

    def delete(self, request, *args, **kwargs):
        """
        El pedido indicado va a ser elininado del carrito de compras
        """

        carrito = get_current_carrito(request.user)
        data = QueryDict(request.body)

        for p in carrito.pedidos.all():
            if int(data.get('platillo')) == int(p.platillo.id):
                logger.debug('si entro')
                p.carrito = None
                p.save()

        messages.warning(request, 'El elemento fue retirado de su carrito')
        return HttpResponse('Deleted', status=status.HTTP_202_ACCEPTED)
