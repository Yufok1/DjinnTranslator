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

import time
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class BreathState:
    """Represents the current state of the automaton's breath cycle."""
    phase: float  # Current phase (0-1)
    frequency: float  # Current frequency in Hz
    depth: float  # Current recursion depth multiplier
    entropy: float  # Current system entropy
    coherence: float  # Current system coherence
    timestamp: float  # Current timestamp

class BreathScheduler:
    """Manages the automaton's breath cycle and recursion depth."""
    
    def __init__(self):
        # Core breath parameters
        self.phase = 0.0
        self.frequency = 1.0  # Base frequency in Hz
        self.depth = 1.0  # Base recursion depth
        
        # Modulation thresholds
        self.entropy_threshold = 0.7
        self.coherence_threshold = 0.8
        
        # Modulation rates
        self.frequency_mod_rate = 0.05  # How quickly frequency adjusts
        self.depth_mod_rate = 0.1  # How quickly depth adjusts
        
        # State history
        self.breath_log: List[BreathState] = []
        self.max_log_size = 1000
        
        # Last update time
        self.last_update = time.time()
        
    def update(self, 
               current_entropy: float, 
               current_coherence: float,
               delta_time: float) -> Tuple[float, float, float]:
        """Update the breath cycle and return current phase, frequency, and depth.
        
        Args:
            current_entropy: Current system entropy (0-1)
            current_coherence: Current system coherence (0-1)
            delta_time: Time since last update in seconds
            
        Returns:
            Tuple of (phase, frequency, depth)
        """
        # Adjust frequency based on entropy
        if current_entropy > self.entropy_threshold:
            # Slow down when entropy is high
            self.frequency *= (1.0 - self.frequency_mod_rate)
        else:
            # Return to normal speed
            self.frequency = min(1.0, self.frequency * (1.0 + self.frequency_mod_rate))
            
        # Adjust depth based on coherence
        if current_coherence > self.coherence_threshold:
            # Allow deeper recursion when system is stable
            self.depth = min(2.0, self.depth * (1.0 + self.depth_mod_rate))
        else:
            # Reduce depth when coherence is low
            self.depth = max(0.5, self.depth * (1.0 - self.depth_mod_rate))
            
        # Update phase
        self.phase += delta_time * self.frequency
        if self.phase >= 1.0:
            self.phase = 0.0
            
        # Log current state
        self._log_state(current_entropy, current_coherence)
        
        return self.phase, self.frequency, self.depth
        
    def _log_state(self, entropy: float, coherence: float):
        """Log the current breath state."""
        state = BreathState(
            phase=self.phase,
            frequency=self.frequency,
            depth=self.depth,
            entropy=entropy,
            coherence=coherence,
            timestamp=time.time()
        )
        
        self.breath_log.append(state)
        if len(self.breath_log) > self.max_log_size:
            self.breath_log.pop(0)
            
    def get_breath_pattern(self, window: int = 100) -> Dict:
        """Get the recent breath pattern statistics.
        
        Args:
            window: Number of recent states to analyze
            
        Returns:
            Dictionary containing breath pattern statistics
        """
        if not self.breath_log:
            return {}
            
        recent = self.breath_log[-window:]
        
        return {
            'avg_frequency': sum(s.frequency for s in recent) / len(recent),
            'avg_depth': sum(s.depth for s in recent) / len(recent),
            'entropy_trend': recent[-1].entropy - recent[0].entropy,
            'coherence_trend': recent[-1].coherence - recent[0].coherence,
            'breath_count': len(recent)
        }
        
    def reset(self):
        """Reset the breath scheduler to initial state."""
        self.phase = 0.0
        self.frequency = 1.0
        self.depth = 1.0
        self.breath_log.clear()
        self.last_update = time.time() 