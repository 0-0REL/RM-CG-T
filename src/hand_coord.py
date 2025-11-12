"""
07-11-2025
@0-0REL
Envia posicion de muñeca, coodendas cartecianas objetivo del robot
"""

import os
import time
import zmq
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

cam = cv2.VideoCapture(0)

class Comu:
    def __init__(self, port = 5556):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")
    def enviar(self, msg):
        if msg is False:
            return
        coordenadas = {
            "timestamp": time.time(),
            "x": msg[0],
            "y": msg[1],
            "z": msg[2] 
        }
        self.socket.send_json(coordenadas)

class Hand:
    def __init__(self):
        MODEL = os.path.abspath('src/hand_landmarker.task')
        BASE_OPTIONS = python.BaseOptions(model_asset_path=MODEL)
        # Modo IMAGE (más simple, sincrónico)
        OPTIONS = vision.HandLandmarkerOptions(
            base_options=BASE_OPTIONS,
            num_hands=1,
            running_mode=mp.tasks.vision.RunningMode.IMAGE
        )
        self.detector = vision.HandLandmarker.create_from_options(OPTIONS)
        self.fx = 526.48134479
        self.fy = 525.59203794
        self.cx = 299.12153832
        self.cy = 231.6123197
        
    def wrist_pos(self, mp_image):
        detection_result = self.detector.detect(mp_image)
        handedness_list = detection_result.handedness
        if len(handedness_list) == 0 or handedness_list[0][0].category_name != "Right":
            return False
        wrist_landmarks = detection_result.hand_landmarks[0][0]
        wrist_landmarks_w = detection_result.hand_world_landmarks[0][0]
        numpy_image = mp_image.numpy_view()
        height, width, _ = numpy_image.shape
        x = int(wrist_landmarks.x * width)
        y = int(wrist_landmarks.y * height)
        z = wrist_landmarks_w.z * 1000
        return (x, y, z)

    def draw_wrist(self, image, coords):
        if coords is False:
            return image 
        annotated = np.copy(image)
        cv2.circle(annotated, (coords[0], coords[1]), 10, (0, 255, 0), -1)
        return annotated

def euler_to_rotation_matrix(euler_angles):
    """
    Convierte ángulos de Euler [roll, pitch, yaw] a matriz de rotación 3x3
    """
    roll, pitch, yaw = euler_angles
    
    # Matrices de rotación individuales
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])
    
    R_y = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    
    R_z = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])
    
    # Combinar: R = R_z * R_y * R_x
    R = R_z @ R_y @ R_x
    
    return R

def pixel_to_world_simple(coords, camera_matrix, rotation):
    """
    Convierte coordenadas pixel a mundo asumiendo:
    - Cámara en origen (0,0,0) 
    - Mirando hacia Z positivo
    - Sin rotación
    
    Args:
        u, v: coordenadas pixel
        Z_world: profundidad conocida del punto
        camera_matrix: [[fx, 0, cx], [0, fy, cy], [0, 0, 1]]
    """
    fx = camera_matrix[0, 0]
    fy = camera_matrix[1, 1]
    cx = camera_matrix[0, 2]
    cy = camera_matrix[1, 2]
    
    X = (coords[0] - cx) * coords[2] / fx
    Y = (coords[1] - cy) * coords[2] / fy
    
    p_c = np.array([X, Y, coords[2]])
    
    p_w = rotation @ p_c
    
    return p_w

try:
    calib_data = np.load('dev/vision/calib_cam_lap.npz')
    K = calib_data['mtx']
    rot = euler_to_rotation_matrix(np.array([np.pi/2, 0, -np.pi/2]))
    #rot = euler_to_rotation_matrix(np.array([0, 0, 0]))
    hand = Hand()
    pubHand = Comu()
    # Posición de la cámara en el mundo [x, y, z]
    camera_position = np.array([0, 0, 0])  # 1 metro de altura

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        
        # Convertir BGR a RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Detección sincrónica (retorna el resultado inmediatamente)
        pos = hand.wrist_pos(mp_image)
        # Dibujar landmarks
        annotated_image = hand.draw_wrist(frame, pos)
          
        if pos != False:
            pos_w = pixel_to_world_simple(pos,K, rot)
            print(pos_w)
            pubHand.enviar(pos_w)
        
        cv2.imshow('Hand Tracking', cv2.flip(annotated_image, 1))
        
        if cv2.waitKey(50) & 0xFF == ord('q'): 
            break
finally:
    cam.release()
    cv2.destroyAllWindows()
    hand.detector.close()
    pubHand.socket.close()
    pubHand.context.term()