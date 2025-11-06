import cv2
import os

# Crear directorio para fotos si no existe
if not os.path.exists('test/fotos'):
    os.makedirs('fotos')

cam = cv2.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not cam.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

print('Presiona "q" para tomar foto y salir')
print('Presiona "ESC" para salir sin tomar foto')

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Fallo al capturar imagen de la cámara")
        break
    #frame = cv2.flip(frame,1)
    cv2.imshow('Camara', frame)
    
    # Esperar por tecla (1ms) y verificar
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):  # Presionar 'q' para tomar foto y salir
        # Guardar la foto
        cv2.imwrite('test/fotos/foto4.jpg', frame)
        print("Foto guardada en 'fotos/foto.jpg'")
        break
    elif key == 27:  # Presionar ESC para salir sin tomar foto
        print("Saliendo sin tomar foto")
        break

# Liberar recursos
cam.release()
cv2.destroyAllWindows()