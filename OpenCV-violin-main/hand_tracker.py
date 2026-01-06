import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.landmark_positions = []

    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = self.hands.process(rgb_frame)
        
        # Clear previous positions
        self.landmark_positions = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on frame
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Store landmark positions
                positions = []
                for landmark in hand_landmarks.landmark:
                    height, width, _ = frame.shape
                    x, y = int(landmark.x * width), int(landmark.y * height)
                    positions.append((x, y))
                self.landmark_positions.append(positions)

        return frame, self.landmark_positions

    def get_pointer_position(self):
        """Returns the position of the index finger tip (landmark 8)"""
        if self.landmark_positions and len(self.landmark_positions[0]) > 8:
            return self.landmark_positions[0][8]
        return None

    def get_hand_height(self):
        """Calculate the relative height of the hand in the frame"""
        if self.landmark_positions and len(self.landmark_positions[0]) > 0:
            y_coordinates = [y for _, y in self.landmark_positions[0]]
            min_y = min(y_coordinates)
            max_y = max(y_coordinates)
            return max_y - min_y
        return 0

    def release(self):
        """Release resources"""
        self.hands.close()