"""
Recibe coordenadas para cinematica inversa
Joint Id        range
    1 	    -168 ~ 168
    2 	    -135 ~ 135
    3 	    -150 ~ 150
    4 	    -145 ~ 145
    5 	    -155 ~ 160
    6 	    -180 ~ 180
"""
import zmq
from pymycobot import MyCobot280

mc = MyCobot280('/dev/ttyUSB0')

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.subscribe("")  # Suscribirse a todos los mensajes

print('Iniciando MyCobot...\n',
      'Robot correction version', mc.get_modify_version(), '\n'
      'System version', mc.get_system_version())

mc.send_angles([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 20)
while mc.is_moving():
  pass
print('MyCobot listo')

try:
    while True:
        pass
        
except KeyboardInterrupt:
    print("\n🛑 Suscriptor terminado por usuario")