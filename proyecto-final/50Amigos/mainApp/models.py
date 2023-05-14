import re
from django.db import models

from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    """
    Modelo personalizado para los usuarios de 50Amigos.
    """
    email = models.EmailField(unique=True, null=False, blank=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"""
            Username: {self.username}
            First name:{self.first_name}
            Last name: {self.last_name}
            Email: {self.email}
            """


class Categoria(models.Model):
    """
    Modelo que representa una categoría en el menu del restaurante.
    """

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f'Id: {self.id}, Nombre: {self.nombre}'


class Subcategoria(models.Model):
    """
    Modelo que representa un tipo de platillo dentro de una categoria. P.e.
    Una subcategoria de la categoria "Antojitos" es "Vegetarianos"
    """

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subcategorias')

    def __str__(self):
        return f"""
                Id: {self.id}
                Nombre: {self.nombre}
                Categoria: {self.categoria}
                """


class Platillo(models.Model):
    """
    Modelo que representa un producto disponible en el menú.
    """

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True, max_length=1000)
    imagen = models.CharField(max_length=1000)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='platillos')
    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='platillos')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ingredientes = models.TextField(max_length=1000, null=True, blank=True)

    def get_ingredientes_list(self):
        """
        Metodo auxiliar para convertir los ingredientes del platillo
        de una representación en string separados por comas, en una
        lista de strings.
        """

        if self.ingredientes is None or self.ingredientes.strip() == '':
            return []

        ingredientes = []
        for ingrediente in self.ingredientes.split(','):
            ingredientes.append(ingrediente)

        return ingredientes

    def disabled_if_helado(self):
        """
        Funcion para deshabilitar los botones en el menu convenientemente
        si se trata de un helado, puesto que el helado es servido de manera
        gratis en el restaurante y por lo tanto no debería ser posible
        agregarlos al carrito.
        """

        if re.search('helado', self.nombre, re.IGNORECASE):
            return 'disabled'
        return ''

    def __str__(self):
        return f"""
                Id: {self.id}
                Nombre: {self.nombre}
                Categoria: {self.categoria}
                """


class Role(models.Model):
    """
    Modelo creado para manejar permisos de los usuarios
    """

    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"""
                Id: {self.id}
                Usuario: {self.usuario}
                Categoria: {self.grupo}
                """


class Orden(models.Model):
    """
    Modelo que representa la cuenta del comensal, la misma cuenta con una
    asociacion para que cada orden pueda estar vinculada a varios pedidos.
    """

    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='orders')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(decimal_places=2, max_digits=100, null=True)
    comentarios = models.TextField(blank=True, max_length=500)
    active = models.BooleanField(default=True)
    helado_escogido = models.ForeignKey(
        Platillo, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'

    def __str__(self):
        return f'Id: {self.id}, Usuario: {self.usuario}, Fecha: {self.fecha}'


class Carrito(models.Model):
    """
    Modelo que representa el carrito de compras, donde se iran acumulando los
    pedidos hasta que se mande a cocina
    """
    id = models.AutoField(primary_key=True)
    orden = models.OneToOneField(
        Orden, on_delete=models.SET_NULL, null=True, related_name='carrito')

    def __str__(self):
        return f'Id: {self.id}, Orden: {self.orden.id}'


class Pedido(models.Model):
    """
    Modelo que representa un pedido de la orden indicada. Un pedido es una
    abstraccion para poder indicar la cantidad de platillos de un mismo
    tipo a pedir para la cuenta.
    """

    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey(
        Orden, on_delete=models.SET_NULL, null=True, related_name='pedidos')
    platillo = models.ForeignKey(
        Platillo, on_delete=models.SET_NULL, null=True, related_name='pedidos')
    cantidad = models.IntegerField(default=1)
    carrito = models.ManyToOneRel(
        to=Carrito,
        field_name='carrito',
        field="id",
        on_delete=models.SET_NULL,
        related_name='pedidos')

    def get_subtotal(self):
        """
        Metodo auxiliar para calcular el costo de todos los elementos del
        pedido.
        """
        return self.platillo.precio * self.cantidad

    def __str__(self):
        return f'Id: {self.id}, Orden: {self.orden}, Platillo: {self.platillo}'


class Promocion(models.Model):
    """
    Modelo que representa una promoción que se puede aplicar a un platillo
    determinado en la cuenta.
    """

    id = models.AutoField(primary_key=True)
    codigo = models.UUIDField(unique=True, auto_created=True)
    platillo = models.ForeignKey(
        Platillo, on_delete=models.CASCADE, null=False)
    imagen = models.TextField(max_length=500, null=False, blank=False)
    valido_hasta = models.DateTimeField(auto_now_add=False)
    active = models.BooleanField(default=True, null=False)

    class Meta:
        verbose_name = 'Promocion'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return f"""
                Id: {self.id}
                Platillo: {self.platillo}
                Expiracion: {self.valido_hasta}
                """


class Cupon(models.Model):
    """
    Modelo que facilita el manejo de las promociones dentro del restaurante.
    """

    id = models.AutoField(primary_key=True)
    codigo = models.UUIDField(unique=True, auto_created=True)
    promocion = models.ForeignKey(
        Promocion,
        on_delete=models.CASCADE,
        null=False,
        related_name='cupones')

    class Meta:
        verbose_name = 'Cupon'
        verbose_name_plural = 'Cupones'

    def __str__(self):
        return f"""
                Id: {self.id}
                Codigo: {self.codigo}
                Promocion: {self.promocion.id}
                """


class Anuncio(models.Model):
    """
    Anuncio a ser mostrado en el feed principal una vez que el responsable
    de tabletas inicia la sesión del comensal.
    """

    id = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=200, null=False, blank=False)
    anunciante = models.TextField(max_length=200, null=False, blank=False)
    valido_hasta = models.DateTimeField(auto_now_add=False)
    imagen = models.TextField(max_length=500, null=False, default="")
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f'Id: {self.id}, Anunciante: {self.id}, Nombre: {self.nombre}'
