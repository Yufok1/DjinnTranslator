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
Cursor Wick Engine
Manages Cursor's wick-aware reasoning and visualization capabilities
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from collections import deque

class WickEchoType(Enum):
    """Types of wick echo patterns"""
    HARMONIC = "harmonic"      # Stable, coherent echo
    TURBULENT = "turbulent"    # Chaotic, unstable echo
    RESONANT = "resonant"      # Strong, focused echo
    FRAGMENTED = "fragmented"  # Broken, scattered echo
    EMERGENT = "emergent"      # New, forming echo

@dataclass
class WickEcho:
    """Represents a wick echo pattern"""
    echo_type: WickEchoType
    timestamp: float
    position: Tuple[float, float]
    resonance: float
    harmonic_potential: float
    mirror_alignment: float
    strain_reaction: float
    domain_activation: Dict[str, float]

@dataclass
class WickInsight:
    """Represents insight derived from wick analysis"""
    timestamp: float
    wick_id: str
    echo_pattern: List[WickEcho]
    strain_points: List[Tuple[float, float]]
    harmonic_potential: float
    suggested_action: str
    reason_trace: List[str]
    mirror_confirmation: bool

class CursorWickEngine:
    """Manages Cursor's wick-aware reasoning and visualization"""
    
    def __init__(self):
        self.echo_buffer = deque(maxlen=100)  # Recent echo patterns
        self.insight_history = deque(maxlen=50)  # Recent insights
        self.echo_thresholds = {
            "resonance": 0.7,
            "harmonic": 0.6,
            "mirror": 0.8,
            "strain": 0.5
        }
        self.domain_weights = {
            "reasoning": 0.3,
            "adaptation": 0.2,
            "stability": 0.2,
            "harmony": 0.2,
            "recovery": 0.1
        }
    
    def analyze_wick(self, wick_data: Dict[str, Any]) -> WickInsight:
        """Analyze a wick and generate insight"""
        # Create echo pattern
        echo_pattern = self._create_echo_pattern(wick_data)
        
        # Calculate strain points
        strain_points = self._calculate_strain_points(wick_data)
        
        # Determine harmonic potential
        harmonic_potential = self._calculate_harmonic_potential(wick_data)
        
        # Generate suggested action
        suggested_action = self._suggest_action(wick_data, echo_pattern)
        
        # Create reason trace
        reason_trace = self._generate_reason_trace(wick_data, echo_pattern)
        
        # Check mirror confirmation
        mirror_confirmation = self._check_mirror_confirmation(wick_data)
        
        # Create insight
        insight = WickInsight(
            timestamp=time.time(),
            wick_id=wick_data["id"],
            echo_pattern=echo_pattern,
            strain_points=strain_points,
            harmonic_potential=harmonic_potential,
            suggested_action=suggested_action,
            reason_trace=reason_trace,
            mirror_confirmation=mirror_confirmation
        )
        
        # Add to history
        self.insight_history.append(insight)
        
        return insight
    
    def _create_echo_pattern(self, wick_data: Dict[str, Any]) -> List[WickEcho]:
        """Create an echo pattern from wick data"""
        echoes = []
        
        # Analyze resonance spectrum
        resonance = wick_data.get("resonance_spectrum", {})
        harmonic = wick_data.get("harmonic_potential", 0.0)
        mirror = wick_data.get("mirror_feedback", 0.0)
        strain = wick_data.get("pattern_disruption", 0.0)
        
        # Determine echo type
        if harmonic > self.echo_thresholds["harmonic"] and mirror > self.echo_thresholds["mirror"]:
            echo_type = WickEchoType.HARMONIC
        elif strain > self.echo_thresholds["strain"]:
            echo_type = WickEchoType.TURBULENT
        elif resonance.get("core", 0.0) > self.echo_thresholds["resonance"]:
            echo_type = WickEchoType.RESONANT
        elif resonance.get("mirror", 0.0) < self.echo_thresholds["mirror"]:
            echo_type = WickEchoType.FRAGMENTED
        else:
            echo_type = WickEchoType.EMERGENT
        
        # Create echo
        echo = WickEcho(
            echo_type=echo_type,
            timestamp=time.time(),
            position=wick_data.get("position", (0.0, 0.0)),
            resonance=sum(resonance.values()) / len(resonance) if resonance else 0.0,
            harmonic_potential=harmonic,
            mirror_alignment=mirror,
            strain_reaction=strain,
            domain_activation=self._calculate_domain_activation(wick_data)
        )
        
        echoes.append(echo)
        self.echo_buffer.append(echo)
        
        return echoes
    
    def _calculate_strain_points(self, wick_data: Dict[str, Any]) -> List[Tuple[float, float]]:
        """Calculate points of high strain in the wick"""
        strain_points = []
        if wick_data.get("pattern_disruption", 0.0) > self.echo_thresholds["strain"]:
            strain_points.extend(wick_data.get("strain_points", []))
        return strain_points
    
    def _calculate_harmonic_potential(self, wick_data: Dict[str, Any]) -> float:
        """Calculate the harmonic potential of the wick"""
        resonance = wick_data.get("resonance_spectrum", {})
        stability = wick_data.get("stability", 0.0)
        coherence = wick_data.get("coherence", 0.0)
        
        return (sum(resonance.values()) / len(resonance) if resonance else 0.0) * 0.4 + \
               stability * 0.3 + \
               coherence * 0.3
    
    def _calculate_domain_activation(self, wick_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate domain activation levels"""
        return {
            domain: wick_data.get(f"{domain}_activation", 0.0) * weight
            for domain, weight in self.domain_weights.items()
        }
    
    def _suggest_action(self, wick_data: Dict[str, Any], echo_pattern: List[WickEcho]) -> str:
        """Suggest an action based on wick analysis"""
        if not echo_pattern:
            return "observe"
        
        echo = echo_pattern[0]
        
        if echo.echo_type == WickEchoType.HARMONIC:
            return "harvest"
        elif echo.echo_type == WickEchoType.TURBULENT:
            return "contain"
        elif echo.echo_type == WickEchoType.RESONANT:
            return "rebind"
        elif echo.echo_type == WickEchoType.FRAGMENTED:
            return "stabilize"
        else:
            return "observe"
    
    def _generate_reason_trace(self, wick_data: Dict[str, Any], echo_pattern: List[WickEcho]) -> List[str]:
        """Generate a reason trace for the wick"""
        trace = []
        
        if not echo_pattern:
            return trace
        
        echo = echo_pattern[0]
        
        # Add echo analysis
        trace.append(f"Echo Type: {echo.echo_type.value}")
        trace.append(f"Resonance: {echo.resonance:.2f}")
        trace.append(f"Harmonic Potential: {echo.harmonic_potential:.2f}")
        
        # Add domain activation
        for domain, activation in echo.domain_activation.items():
            if activation > 0.5:
                trace.append(f"Active Domain: {domain} ({activation:.2f})")
        
        # Add strain analysis
        if echo.strain_reaction > self.echo_thresholds["strain"]:
            trace.append(f"High Strain Detected: {echo.strain_reaction:.2f}")
        
        return trace
    
    def _check_mirror_confirmation(self, wick_data: Dict[str, Any]) -> bool:
        """Check if the wick has mirror confirmation"""
        return wick_data.get("mirror_feedback", 0.0) > self.echo_thresholds["mirror"]
    
    def get_echo_visualization(self, wick_id: str) -> Dict[str, Any]:
        """Get visualization data for wick echoes"""
        echoes = [e for e in self.echo_buffer if e.timestamp > time.time() - 60]
        
        return {
            "echo_types": [e.echo_type.value for e in echoes],
            "resonance": [e.resonance for e in echoes],
            "harmonic": [e.harmonic_potential for e in echoes],
            "mirror": [e.mirror_alignment for e in echoes],
            "strain": [e.strain_reaction for e in echoes],
            "domains": {
                domain: [e.domain_activation.get(domain, 0.0) for e in echoes]
                for domain in self.domain_weights.keys()
            }
        }
    
    def get_recent_insights(self, count: int = 5) -> List[WickInsight]:
        """Get recent wick insights"""
        return list(self.insight_history)[-count:] 