from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Clase de formulario de registro.
    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1',
                  'password2']
