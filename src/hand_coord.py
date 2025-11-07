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
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
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
        
    def wrist_pos(self, mp_image):
        detection_result = self.detector.detect(mp_image)
        handedness_list = detection_result.handedness
        if len(handedness_list) == 0 or handedness_list[0][0].category_name != "Right":
            return False
        wrist_landmarks = detection_result.hand_landmarks[0][0]
        numpy_image = mp_image.numpy_view()
        height, width, _ = numpy_image.shape
        x = int(wrist_landmarks.x * width)
        y = int(wrist_landmarks.y * height)
        return (x, y, 0)

    def draw_wrist(self, image, coords):
        if coords is False:
            return image 
        annotated = np.copy(image)
        cv2.circle(annotated, (coords[0], coords[1]), 10, (0, 255, 0), -1)
        return annotated

try:
    hand = Hand()
    pubHand = Comu()
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        
        # Convertir BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detección sincrónica (retorna el resultado inmediatamente)
        pos = hand.wrist_pos(mp_image)
        # Dibujar landmarks
        annotated_image = hand.draw_wrist(frame, pos)
        pubHand.enviar(pos)
        
        cv2.imshow('Hand Tracking', cv2.flip(annotated_image, 1))
        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
finally:
    cam.release()
    cv2.destroyAllWindows()
    hand.detector.close()