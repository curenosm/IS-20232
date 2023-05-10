from django.db import models

from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username} | {self.first_name} | {self.last_name} | {self.email}'


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f'Id: {self.id}, Nombre: {self.nombre}'


class Subcategoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Id: {self.id}, Nombre: {self.nombre}, Categoria: {self.categoria}'


class Platillo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.CharField(max_length=1000)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True)
    subcategoria = models.ForeignKey(
        Subcategoria, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Id: {self.id}, Nombre: {self.nombre}, Categoria: {self.categoria}'


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Id: {self.id}, Usuario: {self.usuario}, Categoria: {self.grupo}'


class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(decimal_places=2, max_digits=100)
    comentarios = models.TextField(blank=True, max_length=500)
    active = models.BooleanField(default=True)
    helado_escogido = models.ForeignKey(Platillo, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'

    def __str__(self):
        return f'Id: {self.id}, Usuario: {self.usuario}, Fecha: {self.fecha}'


class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, null=True)
    platillo = models.ForeignKey(
        Platillo, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f'Id: {self.id}, Orden: {self.orden}, Platillo: {self.platillo}'


class Promocion(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.UUIDField(unique=True, auto_created=True)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE, null=False)
    imagen = models.TextField(max_length=500, null=False, blank=False)
    valido_hasta = models.DateTimeField(auto_now_add=False)
    active = models.BooleanField(default=True, null=False)

    class Meta:
        verbose_name = 'Promocion'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return f'Id: {self.id}, Platillo: {self.platillo}, Expiracion: {self.valido_hasta}'


class Cupon(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.UUIDField(unique=True, auto_created=True)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = 'Cupon'
        verbose_name_plural = 'Cupones'
    
    def __str__(self):
        return f'Id: {self.id}, Codigo: {self.codigo}, Promocion: {self.promocion.id}'


class Anuncio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=200, null=False, blank=False)
    anunciante = models.TextField(max_length=200, null=False, blank=False)
    valido_hasta = models.DateTimeField(auto_now_add=False)
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f'Id: {self.id}, Anunciante: {self.id}, Nombre: {self.nombre}'