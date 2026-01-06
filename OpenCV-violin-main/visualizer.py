import pygame
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg

class Visualizer:
    def __init__(self, width=1920, height=1080):
        # Initialize pygame
        pygame.init()
        self.width = width
        self.height = height
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Virtual Violin")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.BORDER_COLOR = (100, 100, 100)  # Added border color
        
        # Font setup
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        
        # Setup matplotlib for visualization
        plt.style.use('dark_background')
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 10))
        self.fig.patch.set_facecolor('#1C1C1C')
        
        # Track history for visualization
        self.position_history = []
        self.note_history = []
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
            self.width, self.height = 1920, 1080

    def update(self, frame, hand_positions, current_note=None):
        """Update the display with new frame and data"""
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.toggle_fullscreen()
            elif event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
                self.width, self.height = event.size
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Convert frame to pygame surface
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        
        # Display webcam feed on left side
        frame = pygame.transform.scale(frame, (self.width // 2, self.height))
        self.screen.blit(frame, (0, 0))
        
        # Draw border around webcam feed
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (0, 0, self.width // 2, self.height), 2)
        
        # Draw UI elements with borders
        # Title with border
        title = self.font.render("Virtual Violin", True, self.WHITE)
        title_rect = title.get_rect(center=(self.width // 4, 30))
        pygame.draw.rect(self.screen, self.BORDER_COLOR, title_rect.inflate(20, 10), 2)
        self.screen.blit(title, title_rect)
        
        # Instructions with border
        instructions = self.font.render("Press 'F' to toggle fullscreen", True, self.WHITE)
        inst_rect = instructions.get_rect(center=(self.width // 4, self.height - 30))
        pygame.draw.rect(self.screen, self.BORDER_COLOR, inst_rect.inflate(20, 10), 2)
        self.screen.blit(instructions, inst_rect)
        
        # Update visualization data
        if hand_positions and len(hand_positions) > 0:
            # Invert Y position for more intuitive visualization
            y_pos = hand_positions[0][8][1]
            self.position_history.append(-y_pos)  # Invert Y position
            if len(self.position_history) > 50:
                self.position_history.pop(0)
            
            # Draw volume indicator based on x position
            x_pos = hand_positions[0][8][0]
            volume = x_pos / frame.get_width()
            volume_height = int(150 * volume)
            
            # Draw volume bar with border
            pygame.draw.rect(self.screen, self.BORDER_COLOR, (8, self.height//2 - 152, 24, 154), 2)
            for i in range(volume_height):
                alpha = i / 150
                color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
                pygame.draw.rect(self.screen, color, (10, self.height//2 - i, 20, 2))
            
            # Volume text with border
            volume_text = self.font.render(f"Volume: {int(volume*100)}%", True, self.WHITE)
            volume_rect = volume_text.get_rect(topleft=(35, self.height//2 - 10))
            pygame.draw.rect(self.screen, self.BORDER_COLOR, volume_rect.inflate(20, 10), 2)
            self.screen.blit(volume_text, volume_rect)
        
        if current_note:
            self.note_history.append(current_note)
            if len(self.note_history) > 50:
                self.note_history.pop(0)
            
            # Display current note with border
            note_text = self.font.render(f"Current Note: {current_note}", True, self.WHITE)
            note_rect = note_text.get_rect(center=(self.width // 4, 70))
            pygame.draw.rect(self.screen, self.BORDER_COLOR, note_rect.inflate(20, 10), 2)
            self.screen.blit(note_text, note_rect)
        
        # Update matplotlib visualizations
        self._update_plots()
        
        # Convert matplotlib figure to pygame surface
        canvas = FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()
        size = canvas.get_width_height()
        
        # Create pygame surface from plot
        plot_surface = pygame.image.frombuffer(raw_data, size, "RGBA")
        plot_surface = pygame.transform.scale(plot_surface, (self.width // 2, self.height))
        
        # Display plot on right side with border
        self.screen.blit(plot_surface, (self.width // 2, 0))
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (self.width // 2, 0, self.width // 2, self.height), 2)
        
        # Update display
        pygame.display.flip()

    def _update_plots(self):
        """Update matplotlib plots with enhanced styling"""
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Configure appearance with enhanced styling
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#1C1C1C')
            ax.tick_params(axis='x', colors='#FFFFFF', labelsize=10)
            ax.tick_params(axis='y', colors='#FFFFFF', labelsize=10)
            ax.grid(True, color='#333333', alpha=0.5, linestyle='--')
            for spine in ax.spines.values():
                spine.set_color('#444444')
        
        # Plot hand movement with enhanced visualization
        if self.position_history:
            # Create gradient line
            self.ax1.plot(self.position_history, color='#00FFFF', linewidth=2.5, alpha=0.8)
            # Add fill below line
            self.ax1.fill_between(range(len(self.position_history)), 
                                self.position_history, 
                                self.ax1.get_ylim()[0],
                                alpha=0.2, color='#00FFFF')
            self.ax1.set_title('Hand Movement Visualization', 
                             color='#FFFFFF', 
                             pad=15, 
                             fontsize=12, 
                             fontweight='bold')
        
        # Plot note history with enhanced visualization
        if self.note_history:
            unique_notes = list(set(self.note_history))
            note_indices = [unique_notes.index(note) for note in self.note_history]
            
            # Create gradient line
            self.ax2.plot(note_indices, color='#FF69B4', linewidth=2.5, alpha=0.8)
            
            # Add markers for note changes
            self.ax2.scatter(range(len(note_indices)), 
                           note_indices, 
                           color='#FFD700', 
                           s=30, 
                           alpha=0.6)
            
            self.ax2.set_title('Musical Note Progression', 
                             color='#FFFFFF', 
                             pad=15, 
                             fontsize=12, 
                             fontweight='bold')
            self.ax2.set_yticks(range(len(unique_notes)))
            self.ax2.set_yticklabels(unique_notes, fontsize=10)
        
        self.fig.tight_layout()

    def cleanup(self):
        """Clean up resources"""
        pygame.quit()
        plt.close(self.fig)