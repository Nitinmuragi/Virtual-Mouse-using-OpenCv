import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import keyboard
from hand_detector import HandDetector
from mouse_controller import MouseController
from ui_theme import DarkTheme, GameStats
from game_engine import GameEngine

class VirtualMouse:
    def __init__(self):
        self.cap = None
        self.running = False
        self.hand_detector = None
        self.mouse_controller = None
        
        # Setup UI
        self.setup_ui()
        
        # Setup keyboard shortcut for emergency exit
        keyboard.on_press_key('esc', self.emergency_exit)
        
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Virtual Mouse")
        self.root.attributes('-fullscreen', True)
        
        # Apply dark theme
        self.style = DarkTheme.apply_theme(self.root)
        
        # Main container with dark theme
        main_container = ttk.Frame(self.root, style="Dark.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for video feed (fixed width)
        video_width = 400  # Fixed width for video panel
        left_panel = ttk.Frame(main_container, style="Dark.TFrame", width=video_width)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH)
        left_panel.pack_propagate(False)  # Prevent size changes
        
        # Instructions
        instructions = ttk.Label(
            left_panel, 
            text=(
                "Controls:\n"
                "- Index finger: Move cursor\n"
                "- Thumb up: Left click\n"
                "- Last 2-3 fingers up: Right click\n"
                "- Press 'Esc' for emergency exit\n"
                "- Ctrl+S to toggle mouse control\n\n"
                "Game Rules:\n"
                "- Click all apples to complete round\n"
                "- Faster completion = Higher score\n"
                "- Try to beat your high score!"
            ),
            style="Dark.TLabel",
            justify=tk.LEFT
        )
        instructions.pack(pady=5, padx=5)
        
        # Control frame
        control_frame = ttk.Frame(left_panel, style="Dark.TFrame")
        control_frame.pack(pady=5, padx=5)
        
        self.toggle_btn = ttk.Button(
            control_frame, 
            text="Start (Ctrl+S)", 
            command=self.toggle_mouse,
            style="Dark.TButton"
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(
            control_frame, 
            text="Status: Stopped",
            style="Dark.TLabel"
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Fixed size video frame
        self.video_frame = ttk.Frame(left_panel, style="Dark.TFrame")
        self.video_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        self.video_label = ttk.Label(self.video_frame, style="Dark.TLabel")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Game area
        right_panel = ttk.Frame(main_container, style="Dark.TFrame")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Game stats at top of right panel
        self.game_stats = GameStats(right_panel)
        self.game_stats.pack(pady=5, padx=5, fill=tk.X)
        
        # Game container frame
        game_container = ttk.Frame(
            right_panel,
            style="Dark.TFrame",
            relief="solid",
            borderwidth=2
        )
        game_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Game canvas inside container
        self.game_canvas = tk.Canvas(
            game_container,
            bg=DarkTheme.BACKGROUND,
            highlightthickness=2,
            highlightbackground=DarkTheme.ACCENT
        )
        self.game_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Initialize game engine
        self.game_engine = GameEngine(self.game_canvas, self.game_stats)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self.toggle_mouse())
        self.root.bind('<Escape>', lambda e: self.emergency_exit())
        
    def emergency_exit(self, e=None):
        print("Emergency exit triggered")
        self.stop_mouse()
        self.root.quit()
        
    def toggle_mouse(self):
        if self.running:
            self.stop_mouse()
        else:
            self.start_mouse()
            
    def start_mouse(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open webcam")
                
            self.hand_detector = HandDetector()
            self.mouse_controller = MouseController()
            
            self.running = True
            self.toggle_btn.config(text="Stop (Ctrl+S)")
            self.status_label.config(text="Status: Running")
            self.game_engine.start()
            self.process_video()
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.stop_mouse()
            
    def stop_mouse(self):
        self.running = False
        self.toggle_btn.config(text="Start (Ctrl+S)")
        self.status_label.config(text="Status: Stopped")
        self.game_engine.stop()
        
        if self.cap:
            self.cap.release()
            self.cap = None
            
    def process_video(self):
        if not self.running:
            return
            
        try:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Failed to grab frame")
                
            frame = cv2.flip(frame, 1)  # Mirror the frame
            original_frame = frame.copy()
            
            # Detect hand and landmarks
            frame = self.hand_detector.find_hands(frame)
            landmark_list = self.hand_detector.find_position(frame)
            
            if landmark_list:
                # Get gesture states and index finger position
                left_click, right_click, index_finger = self.hand_detector.get_gesture_state(landmark_list)
                
                if index_finger:
                    # Map coordinates to screen space
                    frame_h, frame_w = original_frame.shape[:2]
                    screen_x, screen_y = self.mouse_controller.map_coordinates(
                        index_finger[1], index_finger[2], frame_w, frame_h
                    )
                    
                    # Move mouse
                    self.mouse_controller.move(screen_x, screen_y)
                    
                    # Draw cursor position
                    cv2.circle(frame, (index_finger[1], index_finger[2]), 10, (0, 255, 0), cv2.FILLED)
                
                # Handle clicks
                if left_click and self.mouse_controller.left_click():
                    cv2.putText(frame, "Left Click!", (50, 50), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                if right_click and self.mouse_controller.right_click():
                    cv2.putText(frame, "Right Click!", (50, 100), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Resize frame to fit video label while maintaining aspect ratio
            frame_h, frame_w = frame.shape[:2]
            video_w = self.video_frame.winfo_width()
            video_h = self.video_frame.winfo_height()
            
            if video_w > 0 and video_h > 0:
                # Calculate scaling factor to fit frame in video area
                scale_w = video_w / frame_w
                scale_h = video_h / frame_h
                scale = min(scale_w, scale_h)
                
                # Calculate new dimensions
                new_w = int(frame_w * scale)
                new_h = int(frame_h * scale)
                
                # Resize frame
                frame = cv2.resize(frame, (new_w, new_h))
            
            # Convert frame for display
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
        except Exception as e:
            print(f"Frame processing error: {e}")
            
        if self.running:
            self.root.after(10, self.process_video)
        
    def run(self):
        try:
            self.root.mainloop()
        finally:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    vm = VirtualMouse()
    vm.run()