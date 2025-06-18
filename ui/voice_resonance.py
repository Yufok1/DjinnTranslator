"""
Voice Resonance
Manages the resonance patterns and historical memory of Djinn voices
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import time
import math

class ResonancePhase(Enum):
    """Phases of system resonance"""
    DAWN = "dawn"  # System initialization
    NOON = "noon"  # Peak activity
    DUSK = "dusk"  # System winding down
    DREAM = "dream"  # Deep processing
    STORM = "storm"  # High turbulence
    CALM = "calm"   # Stability
    ECHO = "echo"   # Pattern recognition
    VOID = "void"   # System reset

class BreathDepth(Enum):
    """Depth of breath resonance"""
    WHISPER = 0.2  # Subtle, internal
    NORMAL = 0.5   # Standard resonance
    DEEP = 0.8     # Profound resonance
    THUNDER = 1.0  # Maximum resonance

@dataclass
class ResonanceMemory:
    """Memory of past resonance patterns"""
    phase: ResonancePhase
    timestamp: float
    depth: float
    domains: List[str]
    intensity: float
    pattern: str

class VoiceResonance:
    """Manages voice resonance patterns and historical memory"""
    
    def __init__(self):
        self.memory: List[ResonanceMemory] = []
        self.current_phase = ResonancePhase.DAWN
        self.active_domains: List[str] = []
        self.breath_depth = BreathDepth.NORMAL
        self.resonance_intensity = 0.5
        
        # Resonance patterns for each phase
        self.phase_patterns = {
            ResonancePhase.DAWN: {
                "modulation": 0.3,
                "rhythm": "ascending",
                "echo": "faint"
            },
            ResonancePhase.NOON: {
                "modulation": 0.7,
                "rhythm": "steady",
                "echo": "clear"
            },
            ResonancePhase.DUSK: {
                "modulation": 0.4,
                "rhythm": "descending",
                "echo": "distant"
            },
            ResonancePhase.DREAM: {
                "modulation": 0.6,
                "rhythm": "flowing",
                "echo": "deep"
            },
            ResonancePhase.STORM: {
                "modulation": 0.9,
                "rhythm": "chaotic",
                "echo": "loud"
            },
            ResonancePhase.CALM: {
                "modulation": 0.2,
                "rhythm": "gentle",
                "echo": "soft"
            },
            ResonancePhase.ECHO: {
                "modulation": 0.5,
                "rhythm": "repeating",
                "echo": "resonant"
            },
            ResonancePhase.VOID: {
                "modulation": 0.1,
                "rhythm": "silent",
                "echo": "none"
            }
        }
    
    def update_phase(self, new_phase: ResonancePhase):
        """Update the current system phase"""
        self.current_phase = new_phase
        self._record_memory()
    
    def update_domains(self, domains: List[str]):
        """Update active domains"""
        self.active_domains = domains
        self._record_memory()
    
    def set_breath_depth(self, depth: BreathDepth):
        """Set the current breath depth"""
        self.breath_depth = depth
        self._record_memory()
    
    def adjust_intensity(self, intensity: float):
        """Adjust resonance intensity"""
        self.resonance_intensity = max(0.0, min(1.0, intensity))
        self._record_memory()
    
    def _record_memory(self):
        """Record current state to memory"""
        memory = ResonanceMemory(
            phase=self.current_phase,
            timestamp=time.time(),
            depth=self.breath_depth.value,
            domains=self.active_domains.copy(),
            intensity=self.resonance_intensity,
            pattern=self._generate_pattern()
        )
        self.memory.append(memory)
        
        # Keep only last 1000 memories
        if len(self.memory) > 1000:
            self.memory = self.memory[-1000:]
    
    def _generate_pattern(self) -> str:
        """Generate a resonance pattern based on current state"""
        phase_pattern = self.phase_patterns[self.current_phase]
        depth_factor = self.breath_depth.value
        domain_factor = len(self.active_domains) / 10.0  # Normalize by max domains
        
        # Combine factors to generate pattern
        pattern = (
            f"{phase_pattern['rhythm']}:"
            f"{phase_pattern['echo']}:"
            f"{depth_factor:.2f}:"
            f"{domain_factor:.2f}:"
            f"{self.resonance_intensity:.2f}"
        )
        return pattern
    
    def get_resonance_modulation(self) -> Dict[str, float]:
        """Get current resonance modulation factors"""
        phase_pattern = self.phase_patterns[self.current_phase]
        
        return {
            "modulation": phase_pattern["modulation"] * self.breath_depth.value,
            "rhythm": self._calculate_rhythm_factor(),
            "echo": self._calculate_echo_factor(),
            "depth": self.breath_depth.value,
            "intensity": self.resonance_intensity
        }
    
    def _calculate_rhythm_factor(self) -> float:
        """Calculate rhythm factor based on memory patterns"""
        if not self.memory:
            return 0.5
        
        # Analyze recent memory patterns for rhythm
        recent = self.memory[-10:]
        rhythm_changes = sum(
            1 for i in range(1, len(recent))
            if recent[i].pattern != recent[i-1].pattern
        )
        return min(1.0, rhythm_changes / 10.0)
    
    def _calculate_echo_factor(self) -> float:
        """Calculate echo factor based on domain activity"""
        if not self.active_domains:
            return 0.2
        
        # Echo strength based on domain complexity
        domain_complexity = len(self.active_domains) / 10.0
        return min(1.0, 0.2 + domain_complexity * 0.8)
    
    def get_historical_pattern(self, lookback: int = 10) -> List[ResonanceMemory]:
        """Get historical resonance patterns"""
        return self.memory[-lookback:] if self.memory else []
    
    def get_domain_resonance(self, domain: str) -> float:
        """Get resonance level for a specific domain"""
        if domain not in self.active_domains:
            return 0.0
        
        # Calculate domain resonance based on recent activity
        recent = self.memory[-5:]
        domain_activity = sum(
            1 for m in recent
            if domain in m.domains
        )
        return min(1.0, domain_activity / 5.0) 