# @0-0REL
# prueba para mover robot con coppelia sim

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time
import math

client = RemoteAPIClient()
sim = client.require('sim')

JOINT = [sim.getObject('/J1'), # Articulaciones
         sim.getObject('/J2'),
         sim.getObject('/J3'),
         sim.getObject('/J4'),
         sim.getObject('/J5'),
         sim.getObject('/J6')]

print('Program started')
sim.startSimulation() # Inicia simulación
for i in range(6):
    sim.setJointTargetPosition(JOINT[i], math.radians(90)) # Mueve articulacion i a 90 grados
    time.sleep(1)
    
print('stopping simulation')
sim.stopSimulation() # Detiene simulación