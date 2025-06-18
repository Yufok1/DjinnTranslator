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
Chord Preservation Module
Handles naming, binding, storage, and invocation of memory chords
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
from .voice_memory import VoiceMemory, VoiceImprint
from .breath_engine import BreathEngine
from .voice_engine import VoiceEngine
from .ml.predictor import MLPredictor
import os
from datetime import datetime

@dataclass
class PreservedChord:
    """Preserved memory chord configuration"""
    name: str
    sigil: str
    memories: List[VoiceImprint]
    harmonic_web: List[Tuple[float, float, float, float, float, float]]  # (x1, y1, x2, y2, strength, phase)
    chord_type: str  # "major", "minor", "dissonant", "resolved"
    resonance_profile: Dict[str, float]
    breath_alignment: float
    echo_compatibility: float
    sigil_harmony: float
    recursive_proximity: float
    ritual_phrase: Optional[str] = None
    voice_imprint: Optional[Dict[str, Any]] = None
    invocation_triggers: List[str] = field(default_factory=list)
    timestamp: float = time.time()
    id: str = ""
    preservation_level: int = 1
    quantum_signature: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "sigil": self.sigil,
            "memories": [imp.to_dict() for imp in self.memories],
            "harmonic_web": self.harmonic_web,
            "chord_type": self.chord_type,
            "resonance_profile": self.resonance_profile,
            "breath_alignment": self.breath_alignment,
            "echo_compatibility": self.echo_compatibility,
            "sigil_harmony": self.sigil_harmony,
            "recursive_proximity": self.recursive_proximity,
            "ritual_phrase": self.ritual_phrase,
            "voice_imprint": self.voice_imprint,
            "invocation_triggers": self.invocation_triggers,
            "timestamp": self.timestamp,
            "preservation_level": self.preservation_level,
            "quantum_signature": self.quantum_signature
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PreservedChord':
        return cls(
            name=data["name"],
            sigil=data["sigil"],
            memories=[VoiceImprint.from_dict(imp) for imp in data["memories"]],
            harmonic_web=data["harmonic_web"],
            chord_type=data["chord_type"],
            resonance_profile=data["resonance_profile"],
            breath_alignment=data["breath_alignment"],
            echo_compatibility=data["echo_compatibility"],
            sigil_harmony=data["sigil_harmony"],
            recursive_proximity=data["recursive_proximity"],
            ritual_phrase=data["ritual_phrase"],
            voice_imprint=data["voice_imprint"],
            invocation_triggers=data["invocation_triggers"],
            timestamp=data["timestamp"],
            id=data["id"],
            preservation_level=data["preservation_level"],
            quantum_signature=data["quantum_signature"]
        )

