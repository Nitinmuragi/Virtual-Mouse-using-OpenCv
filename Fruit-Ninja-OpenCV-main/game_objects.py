import pygame
import random
import math
import os

class Fruit:
    def __init__(self, window_width, window_height):
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.images = {}
        self.particles = []
        
        # Fruit juice colors and effects
        self.fruit_colors = {
            'apple': (255, 50, 50),
            'orange': (255, 165, 0),
            'banana': (255, 255, 0),
            'watermelon': (255, 50, 100),
            'pear': (170, 255, 50)
        }
        
        # Load fruit images
        image_files = {
            'apple': 'fruits/apple.png',
            'orange': 'fruits/orange.png',
            'banana': 'fruits/banana.png',
            'watermelon': 'fruits/watermelon.png',
            'pear': 'fruits/pear.png'
        }
        
        for name, path in image_files.items():
            try:
                self.images[name] = pygame.image.load(path)
                self.images[name] = pygame.transform.scale(self.images[name], (80, 80))
            except:
                surface = pygame.Surface((80, 80), pygame.SRCALPHA)
                color = self.fruit_colors.get(name, (255, 0, 0))
                pygame.draw.circle(surface, color, (40, 40), 40)
                # Add shine effect
                highlight = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.circle(highlight, (255, 255, 255, 50), (30, 30), 20)
                surface.blit(highlight, (0, 0))
                self.images[name] = surface
        
        self.reset()
    
    def reset(self):
        self.type = random.choice(list(self.images.keys()))
        self.x = random.randint(100, self.WINDOW_WIDTH-100)
        self.y = self.WINDOW_HEIGHT + 50
        self.speed_x = random.uniform(-4, 4)
        self.speed_y = random.uniform(-32, -28)  # Higher initial velocity
        self.gravity = 0.4  # Reduced gravity for higher arcs
        self.sliced = False
        self.slice_time = 0
        self.rotation = 0
        self.rotation_speed = random.uniform(-8, 8)
        self.left_rotation = random.uniform(-12, -8)
        self.right_rotation = random.uniform(8, 12)
        self.slice_direction = 0  # Used for slice animation direction
        
    def create_particles(self, slice_angle):
        color = self.fruit_colors.get(self.type, (255, 100, 0))
        perpendicular = slice_angle + 90  # Particles spray perpendicular to slice
        
        for _ in range(25):  # Increased particle count
            # Angle spread based on slice direction
            angle = math.radians(perpendicular + random.uniform(-45, 45))
            speed = random.uniform(10, 20)  # Increased particle speed
            
            particle = {
                'pos': [self.x, self.y],
                'vel': [speed * math.cos(angle), speed * math.sin(angle)],
                'timer': 60,  # Increased lifetime
                'color': color,
                'size': random.uniform(2, 6),
                'alpha': 255
            }
            self.particles.append(particle)
    
    def update(self):
        if not self.sliced:
            self.x += self.speed_x
            self.y += self.speed_y
            self.speed_y += self.gravity
            self.rotation += self.rotation_speed
            
            # Enhanced wobble effect
            wobble_amplitude = 1.0
            wobble_speed = 0.015
            self.x += math.sin(pygame.time.get_ticks() * wobble_speed) * wobble_amplitude
            
            if self.y > self.WINDOW_HEIGHT + 50:
                self.reset()
        else:
            for particle in self.particles[:]:
                particle['pos'][0] += particle['vel'][0]
                particle['pos'][1] += particle['vel'][1]
                particle['vel'][1] += 0.3
                particle['timer'] -= 1
                particle['alpha'] = max(0, particle['alpha'] - 4)
                if particle['timer'] <= 0:
                    self.particles.remove(particle)
    
    def draw(self, screen):
        if not self.sliced:
            rotated_image = pygame.transform.rotate(self.images[self.type], self.rotation)
            rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_image, rect)
        else:
            # Draw particles with alpha
            for particle in self.particles:
                color = list(particle['color'])
                if len(color) == 3:
                    color.append(int(particle['alpha']))
                surf = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
                pygame.draw.circle(surf, color,
                                (int(particle['size']), int(particle['size'])),
                                int(particle['size']))
                screen.blit(surf, (int(particle['pos'][0] - particle['size']),
                                 int(particle['pos'][1] - particle['size'])))
            
            # Enhanced slicing animation
            if pygame.time.get_ticks() - self.slice_time < 1000:
                base_image = self.images[self.type]
                slice_progress = (pygame.time.get_ticks() - self.slice_time) / 1000.0
                slice_dir = math.radians(self.slice_direction)
                
                # Calculate separation direction based on slice angle
                separation = slice_progress * 60
                left_offset_x = -math.cos(slice_dir) * separation
                left_offset_y = -math.sin(slice_dir) * separation
                right_offset_x = math.cos(slice_dir) * separation
                right_offset_y = math.sin(slice_dir) * separation
                
                # Left half with enhanced rotation and movement
                left_half = pygame.Surface((40, 80), pygame.SRCALPHA)
                left_half.blit(base_image, (0, 0))
                left_angle = self.rotation + slice_progress * 360 * self.left_rotation
                left_rotated = pygame.transform.rotate(left_half, left_angle)
                left_rect = left_rotated.get_rect(center=(
                    self.x + left_offset_x,
                    self.y + left_offset_y + slice_progress * 100  # Add downward motion
                ))
                screen.blit(left_rotated, left_rect)
                
                # Right half with enhanced rotation and movement
                right_half = pygame.Surface((40, 80), pygame.SRCALPHA)
                right_half.blit(base_image, (-40, 0))
                right_angle = self.rotation + slice_progress * 360 * self.right_rotation
                right_rotated = pygame.transform.rotate(right_half, right_angle)
                right_rect = right_rotated.get_rect(center=(
                    self.x + right_offset_x,
                    self.y + right_offset_y + slice_progress * 100  # Add downward motion
                ))
                screen.blit(right_rotated, right_rect)

