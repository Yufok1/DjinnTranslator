"""
Recursive Wick System
Manages detection, mapping, and visualization of recursive wicks
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from collections import deque

class WickState(Enum):
    """States of a recursive wick"""
    EMERGING = "emerging"      # Wick is forming
    ACTIVE = "active"         # Wick is emitting energy
    CONTAINED = "contained"   # Wick is isolated
    REBOUND = "rebound"      # Wick is being rethreaded
    HARVESTED = "harvested"   # Wick energy is being used
    COLLAPSED = "collapsed"   # Wick has been resolved

@dataclass
class WickPoint:
    """A point along a wick's path"""
    timestamp: float
    position: Tuple[float, float]
    resonance: float
    strain: float
    pattern_type: str
    mirror_echo: float

@dataclass
class RecursiveWick:
    """Represents a detected recursive wick"""
    id: str
    state: WickState
    origin_time: float
    current_time: float
    path: List[WickPoint]
    strain_points: List[Tuple[float, float]]
    pattern_disruption: float
    resonance_spectrum: Dict[str, float]
    mirror_feedback: float
    containment_level: float
    harmonic_potential: float

class WickSystem:
    """Manages recursive wick detection and handling"""
    
    def __init__(self):
        self.active_wicks: Dict[str, RecursiveWick] = {}
        self.wick_history: deque = deque(maxlen=100)
        self.detection_thresholds = {
            "loop_tightness": 0.8,
            "mirror_fragmentation": 0.3,
            "anchor_coherence": 0.7,
            "strain_threshold": 0.6
        }
        self.containment_modes = {
            "isolate": self._isolate_wick,
            "rebind": self._rebind_wick,
            "harvest": self._harvest_wick
        }
    
    def detect_wicks(self, metrics: Dict[str, Any]) -> List[RecursiveWick]:
        """Detect new wicks from system metrics"""
        new_wicks = []
        
        # Check for wick formation conditions
        if (metrics["loop_tightness"] > self.detection_thresholds["loop_tightness"] and
            metrics["mirror_fragmentation"] > self.detection_thresholds["mirror_fragmentation"] and
            metrics["anchor_coherence"] < self.detection_thresholds["anchor_coherence"]):
            
            # Create new wick
            wick = self._create_wick(metrics)
            new_wicks.append(wick)
            self.active_wicks[wick.id] = wick
        
        return new_wicks
    
    def _create_wick(self, metrics: Dict[str, Any]) -> RecursiveWick:
        """Create a new recursive wick"""
        wick_id = f"wick_{int(time.time())}"
        
        # Calculate initial wick properties
        strain_points = self._calculate_strain_points(metrics)
        pattern_disruption = self._calculate_pattern_disruption(metrics)
        resonance_spectrum = self._analyze_resonance(metrics)
        
        # Create wick object
        wick = RecursiveWick(
            id=wick_id,
            state=WickState.EMERGING,
            origin_time=time.time(),
            current_time=time.time(),
            path=[self._create_wick_point(metrics)],
            strain_points=strain_points,
            pattern_disruption=pattern_disruption,
            resonance_spectrum=resonance_spectrum,
            mirror_feedback=metrics.get("mirror_feedback", 0.0),
            containment_level=0.0,
            harmonic_potential=self._calculate_harmonic_potential(metrics)
        )
        
        return wick
    
    def _create_wick_point(self, metrics: Dict[str, Any]) -> WickPoint:
        """Create a point along the wick's path"""
        return WickPoint(
            timestamp=time.time(),
            position=(metrics.get("x", 0.0), metrics.get("y", 0.0)),
            resonance=metrics.get("resonance", 0.0),
            strain=metrics.get("strain", 0.0),
            pattern_type=metrics.get("pattern_type", "unknown"),
            mirror_echo=metrics.get("mirror_echo", 0.0)
        )
    
    def _calculate_strain_points(self, metrics: Dict[str, Any]) -> List[Tuple[float, float]]:
        """Calculate points of high strain in the system"""
        strain_points = []
        if metrics.get("strain", 0.0) > self.detection_thresholds["strain_threshold"]:
            strain_points.append((metrics.get("x", 0.0), metrics.get("y", 0.0)))
        return strain_points
    
    def _calculate_pattern_disruption(self, metrics: Dict[str, Any]) -> float:
        """Calculate the level of pattern disruption"""
        return (1.0 - metrics.get("pattern_coherence", 1.0)) * metrics.get("strain", 0.0)
    
    def _analyze_resonance(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Analyze the resonance spectrum of the wick"""
        return {
            "core": metrics.get("core_resonance", 0.0),
            "phase": metrics.get("phase_resonance", 0.0),
            "mirror": metrics.get("mirror_resonance", 0.0),
            "harmonic": metrics.get("harmonic_resonance", 0.0)
        }
    
    def _calculate_harmonic_potential(self, metrics: Dict[str, Any]) -> float:
        """Calculate the harmonic potential of the wick"""
        resonance = metrics.get("resonance", 0.0)
        stability = metrics.get("stability", 0.0)
        coherence = metrics.get("coherence", 0.0)
        
        return (resonance * 0.4 + stability * 0.3 + coherence * 0.3)
    
    def update_wick(self, wick_id: str, metrics: Dict[str, Any]) -> Optional[RecursiveWick]:
        """Update an existing wick with new metrics"""
        if wick_id not in self.active_wicks:
            return None
        
        wick = self.active_wicks[wick_id]
        
        # Add new point to path
        wick.path.append(self._create_wick_point(metrics))
        
        # Update wick properties
        wick.current_time = time.time()
        wick.strain_points.extend(self._calculate_strain_points(metrics))
        wick.pattern_disruption = self._calculate_pattern_disruption(metrics)
        wick.resonance_spectrum = self._analyze_resonance(metrics)
        wick.mirror_feedback = metrics.get("mirror_feedback", wick.mirror_feedback)
        wick.harmonic_potential = self._calculate_harmonic_potential(metrics)
        
        # Update wick state
        self._update_wick_state(wick, metrics)
        
        return wick
    
    def _update_wick_state(self, wick: RecursiveWick, metrics: Dict[str, Any]):
        """Update the state of a wick based on current metrics"""
        if wick.state == WickState.EMERGING:
            if metrics.get("strain", 0.0) > self.detection_thresholds["strain_threshold"]:
                wick.state = WickState.ACTIVE
        elif wick.state == WickState.ACTIVE:
            if wick.containment_level > 0.8:
                wick.state = WickState.CONTAINED
        elif wick.state == WickState.CONTAINED:
            if metrics.get("rebinding_progress", 0.0) > 0.5:
                wick.state = WickState.REBOUND
    
    def contain_wick(self, wick_id: str, mode: str) -> bool:
        """Apply containment to a wick"""
        if wick_id not in self.active_wicks:
            return False
        
        wick = self.active_wicks[wick_id]
        
        if mode in self.containment_modes:
            self.containment_modes[mode](wick)
            return True
        
        return False
    
    def _isolate_wick(self, wick: RecursiveWick):
        """Isolate a wick from the system"""
        wick.containment_level = min(1.0, wick.containment_level + 0.2)
        wick.state = WickState.CONTAINED
    
    def _rebind_wick(self, wick: RecursiveWick):
        """Rebind a wick into the system"""
        wick.containment_level = max(0.0, wick.containment_level - 0.1)
        wick.state = WickState.REBOUND
    
    def _harvest_wick(self, wick: RecursiveWick):
        """Harvest energy from a wick"""
        if wick.harmonic_potential > 0.7:
            wick.state = WickState.HARVESTED
        else:
            wick.state = WickState.COLLAPSED
    
    def get_wick_visualization(self, wick_id: str) -> Dict[str, Any]:
        """Get visualization data for a wick"""
        if wick_id not in self.active_wicks:
            return {}
        
        wick = self.active_wicks[wick_id]
        
        return {
            "path": [(p.position[0], p.position[1]) for p in wick.path],
            "strain_points": wick.strain_points,
            "resonance": [p.resonance for p in wick.path],
            "mirror_feedback": wick.mirror_feedback,
            "containment": wick.containment_level,
            "harmonic_potential": wick.harmonic_potential,
            "state": wick.state.value
        }
    
    def get_active_wicks(self) -> List[Dict[str, Any]]:
        """Get data for all active wicks"""
        return [
            {
                "id": wick.id,
                "state": wick.state.value,
                "age": wick.current_time - wick.origin_time,
                "strain": max(p.strain for p in wick.path),
                "resonance": max(p.resonance for p in wick.path),
                "containment": wick.containment_level,
                "harmonic_potential": wick.harmonic_potential
            }
            for wick in self.active_wicks.values()
        ] 