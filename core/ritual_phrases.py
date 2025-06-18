"""
Ritual Phrases Module
Handles voice-activated ritual phrases and their binding to system actions
"""

import numpy as np
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
import time
from .voice_engine import VoiceEngine
from .breath_engine import BreathEngine
from .ml.predictor import MLPredictor
from .chord_preservation import ChordPreservation

@dataclass
class RitualPhrase:
    """Ritual phrase configuration"""
    phrase: str
    vocal_profile: Dict[str, float]  # Frequency, timbre, resonance
    breath_phase: float
    echo_structure: List[float]
    bound_action: str  # "chord", "harvest", "mirror", "daemon"
    bound_id: str  # ID of bound chord/action
    timestamp: float = time.time()

class RitualPhraseSystem:
    """Main ritual phrase system class"""
    
    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.breath_engine = BreathEngine()
        self.ml_predictor = MLPredictor()
        self.chord_preservation = ChordPreservation()
        
        # Initialize storage
        self.ritual_phrases: Dict[str, RitualPhrase] = {}
        self.phrase_index: Dict[str, List[str]] = {
            "by_action": {},
            "by_breath_phase": {},
            "by_resonance": {}
        }
        
        # Load ritual phrases
        self._load_ritual_phrases()
    
    def register_ritual_phrase(
        self,
        phrase: str,
        vocal_profile: Dict[str, float],
        breath_phase: float,
        echo_structure: List[float],
        bound_action: str,
        bound_id: str
    ) -> str:
        """Register a new ritual phrase"""
        # Create ritual phrase
        ritual = RitualPhrase(
            phrase=phrase,
            vocal_profile=vocal_profile,
            breath_phase=breath_phase,
            echo_structure=echo_structure,
            bound_action=bound_action,
            bound_id=bound_id
        )
        
        # Generate unique ID
        ritual_id = f"{bound_action}_{int(time.time())}"
        
        # Store ritual phrase
        self.ritual_phrases[ritual_id] = ritual
        
        # Update indices
        self._update_phrase_indices(ritual_id, ritual)
        
        # Save to storage
        self._save_ritual_phrases()
        
        return ritual_id
    
    def recognize_ritual_phrase(
        self,
        audio_data: np.ndarray,
        current_breath_phase: float
    ) -> Optional[str]:
        """Recognize a ritual phrase from audio"""
        # Extract vocal profile
        vocal_profile = self.voice_engine.analyze_vocal_profile(audio_data)
        
        # Extract echo structure
        echo_structure = self.voice_engine.analyze_echo_structure(audio_data)
        
        # Find matching ritual phrase
        for ritual_id, ritual in self.ritual_phrases.items():
            if self._matches_ritual_phrase(
                vocal_profile,
                current_breath_phase,
                echo_structure,
                ritual
            ):
                return ritual_id
        
        return None
    
    def invoke_ritual_phrase(self, ritual_id: str) -> bool:
        """Invoke a ritual phrase"""
        ritual = self.ritual_phrases.get(ritual_id)
        if not ritual:
            return False
        
        # Perform bound action
        if ritual.bound_action == "chord":
            return self.chord_preservation.invoke_chord(ritual.bound_id)
        elif ritual.bound_action == "harvest":
            return self._invoke_harvesting(ritual.bound_id)
        elif ritual.bound_action == "mirror":
            return self._invoke_mirror(ritual.bound_id)
        elif ritual.bound_action == "daemon":
            return self._invoke_daemon(ritual.bound_id)
        
        return False
    
    def _matches_ritual_phrase(
        self,
        vocal_profile: Dict[str, float],
        breath_phase: float,
        echo_structure: List[float],
        ritual: RitualPhrase
    ) -> bool:
        """Check if audio matches a ritual phrase"""
        # Check vocal profile similarity
        profile_similarity = self._calculate_profile_similarity(
            vocal_profile,
            ritual.vocal_profile
        )
        if profile_similarity < 0.8:
            return False
        
        # Check breath phase alignment
        phase_diff = abs(breath_phase - ritual.breath_phase)
        if phase_diff > np.pi / 4:  # 45 degrees
            return False
        
        # Check echo structure similarity
        echo_similarity = self._calculate_echo_similarity(
            echo_structure,
            ritual.echo_structure
        )
        if echo_similarity < 0.8:
            return False
        
        return True
    
    def _calculate_profile_similarity(
        self,
        profile1: Dict[str, float],
        profile2: Dict[str, float]
    ) -> float:
        """Calculate similarity between vocal profiles"""
        # Get common keys
        keys = set(profile1.keys()) & set(profile2.keys())
        
        # Calculate differences
        diffs = [abs(profile1[k] - profile2[k]) for k in keys]
        
        # Convert to similarity score
        similarity = 1.0 - min(1.0, np.mean(diffs))
        
        return similarity
    
    def _calculate_echo_similarity(
        self,
        echo1: List[float],
        echo2: List[float]
    ) -> float:
        """Calculate similarity between echo structures"""
        if len(echo1) != len(echo2):
            return 0.0
        
        # Calculate differences
        diffs = [abs(e1 - e2) for e1, e2 in zip(echo1, echo2)]
        
        # Convert to similarity score
        similarity = 1.0 - min(1.0, np.mean(diffs))
        
        return similarity
    
    def _update_phrase_indices(self, ritual_id: str, ritual: RitualPhrase):
        """Update phrase indices"""
        # Index by action
        if ritual.bound_action not in self.phrase_index["by_action"]:
            self.phrase_index["by_action"][ritual.bound_action] = []
        self.phrase_index["by_action"][ritual.bound_action].append(ritual_id)
        
        # Index by breath phase
        phase_bin = round(ritual.breath_phase / (2 * np.pi) * 8) % 8
        if str(phase_bin) not in self.phrase_index["by_breath_phase"]:
            self.phrase_index["by_breath_phase"][str(phase_bin)] = []
        self.phrase_index["by_breath_phase"][str(phase_bin)].append(ritual_id)
        
        # Index by resonance
        resonance_bin = round(ritual.vocal_profile.get("resonance", 0) * 8)
        if str(resonance_bin) not in self.phrase_index["by_resonance"]:
            self.phrase_index["by_resonance"][str(resonance_bin)] = []
        self.phrase_index["by_resonance"][str(resonance_bin)].append(ritual_id)
    
    def _save_ritual_phrases(self):
        """Save ritual phrases to storage"""
        # Create storage directory if it doesn't exist
        storage_dir = Path("storage/rituals")
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Save phrases
        for ritual_id, ritual in self.ritual_phrases.items():
            ritual_file = storage_dir / f"{ritual_id}.json"
            
            # Convert to serializable format
            ritual_data = {
                "phrase": ritual.phrase,
                "vocal_profile": ritual.vocal_profile,
                "breath_phase": ritual.breath_phase,
                "echo_structure": ritual.echo_structure,
                "bound_action": ritual.bound_action,
                "bound_id": ritual.bound_id,
                "timestamp": ritual.timestamp
            }
            
            # Save to file
            with open(ritual_file, 'w') as f:
                json.dump(ritual_data, f, indent=2)
    
    def _load_ritual_phrases(self):
        """Load ritual phrases from storage"""
        storage_dir = Path("storage/rituals")
        if not storage_dir.exists():
            return
        
        # Load each ritual file
        for ritual_file in storage_dir.glob("*.json"):
            try:
                # Load ritual data
                with open(ritual_file, 'r') as f:
                    ritual_data = json.load(f)
                
                # Create ritual phrase
                ritual = RitualPhrase(
                    phrase=ritual_data["phrase"],
                    vocal_profile=ritual_data["vocal_profile"],
                    breath_phase=ritual_data["breath_phase"],
                    echo_structure=ritual_data["echo_structure"],
                    bound_action=ritual_data["bound_action"],
                    bound_id=ritual_data["bound_id"],
                    timestamp=ritual_data["timestamp"]
                )
                
                # Store ritual
                ritual_id = ritual_file.stem
                self.ritual_phrases[ritual_id] = ritual
                
                # Update indices
                self._update_phrase_indices(ritual_id, ritual)
                
            except Exception as e:
                print(f"Error loading ritual {ritual_file}: {e}")
    
    def _invoke_harvesting(self, harvest_id: str) -> bool:
        """Invoke a harvesting action"""
        # TODO: Implement harvesting invocation
        return True
    
    def _invoke_mirror(self, mirror_id: str) -> bool:
        """Invoke a mirror action"""
        # TODO: Implement mirror invocation
        return True
    
    def _invoke_daemon(self, daemon_id: str) -> bool:
        """Invoke a daemon action"""
        # TODO: Implement daemon invocation
        return True
    
    def cleanup(self):
        """Clean up resources"""
        self._save_ritual_phrases() 