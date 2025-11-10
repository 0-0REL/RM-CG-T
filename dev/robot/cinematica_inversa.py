import zmq
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.subscribe("")  # Suscribirse a todos los mensajes

print("👂 Suscriptor iniciado - Escuchando datos...")

try:
    while True:
        mensaje = socket.recv_json()
        x = mensaje["x"]
        y = mensaje["y"]
        z = mensaje["z"]
                
        
except KeyboardInterrupt:
    print("\n🛑 Suscriptor terminado por usuario")