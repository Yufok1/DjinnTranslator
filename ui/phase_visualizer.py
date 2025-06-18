# Copyright 2024 SpliceWeb
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Phase Horizon Visualizer
Provides visualization of phase horizons, breach zones, and safe corridors
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Rectangle, Polygon
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import time

class PhaseStability(Enum):
    """Stability levels for phase horizons."""
    STABLE = "stable"           # Green: Safe for navigation
    CAUTIOUS = "cautious"       # Yellow: Requires attention
    UNSTABLE = "unstable"       # Red: Dangerous
    BREACHED = "breached"       # Purple: Active breach
    RECOVERING = "recovering"   # Blue: Healing

@dataclass
class BreachZone:
    """Represents a breach zone in the phase horizon."""
    center: Tuple[float, float]
    radius: float
    severity: float
    type: str
    containment_status: str
    recovery_progress: float

@dataclass
class SafeCorridor:
    """Represents a safe navigation corridor."""
    start: Tuple[float, float]
    end: Tuple[float, float]
    width: float
    stability: float
    entry_points: List[Tuple[float, float]]
    exit_points: List[Tuple[float, float]]

@dataclass
class PhaseHorizon:
    """Represents a phase boundary in the lattice."""
    center: Tuple[float, float]
    radius: float
    stability: PhaseStability
    overlap_zones: List[Tuple[float, float]]
    safe_corridors: List[SafeCorridor]
    breach_zones: List[BreachZone]
    entry_points: List[Tuple[float, float]]
    harmonic_resonance: float
    temporal_alignment: float

