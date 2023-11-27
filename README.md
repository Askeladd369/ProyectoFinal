# ProyectoFinal
En este proyecto, nos enfocaremos en la programación y simulación de la implementación real de un cuadricóptero diseñado para rociar cultivos. Además de la aplicación específica de rociado. Nuestro objetivo es explorar la automatización de procesos agrícolas mediante la integración de tecnologías robóticas. Esta iniciativa busca no solo mejorar la eficiencia en la aplicación de tratamientos agrícolas, sino también avanzar hacia una mayor automatización de las operaciones en el cultivo.

# Requerimentos
Para replicar este proyecto es necesario contar con lo siguiente:
- Webots Version R2023b
- Utilizar el nodo DJI maverick pro2 que proporciona webots
- Controlador del cuadrotor adjunto en este archivo
  ![DJI NODE WEBOTS](https://github.com/Askeladd369/ProyectoFinal/blob/main/Captura%20de%20pantalla%202023-11-27%20171649.png)


# Metodologia
Creamos un nuevo directorio en webots para nuestro mundo, dentro de el insertaremos los siguientes nodos
- Nodo Floor con texura de pasto
- Nodo DJI mavick pro 2
- Nodo Grupo con los siguientes objetos:
    1. Cat
    2. Dog
    3. Tres Solid con nodo shape de 5x2m y textura de arena
    4. Molino
    5. Granero
    6. House Bungalow
       
![Objetos Utilizados](https://github.com/Askeladd369/ProyectoFinal/blob/main/hola2.png)
       
Una vez posicionado nuestro entorno, dentro del Tree de webots en el nodo WorldInfo modificamos el timestep a 32 e insertamos un nodo damping con valores de 0.5 en el valor lineal y angular, despúes dentro del nodo de nuestro dron cargamos el controlador "ControlerMavic.py" adjunto en este documento. El funcionamiento del codigo es de la siguiente forma:

![Importaciones y manejo de dependencias]()
![Función de clamp]()
![Clase Mavic que hereda de Robot]()
![Método init_de la clase Mavics]()
![Método set_position de la clase Mavic]()
![Método move_to_target de la clase Mavic]()
![OMétodo run de la clase Mavic]()
![Bloque principal]()
