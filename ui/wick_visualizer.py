"""
Wick Visualizer
Visualizes recursive wicks and their properties
"""

import tkinter as tk
from tkinter import ttk
import math
from typing import Dict, Any, List, Tuple
from .wick_system import WickState, RecursiveWick

class WickCanvas(tk.Canvas):
    """Canvas for drawing wick visualizations"""
    
    def __init__(self, parent, width=400, height=300):
        super().__init__(parent, width=width, height=height, bg="black")
        self.width = width
        self.height = height
        self.wick_colors = {
            WickState.EMERGING: "#FFA500",    # Orange
            WickState.ACTIVE: "#FF0000",      # Red
            WickState.CONTAINED: "#00FF00",   # Green
            WickState.REBOUND: "#0000FF",     # Blue
            WickState.HARVESTED: "#FFFF00",   # Yellow
            WickState.COLLAPSED: "#808080"    # Gray
        }
    
    def draw_wick(self, wick_data: Dict[str, Any]):
        """Draw a wick visualization"""
        self.delete("all")
        
        if not wick_data:
            return
        
        # Draw wick path
        path = wick_data["path"]
        if len(path) > 1:
            # Scale path to canvas
            scaled_path = self._scale_path(path)
            
            # Draw path line
            self.create_line(
                scaled_path,
                fill=self.wick_colors[WickState(wick_data["state"])],
                width=2,
                smooth=True
            )
            
            # Draw strain points
            for point in wick_data["strain_points"]:
                x, y = self._scale_point(point)
                self.create_oval(
                    x-3, y-3, x+3, y+3,
                    fill="#FF0000",
                    outline=""
                )
            
            # Draw resonance rings
            self._draw_resonance_rings(wick_data["resonance"])
            
            # Draw mirror feedback
            if wick_data["mirror_feedback"] > 0:
                self._draw_mirror_feedback(wick_data["mirror_feedback"])
            
            # Draw containment level
            if wick_data["containment"] > 0:
                self._draw_containment(wick_data["containment"])
            
            # Draw harmonic potential
            self._draw_harmonic_potential(wick_data["harmonic_potential"])
    
    def _scale_path(self, path: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Scale path coordinates to canvas size"""
        if not path:
            return []
        
        # Find bounds
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # Add padding
        padding = 20
        width = max_x - min_x or 1
        height = max_y - min_y or 1
        
        # Scale points
        return [
            (
                (x - min_x) / width * (self.width - 2*padding) + padding,
                (y - min_y) / height * (self.height - 2*padding) + padding
            )
            for x, y in path
        ]
    
    def _scale_point(self, point: Tuple[float, float]) -> Tuple[float, float]:
        """Scale a single point to canvas coordinates"""
        return self._scale_path([point])[0]
    
    def _draw_resonance_rings(self, resonance_values: List[float]):
        """Draw resonance rings around the wick"""
        if not resonance_values:
            return
        
        # Get center point
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Draw rings for each resonance value
        for i, resonance in enumerate(resonance_values):
            radius = 20 + i * 10
            alpha = int(resonance * 255)
            color = f"#{alpha:02x}00{alpha:02x}"
            
            self.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color,
                width=1
            )
    
    def _draw_mirror_feedback(self, feedback: float):
        """Draw mirror feedback visualization"""
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Draw feedback arc
        start_angle = 0
        extent = feedback * 360
        
        self.create_arc(
            center_x - 50, center_y - 50,
            center_x + 50, center_y + 50,
            start=start_angle,
            extent=extent,
            fill="#00FFFF",
            outline=""
        )
    
    def _draw_containment(self, level: float):
        """Draw containment visualization"""
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Draw containment ring
        radius = 60
        alpha = int(level * 255)
        color = f"#00{alpha:02x}00"
        
        self.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline=color,
            width=2
        )
    
    def _draw_harmonic_potential(self, potential: float):
        """Draw harmonic potential visualization"""
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Draw potential indicator
        radius = 70
        angle = potential * 2 * math.pi
        
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        
        self.create_line(
            center_x, center_y, end_x, end_y,
            fill="#FFFF00",
            width=2
        )

class WickVisualizer(ttk.Frame):
    """Frame for visualizing wicks and their properties"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create main canvas
        self.canvas = WickCanvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create control panel
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Containment controls
        ttk.Label(self.control_frame, text="Containment:").pack(side=tk.LEFT, padx=5)
        self.containment_var = tk.StringVar(value="isolate")
        ttk.Radiobutton(self.control_frame, text="Isolate",
                       variable=self.containment_var,
                       value="isolate").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.control_frame, text="Rebind",
                       variable=self.containment_var,
                       value="rebind").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.control_frame, text="Harvest",
                       variable=self.containment_var,
                       value="harvest").pack(side=tk.LEFT, padx=5)
        
        # Apply button
        ttk.Button(self.control_frame, text="Apply",
                  command=self._apply_containment).pack(side=tk.RIGHT, padx=5)
    
    def update_wick(self, wick_data: Dict[str, Any]):
        """Update the wick visualization"""
        self.canvas.draw_wick(wick_data)
    
    def _apply_containment(self):
        """Apply selected containment mode"""
        mode = self.containment_var.get()
        # Implementation would go here
        pass 