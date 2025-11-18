# Prueba de publicador con ZMQ modo pub-sub
import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556") # Comunicación en red local, puerto 5556

print("📡 Publicador iniciado - Transmitiendo datos...")

contador = 0
while contador < 20:
    # Generar 3 floats
    datos = [
        random.uniform(0.0, 1.0),
        random.uniform(-1.0, 1.0),
        random.uniform(10.0, 20.0)
    ]
    
    mensaje = {
        "contador": contador,
        "datos": datos,
        "timestamp": time.time()
    }
    
    socket.send_json(mensaje)
    print(f"📤 Publicado #{contador}: {datos}")
    
    contador += 1
    time.sleep(0.5)  # Más rápido

print("🏁 Publicador terminado")