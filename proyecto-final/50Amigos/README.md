# Requerimientos del sistema


- Definir dos roles, administrador y comensal
- Manejar permisos para diferentes roles
- Definir mockup de la interfaz que tendrán las tabletas
- Iniciar sesion mediante usuario y contraseña para los administradores
- El usuario de tipo comensal elige su entrada, plato principal, bebida, etc.
- Una sesión por mesa por lo que deberá haber un numero de mesa y ubicacion dentro del restaurante
- Mostrar todas las secciones para elegir a los comensales.
- Los platillos deberan tener precio, imagen y breve descripcion asi como un boton para agregar a la orden

**Para los administadores:**

- Agregar platillos
- Eliminar platillos
- Editar platillos
- Tipos de platillos: entrada, bebida, plati principal, postre y helado
- Editar el carrito de orden
- Cuando esté lista se envia a la cocina
- Se informa que la orden fue recibida y se muestra la opcion de escoger el sabor de helado para su mesa, por medio de una votación
- Si aún no se quiere elegir el sabor del helado se puede posponer la elección
- Se pueden agregar n comensales por mesa para el sistema de votacion con un boton de +
- Al iniciar la votación se van mostrando los nombres de los comensales y un dropdown que recibe el sabor de helado por el que vota
- Se muestra el resultado de la votacion, si hay empate se elige un sabor aleatoriamente
