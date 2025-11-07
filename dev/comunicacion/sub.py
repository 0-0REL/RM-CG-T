# suscriptor.py
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
socket.subscribe("")  # Suscribirse a todos los mensajes

print("👂 Suscriptor iniciado - Escuchando datos...")

try:
    while True:
        mensaje = socket.recv_json()
        datos = mensaje["datos"]
        contador = mensaje["contador"]
        
        print(f"📥 Recibido #{contador}: x={datos[0]:.4f}, y={datos[1]:.4f}, z={datos[2]:.4f}")
        
except KeyboardInterrupt:
    print("\n🛑 Suscriptor terminado por usuario")