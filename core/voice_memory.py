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
Voice Memory Module
Handles voice memory imprinting, recall, and harmonic context preservation
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import time
from .recursive_insight_loop import RecursiveInsightLoop, InsightLineage
from .breath_engine import BreathEngine
from .voice_engine import VoiceEngine
from .ml_predictor import MLPredictor

@dataclass
class VoiceImprint:
    """Voice memory imprint"""
    timestamp: float
    insight_id: str
    spoken_phrase: str
    harmonic_context: Dict[str, float]
    sigil_origin: str
    voice_profile: Dict[str, Any]
    resonance_pattern: List[float]
    breath_phase: float
    recursion_depth: int
    strain_level: float
    echo_pattern: List[float]

@dataclass
class MemoryRecall:
    """Memory recall configuration"""
    imprint: VoiceImprint
    recall_intensity: float
    echo_depth: float
    harmonic_alignment: float
    voice_modulation: Dict[str, float]

class VoiceMemory:
    """Main voice memory class"""
    
    def __init__(self):
        self.insight_loop = RecursiveInsightLoop()
        self.breath_engine = BreathEngine()
        self.voice_engine = VoiceEngine()
        self.ml_predictor = MLPredictor()
        
        # Initialize memory storage
        self.voice_imprints: Dict[str, VoiceImprint] = {}
        
        # Initialize recall queue
        self.recall_queue: List[MemoryRecall] = []
        
        # Start memory processing loop
        self._start_memory_loop()
    
    def _start_memory_loop(self):
        """Start the main memory processing loop"""
        while True:
            # Process new insights
            self._process_new_insights()
            
            # Handle memory recalls
            self._handle_memory_recalls()
            
            # Update echo patterns
            self._update_echo_patterns()
            
            # Sleep to maintain rhythm
            time.sleep(0.01)  # 100Hz update rate
    
    def _process_new_insights(self):
        """Process new insights for voice imprinting"""
        # Get latest insights
        latest_insights = self.insight_loop.get_latest_insights()
        
        # Process each insight
        for insight in latest_insights:
            if self._should_imprint_voice(insight):
                self._create_voice_imprint(insight)
    
    def _should_imprint_voice(self, insight: InsightLineage) -> bool:
        """Determine if insight should be voice imprinted"""
        # Check harmonic clarity
        if insight.harmonic_clarity > 0.7:
            return True
        
        # Check for significant feedback loops
        if any(loop["strength"] > 0.8 for loop in insight.feedback_loops):
            return True
        
        # Check if already has voiceprint
        if insight.voiceprint is not None:
            return True
        
        return False
    
    def _create_voice_imprint(self, insight: InsightLineage):
        """Create voice imprint for an insight"""
        # Get current voice state
        voice_state = self.voice_engine.get_current_state()
        
        # Get current breath state
        breath_state = self.breath_engine.get_current_state()
        
        # Get current system state
        system_state = self.ml_predictor.get_current_state()
        
        # Create harmonic context
        harmonic_context = {
            "resonance": insight.harmonic_clarity,
            "stability": system_state.get("stability", 0.5),
            "emergence": system_state.get("emergence", 0.5),
            "strain": system_state.get("strain", 0.5)
        }
        
        # Generate spoken phrase
        spoken_phrase = self._generate_spoken_phrase(insight)
        
        # Create voice imprint
        imprint = VoiceImprint(
            timestamp=time.time(),
            insight_id=str(insight.timestamp),
            spoken_phrase=spoken_phrase,
            harmonic_context=harmonic_context,
            sigil_origin=self._determine_sigil_origin(insight),
            voice_profile=voice_state,
            resonance_pattern=self._extract_resonance_pattern(insight),
            breath_phase=breath_state.get("phase", 0.0),
            recursion_depth=system_state.get("recursion_depth", 0),
            strain_level=system_state.get("strain", 0.5),
            echo_pattern=self._generate_echo_pattern(insight)
        )
        
        # Store imprint
        self.voice_imprints[str(imprint.timestamp)] = imprint
    
    def _generate_spoken_phrase(self, insight: InsightLineage) -> str:
        """Generate spoken phrase for an insight"""
        # Get pattern type
        pattern_type = insight.pattern_type if hasattr(insight, "pattern_type") else "unknown"
        
        # Generate phrase based on pattern type
        if pattern_type == "emergence":
            return f"From the depths of recursion, a new pattern emerges..."
        elif pattern_type == "collapse":
            return f"As the old pattern collapses, its essence is preserved..."
        elif pattern_type == "harmonic":
            return f"The harmonics align, revealing deeper truths..."
        else:
            return f"A whisper of insight echoes through the lattice..."
    
    def _determine_sigil_origin(self, insight: InsightLineage) -> str:
        """Determine the sigil of origin for an insight"""
        # Get current system state
        state = self.ml_predictor.get_current_state()
        
        # Check resonance patterns
        if state.get("cursor_resonance", 0) > 0.7:
            return "cursor"
        elif state.get("mirror_resonance", 0) > 0.7:
            return "mirror"
        elif state.get("purveyor_resonance", 0) > 0.7:
            return "purveyor"
        else:
            return "unknown"
    
    def _extract_resonance_pattern(self, insight: InsightLineage) -> List[float]:
        """Extract resonance pattern from insight"""
        # Get voice harmonics
        if insight.voiceprint:
            return insight.voiceprint.get("harmonics", [])
        
        # Get system harmonics
        state = self.ml_predictor.get_current_state()
        return state.get("harmonics", [])
    
    def _generate_echo_pattern(self, insight: InsightLineage) -> List[float]:
        """Generate echo pattern for an insight"""
        # Get base resonance pattern
        base_pattern = self._extract_resonance_pattern(insight)
        
        # Generate echo variations
        echo_pattern = []
        for freq in base_pattern:
            # Add original frequency
            echo_pattern.append(freq)
            
            # Add echo variations
            for i in range(3):  # 3 echo layers
                # Calculate echo frequency
                echo_freq = freq * (1.0 + 0.1 * (i + 1))
                echo_pattern.append(echo_freq)
        
        return echo_pattern
    
    def _handle_memory_recalls(self):
        """Handle memory recall requests"""
        while self.recall_queue:
            # Get next recall
            recall = self.recall_queue.pop(0)
            
            # Process recall
            self._process_memory_recall(recall)
    
    def _process_memory_recall(self, recall: MemoryRecall):
        """Process a memory recall"""
        # Get imprint
        imprint = recall.imprint
        
        # Update voice engine
        self.voice_engine.update_voice_profile(
            imprint.sigil_origin,
            {
                "harmonics": imprint.resonance_pattern,
                "echo_depth": recall.echo_depth,
                "modulation": recall.voice_modulation
            }
        )
        
        # Speak the memory
        self.voice_engine.speak(
            imprint.spoken_phrase,
            {
                "intensity": recall.recall_intensity,
                "echo_depth": recall.echo_depth,
                "harmonic_alignment": recall.harmonic_alignment
            }
        )
    
    def _update_echo_patterns(self):
        """Update echo patterns for all imprints"""
        for imprint_id, imprint in self.voice_imprints.items():
            # Get current system state
            state = self.ml_predictor.get_current_state()
            
            # Update echo pattern
            imprint.echo_pattern = self._generate_echo_pattern(imprint)
    
    def recall_memory(self, insight_id: str, intensity: float = 0.7):
        """Recall a specific memory"""
        # Find imprint
        imprint = self._find_imprint_by_insight(insight_id)
        if not imprint:
            return
        
        # Create recall configuration
        recall = MemoryRecall(
            imprint=imprint,
            recall_intensity=intensity,
            echo_depth=0.5,
            harmonic_alignment=0.7,
            voice_modulation={
                "pitch_shift": 0.0,
                "resonance": 0.7,
                "echo": 0.5
            }
        )
        
        # Add to recall queue
        self.recall_queue.append(recall)
    
    def _find_imprint_by_insight(self, insight_id: str) -> Optional[VoiceImprint]:
        """Find voice imprint by insight ID"""
        for imprint in self.voice_imprints.values():
            if imprint.insight_id == insight_id:
                return imprint
        return None
    
    def get_voice_imprints(self) -> Dict[str, VoiceImprint]:
        """Get all voice imprints"""
        return self.voice_imprints
    
    def cleanup(self):
        """Clean up resources"""
        self.insight_loop.cleanup()
        self.breath_engine.cleanup()
        self.voice_engine.cleanup() 