class BladeTrail:
    def __init__(self, window_width, window_height):
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.points = []
        self.max_points = 10  # Increased trail length
        self.min_distance = 10
        self.colors = [
            (100, 200, 255, 200),  # Increased opacity
            (50, 150, 255, 150),
            (0, 100, 255, 100)
        ]
        self.surfaces = []
        for _ in self.colors:
            surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            self.surfaces.append(surface)
        
        # Trail fade effect
        self.fade_start = None
        self.fade_duration = 500  # milliseconds
    
    def add_point(self, point, velocity):
        current_time = pygame.time.get_ticks()
        
        # Add point if moving fast enough and far enough from last point
        if velocity > 3:  # Reduced threshold for better responsiveness
            if not self.points or math.dist(point, self.points[-1]) > self.min_distance:
                self.points.append(point)
                self.fade_start = current_time
                if len(self.points) > self.max_points:
                    self.points.pop(0)
        else:
            # Gradually fade out trail when not moving
            if self.fade_start and current_time - self.fade_start > self.fade_duration:
                if self.points:
                    self.points.pop(0)
    
    def draw(self, screen):
        if len(self.points) > 1:  # Need at least 2 points to draw lines
            points_list = [(int(x), int(y)) for x, y in self.points]  # Ensure integer coordinates
            
            # Draw glow effect
            glow_surface = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
            
            for i, surface in enumerate(self.surfaces):
                surface.fill((0, 0, 0, 0))
                
                # Add slight randomness to trail points for energy effect
                trail_points = [(x + random.uniform(-1, 1), y + random.uniform(-1, 1)) 
                              for x, y in points_list]
                
                # Draw main trail with glow
                if len(trail_points) >= 2:  # Verify we have enough points
                    pygame.draw.lines(surface, self.colors[i], False, trail_points, 6 + i*2)
                    # Draw glow with reduced alpha
                    glow_color = (*self.colors[i][:3], 30)  # Use RGB from color with low alpha
                    pygame.draw.lines(glow_surface, glow_color, False, trail_points, 12 + i*4)
            
                screen.blit(glow_surface, (0, 0))
                screen.blit(surface, (0, 0))