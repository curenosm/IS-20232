from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mainApp.models import *

from .models import (
    User,
)


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


admin.site.register(User, CustomUserAdmin)

# Register your models here.
admin.site.register(Platillo)
admin.site.register(Categoria)