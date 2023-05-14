from datetime import datetime, timedelta
import pytz
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from ..models import (
    Anuncio,
    Carrito,
    Categoria,
    Cupon,
    Orden,
    Pedido,
    Platillo,
    Promocion,
    Role,
    Subcategoria,
)

User = get_user_model()


IMAGE_URL = """
https://www.muycomputer.com/wp-content/uploads/2019/11/BlackFriday2019.jpg
"""

TEMPLATES = {
    "inicio": 'inicio.html',
    "carrito": 'carrito.html',
    "contacto": 'contacto.html',
    "index": 'index.html',
    "login": 'registration/login.html',
    "menu": 'menu.html',
    "registro": 'registration/registration.html',
    "votacion": 'votacion.html',
}

REDIRECT_LOGIN_URL = '/accounts/login/?next='

TEST_USERNAME = 'usuarioInexistente'
TEST_PASSWORD = 'wwR25He@7TeD2bf'
TEST_EMAIL = 'prueba@prueba.com'
TEST_FIRST_NAME = 'prueba'
TEST_LAST_NAME = 'prueba'

TEST_ADMIN_USERNAME = 'admin'
TEST_ADMIN_PASSWORD = 'password'
TEST_ADMIN_EMAIL = 'admin@admin.com'

USUARIOS = [{
    'id': 9999,
    'username': TEST_USERNAME,
    'password': TEST_PASSWORD,
    'email': TEST_EMAIL,
}]

CATEGORIAS = [{
    'id': 9999,
    'nombre': 'Prueba',
}]

SUBCATEGORIAS = [{
    'id': 9999,
    'nombre': 'Prueba',
}]

PLATILLOS = [{
    'id': 1,
    'nombre': 'Prueba',
    'imagen': 'noimagen.jpg',
    'precio': '200.00',
    'ingredientes': '',
}, {
    'id': 9999,
    'nombre': 'Prueba',
    'imagen': 'noimagen.jpg',
    'precio': '100.00',
    'ingredientes': '',
}]

ROLES = [{
    'id': 9999,
}]

ORDENES = [{
    'id': 9999,
    'total': '100.00',
    'comentarios': 'Ninguno',
    'active': False,
}]

PEDIDOS = [{
    'id': 9999,
    'cantidad': 1,
}]

CARRITOS = [{
    'id': 9999,
}]

PROMOCIONES = [{
    'id': 9999,
    'imagen': IMAGE_URL,
    'codigo': uuid.uuid4(),
    'valido_hasta': datetime.now(tz=pytz.UTC) + timedelta(days=30),
}]

CUPONES = [{
    'id': 9999,
    'codigo': uuid.uuid4()
}]

ANUNCIOS = [{
    'id': 9999,
    'nombre': 'Tu anuncio aquí',
    'imagen': IMAGE_URL,
    'codigo': uuid.uuid4(),
    'valido_hasta': datetime.now(tz=pytz.UTC) + timedelta(days=30),
    'active': True,
    'anunciante': '50Amigos'
}]


def create_test_data():

    user = None
    for usuario in USUARIOS:
        user = User.objects.create(
            id=usuario.get('id'),
            username=usuario.get('username'),
            password=make_password(usuario.get('password')),
            email=usuario.get('email'))

    category = None
    for categoria in CATEGORIAS:
        category = Categoria.objects.create(
            id=categoria.get('id'),
            nombre=categoria.get('nombre'))

    subcategory = None
    for subcategoria in SUBCATEGORIAS:
        subcategory = Subcategoria.objects.create(
            id=subcategoria.get('id'),
            nombre=subcategoria.get('nombre'))

    platillo_ = None
    for platillo in PLATILLOS:
        platillo_ = Platillo.objects.create(
            id=platillo.get('id'),
            nombre=platillo.get('nombre'),
            descripcion=platillo.get('descripcion'),
            imagen=platillo.get('imagen'),
            categoria=category,
            subcategoria=subcategory,
            precio=platillo.get('precio'),
            ingredientes=platillo.get('ingredientes'))

    role_ = None
    for role in ROLES:
        role_ = Role.objects.create(
            id=role.get('id'),
            usuario=user)

    order = None
    for orden in ORDENES:
        order = Orden.objects.create(
            id=orden.get('id'),
            usuario=user,
            total=orden.get('total'),
            comentarios=orden.get('comentarios'),
            active=orden.get('active'),
            helado_escogido=platillo_)

    pedido_ = None
    for pedido in PEDIDOS:
        pedido_ = Pedido.objects.create(
            id=pedido.get('id'),
            orden=order,
            platillo=platillo_,
            cantidad=pedido.get('cantidad'))

    cart = None
    for carrito in CARRITOS:
        cart = Carrito.objects.create(
            id=carrito.get('id'),
            orden=order)

    promocion_ = None
    for promocion in PROMOCIONES:
        promocion_ = Promocion.objects.create(
            id=promocion.get('id'),
            codigo=promocion.get('codigo'),
            platillo=platillo_,
            valido_hasta=promocion.get('valido_hasta'),
            imagen=promocion.get('imagen'))

    cupon_ = None
    for cupon in CUPONES:
        cupon_ = Cupon.objects.create(
            id=cupon.get('id'),
            codigo=cupon.get('codigo'),
            promocion=promocion_)

    ad = None
    for ad in ANUNCIOS:
        ad = Anuncio.objects.create(
            id=ad.get('id'),
            nombre=ad.get('nombre'),
            anunciante=ad.get('anunciante'),
            valido_hasta=ad.get('valido_hasta'),
            imagen=ad.get('imagen'),
            active=ad.get('active'))

    return [
        user,
        category,
        subcategory,
        platillo_,
        role_,
        order,
        pedido_,
        cart,
        promocion_,
        cupon_,
        ad
    ]
