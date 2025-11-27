# @0-0REL
# 26-11-2025
# Simulación en CoppeliaSim

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import zmq

class coppeliaRobot:
    def __init__(self):
        client = RemoteAPIClient()
        self.sim = client.require('sim')
        # Articulaciones
        self.join = [self.sim.getObject('/J1'), 
                    self.sim.getObject('/J2'),
                    self.sim.getObject('/J3'),
                    self.sim.getObject('/J4'),
                    self.sim.getObject('/J5'),
                    self.sim.getObject('/J6')]
        self.sim.startSimulation() # Inicia simulación
        print('Simulation started.')
        
    def mov_rob(self, q):
        self.sim.setJointTargetPosition(cobot.join[0], q["q0"])
        self.sim.setJointTargetPosition(cobot.join[1], q["q1"])
        self.sim.setJointTargetPosition(cobot.join[2], q["q2"])
        self.sim.setJointTargetPosition(cobot.join[3], q["q3"])
        self.sim.setJointTargetPosition(cobot.join[4], q["q4"])
        self.sim.setJointTargetPosition(cobot.join[5], q["q5"])      

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.CONFLATE, 1)
    socket.connect("tcp://localhost:5557")
    socket.subscribe("")  # Suscribirse a todos los mensajes
    cobot = coppeliaRobot()
    try:
        while True:
            mensaje = socket.recv_json()
            cobot.mov_rob(mensaje)
            
    except KeyboardInterrupt:
        print("Interrumpido")
    finally:
        print("Simulation stopping...")
        cobot.sim.stopSimulation() # Detiene simulación
        socket.close()
        context.term()
        print("Simulation stopped.")