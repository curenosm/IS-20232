# Proyecto Final: 50Amigos


Facultad de Ciencias, UNAM.

---

| **Nombre**                  | **No. de cuenta**  | **Rol** |
|:----------------------------|:------------------:|---------|
| *Almanza Torres José Luis*  |         -          | *Responsable de colaboración* |
| *Bernal Núñez Raúl*         |         -          | *Responsable de calidad* |
| *Cureño Sánchez Misael*     |     418002485      | *Responsable técnico* |
| *Hernández Montoya Ricardo* |         -          | *Responsable del equipo* |


## Instrucciones de ejecución

---

- Dentro de la carpeta base del proyecto ejecutar:

  ```bash
  cd 50Amigos
  conda activate enviro
  python manage.py runserver
  ```



- Util instructions:


  For development
  
    You can execute tests by locating at the same level
    than pytest.ini and executing:
      
      py.test
    
    You can mount the docker image using:

      docker-compose up --build

 For production:
  
    You can mount the docker image using:
    
      docker-compose -f docker-compose.prod.yml up --build
      

  NOTE:
    All documentation associated to this project can be found on the docs/ folder.

## Credenciales

---

Password de los comensales (mesa1, mesa2, mesa3): **restaurante123**