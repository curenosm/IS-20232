from django.shortcuts import render, HttpResponse

from .models import *


# Create your views here.
def index(request):

    # Realizamos las consultas
    all_estudiantes = Estudiante.objects.all()
    estudiantes_grupo_1 = Estudiante.objects.filter(grupo=1)
    estudiantes_grupo_4 = Estudiante.objects.filter(grupo=4)
    mismo_apellido = {}
    misma_edad = {}
    misma_edad_grupo_3 = {}

    # Agrupamos los resultados
    for estudiante in all_estudiantes:

        # Por apellido
        if mismo_apellido.get(estudiante.apellidos):
            mismo_apellido[estudiante.apellidos].append(estudiante)
        else:
            mismo_apellido[estudiante.apellidos] = [estudiante]

        # Por edad
        if misma_edad.get(estudiante.edad):
            misma_edad[estudiante.edad].append(estudiante)
        else:
            misma_edad[estudiante.edad] = [estudiante]

        # Estudiantes grupo 3
        if estudiante.grupo.id_grupo == 3:
            
            # Por edad
            if misma_edad_grupo_3.get(estudiante.edad):
                misma_edad_grupo_3[estudiante.edad].append(estudiante)
            else:
                misma_edad_grupo_3[estudiante.edad] = [estudiante]

    mas_de_uno = lambda l: len(l) > 1

    # Las hacemos listas de listas, para imprimirlos mas facilm
    mismo_apellido     = filter(mas_de_uno, mismo_apellido.values())
    misma_edad         = filter(mas_de_uno, misma_edad.values())
    misma_edad_grupo_3 = filter(mas_de_uno, misma_edad_grupo_3.values())
    
    contexto = {
        'estudiantes_grupo_1': estudiantes_grupo_1,
        'estudiantes_grupo_4': estudiantes_grupo_4,
        'mismo_apellido': mismo_apellido,
        'misma_edad': misma_edad,
        'misma_edad_grupo_3': misma_edad_grupo_3,
        'all_estudiantes': all_estudiantes
    }

    return render(request, 'index.html', context=contexto)
