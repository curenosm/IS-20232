import uuid
from datetime import datetime, timedelta

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from ..models import (Anuncio, Carrito, Categoria, Cupon, Orden, Pedido,
                      Platillo, Promocion, Role, Subcategoria)

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

USUARIOS = [
    {
        'id': 827834768,
        'username': 'administrador',
        'password': 'administrador',
        'email': 'administrador@50amigos.com',
    },
    {
        'id': 1643623,
        'username': 'mesa1',
        'password': 'restaurante123321',
        'email': 'mesa1@50amigos.com',
    },
    {
        'id': 2234231,
        'username': 'mesa2',
        'password': 'restaurante123321',
        'email': 'mesa2@50amigos.com',
    },
    {
        'id': 3212345,
        'username': 'mesa3',
        'password': 'restaurante123321',
        'email': 'mesa3@50amigos.com',
    },
    {
        'id': 5234232,
        'username': 'mesa4',
        'password': 'restaurante123321',
        'email': 'mesa4@50amigos.com',
    },
    {
        'id': 9999,
        'username': TEST_USERNAME,
        'password': TEST_PASSWORD,
        'email': TEST_EMAIL,
    },
]

CATEGORIAS = [
    {
        'id': 9999,
        'nombre': 'Prueba',
    },
    {
        'id': 12213652,
        'nombre': 'Entradas'
    },
    {
        'id': 12213653,
        'nombre': 'Bebidas'
    },
    {
        'id': 1221364232,
        'nombre': 'Postres'
    },
    {
        'id': 1249878,
        'nombre': 'Helados'
    },
]

SUBCATEGORIAS = [
    {
        'id': 9999,
        'nombre': 'Prueba',
        'categoria': 12213652
    },
    {
        'id': 99123435,
        'nombre': 'Clasicos',
        'categoria': 12213652
    },
    {
        'id': 923451359,
        'nombre': 'Clasicos',
        'categoria': 12213652
    },
    {
        'id': 9973452,
        'nombre': 'Bebidas embotelladas',
        'categoria': 12213653
    },
    {
        'id': 9123129,
        'nombre': 'Clasicos',
        'categoria': 1221364232
    },
    {
        'id': 964644449,
        'nombre': 'Clasicos',
        'categoria': 1249878
    },
]

TEST_HELADO = {
    'id': 9999,
    'nombre': 'Helado',
    'imagen': 'noimagen.jpg',
    'precio': '100.00',
    'ingredientes': '',
}

PLATILLOS = [
    {
        'id': 11,
        'nombre': 'Prueba',
        'imagen': 'noimagen.jpg',
        'precio': '200.00',
        'ingredientes': 'ingrediente1,ingrediente2',
    },
    {
        'id': 2,
        'nombre': 'Prueba',
        'imagen': 'noimagen.jpg',
        'precio': '200.00',
        'ingredientes': 'ingrediente1,ingrediente2',
    },
    {
        'id': 33,
        'nombre': 'Prueba',
        'imagen': 'noimagen.jpg',
        'precio': '200.00',
        'ingredientes': 'ingrediente1,ingrediente2',
    },
    {
        'id': 44,
        'nombre': 'Prueba',
        'imagen': 'noimagen.jpg',
        'precio': '200.00',
        'ingredientes': 'ingrediente1,ingrediente2',
    },
    {
        'id': 55,
        'nombre': 'Prueba',
        'imagen': 'noimagen.jpg',
        'precio': '200.00',
        'ingredientes': 'ingrediente1,ingrediente2',
    },
    TEST_HELADO
]

ROLES = [
    {
        'id': 9999,
        'nombre': 'Admin'
    },
    {
        'id': 99,
        'nombre': 'Responsable de tabletas'
    },
    {
        'id': 9,
        'nombre': 'Comensal'
    },
]

ORDENES = [
    {
        'id': 9999,
        'total': '100.00',
        'comentarios': 'Ninguno',
        'active': False,
    },
]

