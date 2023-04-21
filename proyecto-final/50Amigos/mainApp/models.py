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


class Platillo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.CharField(max_length=1000)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.nombre}'
