# Proyecto Final: 50Amigos


Facultad de Ciencias, UNAM.

---

| **Nombre**                  | **No. de cuenta**  | **Rol** |
|:----------------------------|:------------------:|---------|
| *Almanza Torres José Luis*  |     318184140      | *Responsable de colaboración* |
| *Bernal Núñez Raúl*         |     318224187      | *Responsable de calidad* |
| *Cureño Sánchez Misael*     |     418002485      | *Responsable técnico* |


## Instrucciones de ejecución

---

- Crear y activar ambiente virtual con *conda*

    ```bash
    conda create --name orion-enviro python=3
    conda activate orion-enviro
    ```

- Instalar dependencias.

    ```bash
    cd ./proyecto_final/50Amigos
    pip install -f requirements.txt
    ```

- Para ejecutar las pruebas unitarias:

  ```bash
  cd 50Amigos
  conda activate enviro
  python manage.py test -v 2 --parallel auto

  # o bien

  py.test
  ```

- Para ejecutar el coverage report:

  ```bash
  cd 50Amigos
  conda activate enviro
  coverage run manage.py test -v 2 --parallel auto
  coverage html

  # Luego podremos consultar el index.html dentro de la
  # carpeta htmlcov.
  ```

- Para ejecutar el proyecto ejecutar:

  ```bash
  cd 50Amigos
  conda activate enviro
  python manage.py runserver
  ```

- O bien con `docker-compose` desde la raíz del proyecto:

  ```bash
  docker-compose up --build

  # o bien

  docker-compose build --no-cache
  docker-compose up
  docker-compose logs
  ```

  **Notas**:
  
    - Para correr usando docker y docker-compose son necesarias las versiones:

      ```
      Docker version 20.10.21
      Docker Compose version v2.13.0
      ```

    - La documentación asociada a este proyecto se encuentra dentro
  de la carpeta `docs` y si por alguna razón se desea los archivos fuente de
  los diagramas UML, este proceso puede realizarse sin problema instalando
  *StarUML*.

<br>


## Credenciales

---

```bash
# Usuario administrador
Username: admin
Password: admin


# Usuarios comensales
Username: mesa1
Password: restaurante123

Username: mesa2
Password: restaurante123

Username: mesa3
Password: restaurante123

Username: mesa4
Password: restaurante123
```