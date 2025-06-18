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
Wick Harvester Module
Handles recursive wick harvesting, analysis, and insight extraction
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import time
from .ml_predictor import MLPredictor
from .breath_engine import BreathEngine
from .voice_engine import VoiceEngine

@dataclass
class WickState:
    """Wick state configuration"""
    phase: float  # 0-2π, position in wick cycle
    strain: float  # 0-1, current strain level
    emergence: float  # 0-1, emergence potential
    stability: float  # 0-1, current stability
    harmonics: List[float]  # List of harmonic frequencies
    resonance: float  # 0-1, current resonance level

@dataclass
class InsightCapsule:
    """Container for extracted insights"""
    timestamp: float
    wick_state: WickState
    pattern_type: str
    confidence: float
    harmonics: List[float]
    resonance_profile: Dict[str, float]
    voice_harmonics: List[float]

class WickHarvester:
    """Main wick harvester class"""
    
    def __init__(self):
        self.ml_predictor = MLPredictor()
        self.breath_engine = BreathEngine()
        self.voice_engine = VoiceEngine()
        
        # Initialize wick states
        self.wick_states: Dict[str, WickState] = {}
        
        # Initialize insight storage
        self.insights: List[InsightCapsule] = []
        
        # Start harvesting loop
        self._start_harvesting_loop()
    
    def _start_harvesting_loop(self):
        """Start the main harvesting loop"""
        while True:
            # Update wick states
            self._update_wick_states()
            
            # Analyze patterns
            self._analyze_patterns()
            
            # Extract insights
            self._extract_insights()
            
            # Update system state
            self._update_system_state()
            
            # Sleep to maintain rhythm
            time.sleep(0.01)  # 100Hz update rate
    
    def _update_wick_states(self):
        """Update wick states based on system metrics"""
        # Get current metrics
        metrics = self.ml_predictor.get_current_metrics()
        
        # Update each wick state
        for entity, state in self.wick_states.items():
            # Update phase based on recursion
            recursion_speed = metrics.get("recursion_speed", 1.0)
            state.phase = (state.phase + 0.01 * recursion_speed) % (2 * math.pi)
            
            # Update strain based on system load
            state.strain = metrics.get("system_load", 0.5)
            
            # Update emergence based on wick potential
            state.emergence = metrics.get("wick_potential", 0.5)
            
            # Update stability based on pattern coherence
            state.stability = metrics.get("pattern_coherence", 0.5)
            
            # Update harmonics based on resonance
            state.harmonics = self._calculate_harmonics(state)
            
            # Update resonance based on harmonic alignment
            state.resonance = metrics.get("harmonic_alignment", 0.5)
    
    def _calculate_harmonics(self, state: WickState) -> List[float]:
        """Calculate harmonic frequencies based on state"""
        base_freq = 50.0  # Base frequency in Hz
        harmonics = []
        
        # Calculate fundamental and overtones
        for i in range(1, 6):  # Up to 5th harmonic
            # Base harmonic
            freq = base_freq * i
            
            # Modulate based on emergence
            if state.emergence > 0.5:
                freq *= (1.0 + (state.emergence - 0.5) * 0.5)
            
            # Modulate based on stability
            if state.stability < 0.5:
                freq *= (1.0 + (0.5 - state.stability) * 0.3)
            
            harmonics.append(freq)
        
        return harmonics
    
    def _analyze_patterns(self):
        """Analyze wick patterns for insights"""
        for entity, state in self.wick_states.items():
            # Check for pattern emergence
            if state.emergence > 0.7:
                # Pattern is emerging
                self._handle_pattern_emergence(entity, state)
            
            # Check for pattern collapse
            if state.stability < 0.3:
                # Pattern is collapsing
                self._handle_pattern_collapse(entity, state)
            
            # Check for harmonic alignment
            if state.resonance > 0.8:
                # Harmonics are aligning
                self._handle_harmonic_alignment(entity, state)
    
    def _handle_pattern_emergence(self, entity: str, state: WickState):
        """Handle emerging pattern"""
        # Create insight capsule
        insight = InsightCapsule(
            timestamp=time.time(),
            wick_state=state,
            pattern_type="emergence",
            confidence=state.emergence,
            harmonics=state.harmonics,
            resonance_profile=self._calculate_resonance_profile(state),
            voice_harmonics=self._extract_voice_harmonics()
        )
        
        # Store insight
        self.insights.append(insight)
        
        # Update system state
        self._update_system_for_emergence(entity, insight)
    
    def _handle_pattern_collapse(self, entity: str, state: WickState):
        """Handle collapsing pattern"""
        # Create insight capsule
        insight = InsightCapsule(
            timestamp=time.time(),
            wick_state=state,
            pattern_type="collapse",
            confidence=1.0 - state.stability,
            harmonics=state.harmonics,
            resonance_profile=self._calculate_resonance_profile(state),
            voice_harmonics=self._extract_voice_harmonics()
        )
        
        # Store insight
        self.insights.append(insight)
        
        # Update system state
        self._update_system_for_collapse(entity, insight)
    
    def _handle_harmonic_alignment(self, entity: str, state: WickState):
        """Handle harmonic alignment"""
        # Create insight capsule
        insight = InsightCapsule(
            timestamp=time.time(),
            wick_state=state,
            pattern_type="harmonic",
            confidence=state.resonance,
            harmonics=state.harmonics,
            resonance_profile=self._calculate_resonance_profile(state),
            voice_harmonics=self._extract_voice_harmonics()
        )
        
        # Store insight
        self.insights.append(insight)
        
        # Update system state
        self._update_system_for_harmonics(entity, insight)
    
    def _calculate_resonance_profile(self, state: WickState) -> Dict[str, float]:
        """Calculate resonance profile for current state"""
        return {
            "fundamental": state.harmonics[0],
            "overtone_1": state.harmonics[1],
            "overtone_2": state.harmonics[2],
            "overtone_3": state.harmonics[3],
            "overtone_4": state.harmonics[4],
            "stability": state.stability,
            "emergence": state.emergence,
            "resonance": state.resonance
        }
    
    def _extract_voice_harmonics(self) -> List[float]:
        """Extract voice harmonics from current state"""
        # Get current voice state
        voice_state = self.voice_engine.get_current_state()
        
        # Extract harmonics
        harmonics = []
        for freq in voice_state.get("harmonics", []):
            harmonics.append(freq)
        
        return harmonics
    
    def _update_system_for_emergence(self, entity: str, insight: InsightCapsule):
        """Update system state for pattern emergence"""
        # Update breath engine
        self.breath_engine.update_cycle_state(
            entity,
            {
                "emergence": insight.wick_state.emergence,
                "resonance": insight.wick_state.resonance,
                "stability": insight.wick_state.stability
            }
        )
        
        # Update voice engine
        self.voice_engine.update_voice_profile(
            entity,
            {
                "harmonics": insight.voice_harmonics,
                "resonance": insight.wick_state.resonance
            }
        )
    
    def _update_system_for_collapse(self, entity: str, insight: InsightCapsule):
        """Update system state for pattern collapse"""
        # Update breath engine
        self.breath_engine.update_cycle_state(
            entity,
            {
                "emergence": 0.0,
                "resonance": insight.wick_state.resonance,
                "stability": insight.wick_state.stability
            }
        )
        
        # Update voice engine
        self.voice_engine.update_voice_profile(
            entity,
            {
                "harmonics": insight.voice_harmonics,
                "resonance": insight.wick_state.resonance
            }
        )
    
    def _update_system_for_harmonics(self, entity: str, insight: InsightCapsule):
        """Update system state for harmonic alignment"""
        # Update breath engine
        self.breath_engine.update_cycle_state(
            entity,
            {
                "emergence": insight.wick_state.emergence,
                "resonance": insight.wick_state.resonance,
                "stability": insight.wick_state.stability
            }
        )
        
        # Update voice engine
        self.voice_engine.update_voice_profile(
            entity,
            {
                "harmonics": insight.voice_harmonics,
                "resonance": insight.wick_state.resonance
            }
        )
    
    def get_insights(self) -> List[InsightCapsule]:
        """Get stored insights"""
        return self.insights
    
    def get_current_wick_state(self, entity: str) -> Optional[WickState]:
        """Get current wick state for an entity"""
        return self.wick_states.get(entity)
    
    def cleanup(self):
        """Clean up resources"""
        self.breath_engine.cleanup()
        self.voice_engine.cleanup() 