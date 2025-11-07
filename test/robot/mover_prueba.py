"""
@REL
prueba para mover robot con coppelia sim
"""
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time
import math

client = RemoteAPIClient()
sim = client.require('sim')

JOINT = [sim.getObject('/J1'),
         sim.getObject('/J2'),
         sim.getObject('/J3'),
         sim.getObject('/J4'),
         sim.getObject('/J5'),
         sim.getObject('/J6')]

print('Program started')
sim.startSimulation()
for i in range(6):
    sim.setJointTargetPosition(JOINT[i], math.radians(90))
    time.sleep(1)
    
print('stopping simulation')
sim.stopSimulation()