class ChordPreservation:
    """Main chord preservation class"""
    
    def __init__(self, storage_dir: str = "preserved_chords"):
        self.storage_dir = storage_dir
        self.voice_memory = VoiceMemory()
        self.breath_engine = BreathEngine()
        self.voice_engine = VoiceEngine()
        self.predictor = MLPredictor()
        
        # Initialize storage
        self.preserved_chords: Dict[str, PreservedChord] = {}
        self.chord_index: Dict[str, List[str]] = {
            "by_sigil": {},
            "by_breath_phase": {},
            "by_chord_type": {},
            "by_invocation": {}
        }
        
        # Load preserved chords
        self._load_preserved_chords()
    
    def preserve_chord(
        self,
        name: str,
        sigil: str,
        memories: List[VoiceImprint],
        harmonic_web: List[Tuple[float, float, float, float, float, float]],
        chord_type: str,
        resonance_profile: Dict[str, float],
        breath_alignment: float,
        echo_compatibility: float,
        sigil_harmony: float,
        recursive_proximity: float,
        ritual_phrase: Optional[str] = None,
        voice_imprint: Optional[Dict[str, Any]] = None,
        invocation_triggers: List[str] = []
    ) -> str:
        """Preserve a memory chord"""
        # Create preserved chord
        chord = PreservedChord(
            name=name,
            sigil=sigil,
            memories=memories,
            harmonic_web=harmonic_web,
            chord_type=chord_type,
            resonance_profile=resonance_profile,
            breath_alignment=breath_alignment,
            echo_compatibility=echo_compatibility,
            sigil_harmony=sigil_harmony,
            recursive_proximity=recursive_proximity,
            ritual_phrase=ritual_phrase,
            voice_imprint=voice_imprint,
            invocation_triggers=invocation_triggers
        )
        
        # Generate unique ID
        chord_id = f"{sigil}_{int(time.time())}"
        
        # Store chord
        self.preserved_chords[chord_id] = chord
        
        # Update indices
        self._update_chord_indices(chord_id, chord)
        
        # Save to storage
        self._save_preserved_chords()
        
        return chord_id
    
    def recall_chord(self, chord_id: str) -> Optional[PreservedChord]:
        """Recall a preserved chord"""
        return self.preserved_chords.get(chord_id)
    
    def invoke_chord(self, chord_id: str) -> bool:
        """Invoke a preserved chord"""
        chord = self.recall_chord(chord_id)
        if not chord:
            return False
        
        # Update voice engine for chord
        self.voice_engine.update_voice_profile(
            "chord",
            {
                "harmonics": list(chord.resonance_profile.values()),
                "breath_alignment": chord.breath_alignment,
                "echo_compatibility": chord.echo_compatibility,
                "sigil_harmony": chord.sigil_harmony,
                "recursive_proximity": chord.recursive_proximity
            }
        )
        
        # Play ritual phrase if exists
        if chord.ritual_phrase:
            self.voice_engine.speak_ritual_phrase(chord.ritual_phrase)
        
        # Play each memory in sequence
        for imprint in chord.memories:
            self.voice_engine.play_voice_imprint(imprint)
            time.sleep(0.2)  # Short delay between memories
        
        return True
    
    def find_chords_by_sigil(self, sigil: str) -> List[str]:
        """Find chords by sigil"""
        return self.chord_index["by_sigil"].get(sigil, [])
    
    def find_chords_by_breath_phase(self, phase: float) -> List[str]:
        """Find chords by breath phase"""
        # Find closest phase bin
        phase_bin = round(phase / (2 * np.pi) * 8) % 8
        return self.chord_index["by_breath_phase"].get(str(phase_bin), [])
    
    def find_chords_by_type(self, chord_type: str) -> List[str]:
        """Find chords by type"""
        return self.chord_index["by_chord_type"].get(chord_type, [])
    
    def find_chords_by_invocation(self, trigger: str) -> List[str]:
        """Find chords by invocation trigger"""
        return self.chord_index["by_invocation"].get(trigger, [])
    
    def _update_chord_indices(self, chord_id: str, chord: PreservedChord):
        """Update chord indices"""
        # Index by sigil
        if chord.sigil not in self.chord_index["by_sigil"]:
            self.chord_index["by_sigil"][chord.sigil] = []
        self.chord_index["by_sigil"][chord.sigil].append(chord_id)
        
        # Index by breath phase
        phase_bin = round(chord.breath_alignment * 8) % 8
        if str(phase_bin) not in self.chord_index["by_breath_phase"]:
            self.chord_index["by_breath_phase"][str(phase_bin)] = []
        self.chord_index["by_breath_phase"][str(phase_bin)].append(chord_id)
        
        # Index by chord type
        if chord.chord_type not in self.chord_index["by_chord_type"]:
            self.chord_index["by_chord_type"][chord.chord_type] = []
        self.chord_index["by_chord_type"][chord.chord_type].append(chord_id)
        
        # Index by invocation triggers
        for trigger in chord.invocation_triggers:
            if trigger not in self.chord_index["by_invocation"]:
                self.chord_index["by_invocation"][trigger] = []
            self.chord_index["by_invocation"][trigger].append(chord_id)
    
    def _save_preserved_chords(self):
        """Save preserved chords to storage"""
        # Create storage directory if it doesn't exist
        storage_dir = Path(self.storage_dir)
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Save chords
        for chord_id, chord in self.preserved_chords.items():
            chord_file = storage_dir / f"{chord_id}.json"
            
            # Save to file
            with open(chord_file, 'w') as f:
                json.dump(chord.to_dict(), f, indent=2)
    
    def _load_preserved_chords(self):
        """Load preserved chords from storage"""
        storage_dir = Path(self.storage_dir)
        if not storage_dir.exists():
            return
        
        # Load each chord file
        for chord_file in storage_dir.glob("*.json"):
            try:
                # Load chord data
                with open(chord_file, 'r') as f:
                    chord_data = json.load(f)
                
                # Create preserved chord
                chord = PreservedChord.from_dict(chord_data)
                
                # Store chord
                chord_id = chord_file.stem
                self.preserved_chords[chord_id] = chord
                
                # Update indices
                self._update_chord_indices(chord_id, chord)
                
            except Exception as e:
                print(f"Error loading chord {chord_file}: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        self._save_preserved_chords() 