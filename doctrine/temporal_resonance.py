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
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import time
from enum import Enum

class ResonanceThreshold(Enum):
    """Thresholds for triggering different resonance-based actions."""
    JUDGMENT = 0.85  # Threshold for triggering DREDD judgment
    WARNING = 0.70   # Threshold for system warnings
    STABLE = 0.50    # Threshold for stable operation
    CRITICAL = 0.30  # Threshold for critical intervention

@dataclass
class ResonanceMetrics:
    """Metrics for temporal resonance calculations."""
    mirror_strain: float = 0.0  # Tension between mirrors
    entropic_drift: float = 0.0  # Rate of temporal entropy increase
    foresight_reactivity: float = 0.0  # System's ability to respond to foresight
    coherence_threshold: float = 0.0  # Current coherence threshold
    temporal_delta: float = 0.0  # Phase difference between mirrors
    judgment_trigger: bool = False  # Whether judgment should be triggered

class TemporalResonance:
    """Advanced temporal resonance calculations and analysis."""
    def __init__(self):
        self.metrics = ResonanceMetrics()
        self.history: List[Dict[str, Any]] = []
        self.last_calculation = time.time()
        self.strain_threshold = 0.75
        self.drift_threshold = 0.60
        self.reactivity_threshold = 0.80
        
    def calculate_mirror_strain(self, 
                              portent: Dict[str, Any],
                              present: Dict[str, Any],
                              trace: Dict[str, Any]) -> float:
        """Calculate strain between mirrors based on their alignment."""
        # Extract key metrics
        portent_strength = portent.get('strength', 0.0)
        present_coherence = present.get('coherence', 0.0)
        trace_depth = trace.get('depth', 0.0)
        
        # Calculate phase differences
        portent_phase = portent.get('temporal_phase', 0.0)
        present_phase = present.get('temporal_phase', 0.0)
        trace_phase = trace.get('temporal_phase', 0.0)
        
        # Calculate phase deltas
        portent_present_delta = abs(portent_phase - present_phase)
        present_trace_delta = abs(present_phase - trace_phase)
        portent_trace_delta = abs(portent_phase - trace_phase)
        
        # Calculate metric differences
        strength_coherence_diff = abs(portent_strength - present_coherence)
        coherence_depth_diff = abs(present_coherence - trace_depth)
        strength_depth_diff = abs(portent_strength - trace_depth)
        
        # Combine phase and metric differences
        phase_strain = (portent_present_delta + present_trace_delta + portent_trace_delta) / 3.0
        metric_strain = (strength_coherence_diff + coherence_depth_diff + strength_depth_diff) / 3.0
        
        # Calculate final strain
        strain = (phase_strain + metric_strain) / 2.0
        return min(1.0, max(0.0, strain))
        
    def calculate_entropic_drift(self, 
                               current_metrics: Dict[str, float],
                               previous_metrics: Dict[str, float]) -> float:
        """Calculate the rate of temporal entropy increase."""
        # Calculate changes in key metrics
        coherence_drift = abs(current_metrics.get('coherence', 1.0) - 
                            previous_metrics.get('coherence', 1.0))
        resonance_drift = abs(current_metrics.get('resonance', 1.0) - 
                            previous_metrics.get('resonance', 1.0))
        alignment_drift = abs(current_metrics.get('temporal_alignment', 1.0) - 
                            previous_metrics.get('temporal_alignment', 1.0))
        
        # Calculate time delta
        time_delta = time.time() - self.last_calculation
        if time_delta == 0:
            return 0.0
            
        # Calculate drift rates
        coherence_rate = coherence_drift / time_delta
        resonance_rate = resonance_drift / time_delta
        alignment_rate = alignment_drift / time_delta
        
        # Combine drift rates
        total_drift = (coherence_rate + resonance_rate + alignment_rate) / 3.0
        return min(1.0, max(0.0, total_drift))
        
    def calculate_foresight_reactivity(self,
                                     portent: Dict[str, Any],
                                     present: Dict[str, Any],
                                     trace: Dict[str, Any]) -> float:
        """Calculate system's ability to respond to foresight."""
        # Extract foresight metrics
        portent_strength = portent.get('strength', 0.0)
        present_coherence = present.get('coherence', 0.0)
        trace_depth = trace.get('depth', 0.0)
        
        # Calculate reactivity factors
        foresight_clarity = portent_strength * present_coherence
        present_responsiveness = present_coherence * (1.0 - abs(present_coherence - trace_depth))
        trace_influence = trace_depth * portent_strength
        
        # Combine factors
        reactivity = (foresight_clarity + present_responsiveness + trace_influence) / 3.0
        return min(1.0, max(0.0, reactivity))
        
    def calculate_temporal_delta(self,
                               portent: Dict[str, Any],
                               present: Dict[str, Any],
                               trace: Dict[str, Any]) -> float:
        """Calculate phase difference between mirrors."""
        # Extract temporal phases
        portent_phase = portent.get('temporal_phase', 0.0)
        present_phase = present.get('temporal_phase', 0.0)
        trace_phase = trace.get('temporal_phase', 0.0)
        
        # Calculate phase differences
        portent_present_delta = abs(portent_phase - present_phase)
        present_trace_delta = abs(present_phase - trace_phase)
        portent_trace_delta = abs(portent_phase - trace_phase)
        
        # Calculate weighted average
        total_delta = (portent_present_delta + present_trace_delta + portent_trace_delta) / 3.0
        return min(1.0, max(0.0, total_delta))
        
    def check_judgment_trigger(self, metrics: ResonanceMetrics) -> bool:
        """Check if judgment should be triggered based on resonance metrics."""
        # Check individual thresholds
        strain_trigger = metrics.mirror_strain > self.strain_threshold
        drift_trigger = metrics.entropic_drift > self.drift_threshold
        reactivity_trigger = metrics.foresight_reactivity < self.reactivity_threshold
        
        # Check overall coherence
        coherence_trigger = metrics.coherence_threshold < ResonanceThreshold.JUDGMENT.value
        
        # Trigger judgment if multiple conditions are met
        trigger_count = sum([strain_trigger, drift_trigger, 
                           reactivity_trigger, coherence_trigger])
        return trigger_count >= 2
        
    def update_resonance(self,
                        portent: Dict[str, Any],
                        present: Dict[str, Any],
                        trace: Dict[str, Any],
                        current_metrics: Dict[str, float]) -> ResonanceMetrics:
        """Update all resonance metrics based on current mirror states."""
        # Calculate new metrics
        mirror_strain = self.calculate_mirror_strain(portent, present, trace)
        entropic_drift = self.calculate_entropic_drift(
            current_metrics,
            self.history[-1]['metrics'] if self.history else current_metrics
        )
        foresight_reactivity = self.calculate_foresight_reactivity(portent, present, trace)
        temporal_delta = self.calculate_temporal_delta(portent, present, trace)
        
        # Update metrics
        self.metrics.mirror_strain = mirror_strain
        self.metrics.entropic_drift = entropic_drift
        self.metrics.foresight_reactivity = foresight_reactivity
        self.metrics.temporal_delta = temporal_delta
        self.metrics.coherence_threshold = current_metrics.get('coherence', 1.0)
        
        # Check for judgment trigger
        self.metrics.judgment_trigger = self.check_judgment_trigger(self.metrics)
        
        # Record history
        self.history.append({
            'timestamp': time.time(),
            'metrics': current_metrics,
            'resonance_metrics': self.metrics.__dict__
        })
        
        self.last_calculation = time.time()
        return self.metrics
        
    def get_resonance_analysis(self) -> Dict[str, Any]:
        """Get comprehensive resonance analysis."""
        return {
            'current_metrics': self.metrics.__dict__,
            'thresholds': {
                'strain': self.strain_threshold,
                'drift': self.drift_threshold,
                'reactivity': self.reactivity_threshold
            },
            'judgment_triggered': self.metrics.judgment_trigger,
            'history_length': len(self.history)
        } 