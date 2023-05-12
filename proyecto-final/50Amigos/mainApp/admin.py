from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mainApp.models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2')
            }
        ),
    )


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Platillo)
admin.site.register(Role)
admin.site.register(Orden)
admin.site.register(Pedido)
admin.site.register(Promocion)
admin.site.register(Cupon)
admin.site.register(Anuncio)
