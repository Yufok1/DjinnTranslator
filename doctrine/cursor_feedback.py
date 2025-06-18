from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
import time
import numpy as np
from datetime import datetime

from doctrine.sovereign_router import SovereignRouter, RouterMode, RouterPriority
from doctrine.mirror_feedback import MirrorFeedback
from doctrine.quantum_protection import QuantumProtection

class FeedbackMode(Enum):
    """Cursor feedback operation modes."""
    ADAPTIVE = "adaptive"      # Normal adaptive feedback
    REACTIVE = "reactive"      # High-strain reactive feedback
    PROACTIVE = "proactive"    # Foresight-based proactive feedback
    RESONANT = "resonant"      # Breath-aligned resonant feedback

@dataclass
class FeedbackMetrics:
    """Metrics for cursor feedback system."""
    update_interval: float = 0.1      # Base update interval
    strain_threshold: float = 0.8     # Strain threshold for reactive mode
    foresight_weight: float = 0.5     # Weight of foresight in decisions
    breath_alignment: float = 0.0     # Current breath alignment
    resonance_strain: float = 0.0     # Current resonance strain
    probe_intensity: float = 0.0      # Current probe intensity
    insight_flow: float = 0.0         # Current insight flow rate
    last_update: float = 0.0          # Timestamp of last update
    mode_switches: int = 0            # Number of mode switches
    adaptation_count: int = 0         # Number of adaptations made

