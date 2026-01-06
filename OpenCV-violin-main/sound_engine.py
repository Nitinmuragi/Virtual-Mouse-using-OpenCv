import pygame
import numpy as np
from pygame import mixer

class SoundEngine:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init(44100, -16, 2, 2048)
        
        # Define musical notes (frequencies in Hz) - Extended range for violin
        self.notes = {
            'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
            'C4': 261.63, 'D4': 293.66, 'E4': 329.63,
            'F4': 349.23, 'G4': 392.00, 'A4': 440.00,
            'B4': 493.88, 'C5': 523.25, 'D5': 587.33,
            'E5': 659.25, 'F5': 698.46, 'G5': 783.99
        }
        
        # Initialize state variables
        self.current_note = None
        self.is_playing = False
        self.current_volume = 0.5
        self.vibrato_depth = 0.3
        
        # Create sounds for each note
        self.sounds = {}
        self._generate_sounds()
        
    def _generate_violin_wave(self, frequency, duration=1.0):
        """Generate a violin-like wave using harmonics"""
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Create harmonics with different amplitudes for richer violin timbre
        harmonics = [
            (1.0, 0),          # fundamental
            (0.9, 0),          # 2nd harmonic - enhanced
            (0.75, np.pi/2),   # 3rd harmonic - enhanced
            (0.6, np.pi/4),    # 4th harmonic - enhanced
            (0.45, np.pi/6),   # 5th harmonic - enhanced
            (0.3, np.pi/3),    # 6th harmonic - added
            (0.2, np.pi/2),    # 7th harmonic - added
            (0.1, np.pi/4)     # 8th harmonic - added
        ]
        
        wave = np.zeros_like(t)
        for amp, phase in harmonics:
            wave += amp * np.sin(2 * np.pi * frequency * t * (harmonics.index((amp, phase)) + 1) + phase)
        
        # Add vibrato
        vibrato = np.sin(2 * np.pi * 5 * t) * self.vibrato_depth
        wave *= (1 + vibrato)
        
        # Normalize
        wave = wave / np.max(np.abs(wave))
        
        # Apply violin-like envelope
        attack = 0.1
        decay = 0.2
        sustain_level = 0.7
        
        t_norm = t / duration
        envelope = np.ones_like(t)
        attack_mask = t_norm < attack
        decay_mask = (t_norm >= attack) & (t_norm < (attack + decay))
        
        envelope[attack_mask] = t_norm[attack_mask] / attack
        envelope[decay_mask] = 1.0 - (1.0 - sustain_level) * (t_norm[decay_mask] - attack) / decay
        envelope[t_norm >= (attack + decay)] = sustain_level
        
        wave = wave * envelope
        
        # Convert to 16-bit integers
        wave = np.int16(wave * 32767)
        return wave

    def _generate_sounds(self):
        """Generate sound objects for each note"""
        for note, freq in self.notes.items():
            wave = self._generate_violin_wave(freq)
            sound_object = pygame.mixer.Sound(wave)
            self.sounds[note] = sound_object

    def play_note(self, note_name, volume=None):
        """Play a specific note with optional volume"""
        if note_name in self.sounds:
            # Update volume if provided
            if volume is not None:
                self.current_volume = volume
            
            # Stop current note if different
            if self.current_note and self.current_note != note_name:
                self.sounds[self.current_note].stop()
            
            # Play new note
            if self.current_note != note_name or not self.is_playing:
                self.sounds[note_name].play(-1)  # -1 for loop
                self.sounds[note_name].set_volume(self.current_volume)
                self.current_note = note_name
                self.is_playing = True
            # Update volume if same note
            elif volume is not None:
                self.sounds[note_name].set_volume(self.current_volume)

    def stop_current_note(self):
        """Stop the currently playing note"""
        if self.current_note and self.is_playing:
            self.sounds[self.current_note].stop()
            self.current_note = None
            self.is_playing = False

    def get_note_from_position(self, y_pos, screen_height):
        """Convert vertical position to note (pitch control)"""
        note_names = list(self.notes.keys())
        note_idx = int((1 - y_pos / screen_height) * len(note_names))  # Inverted for intuitive control
        note_idx = max(0, min(note_idx, len(note_names) - 1))
        return note_names[note_idx]

    def get_volume_from_position(self, x_pos, screen_width):
        """Convert horizontal position to volume"""
        # Map horizontal position to volume (0.0 to 1.0)
        volume = x_pos / screen_width
        return max(0.1, min(volume, 1.0))  # Ensure minimum volume of 0.1

    def cleanup(self):
        """Clean up resources"""
        pygame.mixer.quit()