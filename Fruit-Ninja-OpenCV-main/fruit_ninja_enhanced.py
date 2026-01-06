import pygame
import cv2
import math
import os
import numpy as np
from hand_tracking import HandTracker
from game_objects import Fruit, BladeTrail
from game_engine import GameEngine

# Initialize Pygame
pygame.init()

# Get display info
display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h

# Game constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Colors
UI_BLUE = (100, 200, 255)
UI_GOLD = (255, 215, 0)
UI_WHITE = (255, 255, 255)

# Camera preview settings
PREVIEW_SIZE = (320, 240)
PREVIEW_PADDING = 20

class FruitNinja:
    def __init__(self):
        # Create required directories
        for dir_name in ['fruits', 'cursor', 'sounds', 'fonts', 'background']:
            os.makedirs(dir_name, exist_ok=True)
        
        # Initialize display
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Fruit Ninja Ultimate Enhanced")
        self.clock = pygame.time.Clock()
        
        # Calculate scaling factors for different resolutions
        self.update_screen_scaling()
        
        # Initialize game components
        self.engine = GameEngine(self.screen_width, self.screen_height)
        self.hand_tracker = HandTracker()
        self.blade_trail = BladeTrail(self.screen_width, self.screen_height)
        
        # Initialize fruits
        self.fruits = [Fruit(self.screen_width, self.screen_height) for _ in range(5)]
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Create static surfaces
        self.preview_bg = pygame.Surface((PREVIEW_SIZE[0] + 4, PREVIEW_SIZE[1] + 4))
        self.preview_bg.fill(UI_WHITE)
        
        # UI Elements
        try:
            self.font = pygame.font.Font('fonts/ninja.ttf', 36)
            self.small_font = pygame.font.Font('fonts/ninja.ttf', 24)
        except:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
    
    def update_screen_scaling(self):
        # Get current screen dimensions
        if self.is_fullscreen:
            self.screen_width = SCREEN_WIDTH
            self.screen_height = SCREEN_HEIGHT
        else:
            self.screen_width = WINDOW_WIDTH
            self.screen_height = WINDOW_HEIGHT
        
        # Calculate scaling factors
        self.scale_x = self.screen_width / WINDOW_WIDTH
        self.scale_y = self.screen_height / WINDOW_HEIGHT
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.update_screen_scaling()
    
    def scale_position(self, x, y):
        # Scale position from camera space (0-1) to screen space with proper range
        # Add offset to center the movement range
        x = (x - 0.1) * 1.25  # Expand range by 25% and offset by 0.1
        y = (y - 0.1) * 1.25
        
        # Clamp values to 0-1 range
        x = max(0, min(1, x))
        y = max(0, min(1, y))
        
        # Scale to screen coordinates
        return int(x * self.screen_width), int(y * self.screen_height)
    
    def frame_to_surface(self, frame):
        try:
            # Resize frame for preview
            frame = cv2.resize(frame, PREVIEW_SIZE)
            # Convert from BGR to RGB and rotate correctly
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Create pygame surface
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            return surface
        except Exception as e:
            print(f"Error converting frame: {e}")
            # Return black surface if conversion fails
            surface = pygame.Surface(PREVIEW_SIZE)
            surface.fill((0, 0, 0))
            return surface
    
    def draw_camera_preview(self, frame, hand_pos, velocity):
        try:
            # Draw tracking visualization
            preview_frame = self.hand_tracker.draw_tracking_info(frame.copy(), hand_pos, velocity)
            
            # Convert frame to pygame surface
            preview_surface = self.frame_to_surface(preview_frame)
            
            # Calculate preview position (bottom-right corner)
            preview_x = self.screen_width - PREVIEW_SIZE[0] - PREVIEW_PADDING
            preview_y = self.screen_height - PREVIEW_SIZE[1] - PREVIEW_PADDING
            
            # Draw background for preview
            self.screen.blit(self.preview_bg, (preview_x - 2, preview_y - 2))
            
            # Draw preview
            self.screen.blit(preview_surface, (preview_x, preview_y))
            
            # Draw connection line between hand and cursor if hand is detected
            if hand_pos[0] is not None and hand_pos[1] is not None:
                game_x, game_y = self.scale_position(hand_pos[0], hand_pos[1])
                preview_hand_x = preview_x + int(hand_pos[0] * PREVIEW_SIZE[0])
                preview_hand_y = preview_y + int(hand_pos[1] * PREVIEW_SIZE[1])
                
                # Draw connecting line with fade effect
                for i in range(3):
                    alpha = 150 - i * 40
                    color = (*UI_BLUE[:3], alpha)
                    line_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                    pygame.draw.line(line_surface, color, 
                                  (preview_hand_x, preview_hand_y),
                                  (game_x, game_y), 2)
                    self.screen.blit(line_surface, (0, 0))
        
        except Exception as e:
            print(f"Error drawing preview: {e}")
    
    def update_fruits(self):
        active_fruits = sum(1 for fruit in self.fruits if not fruit.sliced)
        if active_fruits < 3:
            self.fruits.append(Fruit(self.screen_width, self.screen_height))
            if len(self.fruits) > 8:
                self.fruits.pop(0)
    
    def check_collisions(self, blade_points):
        if len(blade_points) < 2:
            return
        
        # Get latest blade movement
        p1 = blade_points[-2]
        p2 = blade_points[-1]
        
        # Calculate blade velocity and angle
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        blade_velocity = math.sqrt(dx*dx + dy*dy)
        slice_angle = math.degrees(math.atan2(dy, dx))
        
        if blade_velocity < 15:  # Minimum velocity for valid slice
            return
        
        # Check collision with each fruit
        for fruit in self.fruits:
            if not fruit.sliced:
                # Calculate distance from fruit to blade line segment
                fruit_radius = 35 * min(self.scale_x, self.scale_y)  # Scale hitbox with screen size
                dist = abs(dy*fruit.x - dx*fruit.y + p2[0]*p1[1] - p2[1]*p1[0]) / blade_velocity
                
                if dist < fruit_radius:
                    fruit.sliced = True
                    fruit.slice_time = pygame.time.get_ticks()
                    fruit.slice_direction = slice_angle
                    fruit.create_particles(slice_angle)
                    self.engine.play_slice_sound()
                    self.engine.score += 10 * (self.engine.combo + 1)
                    self.engine.update_combo(pygame.time.get_ticks())
    
    def draw_ui(self):
        # Draw score with glow effect
        score_text = f'Score: {self.engine.score}'
        
        # Glow effect
        glow_size = int(36 * self.scale_y + math.sin(pygame.time.get_ticks() * 0.005) * 2)
        glow_font = pygame.font.Font('fonts/ninja.ttf', glow_size) if os.path.exists('fonts/ninja.ttf') else pygame.font.Font(None, glow_size)
        glow_surface = glow_font.render(score_text, True, UI_BLUE)
        glow_rect = glow_surface.get_rect(topleft=(20 * self.scale_x, 20 * self.scale_y))
        
        # Apply glow
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            self.screen.blit(glow_surface, (glow_rect.x + offset[0], glow_rect.y + offset[1]))
        
        # Main score text
        score_surface = self.font.render(score_text, True, UI_WHITE)
        self.screen.blit(score_surface, (20 * self.scale_x, 20 * self.scale_y))
        
        # Draw combo with animation
        if self.engine.combo > 1:
            combo_text = f'Combo x{self.engine.combo}!'
            scale = 1.0 + math.sin(pygame.time.get_ticks() * 0.01) * 0.1
            combo_surface = self.small_font.render(combo_text, True, UI_GOLD)
            scaled_surface = pygame.transform.scale(combo_surface, 
                (int(combo_surface.get_width() * scale * self.scale_x),
                 int(combo_surface.get_height() * scale * self.scale_y)))
            combo_pos = (self.screen_width // 2 - scaled_surface.get_width() // 2, 
                        50 * self.scale_y)
            self.screen.blit(scaled_surface, combo_pos)
    
    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.is_fullscreen:
                            self.toggle_fullscreen()
                        else:
                            running = False
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()
            
            # Draw background
            self.engine.draw_background(self.screen)
            
            # Process hand tracking
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                hand_x, hand_y, velocity, vel_vector = self.hand_tracker.get_hand_position(frame)
                
                if hand_x is not None:
                    # Scale position to screen coordinates
                    game_x, game_y = self.scale_position(hand_x, hand_y)
                    point = (game_x, game_y)
                    
                    # Update and draw blade trail
                    self.blade_trail.add_point(point, velocity)
                    self.blade_trail.draw(self.screen)
                    
                    # Draw katana cursor
                    if len(self.blade_trail.points) > 1:
                        p1 = self.blade_trail.points[-2]
                        p2 = self.blade_trail.points[-1]
                        angle = math.degrees(math.atan2(-(p2[1] - p1[1]), p2[0] - p1[0]))
                        self.engine.draw_katana(self.screen, point, angle)
                    
                    # Check collisions
                    self.check_collisions(self.blade_trail.points)
                
                # Draw camera preview with tracking visualization
                self.draw_camera_preview(frame, (hand_x, hand_y), vel_vector)
            
            # Update and draw fruits
            self.update_fruits()
            for fruit in self.fruits:
                fruit.update()
                fruit.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Cleanup
        self.cap.release()
        pygame.quit()

if __name__ == "__main__":
    game = FruitNinja()
    game.run()