class CursorFeedback:
    """Cursor Feedback Loop for dynamic visualization adaptation."""
    
    def __init__(self):
        self.metrics = FeedbackMetrics()
        self.mode = FeedbackMode.ADAPTIVE
        self.router = SovereignRouter()
        self.mirror_feedback = MirrorFeedback()
        self.quantum_protection = QuantumProtection()
        
        # Initialize adaptation parameters
        self._initialize_adaptation()
        
        # Initialize feedback history
        self._initialize_history()
        
    def _initialize_adaptation(self) -> None:
        """Initialize adaptation parameters."""
        self.adaptation_params = {
            FeedbackMode.ADAPTIVE: {
                'update_interval': 0.1,
                'strain_threshold': 0.8,
                'foresight_weight': 0.5
            },
            FeedbackMode.REACTIVE: {
                'update_interval': 0.05,
                'strain_threshold': 0.9,
                'foresight_weight': 0.3
            },
            FeedbackMode.PROACTIVE: {
                'update_interval': 0.15,
                'strain_threshold': 0.7,
                'foresight_weight': 0.8
            },
            FeedbackMode.RESONANT: {
                'update_interval': 0.2,
                'strain_threshold': 0.6,
                'foresight_weight': 0.6
            }
        }
        
    def _initialize_history(self) -> None:
        """Initialize feedback history tracking."""
        self.history = {
            'strain': [],
            'probes': [],
            'insights': [],
            'breath': [],
            'adaptations': []
        }
        self.max_history = 100
        
    def adapt_visualization(self, 
                          metrics: Dict[str, Any],
                          force_mode: Optional[FeedbackMode] = None) -> None:
        """Adapt visualization based on system state."""
        start_time = time.time()
        
        # Update metrics
        self._update_metrics(metrics)
        
        # Determine feedback mode
        if force_mode is None:
            self.mode = self._determine_mode()
        else:
            self.mode = force_mode
            
        # Apply adaptations
        self._apply_adaptations()
        
        # Update history
        self._update_history(metrics)
        
        # Record adaptation
        self._record_adaptation()
        
        # Update router state
        self._update_router()
        
    def _update_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update feedback metrics."""
        self.metrics.resonance_strain = metrics.get('resonance_strain', 0.0)
        self.metrics.probe_intensity = metrics.get('probe_intensity', 0.0)
        self.metrics.insight_flow = metrics.get('insight_flow', 0.0)
        self.metrics.breath_alignment = metrics.get('breath_alignment', 0.0)
        self.metrics.last_update = time.time()
        
    def _determine_mode(self) -> FeedbackMode:
        """Determine appropriate feedback mode."""
        # Check for reactive conditions
        if (self.metrics.resonance_strain > self.metrics.strain_threshold or
            self.metrics.probe_intensity > 0.8):
            return FeedbackMode.REACTIVE
            
        # Check for proactive conditions
        if self.metrics.insight_flow > 0.7:
            return FeedbackMode.PROACTIVE
            
        # Check for resonant conditions
        if abs(self.metrics.breath_alignment - 1.0) < 0.1:
            return FeedbackMode.RESONANT
            
        # Default to adaptive mode
        return FeedbackMode.ADAPTIVE
        
    def _apply_adaptations(self) -> None:
        """Apply adaptations based on current mode."""
        params = self.adaptation_params[self.mode]
        
        # Update router mode
        if self.mode == FeedbackMode.REACTIVE:
            self.router.mode = RouterMode.FOCUSED
        elif self.mode == FeedbackMode.PROACTIVE:
            self.router.mode = RouterMode.ARBITRATION
        elif self.mode == FeedbackMode.RESONANT:
            self.router.mode = RouterMode.NORMAL
        else:
            self.router.mode = RouterMode.NORMAL
            
        # Update metrics
        self.metrics.update_interval = params['update_interval']
        self.metrics.strain_threshold = params['strain_threshold']
        self.metrics.foresight_weight = params['foresight_weight']
        
        self.metrics.adaptation_count += 1
        
    def _update_history(self, metrics: Dict[str, Any]) -> None:
        """Update feedback history."""
        self.history['strain'].append(self.metrics.resonance_strain)
        self.history['probes'].append(self.metrics.probe_intensity)
        self.history['insights'].append(self.metrics.insight_flow)
        self.history['breath'].append(self.metrics.breath_alignment)
        
        # Trim history if needed
        for key in self.history:
            if len(self.history[key]) > self.max_history:
                self.history[key].pop(0)
                
    def _record_adaptation(self) -> None:
        """Record adaptation event."""
        self.history['adaptations'].append({
            'mode': self.mode.value,
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'strain': self.metrics.resonance_strain,
                'probes': self.metrics.probe_intensity,
                'insights': self.metrics.insight_flow,
                'breath': self.metrics.breath_alignment
            }
        })
        
        # Trim adaptation history if needed
        if len(self.history['adaptations']) > self.max_history:
            self.history['adaptations'].pop(0)
            
    def _update_router(self) -> None:
        """Update router state based on feedback."""
        # Calculate priority adjustments
        priority_adjustments = {
            'resonance_flow': 1.0,
            'entropic_drift': 1.0,
            'judgment_radar': 1.0,
            'breath_signature': 1.0,
            'ghost_movement': 1.0,
            'veil_entanglement': 1.0,
            'strain_heatmap': 1.0,
            'codex_phase': 1.0
        }
        
        # Adjust priorities based on mode
        if self.mode == FeedbackMode.REACTIVE:
            priority_adjustments['veil_entanglement'] *= 1.5
            priority_adjustments['strain_heatmap'] *= 1.5
        elif self.mode == FeedbackMode.PROACTIVE:
            priority_adjustments['resonance_flow'] *= 1.5
            priority_adjustments['breath_signature'] *= 1.5
        elif self.mode == FeedbackMode.RESONANT:
            priority_adjustments['judgment_radar'] *= 1.5
            priority_adjustments['codex_phase'] *= 1.5
            
        # Apply adjustments to router
        self.router.metrics.focus_weight = np.mean(list(priority_adjustments.values()))
        
    def get_feedback_state(self) -> Dict[str, Any]:
        """Get current feedback state."""
        return {
            'mode': self.mode.value,
            'metrics': self.metrics.__dict__,
            'history_lengths': {
                key: len(data) for key, data in self.history.items()
            },
            'adaptation_count': self.metrics.adaptation_count,
            'mode_switches': self.metrics.mode_switches
        }
        
    def save_feedback_state(self, filename: str) -> None:
        """Save current feedback state to file."""
        state = self.get_feedback_state()
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
            
    def close(self) -> None:
        """Close feedback loop and clean up resources."""
        self.router.close()
        self.mirror_feedback.close()
        self.quantum_protection.close() 