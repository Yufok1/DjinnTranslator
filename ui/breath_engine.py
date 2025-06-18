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

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
import time

@dataclass
class BreathState:
    """Represents the current state of the breath system."""
    phase: float = 0.0
    frequency: float = 1.0
    amplitude: float = 1.0
    modulation: Dict[str, float] = field(default_factory=dict)
    resonance: float = 1.0
    coherence: float = 1.0
    stability: float = 1.0
    alignment: float = 1.0
    echo_depth: float = 0.0
    recursive_depth: int = 0
    recursive_breadth: int = 0
    recursive_stability: float = 1.0
    recursive_coherence: float = 1.0
    recursive_resonance: float = 1.0
    recursive_breath: float = 1.0
    recursive_echo: float = 0.0
    recursive_phase: float = 0.0
    recursive_frequency: float = 1.0
    recursive_amplitude: float = 1.0
    recursive_modulation: Dict[str, float] = field(default_factory=dict)
    recursive_resonance_profile: Dict[str, float] = field(default_factory=dict)

class BreathEngine:
    """Manages the breath system and its interactions with voice memories."""
    
    def __init__(self):
        self.state = BreathState()
        self.last_update = time.time()
        self.breath_patterns: Dict[str, List[float]] = {}
        self.resonance_patterns: Dict[str, List[float]] = {}
        self.echo_patterns: Dict[str, List[float]] = {}
        self.recursive_patterns: Dict[str, List[float]] = {}
    
    def update(self, dt: float):
        """Update breath state based on elapsed time."""
        # Update phase
        self.state.phase += self.state.frequency * dt
        
        # Normalize phase to [0, 2π]
        self.state.phase = self.state.phase % (2 * np.pi)
        
        # Update recursive state
        self._update_recursive_state(dt)
        
        # Update modulation
        self._update_modulation(dt)
        
        # Update resonance
        self._update_resonance(dt)
        
        # Update coherence
        self._update_coherence(dt)
        
        # Update stability
        self._update_stability(dt)
        
        # Update alignment
        self._update_alignment(dt)
        
        # Update echo depth
        self._update_echo_depth(dt)
        
        self.last_update = time.time()
    
    def _update_recursive_state(self, dt: float):
        """Update recursive state parameters."""
        # Update recursive phase
        self.state.recursive_phase += self.state.recursive_frequency * dt
        self.state.recursive_phase = self.state.recursive_phase % (2 * np.pi)
        
        # Update recursive modulation
        for key in self.state.recursive_modulation:
            self.state.recursive_modulation[key] *= np.cos(self.state.recursive_phase)
    
    def _update_modulation(self, dt: float):
        """Update breath modulation."""
        for key in self.state.modulation:
            self.state.modulation[key] *= np.cos(self.state.phase)
    
    def _update_resonance(self, dt: float):
        """Update breath resonance."""
        self.state.resonance = np.cos(self.state.phase) * self.state.amplitude
    
    def _update_coherence(self, dt: float):
        """Update breath coherence."""
        self.state.coherence = np.sin(self.state.phase) * self.state.amplitude
    
    def _update_stability(self, dt: float):
        """Update breath stability."""
        self.state.stability = np.cos(self.state.phase * 0.5) * self.state.amplitude
    
    def _update_alignment(self, dt: float):
        """Update breath alignment."""
        self.state.alignment = np.sin(self.state.phase * 0.5) * self.state.amplitude
    
    def _update_echo_depth(self, dt: float):
        """Update echo depth."""
        self.state.echo_depth = np.cos(self.state.phase * 0.25) * self.state.amplitude
    
    def get_breath_value(self) -> float:
        """Get current breath value."""
        return np.sin(self.state.phase) * self.state.amplitude
    
    def get_recursive_breath_value(self) -> float:
        """Get current recursive breath value."""
        return np.sin(self.state.recursive_phase) * self.state.recursive_amplitude
    
    def get_modulation_value(self, key: str) -> float:
        """Get current modulation value for a given key."""
        return self.state.modulation.get(key, 0.0)
    
    def get_recursive_modulation_value(self, key: str) -> float:
        """Get current recursive modulation value for a given key."""
        return self.state.recursive_modulation.get(key, 0.0)
    
    def register_breath_pattern(self, pattern_id: str, pattern: List[float]):
        """Register a new breath pattern."""
        self.breath_patterns[pattern_id] = pattern
    
    def register_resonance_pattern(self, pattern_id: str, pattern: List[float]):
        """Register a new resonance pattern."""
        self.resonance_patterns[pattern_id] = pattern
    
    def register_echo_pattern(self, pattern_id: str, pattern: List[float]):
        """Register a new echo pattern."""
        self.echo_patterns[pattern_id] = pattern
    
    def register_recursive_pattern(self, pattern_id: str, pattern: List[float]):
        """Register a new recursive pattern."""
        self.recursive_patterns[pattern_id] = pattern
    
    def get_breath_pattern(self, pattern_id: str) -> Optional[List[float]]:
        """Get a registered breath pattern."""
        return self.breath_patterns.get(pattern_id)
    
    def get_resonance_pattern(self, pattern_id: str) -> Optional[List[float]]:
        """Get a registered resonance pattern."""
        return self.resonance_patterns.get(pattern_id)
    
    def get_echo_pattern(self, pattern_id: str) -> Optional[List[float]]:
        """Get a registered echo pattern."""
        return self.echo_patterns.get(pattern_id)
    
    def get_recursive_pattern(self, pattern_id: str) -> Optional[List[float]]:
        """Get a registered recursive pattern."""
        return self.recursive_patterns.get(pattern_id) 