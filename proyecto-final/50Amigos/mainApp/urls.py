from django.urls import path

from . import views

app_name = "mainApp"
urlpatterns = [
    path('', views.index, name='index'),
    path('carrito', views.CarritoView.as_view(), name='carrito'),
    path('orden', views.OrdenView.as_view(), name='orden'),
    path('contacto', views.contacto, name='contacto'),
    path('helados', views.get_lista_helados, name='lista_helados'),
    path('inicio', views.inicio_comensal, name='inicio'),
    path('menu', views.menu, name='menu'),
    path('registro', views.registro, name='registro'),
    path('votacion', views.votacion, name='votacion'),
]
