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

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import math
import colorsys

@dataclass
class SymbolicElement:
    """Represents a symbolic element in HSM."""
    primary_glyph: str
    secondary_glyphs: List[str]
    resonance_color: Tuple[int, int, int]
    harmonic_frequency: float
    motion_pattern: str
    ambient_sound: str

@dataclass
class SymbolicState:
    """Represents the current state of symbolic elements."""
    resonance_level: float
    harmonic_phase: float
    motion_amplitude: float
    ambient_intensity: float
    symbolic_density: float

class HighSymbologyMode:
    """Manages the High Symbology Mode interface."""
    
    def __init__(self):
        self.symbolic_elements: Dict[str, SymbolicElement] = {}
        self.current_state = SymbolicState(
            resonance_level=0.0,
            harmonic_phase=0.0,
            motion_amplitude=1.0,
            ambient_intensity=0.5,
            symbolic_density=0.7
        )
        
        # Initialize symbolic elements
        self._initialize_symbolic_elements()
        
    def _initialize_symbolic_elements(self):
        """Initialize the symbolic elements for HSM."""
        self.symbolic_elements = {
            "perception": SymbolicElement(
                primary_glyph="👁️",
                secondary_glyphs=["🌊", "🌀", "✨"],
                resonance_color=(100, 150, 255),
                harmonic_frequency=440.0,  # A4
                motion_pattern="flow",
                ambient_sound="wind"
            ),
            "reasoning": SymbolicElement(
                primary_glyph="⚡",
                secondary_glyphs=["🔮", "💫", "🌌"],
                resonance_color=(150, 255, 150),
                harmonic_frequency=523.25,  # C5
                motion_pattern="pulse",
                ambient_sound="crystal"
            ),
            "memory": SymbolicElement(
                primary_glyph="💾",
                secondary_glyphs=["📚", "🎭", "🔄"],
                resonance_color=(255, 100, 150),
                harmonic_frequency=392.0,  # G4
                motion_pattern="spiral",
                ambient_sound="echo"
            ),
            "action": SymbolicElement(
                primary_glyph="🎯",
                secondary_glyphs=["⚔️", "🌠", "🎨"],
                resonance_color=(255, 200, 100),
                harmonic_frequency=493.88,  # B4
                motion_pattern="burst",
                ambient_sound="thunder"
            )
        }
        
    def get_element_representation(self, element_id: str, 
                                 state: SymbolicState) -> Dict[str, Any]:
        """Get the symbolic representation of an element."""
        element = self.symbolic_elements.get(element_id)
        if not element:
            return {}
            
        # Calculate resonance-based color
        base_color = element.resonance_color
        resonance_mod = math.sin(state.resonance_level * math.pi)
        color = self._modulate_color(base_color, resonance_mod)
        
        # Calculate motion parameters
        motion = self._calculate_motion(element.motion_pattern, state)
        
        # Calculate harmonic parameters
        harmonic = self._calculate_harmonic(element.harmonic_frequency, state)
        
        return {
            "primary_glyph": element.primary_glyph,
            "secondary_glyphs": element.secondary_glyphs,
            "color": color,
            "motion": motion,
            "harmonic": harmonic,
            "ambient": {
                "sound": element.ambient_sound,
                "intensity": state.ambient_intensity
            }
        }
    
    def _modulate_color(self, base_color: Tuple[int, int, int], 
                       modulation: float) -> Tuple[int, int, int]:
        """Modulate a color based on resonance."""
        r, g, b = base_color
        mod = 0.2 * modulation
        
        return (
            int(r * (1.0 + mod)),
            int(g * (1.0 + mod)),
            int(b * (1.0 + mod))
        )
    
    def _calculate_motion(self, pattern: str, 
                         state: SymbolicState) -> Dict[str, float]:
        """Calculate motion parameters based on pattern and state."""
        amplitude = state.motion_amplitude
        phase = state.harmonic_phase
        
        if pattern == "flow":
            return {
                "type": "flow",
                "amplitude": amplitude,
                "direction": math.sin(phase),
                "speed": 1.0 + 0.5 * math.sin(phase * 2)
            }
        elif pattern == "pulse":
            return {
                "type": "pulse",
                "amplitude": amplitude * (0.8 + 0.2 * math.sin(phase)),
                "frequency": 1.0 + 0.5 * math.sin(phase),
                "phase": phase
            }
        elif pattern == "spiral":
            return {
                "type": "spiral",
                "amplitude": amplitude,
                "rotation": phase * 2 * math.pi,
                "expansion": 1.0 + 0.3 * math.sin(phase)
            }
        else:  # burst
            return {
                "type": "burst",
                "amplitude": amplitude * (1.0 + 0.5 * math.sin(phase)),
                "spread": 0.5 + 0.5 * math.sin(phase),
                "intensity": 1.0 + 0.3 * math.sin(phase * 2)
            }
    
    def _calculate_harmonic(self, base_frequency: float, 
                          state: SymbolicState) -> Dict[str, float]:
        """Calculate harmonic parameters based on state."""
        resonance = state.resonance_level
        phase = state.harmonic_phase
        
        return {
            "frequency": base_frequency * (1.0 + 0.1 * math.sin(phase)),
            "amplitude": 0.5 + 0.5 * resonance,
            "phase": phase,
            "modulation": 0.2 * math.sin(phase * 2)
        }
    
    def update_state(self, resonance: float, phase: float, 
                    amplitude: float, intensity: float, density: float):
        """Update the symbolic state."""
        self.current_state = SymbolicState(
            resonance_level=max(0.0, min(1.0, resonance)),
            harmonic_phase=phase % (2 * math.pi),
            motion_amplitude=max(0.0, min(2.0, amplitude)),
            ambient_intensity=max(0.0, min(1.0, intensity)),
            symbolic_density=max(0.0, min(1.0, density))
        )
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get information about the current symbolic state."""
        return {
            "resonance": self.current_state.resonance_level,
            "harmonic_phase": self.current_state.harmonic_phase,
            "motion_amplitude": self.current_state.motion_amplitude,
            "ambient_intensity": self.current_state.ambient_intensity,
            "symbolic_density": self.current_state.symbolic_density,
            "active_elements": len(self.symbolic_elements)
        } 