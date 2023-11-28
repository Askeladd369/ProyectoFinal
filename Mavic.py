from controller import Robot
import sys

try:
    import numpy as np
except ImportError:
    sys.exit("Warning: 'numpy' module not found.")

# Función para limitar un valor dentro de un rango específico
def clamp(value, value_min, value_max):
    return min(max(value, value_min), value_max)

class Mavic(Robot):
    # Constantes de control para el dron
    K_VERTICAL_THRUST = 68.5  # Constante de empuje vertical que eleva el dron
    K_VERTICAL_OFFSET = 0.6  # Desplazamiento vertical para estabilización
    K_VERTICAL_P = 3.0  # P vertical
    K_ROLL_P = 50.0  # P roll
    K_PITCH_P = 30.0  # P pitch

    MAX_YAW_DISTURBANCE = 0.4  # Máxima perturbación de yaw permitida
    MAX_PITCH_DISTURBANCE = -1  # Máxima perturbación de pitch permitida

    # Precisión de la posición objetivo
    target_precision = 0.5

    def __init__(self):
        Robot.__init__(self)

        # Configuración inicial del robot
        self.time_step = int(self.getBasicTimeStep())
        self.camera = self.getDevice("camera")
        self.camera.enable(self.time_step)
        # Sensores y actuadores
        self.imu = self.getDevice("inertial unit")
        self.imu.enable(self.time_step)
        self.gps = self.getDevice("gps")
        self.gps.enable(self.time_step)
        self.gyro = self.getDevice("gyro")
        self.gyro.enable(self.time_step)
        self.front_left_motor = self.getDevice("front left propeller")
        self.front_right_motor = self.getDevice("front right propeller")
        self.rear_left_motor = self.getDevice("rear left propeller")
        self.rear_right_motor = self.getDevice("rear right propeller")
        self.camera_pitch_motor = self.getDevice("camera pitch")
        self.camera_pitch_motor.setPosition(0.7)

        # Configuración de los motores
        motors = [self.front_left_motor, self.front_right_motor,
                  self.rear_left_motor, self.rear_right_motor]
        for motor in motors:
            motor.setPosition(float('inf'))
            motor.setVelocity(1)

        # Estado inicial del robot
        self.current_pose = [0, 0, 0, 0, 0, 0]  # X, Y, Z, yaw, pitch, roll
        self.target_position = [0, 0, 0]
        self.target_index = 0
        self.target_altitude = 0

    def set_position(self, pos):
        # Establece la posición del robot
        self.current_pose = pos

    def move_to_target(self, waypoints, verbose_movement=False, verbose_target=False):
        # Mueve el robot a las coordenadas indicadas
        # Devuelve (float): perturbación de pitch (valor negativo para avanzar)

        # Configuración del primer objetivo si aún no está establecido
        if self.target_position[0:2] == [0, 0]:
            self.target_position[0:2] = waypoints[0]
            if verbose_target:
                print("Primer objetivo: ", self.target_position[0:2])

        # Verificación de si el robot ha alcanzado el objetivo
        if all([abs(x1 - x2) < self.target_precision for (x1, x2) in zip(self.target_position, self.current_pose[0:2])]):
            self.target_index += 1
            if self.target_index > len(waypoints) - 1:
                self.target_index = 0
            self.target_position[0:2] = waypoints[self.target_index]
            if verbose_target:
                print("¡Objetivo alcanzado! Nuevo objetivo: ", self.target_position[0:2])

        # Cálculo de la orientación hacia el objetivo
        self.target_position[2] = np.arctan2(
            self.target_position[1] - self.current_pose[1], self.target_position[0] - self.current_pose[0])

        # Cálculo de la diferencia angular hacia el objetivo
        angle_left = self.target_position[2] - self.current_pose[5]
        angle_left = (angle_left + 2 * np.pi) % (2 * np.pi)
        if (angle_left > np.pi):
            angle_left -= 2 * np.pi

        # Cálculo de la perturbación de yaw
        yaw_disturbance = self.MAX_YAW_DISTURBANCE * angle_left / (2 * np.pi)

        # Cálculo de la perturbación de pitch
        pitch_disturbance = clamp(
            np.log10(abs(angle_left)), self.MAX_PITCH_DISTURBANCE, 0.1)

        # Impresión de información de movimiento si se solicita
        if verbose_movement:
            distance_left = np.sqrt(((self.target_position[0] - self.current_pose[0]) ** 2) + (
                (self.target_position[1] - self.current_pose[1]) ** 2))
            print("ángulo restante: {:.4f}, distancia restante: {:.4f}".format(
                angle_left, distance_left))
        return yaw_disturbance, pitch_disturbance

    def run(self):
        # Función principal que ejecuta el comportamiento del robot
        t1 = self.getTime()

        roll_disturbance = 0
        pitch_disturbance = 0
        yaw_disturbance = 0

        # Definición de la trayectoria deseada
        waypoints = [[6, 2], [0, 2], [0, 4], [7, 4], [1, 1]]
        self.target_altitude = 1

        while self.step(self.time_step) != -1:
            # Lectura de sensores
            roll, pitch, yaw = self.imu.getRollPitchYaw()
            x_pos, y_pos, altitude = self.gps.getValues()
            roll_acceleration, pitch_acceleration, _ = self.gyro.getValues()
            self.set_position([x_pos, y_pos, altitude, roll, pitch, yaw])

            # Verificación de la altitud y movimientos a realizar
            if altitude > self.target_altitude - 1:
                if self.getTime() - t1 > 0.1:
                    yaw_disturbance, pitch_disturbance = self.move_to_target(
                        waypoints)
                    t1 = self.getTime()

            # Cálculo de las entradas de los motores
            roll_input = self.K_ROLL_P * clamp(roll, -1, 1) + roll_acceleration + roll_disturbance
            pitch_input = self.K_PITCH_P * clamp(pitch, -1, 1) + pitch_acceleration + pitch_disturbance
            yaw_input = yaw_disturbance
            clamped_difference_altitude = clamp(self.target_altitude - altitude + self.K_VERTICAL_OFFSET, -1, 1)
            vertical_input = self.K_VERTICAL_P * pow(clamped_difference_altitude, 3.0)

            front_left_motor_input = self.K_VERTICAL_THRUST + vertical_input - yaw_input + pitch_input - roll_input
            front_right_motor_input = self.K_VERTICAL_THRUST + vertical_input + yaw_input + pitch_input + roll_input
            rear_left_motor_input = self.K_VERTICAL_THRUST + vertical_input + yaw_input - pitch_input - roll_input
            rear_right_motor_input = self.K_VERTICAL_THRUST + vertical_input - yaw_input - pitch_input + roll_input

            # Establecimiento de las velocidades de los motores
            self.front_left_motor.setVelocity(front_left_motor_input)
            self.front_right_motor.setVelocity(-front_right_motor_input)
            self.rear_left_motor.setVelocity(-rear_left_motor_input)
            self.rear_right_motor.setVelocity(rear_right_motor_input)

            # Detención y aterrizaje al alcanzar el último objetivo
            if self.target_index == len(waypoints) - 1:
                print("Último objetivo alcanzado. Deteniendo y aterrizando.")
                self.front_left_motor.setVelocity(0)
                self.front_right_motor.setVelocity(0)
                self.rear_left_motor.setVelocity(0)
                self.rear_right_motor.setVelocity(0)
                self.target_altitude -= 0.01

                if altitude < 0.1:
                    print("Dron aterrizado. Terminando la simulación.")
                    break

# Crear una instancia del robot y ejecutar el comportamiento
robot = Mavic()
robot.run()
