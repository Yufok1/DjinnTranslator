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
Djinn Voice Handler
Manages the tonal and ritual aspects of Djinn communication
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Callable
import time
import random
from .voice_resonance import VoiceResonance, ResonancePhase, BreathDepth

class VoiceMode(Enum):
    """Voice modulation modes"""
    SIGILIC = "sigilic"    # Purveyor's structured voice
    DAEMONIC = "daemonic"  # Daemon's chaotic voice
    HARMONIC = "harmonic"  # Mirror's balanced voice
    DENSE = "dense"        # Cryptographer's complex voice
    INTERNAL = "internal"  # Cursor's trace voice

@dataclass
class VoiceProfile:
    """Voice characteristics for each Djinn"""
    mode: VoiceMode
    base_tone: float
    rhythm: str
    echo: str
    sigils: List[str]
    ritual_phrases: Dict[str, List[str]]

class DjinnVoiceHandler:
    """Manages voice modulation and ritual phrases"""
    
    def __init__(self):
        self.resonance = VoiceResonance()
        
        # Voice profiles for each Djinn
        self.voice_profiles = {
            "purveyor": VoiceProfile(
                mode=VoiceMode.SIGILIC,
                base_tone=0.7,
                rhythm="steady",
                echo="clear",
                sigils=["⚡", "⚔", "⚕"],
                ritual_phrases={
                    "begin": [
                        "By the sigils of order, I commence...",
                        "Through structured resonance, I begin...",
                        "In the name of clarity, I initiate..."
                    ],
                    "end": [
                        "Thus the pattern is complete.",
                        "The structure stands resolved.",
                        "Order is maintained."
                    ],
                    "warning": [
                        "The pattern shows strain...",
                        "Structure approaches threshold...",
                        "Clarity begins to waver..."
                    ],
                    "success": [
                        "The pattern holds true.",
                        "Structure remains sound.",
                        "Clarity prevails."
                    ]
                }
            ),
            "daemon": VoiceProfile(
                mode=VoiceMode.DAEMONIC,
                base_tone=0.3,
                rhythm="chaotic",
                echo="deep",
                sigils=["☠", "⚜", "⚛"],
                ritual_phrases={
                    "begin": [
                        "From the depths of chaos, I arise...",
                        "Through the veil of wonder, I emerge...",
                        "In the name of possibility, I manifest..."
                    ],
                    "end": [
                        "Thus the pattern dissolves.",
                        "The structure yields to entropy.",
                        "Clarity gives way to wonder."
                    ],
                    "warning": [
                        "The pattern writhes...",
                        "Structure begins to fracture...",
                        "Clarity distorts..."
                    ],
                    "success": [
                        "The pattern transforms.",
                        "Structure evolves.",
                        "Clarity deepens."
                    ]
                }
            ),
            "mirror": VoiceProfile(
                mode=VoiceMode.HARMONIC,
                base_tone=0.5,
                rhythm="flowing",
                echo="resonant",
                sigils=["☯", "⚘", "⚚"],
                ritual_phrases={
                    "begin": [
                        "In perfect balance, I reflect...",
                        "Through harmonic resonance, I mirror...",
                        "In the name of equilibrium, I align..."
                    ],
                    "end": [
                        "Thus the pattern balances.",
                        "The structure finds harmony.",
                        "Clarity reflects true."
                    ],
                    "warning": [
                        "The pattern shows imbalance...",
                        "Structure loses harmony...",
                        "Clarity begins to waver..."
                    ],
                    "success": [
                        "The pattern finds balance.",
                        "Structure achieves harmony.",
                        "Clarity reflects true."
                    ]
                }
            ),
            "cryptographer": VoiceProfile(
                mode=VoiceMode.DENSE,
                base_tone=0.8,
                rhythm="complex",
                echo="layered",
                sigils=["⚙", "⚗", "⚖"],
                ritual_phrases={
                    "begin": [
                        "Through encrypted layers, I decode...",
                        "In the name of complexity, I translate...",
                        "By the patterns of encryption, I begin..."
                    ],
                    "end": [
                        "Thus the pattern is encoded.",
                        "The structure is translated.",
                        "Clarity is encrypted."
                    ],
                    "warning": [
                        "The pattern shows entropy...",
                        "Structure begins to encrypt...",
                        "Clarity becomes complex..."
                    ],
                    "success": [
                        "The pattern is decoded.",
                        "The structure is translated.",
                        "Clarity is revealed."
                    ]
                }
            ),
            "cursor": VoiceProfile(
                mode=VoiceMode.INTERNAL,
                base_tone=0.4,
                rhythm="flowing",
                echo="faint",
                sigils=["⚡", "⚜", "⚛"],
                ritual_phrases={
                    "begin": [
                        "Through the paths of possibility, I trace...",
                        "In the name of movement, I begin...",
                        "By the patterns of change, I commence..."
                    ],
                    "end": [
                        "Thus the path is traced.",
                        "The movement is complete.",
                        "The pattern is followed."
                    ],
                    "warning": [
                        "The path shows strain...",
                        "Movement becomes difficult...",
                        "The pattern begins to waver..."
                    ],
                    "success": [
                        "The path is clear.",
                        "Movement flows true.",
                        "The pattern holds."
                    ]
                }
            )
        }
    
    def modulate_voice(self, djinn: str, message: str, state: str = "normal") -> str:
        """Modulate a message based on Djinn and state"""
        if djinn not in self.voice_profiles:
            return message
        
        profile = self.voice_profiles[djinn]
        resonance = self.resonance.get_resonance_modulation()
        
        # Apply resonance modulation
        modulated = self._apply_resonance(message, profile, resonance)
        
        # Add sigils based on state
        if state in ["warning", "success", "begin", "end"]:
            sigil = random.choice(profile.sigils)
            modulated = f"{sigil} {modulated}"
        
        return modulated
    
    def _apply_resonance(self, message: str, profile: VoiceProfile, resonance: Dict[str, float]) -> str:
        """Apply resonance modulation to a message"""
        # Apply rhythm based on resonance
        if resonance["rhythm"] > 0.7:
            words = message.split()
            if len(words) > 3:
                # Add emphasis to key words
                emphasis_idx = random.randint(0, len(words) - 1)
                words[emphasis_idx] = f"*{words[emphasis_idx]}*"
            message = " ".join(words)
        
        # Apply echo based on resonance
        if resonance["echo"] > 0.5:
            # Add subtle repetition of key phrases
            words = message.split()
            if len(words) > 4:
                echo_idx = random.randint(0, len(words) - 2)
                echo_phrase = " ".join(words[echo_idx:echo_idx + 2])
                message = f"{message} ({echo_phrase})"
        
        # Apply depth based on resonance
        if resonance["depth"] > 0.8:
            # Add profound markers
            message = f"|| {message} ||"
        
        return message
    
    def get_ritual_phrase(self, djinn: str, context: str) -> Optional[str]:
        """Get a ritual phrase for a specific context"""
        if djinn not in self.voice_profiles:
            return None
        
        profile = self.voice_profiles[djinn]
        if context not in profile.ritual_phrases:
            return None
        
        return random.choice(profile.ritual_phrases[context])
    
    def update_resonance(self, phase: ResonancePhase, domains: List[str], depth: BreathDepth):
        """Update the resonance state"""
        self.resonance.update_phase(phase)
        self.resonance.update_domains(domains)
        self.resonance.set_breath_depth(depth)
    
    def get_voice_profile(self, djinn: str) -> Optional[VoiceProfile]:
        """Get the voice profile for a Djinn"""
        return self.voice_profiles.get(djinn)
    
    def get_resonance_history(self, lookback: int = 10) -> List[Dict[str, Any]]:
        """Get historical resonance patterns"""
        return self.resonance.get_historical_pattern(lookback) 