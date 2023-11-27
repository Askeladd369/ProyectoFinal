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

![Importaciones y manejo de dependencias](https://github.com/Askeladd369/ProyectoFinal/blob/main/1.png)

Importa la clase Robot del módulo controller para controlar el robot en la simulación.
Intenta importar la biblioteca NumPy para operaciones numéricas y maneja la excepción si no puede importarse.

![Función de clamp](https://github.com/Askeladd369/ProyectoFinal/blob/main/2.png)

Define una función clamp que limita un valor dentro de un rango específico.

![Clase Mavic que hereda de Robot](https://github.com/Askeladd369/ProyectoFinal/blob/main/3.png)

Define una clase Mavic que hereda de la clase Robot.
Incluye constantes que representan parámetros de control empíricamente encontrados.

![Método init_de la clase Mavics](https://github.com/Askeladd369/ProyectoFinal/blob/main/4.png)

Inicializa la clase Mavic llamando al constructor de la clase Robot.
Configura y habilita varios dispositivos y motores del dron.

![Método set_position de la clase Mavic](https://github.com/Askeladd369/ProyectoFinal/blob/main/5.png)

Establece la nueva posición absoluta del robot.

![Método move_to_target de la clase Mavic](https://github.com/Askeladd369/ProyectoFinal/blob/main/6.png)

Mueve el robot hacia las coordenadas dadas y proporciona información opcionalmente detallada sobre el movimiento y los objetivos.

![Método run de la clase Mavic](https://github.com/Askeladd369/ProyectoFinal/blob/main/7.png)

Método principal que ejecuta el control del dron en un bucle mientras la simulación está en ejecución.

![Bloque principal](https://github.com/Askeladd369/ProyectoFinal/blob/main/8.png)

Crea una instancia de la clase Mavic.
Ejecuta el método run, que controla el dron en el entorno de simulación

# Resultados
En el siguiente video mostramos el comportamiento del proyecto realizado:

