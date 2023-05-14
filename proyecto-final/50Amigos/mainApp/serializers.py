from rest_framework import serializers

from .models import Platillo


class PlatilloSerializer(serializers.ModelSerializer):
    """
    Clase utilizada para convertir fácilmente un objeto de tipo
    platillo en un json.
    """

    class Meta:
        model = Platillo
        fields = [
            'id',
            'nombre',
            'categoria',
            'subcategoria',
            'precio',
            'ingredientes']