class PhaseVisualizer:
    """Handles visualization of phase horizons and related elements."""
    
    def __init__(self, parent_frame: ttk.Frame):
        """Initialize the phase visualizer."""
        self.frame = ttk.LabelFrame(parent_frame, text="Phase Horizon Visualization", padding=10)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Create axes
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.3)
        
        # Define colors
        self.stability_colors = {
            PhaseStability.STABLE: '#00ff00',      # Green
            PhaseStability.CAUTIOUS: '#ffff00',    # Yellow
            PhaseStability.UNSTABLE: '#ff0000',    # Red
            PhaseStability.BREACHED: '#800080',    # Purple
            PhaseStability.RECOVERING: '#0000ff'   # Blue
        }
        
        # Initialize empty lists for tracking elements
        self.horizon_patches = []
        self.breach_patches = []
        self.corridor_patches = []
        self.entry_point_patches = []
        
        # LOW-RHYTHM mode settings
        self.low_rhythm_mode = True
        self.update_interval = 10.0  # Update every 10 seconds in LOW-RHYTHM mode
        self.last_update = 0.0
        self.visualization_threshold = 0.5  # Only show significant changes
        self.simplified_rendering = True  # Use simplified rendering in LOW-RHYTHM mode
        
    def update_visualization(self, horizon: PhaseHorizon):
        """Update the visualization with new phase horizon data."""
        current_time = time.time()
        
        # Check if we should update in LOW-RHYTHM mode
        if self.low_rhythm_mode:
            if current_time - self.last_update < self.update_interval:
                return
            
            # Check if changes are significant enough to warrant an update
            if not self._should_update_visualization(horizon):
                return
        
        # Clear previous elements
        self._clear_visualization()
        
        # Draw phase horizon
        self._draw_phase_horizon(horizon)
        
        # Draw breach zones
        self._draw_breach_zones(horizon.breach_zones)
        
        # Draw safe corridors
        self._draw_safe_corridors(horizon.safe_corridors)
        
        # Draw entry points
        self._draw_entry_points(horizon.entry_points)
        
        # Update canvas
        self.canvas.draw()
        
        # Update last update time
        self.last_update = current_time
    
    def _should_update_visualization(self, horizon: PhaseHorizon) -> bool:
        """Check if changes are significant enough to warrant an update in LOW-RHYTHM mode."""
        # Check stability changes
        if hasattr(self, 'last_horizon'):
            if horizon.stability != self.last_horizon.stability:
                return True
            
            # Check breach zone changes
            if len(horizon.breach_zones) != len(self.last_horizon.breach_zones):
                return True
            
            # Check significant changes in metrics
            if abs(horizon.harmonic_resonance - self.last_horizon.harmonic_resonance) > self.visualization_threshold:
                return True
            if abs(horizon.temporal_alignment - self.last_horizon.temporal_alignment) > self.visualization_threshold:
                return True
        
        # Store current horizon for next comparison
        self.last_horizon = horizon
        return True
    
    def _clear_visualization(self):
        """Clear all visualization elements."""
        for patch in (self.horizon_patches + self.breach_patches + 
                     self.corridor_patches + self.entry_point_patches):
            patch.remove()
        
        self.horizon_patches = []
        self.breach_patches = []
        self.corridor_patches = []
        self.entry_point_patches = []
        
    def _draw_phase_horizon(self, horizon: PhaseHorizon):
        """Draw the main phase horizon."""
        # Draw main horizon circle
        horizon_circle = Circle(
            horizon.center,
            horizon.radius,
            fill=False,
            edgecolor=self.stability_colors[horizon.stability],
            linewidth=2,
            alpha=0.3 if not self.simplified_rendering else 0.5
        )
        self.ax.add_patch(horizon_circle)
        self.horizon_patches.append(horizon_circle)
        
        # Draw overlap zones only if not in simplified rendering
        if not self.simplified_rendering:
            for zone in horizon.overlap_zones:
                overlap_circle = Circle(
                    zone,
                    5,
                    fill=True,
                    color=self.stability_colors[horizon.stability],
                    alpha=0.2
                )
                self.ax.add_patch(overlap_circle)
                self.horizon_patches.append(overlap_circle)
        
    def _draw_breach_zones(self, breach_zones: List[BreachZone]):
        """Draw breach zones."""
        for zone in breach_zones:
            # Draw breach zone circle
            breach_circle = Circle(
                zone.center,
                zone.radius,
                fill=True,
                color='#ff0000',
                alpha=0.2 * zone.severity if not self.simplified_rendering else 0.4
            )
            self.ax.add_patch(breach_circle)
            self.breach_patches.append(breach_circle)
            
            # Draw containment ring if active and not in simplified rendering
            if zone.containment_status == 'active' and not self.simplified_rendering:
                containment_ring = Circle(
                    zone.center,
                    zone.radius * 1.2,
                    fill=False,
                    edgecolor='#ff0000',
                    linewidth=2,
                    linestyle='--'
                )
                self.ax.add_patch(containment_ring)
                self.breach_patches.append(containment_ring)
            
            # Draw recovery progress if recovering and not in simplified rendering
            if zone.recovery_progress > 0 and not self.simplified_rendering:
                recovery_arc = Circle(
                    zone.center,
                    zone.radius * 1.1,
                    fill=False,
                    edgecolor='#00ff00',
                    linewidth=2,
                    alpha=zone.recovery_progress
                )
                self.ax.add_patch(recovery_arc)
                self.breach_patches.append(recovery_arc)
        
    def _draw_safe_corridors(self, corridors: List[SafeCorridor]):
        """Draw safe navigation corridors."""
        for corridor in corridors:
            # Calculate corridor width
            width = corridor.width
            
            # Draw corridor rectangle
            dx = corridor.end[0] - corridor.start[0]
            dy = corridor.end[1] - corridor.start[1]
            angle = np.arctan2(dy, dx)
            
            # Create corridor polygon
            corridor_points = [
                (corridor.start[0] - width/2 * np.sin(angle),
                 corridor.start[1] + width/2 * np.cos(angle)),
                (corridor.start[0] + width/2 * np.sin(angle),
                 corridor.start[1] - width/2 * np.cos(angle)),
                (corridor.end[0] + width/2 * np.sin(angle),
                 corridor.end[1] - width/2 * np.cos(angle)),
                (corridor.end[0] - width/2 * np.sin(angle),
                 corridor.end[1] + width/2 * np.cos(angle))
            ]
            
            corridor_polygon = Polygon(
                corridor_points,
                fill=True,
                color='#00ff00',
                alpha=0.2 * corridor.stability if not self.simplified_rendering else 0.4
            )
            self.ax.add_patch(corridor_polygon)
            self.corridor_patches.append(corridor_polygon)
            
            # Draw entry and exit points only if not in simplified rendering
            if not self.simplified_rendering:
                for point in corridor.entry_points:
                    entry_point = Circle(
                        point,
                        2,
                        fill=True,
                        color='#00ff00'
                    )
                    self.ax.add_patch(entry_point)
                    self.entry_point_patches.append(entry_point)
                
                for point in corridor.exit_points:
                    exit_point = Circle(
                        point,
                        2,
                        fill=True,
                        color='#00ff00'
                    )
                    self.ax.add_patch(exit_point)
                    self.entry_point_patches.append(exit_point)
        
    def _draw_entry_points(self, entry_points: List[Tuple[float, float]]):
        """Draw entry points."""
        if not self.simplified_rendering:
            for point in entry_points:
                entry_point = Circle(
                    point,
                    2,
                    fill=True,
                    color='#00ff00'
                )
                self.ax.add_patch(entry_point)
                self.entry_point_patches.append(entry_point)
    
    def set_low_rhythm_mode(self, enabled: bool):
        """Enable or disable LOW-RHYTHM mode."""
        self.low_rhythm_mode = enabled
        if enabled:
            self.update_interval = 10.0
            self.simplified_rendering = True
        else:
            self.update_interval = 0.0
            self.simplified_rendering = False 