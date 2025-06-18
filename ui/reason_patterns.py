"""
Reason Pattern Analysis
Analyzes patterns in Cursor's reasoning and their resonance across the system
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import deque
import time

class PatternType(Enum):
    """Types of reason patterns."""
    BREAKTHROUGH = "breakthrough"  # Insight-driven pattern
    TURBULENCE = "turbulence"      # Strain-driven pattern
    HARMONY = "harmony"           # Stability-driven pattern
    EXPLORATION = "exploration"    # Discovery-driven pattern
    RECOVERY = "recovery"         # Healing-driven pattern

@dataclass
class Pattern:
    """A detected reason pattern."""
    pattern_type: PatternType
    sequence: List[str]  # List of reason types in sequence
    start_time: float
    end_time: float
    resonance: float
    mirror_echo: bool
    loop_tightness: float  # How quickly the pattern resolves
    domain_activation: Dict[str, float]  # Which domains were activated

class ReasonPatternAnalyzer:
    """Analyzes patterns in Cursor's reasoning."""
    
    def __init__(self, window_size: int = 10):
        """Initialize the pattern analyzer."""
        self.window_size = window_size
        self.reason_buffer = deque(maxlen=window_size)
        self.patterns: List[Pattern] = []
        
        # Pattern templates
        self.pattern_templates = {
            PatternType.BREAKTHROUGH: [
                ["STABILIZING", "EXPLORATIVE", "HARMONIC"],
                ["REACTIVE", "EXPLORATIVE", "HARMONIC"]
            ],
            PatternType.TURBULENCE: [
                ["REACTIVE", "REACTIVE", "DEFERRED"],
                ["STABILIZING", "REACTIVE", "DEFERRED"]
            ],
            PatternType.HARMONY: [
                ["STABILIZING", "HARMONIC", "STABILIZING"],
                ["HARMONIC", "STABILIZING", "HARMONIC"]
            ],
            PatternType.EXPLORATION: [
                ["EXPLORATIVE", "EXPLORATIVE", "HARMONIC"],
                ["EXPLORATIVE", "STABILIZING", "EXPLORATIVE"]
            ],
            PatternType.RECOVERY: [
                ["DEFERRED", "STABILIZING", "HARMONIC"],
                ["REACTIVE", "STABILIZING", "HARMONIC"]
            ]
        }
        
        # Domain activation thresholds
        self.domain_thresholds = {
            "cryptographer": 0.7,
            "arbiter": 0.6,
            "mirror": 0.8,
            "purveyor": 0.5
        }
    
    def add_reason_event(self, event: Any):
        """Add a reason event to the buffer and analyze patterns."""
        self.reason_buffer.append(event)
        self._analyze_patterns()
    
    def _analyze_patterns(self):
        """Analyze the current buffer for patterns."""
        if len(self.reason_buffer) < 3:
            return
        
        # Convert buffer to sequence of reason types
        sequence = [event.reason_type.value for event in self.reason_buffer]
        
        # Check against pattern templates
        for pattern_type, templates in self.pattern_templates.items():
            for template in templates:
                if self._matches_template(sequence[-len(template):], template):
                    self._create_pattern(pattern_type, sequence[-len(template):])
    
    def _matches_template(self, sequence: List[str], template: List[str]) -> bool:
        """Check if a sequence matches a template."""
        return sequence == template
    
    def _create_pattern(self, pattern_type: PatternType, sequence: List[str]):
        """Create a new pattern from the detected sequence."""
        # Calculate pattern metrics
        start_time = self.reason_buffer[-len(sequence)].timestamp
        end_time = self.reason_buffer[-1].timestamp
        loop_tightness = self._calculate_loop_tightness(sequence)
        resonance = self._calculate_pattern_resonance(sequence)
        mirror_echo = self._check_mirror_echo(sequence)
        domain_activation = self._calculate_domain_activation(sequence)
        
        # Create pattern
        pattern = Pattern(
            pattern_type=pattern_type,
            sequence=sequence,
            start_time=start_time,
            end_time=end_time,
            resonance=resonance,
            mirror_echo=mirror_echo,
            loop_tightness=loop_tightness,
            domain_activation=domain_activation
        )
        
        self.patterns.append(pattern)
    
    def _calculate_loop_tightness(self, sequence: List[str]) -> float:
        """Calculate how quickly a pattern resolves."""
        if len(sequence) < 2:
            return 1.0
        
        # Calculate time between events
        times = [event.timestamp for event in self.reason_buffer[-len(sequence):]]
        intervals = [times[i+1] - times[i] for i in range(len(times)-1)]
        
        # Normalize to 0-1 range (1 = tight, 0 = loose)
        if not intervals:
            return 1.0
        
        max_interval = max(intervals)
        if max_interval == 0:
            return 1.0
        
        return 1.0 - (sum(intervals) / (max_interval * len(intervals)))
    
    def _calculate_pattern_resonance(self, sequence: List[str]) -> float:
        """Calculate the resonance strength of a pattern."""
        if not sequence:
            return 0.0
        
        # Calculate average resonance of events
        resonances = [event.resonance for event in self.reason_buffer[-len(sequence):]]
        return sum(resonances) / len(resonances)
    
    def _check_mirror_echo(self, sequence: List[str]) -> bool:
        """Check if a pattern has mirror echo."""
        # Count mirror confirmations
        confirmations = sum(1 for event in self.reason_buffer[-len(sequence):]
                          if event.mirror_confirmed)
        return confirmations / len(sequence) >= 0.5
    
    def _calculate_domain_activation(self, sequence: List[str]) -> Dict[str, float]:
        """Calculate which domains were activated during the pattern."""
        activations = {
            "cryptographer": 0.0,
            "arbiter": 0.0,
            "mirror": 0.0,
            "purveyor": 0.0
        }
        
        # This would be more sophisticated in practice
        # For now, we'll use some heuristics based on reason types
        for event in self.reason_buffer[-len(sequence):]:
            if event.reason_type.value == "EXPLORATIVE":
                activations["cryptographer"] += 0.3
            elif event.reason_type.value == "REACTIVE":
                activations["arbiter"] += 0.3
            elif event.reason_type.value == "HARMONIC":
                activations["mirror"] += 0.3
            elif event.reason_type.value == "STABILIZING":
                activations["purveyor"] += 0.3
        
        # Normalize activations
        for domain in activations:
            activations[domain] = min(1.0, activations[domain])
        
        return activations
    
    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get a summary of recent patterns."""
        if not self.patterns:
            return {}
        
        # Get recent patterns
        recent_patterns = self.patterns[-5:]  # Last 5 patterns
        
        # Calculate pattern statistics
        pattern_types = [p.pattern_type.value for p in recent_patterns]
        pattern_resonances = [p.resonance for p in recent_patterns]
        pattern_tightness = [p.loop_tightness for p in recent_patterns]
        
        # Calculate domain activation trends
        domain_trends = {}
        for domain in self.domain_thresholds:
            activations = [p.domain_activation[domain] for p in recent_patterns]
            domain_trends[domain] = {
                "current": activations[-1] if activations else 0.0,
                "trend": self._calculate_trend(activations)
            }
        
        return {
            "recent_patterns": [
                {
                    "type": p.pattern_type.value,
                    "sequence": p.sequence,
                    "resonance": p.resonance,
                    "mirror_echo": p.mirror_echo,
                    "loop_tightness": p.loop_tightness,
                    "domain_activation": p.domain_activation
                }
                for p in recent_patterns
            ],
            "statistics": {
                "pattern_types": pattern_types,
                "average_resonance": sum(pattern_resonances) / len(pattern_resonances),
                "average_tightness": sum(pattern_tightness) / len(pattern_tightness)
            },
            "domain_trends": domain_trends
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values."""
        if len(values) < 2:
            return "stable"
        
        # Calculate linear regression
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def predict_next_pattern(self) -> Optional[PatternType]:
        """Predict the next likely pattern type."""
        if len(self.patterns) < 2:
            return None
        
        # Get recent patterns
        recent_patterns = self.patterns[-3:]
        
        # Calculate pattern transition probabilities
        transitions = {}
        for i in range(len(recent_patterns)-1):
            current = recent_patterns[i].pattern_type
            next_pattern = recent_patterns[i+1].pattern_type
            
            if current not in transitions:
                transitions[current] = {}
            if next_pattern not in transitions[current]:
                transitions[current][next_pattern] = 0
            transitions[current][next_pattern] += 1
        
        # Predict next pattern
        if recent_patterns:
            last_pattern = recent_patterns[-1].pattern_type
            if last_pattern in transitions:
                next_patterns = transitions[last_pattern]
                if next_patterns:
                    return max(next_patterns.items(), key=lambda x: x[1])[0]
        
        return None 