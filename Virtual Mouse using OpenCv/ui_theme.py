from tkinter import ttk
import tkinter as tk

class DarkTheme:
    # Color palette
    BACKGROUND = "#1e1e1e"
    SECONDARY = "#2d2d2d"
    ACCENT = "#0078d4"
    TEXT = "#ffffff"
    TEXT_SUBDUED = "#cccccc"
    SUCCESS = "#4caf50"
    ERROR = "#f44336"
    
    @staticmethod
    def apply_theme(root):
        style = ttk.Style()
        style.configure("Dark.TFrame", background=DarkTheme.BACKGROUND)
        style.configure("Dark.TLabel", 
                       background=DarkTheme.BACKGROUND,
                       foreground=DarkTheme.TEXT)
        style.configure("Dark.TButton",
                       background=DarkTheme.ACCENT,
                       foreground=DarkTheme.TEXT)
        
        root.configure(bg=DarkTheme.BACKGROUND)
        
        return style

class GameStats(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=DarkTheme.BACKGROUND)
        
        self.score = 0
        self.high_score = 0
        self.accuracy = 0
        self.total_shots = 0
        self.hits = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Score label
        self.score_label = tk.Label(
            self,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            fg=DarkTheme.TEXT,
            bg=DarkTheme.BACKGROUND
        )
        self.score_label.pack(pady=5)
        
        # High score label
        self.high_score_label = tk.Label(
            self,
            text="High Score: 0",
            font=("Arial", 12),
            fg=DarkTheme.TEXT_SUBDUED,
            bg=DarkTheme.BACKGROUND
        )
        self.high_score_label.pack(pady=5)
        
        # Accuracy label
        self.accuracy_label = tk.Label(
            self,
            text="Accuracy: 0%",
            font=("Arial", 12),
            fg=DarkTheme.TEXT_SUBDUED,
            bg=DarkTheme.BACKGROUND
        )
        self.accuracy_label.pack(pady=5)
        
    def update_score(self, points):
        self.score += points
        self.hits += 1
        self.total_shots += 1
        self.high_score = max(self.score, self.high_score)
        self.accuracy = (self.hits / self.total_shots) * 100 if self.total_shots > 0 else 0
        self.update_labels()
        
    def register_miss(self):
        self.total_shots += 1
        self.accuracy = (self.hits / self.total_shots) * 100 if self.total_shots > 0 else 0
        self.update_labels()
        
    def update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")
        self.accuracy_label.config(text=f"Accuracy: {self.accuracy:.1f}%")
        
    def reset(self):
        self.score = 0
        self.total_shots = 0
        self.hits = 0
        self.accuracy = 0
        self.update_labels()