PEDIDOS = [
    {
        'id': 9999,
        'cantidad': 2,
        'platillo': 1,
    },
]

CARRITOS = [
    {
        'id': 9999,
        'active': True,
    },
]

PROMOCIONES = [
    {
        'id': 9999,
        'imagen': IMAGE_URL,
        'codigo': uuid.uuid4(),
        'valido_hasta': datetime.now(tz=pytz.UTC) + timedelta(days=30),
    },
]

CUPONES = [
    {
        'id': 9999,
        'codigo': uuid.uuid4(),
    },
]

ANUNCIOS = [
    {
        'id': 9999,
        'nombre': 'Tu anuncio aquí',
        'imagen': IMAGE_URL,
        'codigo': uuid.uuid4(),
        'valido_hasta': datetime.now(tz=pytz.UTC) + timedelta(days=30),
        'active': True,
        'anunciante': '50Amigos'
    },
]


def create_test_data():

    users = []
    for usuario in USUARIOS:
        users.append(User.objects.create(
            id=usuario.get('id'),
            username=usuario.get('username'),
            password=make_password(usuario.get('password')),
            email=usuario.get('email')))

    categorias = []
    for categoria in CATEGORIAS:
        categorias.append(Categoria.objects.create(
            id=categoria.get('id'),
            nombre=categoria.get('nombre')))

    subcategorias = []
    for subcategoria in SUBCATEGORIAS:
        subcategorias.append(Subcategoria.objects.create(
            id=subcategoria.get('id'),
            nombre=subcategoria.get('nombre')))

    platillos = []
    for platillo in PLATILLOS:
        platillos.append(Platillo.objects.create(
            id=platillo.get('id'),
            nombre=platillo.get('nombre'),
            descripcion=platillo.get('descripcion'),
            imagen=platillo.get('imagen'),
            categoria=categorias[0],
            subcategoria=subcategorias[0],
            precio=platillo.get('precio'),
            ingredientes=platillo.get('ingredientes')))

    roles = []
    for role in ROLES:
        roles.append(Role.objects.create(
            id=role.get('id'),
            usuario=users[0]))

    ordenes = []
    for orden in ORDENES:
        ordenes.append(Orden.objects.create(
            id=orden.get('id'),
            usuario=users[0],
            total=orden.get('total'),
            comentarios=orden.get('comentarios'),
            active=orden.get('active'),
            helado_escogido=platillos[-1]))

    carritos = []
    for carrito in CARRITOS:
        carritos.append(Carrito.objects.create(
            id=carrito.get('id'),
            orden=ordenes[0]))

    pedidos = []
    for pedido in PEDIDOS:
        pedidos.append(Pedido.objects.create(
            id=pedido.get('id'),
            carrito=carritos[0],
            platillo=platillos[0],
            cantidad=pedido.get('cantidad')))

    promociones = []
    for promocion in PROMOCIONES:
        promociones.append(Promocion.objects.create(
            id=promocion.get('id'),
            codigo=promocion.get('codigo'),
            platillo=platillos[0],
            valido_hasta=promocion.get('valido_hasta'),
            imagen=promocion.get('imagen')))

    cupones = []
    for cupon in CUPONES:
        cupones.append(Cupon.objects.create(
            id=cupon.get('id'),
            codigo=cupon.get('codigo'),
            promocion=promociones[0]))

    ads = []
    for ad in ANUNCIOS:
        ads.append(Anuncio.objects.create(
            id=ad.get('id'),
            nombre=ad.get('nombre'),
            anunciante=ad.get('anunciante'),
            valido_hasta=ad.get('valido_hasta'),
            imagen=ad.get('imagen'),
            active=ad.get('active')))

    return [
        users,
        categorias,
        subcategorias,
        platillos,
        roles,
        ordenes,
        pedidos,
        carritos,
        promociones,
        cupones,
        ads
    ]
