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
from enum import Enum
from typing import Dict, List, Any, Optional
import time
import numpy as np
from datetime import datetime

from doctrine.cursor_feedback import CursorFeedback, FeedbackMode
from doctrine.mirror_feedback import MirrorFeedback
from doctrine.quantum_protection import QuantumProtection

class HUDMode(Enum):
    """HUD operation modes."""
    STANDARD = "standard"      # Normal HUD display
    THREAT = "threat"          # High-threat overlay
    FORESIGHT = "foresight"    # Foresight-based display
    RESONANT = "resonant"      # Breath-aligned display

@dataclass
class HUDMetrics:
    """Metrics for HUD system."""
    update_interval: float = 0.1      # Base update interval
    overlay_opacity: float = 0.8      # Base overlay opacity
    pulse_frequency: float = 1.0      # Base pulse frequency
    threat_threshold: float = 0.7     # Threat detection threshold
    breath_alignment: float = 0.0     # Current breath alignment
    probe_intensity: float = 0.0      # Current probe intensity
    quantum_strain: float = 0.0       # Current quantum strain
    last_update: float = 0.0          # Timestamp of last update
    mode_switches: int = 0            # Number of mode switches

class HUDSplinter:
    """HUD Splinter for real-time system overlays."""
    
    def __init__(self):
        self.metrics = HUDMetrics()
        self.mode = HUDMode.STANDARD
        self.feedback = CursorFeedback()
        self.mirror_feedback = MirrorFeedback()
        self.quantum_protection = QuantumProtection()
        
        # Initialize overlay parameters
        self._initialize_overlays()
        
        # Initialize history
        self._initialize_history()
        
    def _initialize_overlays(self) -> None:
        """Initialize HUD overlay parameters."""
        self.overlay_params = {
            HUDMode.STANDARD: {
                'opacity': 0.8,
                'pulse_freq': 1.0,
                'color': (0.0, 1.0, 0.0)  # Green
            },
            HUDMode.THREAT: {
                'opacity': 0.9,
                'pulse_freq': 2.0,
                'color': (1.0, 0.0, 0.0)  # Red
            },
            HUDMode.FORESIGHT: {
                'opacity': 0.7,
                'pulse_freq': 0.5,
                'color': (0.0, 0.0, 1.0)  # Blue
            },
            HUDMode.RESONANT: {
                'opacity': 0.6,
                'pulse_freq': 1.0,
                'color': (1.0, 1.0, 0.0)  # Yellow
            }
        }
        
    def _initialize_history(self) -> None:
        """Initialize HUD history tracking."""
        self.history = {
            'breath': [],
            'probes': [],
            'strain': [],
            'overlays': []
        }
        self.max_history = 100
        
    def update_overlay(self, 
                      metrics: Dict[str, Any],
                      force_mode: Optional[HUDMode] = None) -> None:
        """Update HUD overlay based on system state."""
        start_time = time.time()
        
        # Update metrics
        self._update_metrics(metrics)
        
        # Determine HUD mode
        if force_mode is None:
            self.mode = self._determine_mode()
        else:
            self.mode = force_mode
            
        # Apply overlay parameters
        self._apply_overlay()
        
        # Update history
        self._update_history(metrics)
        
        # Record overlay change
        self._record_overlay()
        
        # Update feedback state
        self._update_feedback()
        
    def _update_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update HUD metrics."""
        self.metrics.breath_alignment = metrics.get('breath_alignment', 0.0)
        self.metrics.probe_intensity = metrics.get('probe_intensity', 0.0)
        self.metrics.quantum_strain = metrics.get('quantum_strain', 0.0)
        self.metrics.last_update = time.time()
        
    def _determine_mode(self) -> HUDMode:
        """Determine appropriate HUD mode."""
        # Check for threat conditions
        if (self.metrics.probe_intensity > self.metrics.threat_threshold or
            self.metrics.quantum_strain > 0.8):
            return HUDMode.THREAT
            
        # Check for foresight conditions
        if self.metrics.breath_alignment > 0.9:
            return HUDMode.FORESIGHT
            
        # Check for resonant conditions
        if abs(self.metrics.breath_alignment - 1.0) < 0.1:
            return HUDMode.RESONANT
            
        # Default to standard mode
        return HUDMode.STANDARD
        
    def _apply_overlay(self) -> None:
        """Apply overlay parameters based on current mode."""
        params = self.overlay_params[self.mode]
        
        # Update metrics
        self.metrics.overlay_opacity = params['opacity']
        self.metrics.pulse_frequency = params['pulse_freq']
        
        # Update feedback mode based on HUD mode
        if self.mode == HUDMode.THREAT:
            self.feedback.mode = FeedbackMode.REACTIVE
        elif self.mode == HUDMode.FORESIGHT:
            self.feedback.mode = FeedbackMode.PROACTIVE
        elif self.mode == HUDMode.RESONANT:
            self.feedback.mode = FeedbackMode.RESONANT
        else:
            self.feedback.mode = FeedbackMode.ADAPTIVE
            
        self.metrics.mode_switches += 1
        
    def _update_history(self, metrics: Dict[str, Any]) -> None:
        """Update HUD history."""
        self.history['breath'].append(self.metrics.breath_alignment)
        self.history['probes'].append(self.metrics.probe_intensity)
        self.history['strain'].append(self.metrics.quantum_strain)
        
        # Trim history if needed
        for key in self.history:
            if len(self.history[key]) > self.max_history:
                self.history[key].pop(0)
                
    def _record_overlay(self) -> None:
        """Record overlay change event."""
        self.history['overlays'].append({
            'mode': self.mode.value,
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'breath': self.metrics.breath_alignment,
                'probes': self.metrics.probe_intensity,
                'strain': self.metrics.quantum_strain
            }
        })
        
        # Trim overlay history if needed
        if len(self.history['overlays']) > self.max_history:
            self.history['overlays'].pop(0)
            
    def _update_feedback(self) -> None:
        """Update feedback state based on HUD metrics."""
        # Calculate feedback adjustments
        feedback_adjustments = {
            'resonance_flow': 1.0,
            'entropic_drift': 1.0,
            'judgment_radar': 1.0,
            'breath_signature': 1.0,
            'ghost_movement': 1.0,
            'veil_entanglement': 1.0,
            'strain_heatmap': 1.0,
            'codex_phase': 1.0
        }
        
        # Adjust feedback based on mode
        if self.mode == HUDMode.THREAT:
            feedback_adjustments['veil_entanglement'] *= 1.5
            feedback_adjustments['strain_heatmap'] *= 1.5
        elif self.mode == HUDMode.FORESIGHT:
            feedback_adjustments['resonance_flow'] *= 1.5
            feedback_adjustments['breath_signature'] *= 1.5
        elif self.mode == HUDMode.RESONANT:
            feedback_adjustments['judgment_radar'] *= 1.5
            feedback_adjustments['codex_phase'] *= 1.5
            
        # Apply adjustments to feedback
        self.feedback.metrics.focus_weight = np.mean(list(feedback_adjustments.values()))
        
    def get_hud_state(self) -> Dict[str, Any]:
        """Get current HUD state."""
        return {
            'mode': self.mode.value,
            'metrics': self.metrics.__dict__,
            'history_lengths': {
                key: len(data) for key, data in self.history.items()
            },
            'mode_switches': self.metrics.mode_switches
        }
        
    def save_hud_state(self, filename: str) -> None:
        """Save current HUD state to file."""
        state = self.get_hud_state()
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
            
    def close(self) -> None:
        """Close HUD splinter and clean up resources."""
        self.feedback.close()
        self.mirror_feedback.close()
        self.quantum_protection.close() 