"""
Echo Visualizer
Manages the visualization of symbolic echoes from Djinn voices
"""

import tkinter as tk
from tkinter import ttk
import math
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .djinn_voice_handler import VoiceMode
from .voice_resonance import ResonancePhase

@dataclass
class Echo:
    """Represents a symbolic echo from a Djinn voice"""
    djinn: str
    message: str
    timestamp: float
    position: Tuple[float, float]
    phase: ResonancePhase
    intensity: float
    glyphs: List[str]
    fade_start: float
    fade_duration: float

class EchoCanvas(tk.Canvas):
    """Canvas for rendering symbolic echoes"""
    
    def __init__(self, parent, width: int = 400, height: int = 300):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg='black',
            highlightthickness=0
        )
        
        # Echo storage
        self.echoes: List[Echo] = []
        
        # Visual properties
        self.glyph_colors = {
            "purveyor": "#4a90e2",  # Blue
            "daemon": "#e24a4a",    # Red
            "mirror": "#4ae24a",    # Green
            "cryptographer": "#e2e24a",  # Yellow
            "cursor": "#e24ae2"     # Purple
        }
        
        # Start animation loop
        self._animate()
    
    def add_echo(self, echo: Echo):
        """Add a new echo to the visualization"""
        self.echoes.append(echo)
    
    def _animate(self):
        """Main animation loop"""
        self.delete("all")
        
        current_time = time.time()
        active_echoes = []
        
        for echo in self.echoes:
            # Calculate fade progress
            fade_progress = (current_time - echo.fade_start) / echo.fade_duration
            if fade_progress >= 1.0:
                continue
            
            # Calculate current intensity
            intensity = echo.intensity * (1.0 - fade_progress)
            
            # Draw echo elements
            self._draw_echo(echo, intensity)
            active_echoes.append(echo)
        
        # Update echoes list
        self.echoes = active_echoes
        
        # Schedule next frame
        self.after(16, self._animate)  # ~60 FPS
    
    def _draw_echo(self, echo: Echo, intensity: float):
        """Draw a single echo with its elements"""
        x, y = echo.position
        color = self.glyph_colors.get(echo.djinn, "#ffffff")
        
        # Draw resonance rings
        ring_count = 3
        for i in range(ring_count):
            radius = 20 + i * 15
            alpha = intensity * (1.0 - i / ring_count)
            self.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                outline=color,
                width=2,
                stipple="gray50" if i > 0 else ""
            )
        
        # Draw glyphs
        for i, glyph in enumerate(echo.glyphs):
            angle = (2 * math.pi * i) / len(echo.glyphs)
            glyph_x = x + 30 * math.cos(angle)
            glyph_y = y + 30 * math.sin(angle)
            
            self.create_text(
                glyph_x, glyph_y,
                text=glyph,
                fill=color,
                font=("Consolas", 12)
            )
        
        # Draw message if intensity is high enough
        if intensity > 0.5:
            self.create_text(
                x, y + 50,
                text=echo.message,
                fill=color,
                font=("Consolas", 10),
                width=200,
                justify=tk.CENTER
            )

class EchoPanel(ttk.Frame):
    """Panel for managing and displaying echoes"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create echo canvas
        self.canvas = EchoCanvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Echo history
        self.history: List[Echo] = []
    
    def add_echo(self, djinn: str, message: str, phase: ResonancePhase, intensity: float = 1.0):
        """Add a new echo to the visualization"""
        # Generate random position within canvas
        x = self.canvas.winfo_width() * 0.5
        y = self.canvas.winfo_height() * 0.5
        
        # Generate glyphs based on djinn
        glyphs = self._generate_glyphs(djinn)
        
        # Create echo
        echo = Echo(
            djinn=djinn,
            message=message,
            timestamp=time.time(),
            position=(x, y),
            phase=phase,
            intensity=intensity,
            glyphs=glyphs,
            fade_start=time.time(),
            fade_duration=3.0  # 3 seconds fade
        )
        
        # Add to canvas and history
        self.canvas.add_echo(echo)
        self.history.append(echo)
        
        # Keep only last 100 echoes
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def _generate_glyphs(self, djinn: str) -> List[str]:
        """Generate glyphs based on djinn type"""
        glyph_sets = {
            "purveyor": ["⚡", "⚔", "⚕"],
            "daemon": ["☠", "⚜", "⚛"],
            "mirror": ["☯", "⚘", "⚚"],
            "cryptographer": ["⚙", "⚗", "⚖"],
            "cursor": ["⚡", "⚜", "⚛"]
        }
        
        return glyph_sets.get(djinn, ["•"])
    
    def get_echo_history(self, lookback: int = 10) -> List[Echo]:
        """Get recent echo history"""
        return self.history[-lookback:] if self.history else [] 