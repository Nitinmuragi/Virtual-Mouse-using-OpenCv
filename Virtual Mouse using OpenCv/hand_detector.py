import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
        return img
    
    def find_position(self, img):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            for id, landmark in enumerate(hand.landmark):
                height, width, _ = img.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                landmark_list.append([id, cx, cy])
        return landmark_list
    
    def get_gesture_state(self, landmark_list):
        if len(landmark_list) == 0:
            return False, False, None
            
        # Get finger states
        fingers = []
        if len(landmark_list) >= 21:  
            # Thumb (compare tip with pip)
            if landmark_list[4][1] < landmark_list[3][1]:  # For right hand
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other fingers (compare tip with pip)
            for tip in range(8, 21, 4):  # Index: 8, Middle: 12, Ring: 16, Pinky: 20
                if landmark_list[tip][2] < landmark_list[tip-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                    
        # Detect gestures
        thumb_up = fingers[0] == 1 and sum(fingers[1:]) <= 1  # Thumb up, others down
        last_fingers_up = sum(fingers[3:]) >= 2 and sum(fingers[:2]) == 0  # Last 2-3 fingers up
        
        # Return gesture states and index finger position
        return thumb_up, last_fingers_up, landmark_list[8] if len(landmark_list) >= 9 else None