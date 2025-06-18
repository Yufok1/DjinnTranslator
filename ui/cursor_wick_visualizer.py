"""
Cursor Wick Visualizer
Visualizes Cursor's wick echo patterns and insights
"""

import tkinter as tk
from tkinter import ttk
import math
from typing import Dict, Any, List, Tuple
from .cursor_wick_engine import WickEchoType, WickEcho, WickInsight

class EchoCanvas(tk.Canvas):
    """Canvas for visualizing wick echo patterns"""
    
    def __init__(self, parent, width=400, height=300):
        super().__init__(parent, width=width, height=height, bg='black')
        self.width = width
        self.height = height
        self.echo_colors = {
            WickEchoType.HARMONIC: "#00ff00",    # Green
            WickEchoType.TURBULENT: "#ff0000",   # Red
            WickEchoType.RESONANT: "#0000ff",    # Blue
            WickEchoType.FRAGMENTED: "#ff00ff",  # Magenta
            WickEchoType.EMERGENT: "#ffff00"     # Yellow
        }
    
    def draw_echo(self, echo: WickEcho):
        """Draw a wick echo pattern"""
        self.delete("all")
        
        # Draw echo center
        center_x, center_y = self._scale_position(echo.position)
        self.create_oval(
            center_x - 5, center_y - 5,
            center_x + 5, center_y + 5,
            fill=self.echo_colors[echo.echo_type],
            outline="white"
        )
        
        # Draw resonance rings
        for i in range(3):
            radius = 20 + i * 15
            alpha = 0.7 - i * 0.2
            self.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=self.echo_colors[echo.echo_type],
                width=2
            )
        
        # Draw strain points
        for point in echo.strain_points:
            x, y = self._scale_position(point)
            self.create_oval(
                x - 3, y - 3,
                x + 3, y + 3,
                fill="red",
                outline="white"
            )
        
        # Draw domain activations
        angle = 0
        for domain, activation in echo.domain_activation.items():
            if activation > 0.5:
                radius = 30
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.create_text(
                    x, y,
                    text=domain[:3],
                    fill="white",
                    font=("Arial", 8)
                )
                angle += math.pi / 3
    
    def _scale_position(self, pos: Tuple[float, float]) -> Tuple[float, float]:
        """Scale position to canvas coordinates"""
        x, y = pos
        return (
            self.width * (x + 1) / 2,
            self.height * (y + 1) / 2
        )

class InsightPanel(ttk.Frame):
    """Panel for displaying wick insights"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create text widget for insights
        self.text = tk.Text(
            self,
            wrap=tk.WORD,
            width=40,
            height=10,
            bg='black',
            fg='white',
            font=("Consolas", 10)
        )
        self.text.pack(fill=tk.BOTH, expand=True)
    
    def update_insight(self, insight: WickInsight):
        """Update the insight display"""
        self.text.delete(1.0, tk.END)
        
        # Add timestamp
        self.text.insert(tk.END, f"Time: {insight.timestamp:.1f}\n", "time")
        
        # Add wick ID
        self.text.insert(tk.END, f"Wick: {insight.wick_id}\n", "wick")
        
        # Add harmonic potential
        self.text.insert(tk.END, f"Harmonic: {insight.harmonic_potential:.2f}\n", "harmonic")
        
        # Add suggested action
        self.text.insert(tk.END, f"Action: {insight.suggested_action}\n", "action")
        
        # Add reason trace
        self.text.insert(tk.END, "\nReason Trace:\n", "trace_header")
        for line in insight.reason_trace:
            self.text.insert(tk.END, f"  {line}\n", "trace")
        
        # Configure tags
        self.text.tag_configure("time", foreground="#888888")
        self.text.tag_configure("wick", foreground="#00ff00")
        self.text.tag_configure("harmonic", foreground="#0000ff")
        self.text.tag_configure("action", foreground="#ff00ff")
        self.text.tag_configure("trace_header", foreground="#ffff00")
        self.text.tag_configure("trace", foreground="#ffffff")

class CursorWickVisualizer(ttk.Frame):
    """Main visualizer for Cursor's wick echo patterns"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create echo canvas
        self.echo_canvas = EchoCanvas(self)
        self.echo_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create insight panel
        self.insight_panel = InsightPanel(self)
        self.insight_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def update_visualization(self, echo: WickEcho, insight: WickInsight):
        """Update the visualization with new echo and insight data"""
        self.echo_canvas.draw_echo(echo)
        self.insight_panel.update_insight(insight) 