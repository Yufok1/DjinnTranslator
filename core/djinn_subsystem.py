"""
Djinn Subsystem Module

Handles the whispering of cryptographic messages and speaking of portents
through the Djinn interface. Manages whisper pulses and portent vocalization.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

@dataclass
class WhisperPulse:
    """Represents a cryptographic whisper pulse."""
    id: str
    source: str
    depth: int
    content: str
    resonance: float
    timestamp: datetime
    echo_depth: int = 0
    active: bool = True

@dataclass
class PortentVocalization:
    """Represents a portent vocalization with foresight data."""
    id: str
    aspect: str
    horizon: str
    probability: float
    timestamp: datetime
    resonance: float
    echo_depth: int = 0

class DjinnSubsystem:
    """Manages djinn whispering and portent vocalization."""
    
    def __init__(self):
        self.active_whispers: List[WhisperPulse] = []
        self.portent_history: List[PortentVocalization] = []
        self.djinn_state: Dict = {
            'whisper_resonance': 0.0,
            'portent_alignment': 0.0,
            'echo_depth': 0
        }
        
    def whisper(self, source: str, depth: int) -> WhisperPulse:
        """
        Emit a cryptographic whisper pulse from the specified source.
        
        Args:
            source: The source of the whisper
            depth: The depth of the whisper
            
        Returns:
            The whisper pulse
        """
        # Generate whisper content based on source and depth
        content = self._generate_whisper_content(source, depth)
        
        # Calculate resonance based on depth
        resonance = 1.0 - (depth * 0.1)  # Decreases with depth
        
        whisper = WhisperPulse(
            id=f"whisper_{len(self.active_whispers)}",
            source=source,
            depth=depth,
            content=content,
            resonance=max(0.0, resonance),
            timestamp=datetime.now()
        )
        
        self.active_whispers.append(whisper)
        self._update_djinn_state()
        
        return whisper
    
    def speak_portent(self, aspect: str) -> PortentVocalization:
        """
        Vocalize a portent for the specified aspect.
        
        Args:
            aspect: The aspect to speak of
            
        Returns:
            The portent vocalization
        """
        # Generate portent data
        horizon = self._determine_horizon(aspect)
        probability = np.random.uniform(0.5, 1.0)
        resonance = np.random.uniform(0.6, 0.9)
        
        portent = PortentVocalization(
            id=f"portent_{len(self.portent_history)}",
            aspect=aspect,
            horizon=horizon,
            probability=probability,
            timestamp=datetime.now(),
            resonance=resonance
        )
        
        self.portent_history.append(portent)
        self._update_djinn_state()
        
        return portent
    
    def _generate_whisper_content(self, source: str, depth: int) -> str:
        """Generate whisper content based on source and depth."""
        # This is a placeholder for actual cryptographic content generation
        return f"Cryptographic whisper from {source} at depth {depth}"
    
    def _determine_horizon(self, aspect: str) -> str:
        """Determine the temporal horizon for a portent."""
        horizons = ['immediate', 'near', 'far', 'distant']
        weights = [0.3, 0.4, 0.2, 0.1]  # Probability weights for each horizon
        return np.random.choice(horizons, p=weights)
    
    def _update_djinn_state(self):
        """Update the overall djinn state based on active whispers and recent portents."""
        # Update whisper resonance
        active_whispers = [w for w in self.active_whispers if w.active]
        if active_whispers:
            self.djinn_state['whisper_resonance'] = sum(w.resonance for w in active_whispers) / len(active_whispers)
        
        # Update portent alignment
        recent_portents = [p for p in self.portent_history if (datetime.now() - p.timestamp).total_seconds() < 300]  # Last 5 minutes
        if recent_portents:
            self.djinn_state['portent_alignment'] = sum(p.resonance for p in recent_portents) / len(recent_portents)
        
        # Update echo depth
        if active_whispers:
            self.djinn_state['echo_depth'] = max(w.echo_depth for w in active_whispers)
    
    def get_djinn_state(self) -> Dict:
        """Get the current djinn state."""
        return self.djinn_state
    
    def cleanup(self):
        """Clean up resources and reset state."""
        self.active_whispers.clear()
        self.portent_history.clear()
        self.djinn_state = {
            'whisper_resonance': 0.0,
            'portent_alignment': 0.0,
            'echo_depth': 0
        } 