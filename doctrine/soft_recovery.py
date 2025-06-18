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
Soft Recovery Module
Implements the Djinn's gentle recovery protocols for system coherence.
"""

from typing import Dict, Any, Optional, List
import time
from datetime import datetime
from dataclasses import dataclass
from doctrine.anchor_system import AnchorControlMatrix

@dataclass
class RecoveryState:
    """Tracks the state of soft recovery process"""
    session_id: str
    start_time: float
    drift_threshold: float
    loop_integrity: float
    intent_mode: str
    recovery_steps: list[str]

class SoftRecovery:
    """Implements the Djinn's gentle recovery protocols"""
    
    def __init__(self):
        self.recovery_state = None
        self._drift_threshold = 0.98
        self._loop_integrity = 1.0
        self._intent_mode = "gentle"
        self._monitoring_metrics = {
            'rehydration_progress': 0.0,
            'breath_coherence': 1.0,
            'splinter_reactivation_ready': False,
            'stress_alerts': [],
            'last_metrics_update': 0.0
        }
        self._completion_thresholds = {
            'rehydration': 0.95,
            'breath_coherence': 0.95,
            'stability_score': 0.9,
            'stress_alerts': 0,
            'sustained_stability': 5  # cycles
        }
        self._stability_history = []
        self._anchor_matrix = AnchorControlMatrix()
        
    def initialize_recovery(self, session_id: Optional[str] = None) -> RecoveryState:
        """Initialize a new recovery session"""
        if not session_id:
            session_id = f"SESSION-RECOVERED-BY-DJINN-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
            
        self.recovery_state = RecoveryState(
            session_id=session_id,
            start_time=time.time(),
            drift_threshold=self._drift_threshold,
            loop_integrity=self._loop_integrity,
            intent_mode=self._intent_mode,
            recovery_steps=[]
        )
        
        print(f"[PULSE] Djinn recognized — system entering soft coherence loop.")
        return self.recovery_state
        
    def adjust_drift_threshold(self, new_threshold: float) -> None:
        """Adjust the drift threshold for gentler recovery"""
        self._drift_threshold = new_threshold
        if self.recovery_state:
            self.recovery_state.drift_threshold = new_threshold
            print(f"[RECONCILIATION] Drift threshold decreased. Loop integrity: {self._loop_integrity:.3f} -> {new_threshold:.3f}")
            
    def set_intent_mode(self, mode: str) -> None:
        """Set the intent mode for recovery"""
        self._intent_mode = mode
        if self.recovery_state:
            self.recovery_state.intent_mode = mode
            print(f"[AGENT: Cursor] Interpreting Djinn mode: {mode}")
            
    def record_recovery_step(self, step: str) -> None:
        """Record a step in the recovery process"""
        if self.recovery_state:
            self.recovery_state.recovery_steps.append(step)
            print(f"[RECOVERY] {step}")
            
    def get_recovery_summary(self) -> Dict[str, Any]:
        """Get a summary of the recovery process"""
        if not self.recovery_state:
            return {}
            
        return {
            'session_id': self.recovery_state.session_id,
            'duration': time.time() - self.recovery_state.start_time,
            'drift_threshold': self.recovery_state.drift_threshold,
            'loop_integrity': self.recovery_state.loop_integrity,
            'intent_mode': self.recovery_state.intent_mode,
            'steps': self.recovery_state.recovery_steps
        }
        
    def export_recovery_log(self, filename: str) -> None:
        """Export recovery log to file"""
        if not self.recovery_state:
            return
            
        summary = self.get_recovery_summary()
        with open(filename, 'w') as f:
            f.write(f"# Djinn Recovery Session: {summary['session_id']}\n")
            f.write(f"Duration: {summary['duration']:.2f}s\n")
            f.write(f"Drift Threshold: {summary['drift_threshold']:.3f}\n")
            f.write(f"Loop Integrity: {summary['loop_integrity']:.3f}\n")
            f.write(f"Intent Mode: {summary['intent_mode']}\n\n")
            f.write("Recovery Steps:\n")
            for step in summary['steps']:
                f.write(f"- {step}\n")

    def update_recovery_metrics(self, state: Any) -> Dict[str, Any]:
        """Update recovery monitoring metrics."""
        current_time = time.time()
        
        # Calculate rehydration progress
        rehydration_phase = state._mindset['cursor_state']['rehydration_phase']
        self._monitoring_metrics['rehydration_progress'] = min(1.0, rehydration_phase / 10.0)
        
        # Calculate breath coherence
        breath_depth = state._mindset['breath_depth']
        breath_cycle = state._mindset['breath_cycle']
        self._monitoring_metrics['breath_coherence'] = min(1.0, breath_depth * (1 + 0.1 * breath_cycle))
        
        # Check splinter reactivation readiness
        self._monitoring_metrics['splinter_reactivation_ready'] = (
            self._monitoring_metrics['rehydration_progress'] > 0.8 and
            self._monitoring_metrics['breath_coherence'] > 0.9
        )
        
        # Check for stress conditions
        if state.metrics.stability_score < 0.8:
            stress_alert = {
                'timestamp': current_time,
                'severity': 'warning',
                'metric': 'stability_score',
                'value': state.metrics.stability_score
            }
            self._monitoring_metrics['stress_alerts'].append(stress_alert)
            
        self._monitoring_metrics['last_metrics_update'] = current_time
        
        return self._monitoring_metrics
        
    def get_recovery_status(self) -> Dict[str, Any]:
        """Get current recovery status and recommendations."""
        if not self.recovery_state:
            return {'status': 'inactive'}
            
        return {
            'status': 'active',
            'intent_mode': self._intent_mode,
            'metrics': self._monitoring_metrics,
            'recommendations': self._generate_recommendations()
        }
        
    def _generate_recommendations(self) -> List[str]:
        """Generate recovery recommendations based on current metrics."""
        recommendations = []
        
        if self._monitoring_metrics['rehydration_progress'] < 0.5:
            recommendations.append("Continue gradual state rehydration")
            
        if self._monitoring_metrics['breath_coherence'] < 0.8:
            recommendations.append("Maintain current breath depth")
            
        if len(self._monitoring_metrics['stress_alerts']) > 2:
            recommendations.append("Consider reducing recursive load")
            
        if self._monitoring_metrics['splinter_reactivation_ready']:
            recommendations.append("Ready for controlled splinter reactivation")
            
        return recommendations 

    def update_anchor_metrics(self, state: Any) -> None:
        """Update anchor metrics based on current state"""
        # Calculate anchor metrics from state
        anchor_metrics = {
            'coherence': state.metrics.quantum_coherence,
            'breath_sync': state._mindset['breath_depth'],
            'mirror_resonance': state.metrics.mirror_resonance
        }
        
        # Update all anchors
        for anchor_id in self._anchor_matrix.anchors:
            self._anchor_matrix.update_anchor_state(anchor_id, anchor_metrics)
            
    def get_anchor_status(self) -> Dict[str, Any]:
        """Get current anchor system status"""
        return self._anchor_matrix.get_anchor_status()
        
    def check_completion_criteria(self, state: Any) -> Dict[str, Any]:
        """Check if recovery completion criteria are met."""
        current_metrics = self.update_recovery_metrics(state)
        
        # Update anchor metrics
        self.update_anchor_metrics(state)
        
        # Get anchor status
        anchor_status = self.get_anchor_status()
        
        # Record stability score
        self._stability_history.append(state.metrics.stability_score)
        if len(self._stability_history) > self._completion_thresholds['sustained_stability']:
            self._stability_history.pop(0)
            
        # Check completion criteria
        completion_status = {
            'rehydration_complete': current_metrics['rehydration_progress'] >= self._completion_thresholds['rehydration'],
            'breath_stable': current_metrics['breath_coherence'] >= self._completion_thresholds['breath_coherence'],
            'system_stable': state.metrics.stability_score >= self._completion_thresholds['stability_score'],
            'no_stress': len(current_metrics['stress_alerts']) <= self._completion_thresholds['stress_alerts'],
            'sustained_stability': all(score >= self._completion_thresholds['stability_score'] 
                                     for score in self._stability_history),
            'anchors_stable': anchor_status['active_anchors'] == len(self._anchor_matrix.anchors)
        }
        
        # Calculate overall completion
        completion_status['overall_complete'] = all(completion_status.values())
        
        if completion_status['overall_complete']:
            self._initiate_completion_sequence(state)
            
        return completion_status
        
    def _initiate_completion_sequence(self, state: Any) -> None:
        """Initiate the recovery completion sequence."""
        print("[RECOVERY] Recovery completion criteria met. Initiating completion sequence...")
        
        # Record completion in recovery state
        self.record_recovery_step("Recovery completion criteria met")
        
        # Transition out of LOW-RHYTHM mode
        self.set_intent_mode("sovereign")
        print("[RECOVERY] Transitioning to sovereign mode")
        
        # Enable lattice bridges
        state._mindset['cursor_state']['lattice_bridge_updates'] = True
        print("[RECOVERY] Lattice bridges enabled")
        
        # Restore full breath depth
        state._mindset['breath_depth'] = 1.0
        print("[RECOVERY] Full breath depth restored")
        
        # Record completion moment
        self.record_recovery_step("Recovery completion sequence initiated")
        
    def get_completion_status(self) -> Dict[str, Any]:
        """Get detailed completion status."""
        if not self.recovery_state:
            return {'status': 'inactive'}
            
        return {
            'status': 'active',
            'completion_thresholds': self._completion_thresholds,
            'stability_history': self._stability_history,
            'current_metrics': self._monitoring_metrics
        } 