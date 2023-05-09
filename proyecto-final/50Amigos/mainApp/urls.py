from django.urls import path
from . import views

app_name = "mainApp"
urlpatterns = [
    path('', views.index, name='index'),
    path('registro', views.registro, name='registro'),
    path('inicio', views.inicio_comensal, name='inicio'),
    path('menu', views.menu, name='menu'),
    path('carrito', views.carrito, name='carrito'),
    path('votacion', views.votacion, name='votacion'),
    path('contacto', views.contacto, name='contacto'),
]
