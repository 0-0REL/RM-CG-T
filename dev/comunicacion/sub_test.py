# Preuba de subscriptor para recibit datos del publicador
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB) # socket tipo subscritor
socket.connect("tcp://localhost:5556") # Red local a puerto 5556
socket.subscribe("")  # Suscribirse a todos los mensajes

print("👂 Suscriptor iniciado - Escuchando datos...")

try:
    while True:
        mensaje = socket.recv_json()
        x = mensaje["x"]
        y = mensaje["y"]
        z = mensaje["z"]
        timestamp = mensaje["timestamp"]
        
        print(f"📥 Recibido #{timestamp}: x={x:.4f}, y={y:.4f}, z={z:.4f}")
        
except KeyboardInterrupt:
    print("\n🛑 Suscriptor terminado por usuario")