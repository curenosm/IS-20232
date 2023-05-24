import re

from django.contrib.auth.models import AbstractUser, Group
from django.db import models


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
                First name: {self.first_name}
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
        return f"""
                Id: {self.id}
                Nombre: {self.nombre}
                """


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

    def hidden_if_helado(self):
        """
        Funcion para esconder los componentes de las tarjetas de helado en el
        menú.
        """

        if re.search('helado', self.nombre, re.IGNORECASE):
            return 'hidden'
        return ''

    def line_through_if_helado(self):
        """
        Funcion para decidir si el precio va a aparecer tachado
        o no dependiendo si se trata de un helado.
        """

        if re.search('helado', self.nombre, re.IGNORECASE):
            return 'text-decoration-line-through'
        return ''

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
                Grupo: {self.grupo}
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
    helado_escogido = models.ForeignKey(
        Platillo, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'

    def desmarcar_carritos_como_activos(self):
        """
        Función auxiliar para cerrar los carritos al momento de cerrar
        la cuenta.
        """

        for c in self.carritos.all():
            c.active = False
            c.save()

    def votacion_concluida(self):
        """
        Función para determinar si la votación para el helado de la orden
        ya tomó lugar.
        """
        return self.helado_escogido is not None

    def hidden_if_votacion_concluida(self):
        """
        Metodo para elegir el estado inicial de la gráfica de resultados
        """

        return 'hidden' if self.votacion_concluida() else ''

    def disabled_if_votacion_concluida(self):
        """
        Metodo para deshabilitar el voton de votación una vez se haya
        concluido la misma para la orden actual.
        """

        return 'disabled' if self.votacion_concluida() else ''

    def get_total(self):
        """
        Metodo para obtener el total de todos los pedidos en la cuenta.
        """
        total = 0
        for p in self.get_pedidos():
            total += p.get_subtotal()
        return total

    def get_pedidos(self):
        """
        Metodo auxiliar para obtener todos los pedidos asociados
        a cada carrito de la orden.
        """

        res = []
        for c in self.carritos.all():
            if not c.active:
                for p in c.pedidos.all():
                    res.append(p)
        return res

    def __str__(self):
        return f"""
                Id: {self.id}
                Usuario: {self.usuario}
                Fecha: {self.fecha}
                Active: {self.active}
                Helado escogido: {self.helado_escogido}
                """


class Carrito(models.Model):
    """
    Modelo que representa el carrito de compras, donde se iran acumulando los
    pedidos hasta que se mande a cocina
    """

    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='carritos')
    orden = models.ForeignKey(
        Orden, on_delete=models.SET_NULL, null=True, related_name='carritos')
    active = models.BooleanField(default=True)

    def get_total(self):
        """
        Metodo para obtener el total de todos los pedidos en la cuenta.
        """
        total = 0
        for p in self.pedidos.all():
            total += p.get_subtotal()

        return total

    def __str__(self):
        return f"""
                Id: {self.id}
                Orden: {self.orden}
                """


class Pedido(models.Model):
    """
    Modelo que representa un pedido de la orden indicada. Un pedido es una
    abstraccion para poder indicar la cantidad de platillos de un mismo
    tipo a pedir para la cuenta.
    """

    id = models.AutoField(primary_key=True)
    platillo = models.ForeignKey(
        Platillo, on_delete=models.SET_NULL, null=True, related_name='pedidos')
    cantidad = models.IntegerField(default=1)
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pedidos')

    def get_subtotal(self):
        """
        Metodo auxiliar para calcular el costo de todos los elementos del
        pedido.
        """
        return float(self.platillo.precio) * float(self.cantidad)

    def __str__(self):
        return f"""
                Id: {self.id}
                Carrito:
                    {self.carrito}
                Platillo: {self.platillo}
                """


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
