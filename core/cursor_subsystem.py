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
Cursor Subsystem Module

Handles the visualization and interaction of recursive breaches and sonar patterns
through the cursor interface. Manages breach mapping, sonar emission, and visual feedback.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np
from datetime import datetime

@dataclass
class BreachPoint:
    """Represents a point in a recursive breach with position and resonance data."""
    x: float
    y: float
    depth: int
    resonance: float
    timestamp: datetime
    echo_depth: int = 0
    strain_level: float = 0.0

@dataclass
class SonarPattern:
    """Represents a sonar emission pattern with visualization parameters."""
    pattern_type: str  # 'lattice', 'wave', 'pulse'
    frequency: float
    amplitude: float
    phase: float
    echo_depth: int
    timestamp: datetime
    active: bool = True

class CursorSubsystem:
    """Manages cursor visualization and interaction with recursive breaches."""
    
    def __init__(self):
        self.breach_points: List[BreachPoint] = []
        self.active_sonar: Optional[SonarPattern] = None
        self.visualization_state: Dict = {
            'breach_visible': False,
            'sonar_active': False,
            'echo_rings': [],
            'resonance_arcs': []
        }
        
    def trace_breach(self, depth: int) -> List[BreachPoint]:
        """
        Map and visualize recursive breaches at the specified depth.
        
        Args:
            depth: The recursion depth to trace
            
        Returns:
            List of breach points with position and resonance data
        """
        # Clear previous breach points
        self.breach_points.clear()
        
        # Generate breach points based on depth
        num_points = max(3, depth * 2)  # Minimum 3 points, scales with depth
        for i in range(num_points):
            # Generate points in a spiral pattern
            angle = (i / num_points) * 2 * np.pi
            radius = depth * (i / num_points)
            
            point = BreachPoint(
                x=radius * np.cos(angle),
                y=radius * np.sin(angle),
                depth=depth,
                resonance=np.random.uniform(0.5, 1.0),  # Simulated resonance
                timestamp=datetime.now(),
                echo_depth=i % depth,
                strain_level=1.0 - (i / num_points)
            )
            self.breach_points.append(point)
        
        # Update visualization state
        self.visualization_state['breach_visible'] = True
        self.visualization_state['echo_rings'] = [
            {'radius': r, 'opacity': 0.7 - (i * 0.1)}
            for i, r in enumerate(np.linspace(0.1, depth, 5))
        ]
        
        return self.breach_points
    
    def emit_sonar(self, pattern: str) -> SonarPattern:
        """
        Trigger sonar lattice visualization with the specified pattern.
        
        Args:
            pattern: The type of sonar pattern to emit ('lattice', 'wave', 'pulse')
            
        Returns:
            The active sonar pattern
        """
        # Create new sonar pattern
        self.active_sonar = SonarPattern(
            pattern_type=pattern,
            frequency=2.0 if pattern == 'lattice' else 1.0,
            amplitude=1.0,
            phase=0.0,
            echo_depth=3,
            timestamp=datetime.now()
        )
        
        # Update visualization state
        self.visualization_state['sonar_active'] = True
        self.visualization_state['resonance_arcs'] = [
            {'angle': a, 'length': 1.0, 'opacity': 0.8}
            for a in np.linspace(0, 2 * np.pi, 8)
        ]
        
        return self.active_sonar
    
    def get_visualization_state(self) -> Dict:
        """Get the current visualization state for rendering."""
        return self.visualization_state
    
    def cleanup(self):
        """Clean up resources and reset state."""
        self.breach_points.clear()
        self.active_sonar = None
        self.visualization_state = {
            'breach_visible': False,
            'sonar_active': False,
            'echo_rings': [],
            'resonance_arcs': []
        } 