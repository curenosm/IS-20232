from datetime import datetime, timedelta
import pytz
import uuid

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

USUARIOS = [{
    'id': 9999,
    'username': 'prueba',
    'password': 'password',
    'email': 'prueba@prueba.com',
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
