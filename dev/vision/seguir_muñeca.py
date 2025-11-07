"""
Deteccion de muñeca en vivio
"""

import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

CAMARA = cv2.VideoCapture(0)

MODEL = os.path.abspath('src/hand_landmarker.task')
BASE_OPTIONS = python.BaseOptions(model_asset_path=MODEL)

# Modo IMAGE (más simple, sincrónico)
OPTIONS = vision.HandLandmarkerOptions(
    base_options=BASE_OPTIONS,
    num_hands=1,
    running_mode=mp.tasks.vision.RunningMode.IMAGE
)
DETECTOR = vision.HandLandmarker.create_from_options(OPTIONS)

def draw_wrist(image, result):
    handedness_list = detection_result.handedness
    if len(handedness_list) == 0 or handedness_list[0][0].category_name != "Right":
        return image
    
    wrist_landmarks = result.hand_landmarks[0][0]
    annotated = np.copy(image)
    height, width, _ = annotated.shape
    x = int(wrist_landmarks.x * width)
    y = int(wrist_landmarks.y * height)
    cv2.circle(annotated, (x,y), 10, (0, 255, 0), -1)
    return annotated

try:
    while True:
        ret, frame = CAMARA.read()
        if not ret:
            break
        
        # Convertir BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detección sincrónica (retorna el resultado inmediatamente)
        detection_result = DETECTOR.detect(mp_image)
        
        # Dibujar landmarks
        annotated_image = draw_wrist(frame, detection_result)
        
        cv2.imshow('Hand Tracking', cv2.flip(annotated_image, 1))
        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
finally:
    CAMARA.release()
    cv2.destroyAllWindows()
    DETECTOR.close()