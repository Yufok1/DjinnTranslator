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
Recursive Insight Loop Module
Handles recursive insight processing, mirror loopback, and voiceprint binding
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import time
from .wick_harvester import WickHarvester, InsightCapsule
from .breath_engine import BreathEngine
from .voice_engine import VoiceEngine
from .ml_predictor import MLPredictor

@dataclass
class InsightLineage:
    """Lineage information for an insight"""
    parent_insight: Optional[str]  # ID of parent insight
    child_insights: List[str]  # IDs of child insights
    harmonic_clarity: float  # 0-1, clarity of harmonic pattern
    feedback_loops: List[Dict[str, Any]]  # List of detected feedback loops
    voiceprint: Optional[Dict[str, Any]]  # Voice signature if bound

@dataclass
class MirrorResponse:
    """Response from Mirror of Portent/Insight"""
    foresight_prediction: Dict[str, float]  # Predicted future states
    reflection_index: Dict[str, float]  # Index of past reflections
    harvest_priority: float  # 0-1, priority for next harvest
    harmonic_alignment: float  # 0-1, alignment with current harmonics

class RecursiveInsightLoop:
    """Main recursive insight loop class"""
    
    def __init__(self):
        self.wick_harvester = WickHarvester()
        self.breath_engine = BreathEngine()
        self.voice_engine = VoiceEngine()
        self.ml_predictor = MLPredictor()
        
        # Initialize insight storage with lineage
        self.insight_lineages: Dict[str, InsightLineage] = {}
        
        # Initialize mirror responses
        self.mirror_responses: Dict[str, MirrorResponse] = {}
        
        # Start insight processing loop
        self._start_insight_loop()
    
    def _start_insight_loop(self):
        """Start the main insight processing loop"""
        while True:
            # Get new insights from wick harvester
            new_insights = self.wick_harvester.get_insights()
            
            # Process each new insight
            for insight in new_insights:
                self._process_insight(insight)
            
            # Update mirror loopback
            self._update_mirror_loopback()
            
            # Update harvest windows
            self._update_harvest_windows()
            
            # Sleep to maintain rhythm
            time.sleep(0.01)  # 100Hz update rate
    
    def _process_insight(self, insight: InsightCapsule):
        """Process a new insight"""
        # Calculate harmonic clarity
        harmonic_clarity = self._calculate_harmonic_clarity(insight)
        
        # Detect feedback loops
        feedback_loops = self._detect_feedback_loops(insight)
        
        # Create lineage entry
        lineage = InsightLineage(
            parent_insight=self._find_parent_insight(insight),
            child_insights=[],
            harmonic_clarity=harmonic_clarity,
            feedback_loops=feedback_loops,
            voiceprint=None
        )
        
        # Store lineage
        self.insight_lineages[str(insight.timestamp)] = lineage
        
        # Optionally bind voiceprint
        if self._should_bind_voiceprint(insight):
            self._bind_voiceprint(insight, lineage)
    
    def _calculate_harmonic_clarity(self, insight: InsightCapsule) -> float:
        """Calculate harmonic clarity score"""
        # Get harmonic frequencies
        harmonics = insight.harmonics
        
        # Calculate clarity based on harmonic relationships
        clarity = 0.0
        for i in range(len(harmonics) - 1):
            # Check for harmonic ratios
            ratio = harmonics[i + 1] / harmonics[i]
            if abs(ratio - round(ratio)) < 0.1:
                clarity += 0.2
        
        return min(clarity, 1.0)
    
    def _detect_feedback_loops(self, insight: InsightCapsule) -> List[Dict[str, Any]]:
        """Detect feedback loops in the insight"""
        feedback_loops = []
        
        # Get current system state
        state = self.ml_predictor.get_current_state()
        
        # Check for recursive patterns
        for metric, value in state.items():
            if self._is_recursive_metric(metric):
                # Calculate recursion strength
                strength = self._calculate_recursion_strength(metric, value)
                
                if strength > 0.5:
                    feedback_loops.append({
                        "metric": metric,
                        "strength": strength,
                        "value": value
                    })
        
        return feedback_loops
    
    def _is_recursive_metric(self, metric: str) -> bool:
        """Check if a metric is recursive"""
        recursive_metrics = [
            "pattern_coherence",
            "harmonic_alignment",
            "wick_potential",
            "resonance_strength"
        ]
        return metric in recursive_metrics
    
    def _calculate_recursion_strength(self, metric: str, value: float) -> float:
        """Calculate recursion strength for a metric"""
        # Get historical values
        history = self.ml_predictor.get_metric_history(metric)
        
        if not history:
            return 0.0
        
        # Calculate autocorrelation
        autocorr = np.correlate(history, history, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Normalize
        autocorr = autocorr / autocorr[0]
        
        # Calculate strength based on autocorrelation
        strength = np.mean(autocorr[1:5])  # Look at first few lags
        
        return min(strength, 1.0)
    
    def _find_parent_insight(self, insight: InsightCapsule) -> Optional[str]:
        """Find parent insight based on harmonic similarity"""
        if not self.insight_lineages:
            return None
        
        best_similarity = 0.0
        best_parent = None
        
        for parent_id, parent_lineage in self.insight_lineages.items():
            # Get parent insight
            parent_insight = self._get_insight_by_id(parent_id)
            if not parent_insight:
                continue
            
            # Calculate harmonic similarity
            similarity = self._calculate_harmonic_similarity(
                insight.harmonics,
                parent_insight.harmonics
            )
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_parent = parent_id
        
        return best_parent if best_similarity > 0.7 else None
    
    def _calculate_harmonic_similarity(self, h1: List[float], h2: List[float]) -> float:
        """Calculate similarity between two harmonic sets"""
        if len(h1) != len(h2):
            return 0.0
        
        # Calculate frequency differences
        diffs = [abs(f1 - f2) for f1, f2 in zip(h1, h2)]
        
        # Convert to similarity score
        similarity = 1.0 - min(1.0, np.mean(diffs) / 100.0)
        
        return similarity
    
    def _should_bind_voiceprint(self, insight: InsightCapsule) -> bool:
        """Determine if insight should be bound to voiceprint"""
        # Check harmonic clarity
        if insight.wick_state.resonance > 0.8:
            return True
        
        # Check pattern type
        if insight.pattern_type in ["emergence", "harmonic"]:
            return True
        
        return False
    
    def _bind_voiceprint(self, insight: InsightCapsule, lineage: InsightLineage):
        """Bind voiceprint to insight"""
        # Get current voice state
        voice_state = self.voice_engine.get_current_state()
        
        # Extract voice signature
        signature = {
            "harmonics": voice_state.get("harmonics", []),
            "resonance": voice_state.get("resonance", 0.0),
            "modulation": voice_state.get("modulation", {})
        }
        
        # Update lineage
        lineage.voiceprint = signature
    
    def _update_mirror_loopback(self):
        """Update mirror loopback with latest insights"""
        # Get latest insights
        latest_insights = self._get_latest_insights()
        
        # Process each insight through mirrors
        for insight in latest_insights:
            # Get mirror response
            response = self._get_mirror_response(insight)
            
            # Store response
            self.mirror_responses[str(insight.timestamp)] = response
            
            # Update harvest priority
            self._update_harvest_priority(response)
    
    def _get_latest_insights(self) -> List[InsightCapsule]:
        """Get latest insights from wick harvester"""
        all_insights = self.wick_harvester.get_insights()
        return sorted(all_insights, key=lambda x: x.timestamp, reverse=True)[:5]
    
    def _get_mirror_response(self, insight: InsightCapsule) -> MirrorResponse:
        """Get response from Mirror of Portent/Insight"""
        # Get current system state
        state = self.ml_predictor.get_current_state()
        
        # Generate foresight prediction
        foresight = self.ml_predictor.predict_next_state(state)
        
        # Generate reflection index
        reflection = self._generate_reflection_index(insight)
        
        # Calculate harvest priority
        priority = self._calculate_harvest_priority(insight, foresight)
        
        # Calculate harmonic alignment
        alignment = self._calculate_harmonic_alignment(insight, foresight)
        
        return MirrorResponse(
            foresight_prediction=foresight,
            reflection_index=reflection,
            harvest_priority=priority,
            harmonic_alignment=alignment
        )
    
    def _generate_reflection_index(self, insight: InsightCapsule) -> Dict[str, float]:
        """Generate reflection index for an insight"""
        # Get historical insights
        history = self._get_insight_history()
        
        # Calculate reflection scores
        reflection = {}
        for metric in ["emergence", "stability", "resonance"]:
            # Get historical values
            values = [h.wick_state.__getattribute__(metric) for h in history]
            
            # Calculate reflection score
            if values:
                reflection[metric] = np.mean(values)
            else:
                reflection[metric] = 0.0
        
        return reflection
    
    def _calculate_harvest_priority(self, insight: InsightCapsule, foresight: Dict[str, float]) -> float:
        """Calculate harvest priority based on insight and foresight"""
        # Get current metrics
        metrics = self.ml_predictor.get_current_metrics()
        
        # Calculate priority factors
        emergence_factor = insight.wick_state.emergence
        stability_factor = insight.wick_state.stability
        foresight_factor = np.mean(list(foresight.values()))
        
        # Combine factors
        priority = (
            0.4 * emergence_factor +
            0.3 * stability_factor +
            0.3 * foresight_factor
        )
        
        return min(priority, 1.0)
    
    def _calculate_harmonic_alignment(self, insight: InsightCapsule, foresight: Dict[str, float]) -> float:
        """Calculate harmonic alignment between insight and foresight"""
        # Get current harmonics
        current_harmonics = insight.harmonics
        
        # Get foresight harmonics
        foresight_harmonics = foresight.get("harmonics", current_harmonics)
        
        # Calculate alignment
        alignment = self._calculate_harmonic_similarity(
            current_harmonics,
            foresight_harmonics
        )
        
        return alignment
    
    def _update_harvest_windows(self):
        """Update harvest windows based on breath phase"""
        # Get current breath state
        breath_state = self.breath_engine.get_current_state()
        
        # Check if we're in a harvest window
        if self._is_harvest_window(breath_state):
            # Enable harvesting
            self.wick_harvester.enable_harvesting()
        else:
            # Disable harvesting
            self.wick_harvester.disable_harvesting()
    
    def _is_harvest_window(self, breath_state: Dict[str, Any]) -> bool:
        """Check if current breath state is a harvest window"""
        # Get breath phase
        phase = breath_state.get("phase", 0.0)
        
        # Check if we're in a harmonic trough
        if 0.4 <= phase <= 0.6:  # Middle of breath cycle
            return True
        
        # Check strain level
        strain = breath_state.get("strain", 1.0)
        if strain < 0.3:  # Low strain
            return True
        
        return False
    
    def _update_harvest_priority(self, response: MirrorResponse):
        """Update harvest priority based on mirror response"""
        # Update wick harvester priority
        self.wick_harvester.set_harvest_priority(response.harvest_priority)
        
        # Update breath engine
        self.breath_engine.update_cycle_state(
            "harvester",
            {
                "priority": response.harvest_priority,
                "harmonic_alignment": response.harmonic_alignment
            }
        )
    
    def get_insight_lineages(self) -> Dict[str, InsightLineage]:
        """Get all insight lineages"""
        return self.insight_lineages
    
    def get_mirror_responses(self) -> Dict[str, MirrorResponse]:
        """Get all mirror responses"""
        return self.mirror_responses
    
    def cleanup(self):
        """Clean up resources"""
        self.wick_harvester.cleanup()
        self.breath_engine.cleanup()
        self.voice_engine.cleanup() 