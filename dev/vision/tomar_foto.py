import cv2

cam = cv2.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not cam.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

print('Presiona "q" para tomar foto y salir')
print('Presiona "ESC" para salir sin tomar foto')

nfoto = 1
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Fallo al capturar imagen de la cámara")
        break
    #frame = cv2.flip(frame,1)
    cv2.imshow('Camara', cv2.flip(frame, 1))
    
    # Esperar por tecla (1ms) y verificar
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):  # Presionar 'q' para tomar foto y salir
        # Guardar la foto
        cv2.imwrite('test/vision/fotos/cameraCalib/lap_pant/foto5.jpg', frame)
        break
    elif key == ord('s'):  # Presionar 'c' para tomar foto sin salir
        cv2.imwrite(f'test/vision/fotos/cameraCalib/lap_pant/foto{nfoto}.jpg', frame)
        print("Foto guardada")
        nfoto += 1
    elif key == 27:  # Presionar ESC para salir sin tomar foto
        print("Saliendo sin tomar foto")
        break

# Liberar recursos
cam.release()
cv2.destroyAllWindows()