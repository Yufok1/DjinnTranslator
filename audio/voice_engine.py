"""
Voice Engine Module
Handles voice synthesis, modulation, and spatial audio processing
"""

import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import torch
import torchaudio
from TTS.api import TTS
import sounddevice as sd
from scipy import signal
import librosa
import os

@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    djinn_type: str
    base_tone: float  # Hz
    resonance: float  # 0-1
    echo_depth: float  # 0-1
    spatial_position: tuple  # (x, y, z) coordinates
    modulation_range: tuple  # (min, max) Hz

class VoiceEngine:
    """Main voice engine class"""
    
    def __init__(self, model_dir: str = "models/tts"):
        self.model_dir = model_dir
        self.tts_models: Dict[str, TTS] = {}
        self.voice_profiles: Dict[str, VoiceProfile] = {}
        self.sample_rate = 22050
        
        # Create model directory
        os.makedirs(model_dir, exist_ok=True)
        
        # Initialize TTS models
        self._init_tts_models()
        
        # Initialize voice profiles
        self._init_voice_profiles()
    
    def _init_tts_models(self):
        """Initialize TTS models for different voices"""
        # Load base model
        self.tts_models["base"] = TTS("tts_models/en/ljspeech/tacotron2-DDC")
        
        # Load specialized models if available
        model_paths = {
            "purveyor": "tts_models/en/ljspeech/tacotron2-DDC",
            "daemon": "tts_models/en/ljspeech/tacotron2-DDC",
            "cursor": "tts_models/en/ljspeech/tacotron2-DDC",
            "mirror": "tts_models/en/ljspeech/tacotron2-DDC",
            "cryptographer": "tts_models/en/ljspeech/tacotron2-DDC"
        }
        
        for name, path in model_paths.items():
            try:
                self.tts_models[name] = TTS(path)
            except:
                self.tts_models[name] = self.tts_models["base"]
    
    def _init_voice_profiles(self):
        """Initialize voice profiles for each Djinn"""
        self.voice_profiles = {
            "purveyor": VoiceProfile(
                djinn_type="purveyor",
                base_tone=120.0,
                resonance=0.3,
                echo_depth=0.2,
                spatial_position=(0.0, 0.0, 0.0),
                modulation_range=(100.0, 140.0)
            ),
            "daemon": VoiceProfile(
                djinn_type="daemon",
                base_tone=85.0,
                resonance=0.7,
                echo_depth=0.8,
                spatial_position=(0.5, 0.5, 0.5),
                modulation_range=(70.0, 100.0)
            ),
            "cursor": VoiceProfile(
                djinn_type="cursor",
                base_tone=200.0,
                resonance=0.2,
                echo_depth=0.1,
                spatial_position=(-0.5, 0.0, 0.0),
                modulation_range=(180.0, 220.0)
            ),
            "mirror": VoiceProfile(
                djinn_type="mirror",
                base_tone=150.0,
                resonance=0.4,
                echo_depth=0.3,
                spatial_position=(0.0, -0.5, 0.0),
                modulation_range=(130.0, 170.0)
            ),
            "cryptographer": VoiceProfile(
                djinn_type="cryptographer",
                base_tone=110.0,
                resonance=0.5,
                echo_depth=0.6,
                spatial_position=(0.0, 0.0, 0.5),
                modulation_range=(90.0, 130.0)
            )
        }
    
    def synthesize_voice(self, text: str, djinn_type: str, state: Dict[str, Any]) -> np.ndarray:
        """Synthesize voice with modulation based on state"""
        # Get voice profile
        profile = self.voice_profiles.get(djinn_type, self.voice_profiles["base"])
        
        # Get TTS model
        model = self.tts_models.get(djinn_type, self.tts_models["base"])
        
        # Generate base audio
        audio = model.tts(text)
        
        # Apply modulation
        audio = self._apply_modulation(audio, profile, state)
        
        return audio
    
    def _apply_modulation(self, audio: np.ndarray, profile: VoiceProfile, state: Dict[str, Any]) -> np.ndarray:
        """Apply voice modulation effects"""
        # Pitch shift based on state
        pitch_shift = self._calculate_pitch_shift(profile, state)
        audio = librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=pitch_shift)
        
        # Apply resonance
        if profile.resonance > 0:
            audio = self._apply_resonance(audio, profile.resonance)
        
        # Apply echo
        if profile.echo_depth > 0:
            audio = self._apply_echo(audio, profile.echo_depth)
        
        # Apply spatial positioning
        audio = self._apply_spatial_positioning(audio, profile.spatial_position)
        
        return audio
    
    def _calculate_pitch_shift(self, profile: VoiceProfile, state: Dict[str, Any]) -> float:
        """Calculate pitch shift based on state"""
        # Base shift from profile
        base_shift = (profile.base_tone - 100.0) / 100.0
        
        # Adjust based on state
        if "intensity" in state:
            intensity = state["intensity"]
            shift_range = profile.modulation_range[1] - profile.modulation_range[0]
            shift = base_shift + (intensity - 0.5) * shift_range / 100.0
            return shift
        
        return base_shift
    
    def _apply_resonance(self, audio: np.ndarray, resonance: float) -> np.ndarray:
        """Apply resonance effect"""
        # Create resonant filter
        nyquist = self.sample_rate / 2
        low = 100.0 / nyquist
        high = 1000.0 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        
        # Apply filter
        resonant = signal.filtfilt(b, a, audio)
        
        # Mix with original
        return audio * (1 - resonance) + resonant * resonance
    
    def _apply_echo(self, audio: np.ndarray, echo_depth: float) -> np.ndarray:
        """Apply echo effect"""
        # Create echo
        delay = int(0.3 * self.sample_rate)  # 300ms delay
        echo = np.zeros_like(audio)
        echo[delay:] = audio[:-delay] * echo_depth
        
        # Mix with original
        return audio + echo
    
    def _apply_spatial_positioning(self, audio: np.ndarray, position: tuple) -> np.ndarray:
        """Apply spatial positioning effect"""
        # Simple stereo panning
        x, y, z = position
        
        # Calculate pan values
        left_pan = max(0, 1 - x)
        right_pan = max(0, 1 + x)
        
        # Normalize
        total = left_pan + right_pan
        left_pan /= total
        right_pan /= total
        
        # Create stereo signal
        stereo = np.vstack((audio * left_pan, audio * right_pan)).T
        
        return stereo
    
    def play_audio(self, audio: np.ndarray):
        """Play audio through speakers"""
        sd.play(audio, self.sample_rate)
        sd.wait()
    
    def save_audio(self, audio: np.ndarray, filename: str):
        """Save audio to file"""
        torchaudio.save(filename, torch.FloatTensor(audio).unsqueeze(0), self.sample_rate)
    
    def update_voice_profile(self, djinn_type: str, profile: VoiceProfile):
        """Update voice profile for a Djinn"""
        self.voice_profiles[djinn_type] = profile 