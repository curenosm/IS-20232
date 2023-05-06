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
        return f'Id: {self.id}, Nombre: {self.nombre}, Categoria: {self.categoria}'


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

    def __str__(self):
        return f'Id: {self.id}, Usuario: {self.usuario}, Fecha: {self.fecha}'


class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey(Orden, on_delete=models.SET_NULL, null=True)
    platillo = models.ForeignKey(
        Platillo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Id: {self.id}, Orden: {self.orden}, Platillo: {self.platillo}'
