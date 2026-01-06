import pyautogui
import numpy as np
from time import sleep

class MouseController:
    def __init__(self, smoothing=0.5, screen_margin=50):
        self.prev_x = 0
        self.prev_y = 0
        self.smoothing = smoothing
        self.screen_margin = screen_margin
        self.last_click_time = 0
        self.click_cooldown = 0.5  # Seconds between clicks
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = False  # We'll implement our own safety checks
        pyautogui.PAUSE = 0.01      # Reduce delay between commands
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Define safe boundaries
        self.min_x = self.screen_margin
        self.max_x = self.screen_width - self.screen_margin
        self.min_y = self.screen_margin
        self.max_y = self.screen_height - self.screen_margin
        
    def move(self, x, y, smooth=True):
        # Ensure coordinates are within safe boundaries
        x = np.clip(x, self.min_x, self.max_x)
        y = np.clip(y, self.min_y, self.max_y)
        
        if smooth:
            # Apply smoothing
            x = int(x * self.smoothing + self.prev_x * (1 - self.smoothing))
            y = int(y * self.smoothing + self.prev_y * (1 - self.smoothing))
        
        try:
            pyautogui.moveTo(x, y)
            self.prev_x, self.prev_y = x, y
        except Exception as e:
            print(f"Mouse movement error: {e}")
    
    def can_click(self):
        current_time = pyautogui.time.time()
        if current_time - self.last_click_time >= self.click_cooldown:
            self.last_click_time = current_time
            return True
        return False
            
    def left_click(self):
        try:
            if (self.min_x < self.prev_x < self.max_x and 
                self.min_y < self.prev_y < self.max_y and 
                self.can_click()):
                pyautogui.click(button='left')
                return True
        except Exception as e:
            print(f"Left click error: {e}")
        return False

    def right_click(self):
        try:
            if (self.min_x < self.prev_x < self.max_x and 
                self.min_y < self.prev_y < self.max_y and 
                self.can_click()):
                pyautogui.click(button='right')
                return True
        except Exception as e:
            print(f"Right click error: {e}")
        return False
            
    def map_coordinates(self, x, y, input_width, input_height):
        """Map coordinates from input space (e.g., webcam) to screen space"""
        screen_x = np.interp(x, [0, input_width], [self.min_x, self.max_x])
        screen_y = np.interp(y, [0, input_height], [self.min_y, self.max_y])
        return int(screen_x), int(screen_y)