#Recibe coordenadas para cinematica inversa
#Joint Id      range
#    1 	    -168 ~ 168
#    2 	    -50 ~ 135
#    3 	    -130 ~ 110
#    4 	    -145 ~ 55
#    5 	    -155 ~ 50
#    6 	    -180 ~ 180

import zmq
from pymycobot import MyCobot280
import time
import numpy as np
import math

class robot:
    def __init__(self,modo:int=1, port:str='/dev/ttyUSB0', bps:int=1000000, port_sim:int=5557):
        """_summary_

        Args:
            modo (int, optional): Set mode: 1 robot is connected, 2 test, 3 simulation. Defaults to 1.
            port (str, optional): _description_. Defaults to '/dev/ttyUSB0'.
            bps (int, optional): _description_. Defaults to 1000000.
            port_sim (int, optional): _description_. Defaults to 5557.
        """
        self.q_ini = np.deg2rad(np.array([0, 90, 0, -90, -90, 0]))
        self.robotMode = modo
        
        if modo == 1:
            self.mc = MyCobot280(port, bps)
            print('Iniciando MyCobot280')
            
            if self.mc.is_power_on() == 0:
                self.mc.power_on()
            time.sleep(2)
            
            print('\tRobot correction version', self.mc.get_modify_version())
            print('\tSystem version', self.mc.get_system_version())
            
            self.mc.send_angles([0, 90, 0, -90, -90, 0], 30)
            while self.mc.is_moving():
                pass
            
            print('MyCobot280 listo')
            
        elif modo == 2:
            print("Modo prueba, sin robot")
        elif modo == 3 or modo == 4:
            print("Simulación")
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.PUB)
            self.socket.bind(f"tcp://*:{port_sim}")
        else:
            raise ValueError("Modo no válido")
            
      
    def fwd_k(self, q_1:float, q_2:float, q_3:float, q_4:float, q_5:float, q_6:float) -> np.ndarray:
        """Cinematica directa de MyCobot280

        Args:
            q_1 (float): theta_1
            q_2 (float): theta_2
            q_3 (float): theta_3
            q_4 (float): theta_4
            q_5 (float): theta_5
            q_6 (float): theta_6

        Returns:
            np.ndarray: Matriz 3x4 R|T
        """
        t2 = math.cos(q_1)
        t3 = math.cos(q_2)
        t4 = math.cos(q_3)
        t5 = math.cos(q_4)
        t6 = math.cos(q_5)
        t7 = math.cos(q_6)
        t8 = math.sin(q_1)
        t9 = math.sin(q_2)
        t10 = math.sin(q_3)
        t11 = math.sin(q_4)
        t12 = math.sin(q_5)
        t13 = math.sin(q_6)
        t14 = t3*t4
        t15 = t3*t10
        t16 = t4*t9
        t17 = t2*t12
        t18 = t9*t10
        t19 = t8*t12
        t20 = t8*t18
        t21 = -t18
        t22 = t2*t14
        t23 = t2*t15
        t24 = t2*t16
        t25 = t8*t14
        t26 = t2*t18
        t27 = t8*t15
        t28 = t8*t16
        t31 = t15+t16
        t29 = -t25
        t30 = t2*t21
        t32 = t14+t21
        t33 = t5*t31
        t34 = t11*t31
        t35 = t23+t24
        t36 = t27+t28
        t37 = t5*t32
        t38 = t11*t32
        t40 = t22+t30
        t41 = t20+t29
        t42 = t5*t35
        t43 = t11*t35
        t44 = t5*t36
        t45 = t11*t36
        t46 = t5*t40
        t47 = t11*t40
        t49 = t5*t41
        t50 = t11*t41
        t52 = t33+t38
        t51 = -t50
        t54 = t42+t47
        t55 = t45+t49
        t61 = t6*(t43-t46)
        t57 = t44+t51
        t58 = t6*t55
        t63 = t19+t61
        t60 = -t58
        t62 = t17+t60
        mt1 = [t13*t54-t7*t63,t7*t62+t13*t57,t13*(t34-t37)+t6*t7*t52,t7*t54+t13*t63,t7*t57-t13*t62,t7*(t34-t37)-t6*t13*t52,-t6*t8+t12*(t43-t46),t2*t6+t12*t55,-t12*t52,t8*(3.17e+2/5.0)+t22*9.6e+1-t26*9.6e+1-t42*7.505e+1-t47*7.505e+1+t2*t3*1.1e+2-t6*t8*(2.28e+2/5.0)+t12*(t43-t46)*(2.28e+2/5.0)]
        mt2 = [t2*(-3.17e+2/5.0)-t20*9.6e+1+t25*9.6e+1-t44*7.505e+1+t50*7.505e+1+t2*t6*(2.28e+2/5.0)+t3*t8*1.1e+2+t12*t55*(2.28e+2/5.0),t9*1.1e+2+t31*9.6e+1-t34*7.505e+1+t37*7.505e+1-t12*t52*(2.28e+2/5.0)+5.39e+2/4.0]
        return np.reshape(mt1 + mt2, (3, 4), order='F')
    
    def jaco_num(self,fwd_func, q, delta=1e-6):
        """
        Calcula el Jacobiano numéricamente usando diferencias finitas
        fwd_func: función de cinemática directa que retorna array (3,4)
        q: array de 6 valores articulares
        delta: perturbación pequeña
        """
        # Evaluar la posición actual
        f0 = fwd_func(*q).flatten()
        jac = np.zeros((12, 6))  # Jacobiano 12x6
        
        for i in range(6):
            # Perturbar la articulación i
            q_perturbed = q.copy()
            q_perturbed[i] += delta
            
            # Evaluar la posición perturbada
            f_perturbed = fwd_func(*q_perturbed).flatten()
            
            # Calcular derivada numérica (Jacobiano columna i)
            jac[:, i] = (f_perturbed - f0) / delta
        
        return jac
    
    def inv_k(self, orientacion = 0, x=45.6000, y=-63.4000, z=415.8000):
        # Definir la matriz xd
        xd = np.array([
            [0, 0, 1, x],
            [-1, 0, 0, y], 
            [0, -1, 0, z]
        ])
        # Convertir ángulos de grados a radianes
        q_k = self.q_ini

        epsi = 1e-3  # tolerancia en la solución "Error"

        # Límites de movimiento en radianes
        limAng = np.deg2rad(np.array([
            [-168, 168],   # Límites para joint 1
            [-50, 135],   # Límites para joint 2
            [-130, 110],   # Límites para joint 3
            [-145, 55],   # Límites para joint 4
            [-155, 50],   # Límites para joint 5
            [-180, 180]    # Límites para joint 6
        ]))

        ok = False

        for _ in range(1000):  # Comienza cálculo
            # Establece los límites de movimiento
            for i in range(6):
                if q_k[i] > limAng[i, 1] or q_k[i] < limAng[i, 0]:
                    q_k[i] = np.sum(limAng[i, :]) / 2
            
            fwd = self.fwd_k(q_k[0], q_k[1], q_k[2], q_k[3], q_k[4], q_k[5])
            
            error = xd.flatten() - fwd.flatten()
            
            if np.linalg.norm(error) < epsi:
                # print('Funcionó')
                ok = True
                break
            
            J = self.jaco_num(self.fwd_k, q_k)
            Jinv = np.linalg.pinv(J)
            #Jinv = np.linalg.pinv(self.jaco(q_k[0], q_k[1], q_k[2], q_k[3], q_k[4], q_k[5]))
            q_k = q_k + Jinv @ error
            
            # Encierra los ángulos en [-pi, pi]
            for i in range(6):
                while True:
                    if q_k[i] > 2 * np.pi:
                        q_k[i] = q_k[i] % (2 * np.pi)
                        if q_k[i] > np.pi:
                            q_k[i] = q_k[i] - 2 * np.pi
                    elif q_k[i] < -2 * np.pi:
                        q_k[i] = q_k[i] % (-2 * np.pi)
                        if q_k[i] < -np.pi:
                            q_k[i] = q_k[i] + 2 * np.pi
                    else:
                        break
        if ok:
            self.q_ini = q_k
            if self.robotMode == 1:
                q_k = np.rad2deg(q_k)
                self.mc.send_angles([q_k[0], q_k[1], q_k[2], q_k[3], q_k[4], q_k[5]], 50)
                while self.mc.is_moving():
                    pass
            elif self.robotMode == 3 or self.robotMode == 4:
                mensaje = {
                    "q0": q_k[0],
                    "q1": q_k[1],
                    "q2": q_k[2],
                    "q3": q_k[3],
                    "q4": q_k[4],
                    "q5": q_k[5],
                    "timestamp": time.time()
                }
                self.socket.send_json(mensaje)
            return True
        else:
            return False
        
if __name__ == "__main__":
    try:
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt(zmq.CONFLATE, 1)
        socket.connect("tcp://localhost:5556")
        socket.subscribe("")  # Suscribirse a todos los mensajes
        rob = robot(3)
        while True:
            if rob.robotMode == 2 or rob.robotMode == 4:
                x, y, z = map(float, input("Ingresar coordenada: ").split())
            else:
                mensaje = socket.recv_json()
                x = mensaje["x"]
                y = mensaje["y"]
                z = mensaje["z"]
                timestamp = mensaje["timestamp"]
            
            if rob.inv_k(x=45.6+x, y=-63.4+y, z=415.8+z):
                #print(timestamp)
                pass
            
    except KeyboardInterrupt:
        print("\nInterrumpido")
        
    finally:
        if rob.robotMode == 1:
            print("Apagando Robot...")
            rob.mc.send_angles([0, 135, -120, 30, -90, 0], 100)
            while rob.mc.is_moving():
                pass
            rob.mc.power_off()
            time.sleep(1)
            rob.mc.close()
        elif rob.robotMode == 3:
            rob.socket.close()
            rob.context.term()
        socket.close()
        context.term()