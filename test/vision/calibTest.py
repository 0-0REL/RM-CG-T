import cv2
import numpy as np

# Tus parámetros
camera_matrix = np.array([
    [526.48134479, 0.0, 299.12153832],
    [0.0, 525.59203794, 231.6123197],
    [0.0, 0.0, 1.0]
])

dist_coeffs = np.array([[-0.01308301, 0.03617054, 0.00575928, -0.00136356, -0.00339902]])

import cv2
import numpy as np

# Tus parámetros de calibración
camera_matrix = np.array([
    [526.48134479, 0.0, 299.12153832],
    [0.0, 525.59203794, 231.6123197],
    [0.0, 0.0, 1.0]
])

dist_coeffs = np.array([[-0.01308301, 0.03617054, 0.00575928, -0.00136356, -0.00339902]])

def corregir_distorsion(imagen, camera_matrix, dist_coeffs):
    """
    Corrige la distorsión de una imagen usando los parámetros de calibración
    
    Args:
        imagen: Imagen distorsionada
        camera_matrix: Matriz de cámara
        dist_coeffs: Coeficientes de distorsión
    
    Returns:
        imagen_corregida: Imagen sin distorsión
    """
    h, w = imagen.shape[:2]
    
    # Método 1: Corrección directa
    imagen_corregida = cv2.undistort(imagen, camera_matrix, dist_coeffs)
    
    return imagen_corregida

# Método alternativo con mapa de corrección (más eficiente para video)
def inicializar_mapa_correccion(camera_matrix, dist_coeffs, tamaño_imagen):
    """
    Inicializa el mapa de corrección (útil para video en tiempo real)
    """
    h, w = tamaño_imagen
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, dist_coeffs, (w, h), 1, (w, h)
    )
    
    mapx, mapy = cv2.initUndistortRectifyMap(
        camera_matrix, dist_coeffs, None, new_camera_matrix, (w, h), cv2.CV_32FC1
    )
    
    return mapx, mapy, roi

def corregir_distorsion_rapida(imagen, mapx, mapy, roi):
    """
    Corrección rápida usando mapa precalculado
    """
    imagen_corregida = cv2.remap(imagen, mapx, mapy, cv2.INTER_LINEAR)
    x, y, w, h = roi
    imagen_recortada = imagen_corregida[y:y+h, x:x+w]
    
    return imagen_recortada

# Para imágenes individuales
def procesar_imagen(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("Error: No se pudo cargar la imagen")
        return
    
    imagen_corregida = cv2.undistort(imagen, camera_matrix, dist_coeffs)
    
    # Mostrar comparación
    cv2.imshow('Original (Distorsionada)', imagen)
    cv2.imshow('Corregida', imagen_corregida)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Para video en tiempo real (más eficiente)
cap = cv2.VideoCapture(0)

# Precalcular mapa de corrección (solo una vez)
ret, frame = cap.read()
if ret:
    h, w = frame.shape[:2]
    mapx, mapy, roi = inicializar_mapa_correccion(camera_matrix, dist_coeffs, (w, h))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Corrección rápida
        #frame_corregido = corregir_distorsion_rapida(frame, mapx, mapy, roi)
        frame_corregido = corregir_distorsion(frame, camera_matrix, dist_coeffs)
        
        cv2.imshow('Original', frame)
        cv2.imshow('Sin Distorsion', frame_corregido)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()