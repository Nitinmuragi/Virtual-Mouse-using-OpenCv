import pygame
import os
import math
import random

class GameEngine:
    def __init__(self, window_width, window_height):
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        
        # Initialize audio system
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        
        # Load sound effects
        self.slice_sounds = []
        for i in range(1, 4):
            try:
                sound = pygame.mixer.Sound(f'sounds/slice{i}.mp3')
                sound.set_volume(0.5)
                self.slice_sounds.append(sound)
            except Exception as e:
                print(f"Error loading sound {i}: {e}")
        
        if not self.slice_sounds:
            self.slice_sounds = [pygame.mixer.Sound(buffer=bytes(44100))]
        
        # Load fonts
        try:
            self.font = pygame.font.Font('fonts/ninja.ttf', 48)
            self.combo_font = pygame.font.Font('fonts/ninja.ttf', 24)
        except:
            self.font = pygame.font.Font(None, 48)
            self.combo_font = pygame.font.Font(None, 24)
        
        # Load katana cursor
        try:
            self.katana = pygame.image.load('cursor/katana.png')
            self.katana = pygame.transform.scale(self.katana, (150, 150))
        except:
            self.katana = pygame.Surface((150, 150), pygame.SRCALPHA)
            pygame.draw.line(self.katana, (255, 255, 255), (0, 75), (150, 75), 5)
        
        # Load background
        try:
            self.background = pygame.image.load('background/dojo.png')
            self.background = pygame.transform.scale(self.background, (window_width, window_height))
        except:
            self.background = None
        
        # Initialize game state
        self.score = 0
        self.combo = 0
        self.last_slice_time = 0
        self.combo_duration = 1000  # milliseconds
        
        # Smooth rotation
        self.current_angle = 0
        self.angle_smooth_factor = 0.2
        
        # Motion trail
        self.prev_positions = []
        self.max_trail_length = 3
    
    def play_slice_sound(self):
        if self.slice_sounds:
            random.choice(self.slice_sounds).play()
    
    def get_smooth_angle(self, target):
        diff = (target - self.current_angle + 180) % 360 - 180
        self.current_angle = (self.current_angle + diff * self.angle_smooth_factor) % 360
        return self.current_angle
    
    def update_combo(self, current_time):
        if current_time - self.last_slice_time < self.combo_duration:
            self.combo += 1
        else:
            self.combo = 0
        self.last_slice_time = current_time
    
    def draw_ui(self, screen):
        # Draw score with shadow
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_shadow = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_shadow, (22, 22))
        screen.blit(score_text, (20, 20))
        
        # Draw combo with animation
        if self.combo > 1:
            scale = 1.0 + math.sin(pygame.time.get_ticks() * 0.01) * 0.1
            combo_text = self.combo_font.render(f'Combo x{self.combo}!', True, (255, 215, 0))
            scaled_text = pygame.transform.scale(combo_text, 
                (int(combo_text.get_width() * scale), 
                 int(combo_text.get_height() * scale)))
            combo_pos = (self.WINDOW_WIDTH // 2 - scaled_text.get_width() // 2, 50)
            screen.blit(scaled_text, combo_pos)
    
    def draw_background(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((20, 20, 50))
    
    def draw_katana(self, screen, position, angle):
        # Update motion trail
        self.prev_positions.append((position, angle))
        if len(self.prev_positions) > self.max_trail_length:
            self.prev_positions.pop(0)
        
        # Draw motion trail
        for i, (pos, ang) in enumerate(self.prev_positions[:-1]):
            alpha = 100 - (i * 30)  # Fade out trailing images
            ghost = self.katana.copy()
            ghost.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
            
            smooth_angle = self.get_smooth_angle(ang)
            rotated = pygame.transform.rotate(ghost, smooth_angle)
            rect = rotated.get_rect(center=pos)
            screen.blit(rotated, rect)
        
        # Draw main katana with smooth rotation and slight wobble
        smooth_angle = self.get_smooth_angle(angle)
        wobble = math.sin(pygame.time.get_ticks() * 0.01) * 2
        final_angle = smooth_angle + wobble
        
        rotated_katana = pygame.transform.rotate(self.katana, final_angle)
        katana_rect = rotated_katana.get_rect(center=position)
        screen.blit(rotated_katana, katana_rect)