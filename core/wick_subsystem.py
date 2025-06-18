"""
Wick Subsystem Module

Handles the binding of wicks and harvesting of insight from the system.
Manages wick resonance, insight capsules, and stabilization cycles.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

@dataclass
class WickBinding:
    """Represents a bound wick with resonance and stabilization data."""
    id: str
    strength: float
    cycles: int
    start_time: datetime
    resonance_level: float
    stabilization_progress: float = 0.0
    active: bool = True

@dataclass
class InsightCapsule:
    """Represents an insight capsule harvested from the system."""
    id: str
    depth: int
    content: str
    resonance: float
    timestamp: datetime
    source: str
    echo_depth: int = 0

class WickSubsystem:
    """Manages wick binding and insight harvesting."""
    
    def __init__(self):
        self.active_bindings: List[WickBinding] = []
        self.insight_capsules: List[InsightCapsule] = []
        self.stabilization_state: Dict = {
            'active_cycles': 0,
            'total_resonance': 0.0,
            'stabilization_level': 0.0
        }
        
    def bind_wick(self, strength: float, cycles: int) -> WickBinding:
        """
        Create a new wick binding with the specified strength and cycles.
        
        Args:
            strength: The binding strength (0.0 to 1.0)
            cycles: Number of stabilization cycles
            
        Returns:
            The created wick binding
        """
        binding = WickBinding(
            id=f"wick_{len(self.active_bindings)}",
            strength=min(1.0, max(0.0, strength)),
            cycles=max(1, cycles),
            start_time=datetime.now(),
            resonance_level=strength
        )
        
        self.active_bindings.append(binding)
        self.stabilization_state['active_cycles'] += cycles
        
        return binding
    
    def harvest_insight(self, depth: int) -> List[InsightCapsule]:
        """
        Harvest insight capsules from the specified depth.
        
        Args:
            depth: The depth to harvest from
            
        Returns:
            List of harvested insight capsules
        """
        # Generate insight capsules based on depth
        num_capsules = max(1, depth)
        new_capsules = []
        
        for i in range(num_capsules):
            capsule = InsightCapsule(
                id=f"insight_{len(self.insight_capsules)}",
                depth=depth,
                content=f"Insight at depth {depth}",
                resonance=np.random.uniform(0.5, 1.0),
                timestamp=datetime.now(),
                source="system",
                echo_depth=i % depth
            )
            new_capsules.append(capsule)
            self.insight_capsules.append(capsule)
        
        return new_capsules
    
    def update_stabilization(self):
        """Update the stabilization state of all active bindings."""
        for binding in self.active_bindings:
            if binding.active:
                # Calculate stabilization progress
                elapsed_cycles = (datetime.now() - binding.start_time).total_seconds() / 5.0  # 5 seconds per cycle
                binding.stabilization_progress = min(1.0, elapsed_cycles / binding.cycles)
                
                if binding.stabilization_progress >= 1.0:
                    binding.active = False
                    self.stabilization_state['active_cycles'] -= binding.cycles
        
        # Update overall stabilization state
        active_bindings = [b for b in self.active_bindings if b.active]
        if active_bindings:
            self.stabilization_state['total_resonance'] = sum(b.resonance_level for b in active_bindings) / len(active_bindings)
            self.stabilization_state['stabilization_level'] = sum(b.stabilization_progress for b in active_bindings) / len(active_bindings)
        else:
            self.stabilization_state['total_resonance'] = 0.0
            self.stabilization_state['stabilization_level'] = 0.0
    
    def get_stabilization_state(self) -> Dict:
        """Get the current stabilization state."""
        return self.stabilization_state
    
    def cleanup(self):
        """Clean up resources and reset state."""
        self.active_bindings.clear()
        self.insight_capsules.clear()
        self.stabilization_state = {
            'active_cycles': 0,
            'total_resonance': 0.0,
            'stabilization_level': 0.0
        } 