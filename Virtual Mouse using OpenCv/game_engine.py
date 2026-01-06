import tkinter as tk
import random
from ui_theme import DarkTheme
import time

class Apple:
    def __init__(self, canvas, x, y, size=30):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        
        # Create apple shape
        self.shape = canvas.create_oval(
            x - size, y - size,
            x + size, y + size,
            fill='red',
            outline='darkred'
        )
        # Add stem
        self.stem = canvas.create_line(
            x, y - size,
            x, y - size - 10,
            fill='brown',
            width=3
        )
        
    def delete(self):
        self.canvas.delete(self.shape)
        self.canvas.delete(self.stem)
        
    def is_clicked(self, click_x, click_y):
        # Check if click is within apple bounds
        distance = ((click_x - self.x) ** 2 + (click_y - self.y) ** 2) ** 0.5
        return distance <= self.size

class GameEngine:
    def __init__(self, canvas, stats):
        self.canvas = canvas
        self.stats = stats
        self.apples = []
        self.running = False
        self.start_time = None
        self.apple_count = 3  # Number of apples per round
        
        # Bind canvas click
        self.canvas.bind('<Button-1>', self.handle_click)
        
    def start(self):
        self.running = True
        self.stats.reset()
        self.start_new_round()
        
    def stop(self):
        self.running = False
        self.clear_apples()
        
    def clear_apples(self):
        for apple in self.apples:
            apple.delete()
        self.apples.clear()
        
    def get_spawn_area(self):
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Define spawn margins (20% of dimensions)
        margin_x = width * 0.1
        margin_y = height * 0.1
        
        return (
            margin_x, margin_y,  # min x, min y
            width - margin_x, height - margin_y  # max x, max y
        )
        
    def start_new_round(self):
        if not self.running:
            return
            
        self.clear_apples()
        self.start_time = time.time()
        
        # Get spawn area
        left, top, right, bottom = self.get_spawn_area()
        
        # Generate apples in random positions
        for _ in range(self.apple_count):
            while True:
                x = random.randint(int(left), int(right))
                y = random.randint(int(top), int(bottom))
                
                # Check if position is far enough from other apples
                valid_position = True
                for apple in self.apples:
                    distance = ((x - apple.x) ** 2 + (y - apple.y) ** 2) ** 0.5
                    if distance < 100:  # Minimum distance between apples
                        valid_position = False
                        break
                
                if valid_position:
                    self.apples.append(Apple(self.canvas, x, y))
                    break
        
        # Show round start message
        self.show_message("Collect all apples!", 2000)
        
    def show_message(self, text, duration=1000):
        msg = self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=text,
            fill=DarkTheme.TEXT,
            font=("Arial", 24, "bold")
        )
        self.canvas.after(duration, lambda: self.canvas.delete(msg))
        
    def handle_click(self, event):
        if not self.running or not self.start_time:
            return
            
        for apple in self.apples[:]:  # Copy list to avoid modification during iteration
            if apple.is_clicked(event.x, event.y):
                apple.delete()
                self.apples.remove(apple)
                
                # Show hit effect
                self.show_hit_effect(event.x, event.y)
                
                # Check if all apples are collected
                if not self.apples:
                    # Calculate score based on time
                    time_taken = time.time() - self.start_time
                    base_score = 1000
                    time_penalty = int(time_taken * 10)  # 10 points per second
                    score = max(base_score - time_penalty, 100)  # Minimum score of 100
                    
                    self.stats.update_score(score)
                    
                    # Show round completion message
                    self.show_message(
                        f"Round Complete!\nTime: {time_taken:.1f}s\nScore: {score}",
                        2000
                    )
                    
                    # Start new round after delay
                    self.canvas.after(2000, self.start_new_round)
                break
        
    def show_hit_effect(self, x, y):
        # Create hit effect
        effect = self.canvas.create_text(
            x, y,
            text="✓",
            fill=DarkTheme.SUCCESS,
            font=("Arial", 24, "bold")
        )
        
        def fade_out():
            self.canvas.delete(effect)
        
        self.canvas.after(500, fade_out)