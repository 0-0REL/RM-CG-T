"""
Deteccion de dibuja puntos de la mano en vivio
"""

import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

CAMARA = cv2.VideoCapture(0)

MODEL = os.path.abspath('src/hand_landmarker.task')
BASE_OPTIONS = python.BaseOptions(model_asset_path=MODEL)

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)

def draw_landmarks_on_image(rgb_image, detection_result):
    if detection_result is None:
        return rgb_image
        
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style())

        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image

# Modo IMAGE (más simple, sincrónico)
OPTIONS = vision.HandLandmarkerOptions(
    base_options=BASE_OPTIONS,
    num_hands=2,
    running_mode=mp.tasks.vision.RunningMode.IMAGE
)
DETECTOR = vision.HandLandmarker.create_from_options(OPTIONS)

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
        annotated_image = draw_landmarks_on_image(rgb_frame, detection_result)
        
        # Convertir de vuelta a BGR para mostrar
        display_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        cv2.imshow('Hand Tracking', cv2.flip(display_image, 1))
        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
finally:
    CAMARA.release()
    cv2.destroyAllWindows()
    DETECTOR.close()