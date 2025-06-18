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
Visual Renderer Module

Provides core rendering capabilities for the dashboard visualization system.
Integrates with the existing visualization infrastructure.
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import numpy as np
from .visualization import VisualizationSystem, VisualStyle, AnimationState

class VisualRenderer:
    """Core renderer for dashboard visualization components."""
    
    def __init__(self):
        """Initialize VisualRenderer with visualization system integration."""
        self.visualization_system = VisualizationSystem()
        self.active = False
        self.current_phase = "init"
        self.resonance = 0.0
        self.animation_states: Dict[str, AnimationState] = {}
        
    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render visual data using the visualization system.
        
        Args:
            data: Dictionary containing visualization data including:
                - phase: Current breath phase
                - resonance: Current resonance level
                - elements: Visual elements to render
                - animations: Animation states
                
        Returns:
            Dictionary containing rendered visual state
        """
        self.active = True
        self.current_phase = data.get("phase", self.current_phase)
        self.resonance = data.get("resonance", self.resonance)
        
        # Update visualization system state
        visual_state = {
            "phase": self.current_phase,
            "resonance": self.resonance,
            "elements": data.get("elements", {}),
            "animations": self.animation_states
        }
        
        # Process through visualization system
        rendered_state = self.visualization_system.visualize_phase_reflection(phase=self.current_phase, resonance=self.resonance)
        
        # Merge with additional elements
        rendered_state.update(visual_state)
        
        return rendered_state

    def export(self, path: str) -> bool:
        """Export current visual state to specified path.
        
        Args:
            path: File path to export visual state
            
        Returns:
            True if export successful, False otherwise
        """
        if not self.active:
            return False
            
        try:
            # Get current system state
            state = self.visualization_system.get_system_state()
            
            # Add renderer state
            state.update({
                "active": self.active,
                "current_phase": self.current_phase,
                "resonance": self.resonance,
                "animation_states": self.animation_states
            })
            
            # Export using visualization system
            self.visualization_system.cleanup()
            return True
            
        except Exception:
            return False

    def clear(self) -> None:
        """Clear all visual states and reset renderer."""
        self.active = False
        self.current_phase = "init"
        self.resonance = 0.0
        self.animation_states.clear()
        self.visualization_system.cleanup()

    def update_visual_state(self, entity, visual_state):
        """
        Update the visual state for a specific entity. This method accepts
        both the entity and the new visual state to update the internal state.

        :param entity: The entity whose visual state is being updated.
        :param visual_state: The new visual state to assign to the entity.
        """
        print(f"Updating visual state for {entity}: {visual_state}")
        if not hasattr(self, 'visual_state') or not isinstance(self.visual_state, dict):
            self.visual_state = {}
        self.visual_state[entity] = visual_state  # Store entity and state in visual_state

# Example utility function to demonstrate visual state updates

def update_state_example():
    """
    A sample utility function to demonstrate how the visual state might be updated.
    """
    renderer = VisualRenderer()
    new_state = {"color": "blue", "status": "active"}
    renderer.update_visual_state("entity_1", new_state)
    print(f"Visual state updated: {renderer.visual_state}")
    return renderer.visual_state 