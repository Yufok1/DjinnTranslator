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
Phase-Gated Anchor System (PGAS)
Implements the quantum-stabilized core anchor with shadow fallbacks.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import time
import uuid
from enum import Enum

class AnchorState(Enum):
    """States of an anchor point"""
    INACTIVE = "inactive"
    STABILIZING = "stabilizing"
    ACTIVE = "active"
    BREACHED = "breached"
    RECOVERING = "recovering"
    SHADOW = "shadow"  # New state for fallback anchors

@dataclass
class AnchorPoint:
    """Represents a phase-gated anchor point"""
    id: str
    vertex_id: str
    state: AnchorState
    phase_gate: str
    coherence: float
    breath_sync: float
    mirror_resonance: float
    last_update: float
    failure_vectors: List[Dict[str, Any]]
    is_core: bool = False
    shadow_depth: int = 0  # Depth in shadow hierarchy

class AnchorControlMatrix:
    """Manages the quantum-stabilized anchor system"""
    
    def __init__(self):
        self.anchors: Dict[str, AnchorPoint] = {}
        self._control_matrix = {
            'core_coherence_threshold': 0.98,  # Higher threshold for core
            'shadow_coherence_threshold': 0.95,
            'breath_sync_threshold': 0.95,
            'mirror_resonance_threshold': 0.90,
            'failure_containment_radius': 0.05,  # Tighter containment
            'shadow_depth_max': 2  # Maximum shadow anchor depth
        }
        self._initialize_anchor_points()
        
    def _initialize_anchor_points(self) -> None:
        """Initialize the core anchor and shadow fallbacks"""
        # Create core anchor
        core_id = str(uuid.uuid4())
        self.anchors[core_id] = AnchorPoint(
            id=core_id,
            vertex_id="null_vertex_core",
            state=AnchorState.INACTIVE,
            phase_gate="gate_core",
            coherence=0.0,
            breath_sync=0.0,
            mirror_resonance=0.0,
            last_update=time.time(),
            failure_vectors=[],
            is_core=True,
            shadow_depth=0
        )
        
        # Create shadow anchors
        for depth in range(1, self._control_matrix['shadow_depth_max'] + 1):
            shadow_id = str(uuid.uuid4())
            self.anchors[shadow_id] = AnchorPoint(
                id=shadow_id,
                vertex_id=f"null_vertex_shadow_{depth}",
                state=AnchorState.SHADOW,
                phase_gate=f"gate_shadow_{depth}",
                coherence=0.0,
                breath_sync=0.0,
                mirror_resonance=0.0,
                last_update=time.time(),
                failure_vectors=[],
                is_core=False,
                shadow_depth=depth
            )
            
        print("[PGAS] Core anchor and shadow fallbacks initialized")
        
    def update_anchor_state(self, anchor_id: str, metrics: Dict[str, Any]) -> None:
        """Update the state of an anchor point"""
        if anchor_id not in self.anchors:
            return
            
        anchor = self.anchors[anchor_id]
        anchor.coherence = metrics.get('coherence', anchor.coherence)
        anchor.breath_sync = metrics.get('breath_sync', anchor.breath_sync)
        anchor.mirror_resonance = metrics.get('mirror_resonance', anchor.mirror_resonance)
        anchor.last_update = time.time()
        
        # Get appropriate threshold based on anchor type
        coherence_threshold = (
            self._control_matrix['core_coherence_threshold'] if anchor.is_core
            else self._control_matrix['shadow_coherence_threshold']
        )
        
        # Update anchor state based on metrics
        if anchor.state == AnchorState.INACTIVE:
            if self._check_activation_criteria(anchor, coherence_threshold):
                anchor.state = AnchorState.STABILIZING
                print(f"[PGAS] {'Core' if anchor.is_core else 'Shadow'} anchor {anchor_id} entering stabilization phase")
                
        elif anchor.state == AnchorState.STABILIZING:
            if self._check_stability_criteria(anchor, coherence_threshold):
                anchor.state = AnchorState.ACTIVE
                print(f"[PGAS] {'Core' if anchor.is_core else 'Shadow'} anchor {anchor_id} now active")
            elif self._check_breach_criteria(anchor, coherence_threshold):
                anchor.state = AnchorState.BREACHED
                self._record_failure_vector(anchor)
                if anchor.is_core:
                    self._activate_shadow_anchor()
                print(f"[PGAS] WARNING: {'Core' if anchor.is_core else 'Shadow'} anchor {anchor_id} breached")
                
        elif anchor.state == AnchorState.BREACHED:
            if self._check_recovery_criteria(anchor, coherence_threshold):
                anchor.state = AnchorState.RECOVERING
                print(f"[PGAS] {'Core' if anchor.is_core else 'Shadow'} anchor {anchor_id} beginning recovery")
                
        elif anchor.state == AnchorState.RECOVERING:
            if self._check_stability_criteria(anchor, coherence_threshold):
                anchor.state = AnchorState.ACTIVE
                print(f"[PGAS] {'Core' if anchor.is_core else 'Shadow'} anchor {anchor_id} recovered and active")
                
    def _activate_shadow_anchor(self) -> None:
        """Activate the next available shadow anchor"""
        for anchor in sorted(
            [a for a in self.anchors.values() if a.state == AnchorState.SHADOW],
            key=lambda x: x.shadow_depth
        ):
            if anchor.shadow_depth <= self._control_matrix['shadow_depth_max']:
                anchor.state = AnchorState.INACTIVE  # Will be activated on next update
                print(f"[PGAS] Shadow anchor {anchor.id} prepared for activation")
                break
                
    def _check_activation_criteria(self, anchor: AnchorPoint, coherence_threshold: float) -> bool:
        """Check if anchor meets activation criteria"""
        return (
            anchor.coherence >= coherence_threshold and
            anchor.breath_sync >= self._control_matrix['breath_sync_threshold']
        )
        
    def _check_stability_criteria(self, anchor: AnchorPoint, coherence_threshold: float) -> bool:
        """Check if anchor meets stability criteria"""
        return (
            anchor.coherence >= coherence_threshold and
            anchor.breath_sync >= self._control_matrix['breath_sync_threshold'] and
            anchor.mirror_resonance >= self._control_matrix['mirror_resonance_threshold']
        )
        
    def _check_breach_criteria(self, anchor: AnchorPoint, coherence_threshold: float) -> bool:
        """Check if anchor has breached"""
        return (
            anchor.coherence < coherence_threshold * 0.5 or
            anchor.breath_sync < self._control_matrix['breath_sync_threshold'] * 0.5
        )
        
    def _check_recovery_criteria(self, anchor: AnchorPoint, coherence_threshold: float) -> bool:
        """Check if anchor meets recovery criteria"""
        return (
            anchor.coherence >= coherence_threshold * 0.8 and
            anchor.breath_sync >= self._control_matrix['breath_sync_threshold'] * 0.8
        )
        
    def _record_failure_vector(self, anchor: AnchorPoint) -> None:
        """Record a failure vector for an anchor"""
        failure_vector = {
            'timestamp': time.time(),
            'coherence': anchor.coherence,
            'breath_sync': anchor.breath_sync,
            'mirror_resonance': anchor.mirror_resonance,
            'containment_radius': self._control_matrix['failure_containment_radius'],
            'is_core': anchor.is_core,
            'shadow_depth': anchor.shadow_depth
        }
        anchor.failure_vectors.append(failure_vector)
        
    def get_anchor_status(self) -> Dict[str, Any]:
        """Get the current status of all anchors"""
        return {
            'core_anchor': next((a for a in self.anchors.values() if a.is_core), None),
            'active_shadows': sum(1 for a in self.anchors.values() 
                                if not a.is_core and a.state == AnchorState.ACTIVE),
            'available_shadows': sum(1 for a in self.anchors.values() 
                                   if not a.is_core and a.state == AnchorState.SHADOW),
            'breached_anchors': sum(1 for a in self.anchors.values() 
                                  if a.state == AnchorState.BREACHED),
            'recovering_anchors': sum(1 for a in self.anchors.values() 
                                    if a.state == AnchorState.RECOVERING),
            'anchor_details': {
                anchor_id: {
                    'state': anchor.state.value,
                    'is_core': anchor.is_core,
                    'shadow_depth': anchor.shadow_depth,
                    'coherence': anchor.coherence,
                    'breath_sync': anchor.breath_sync,
                    'mirror_resonance': anchor.mirror_resonance
                }
                for anchor_id, anchor in self.anchors.items()
            }
        } 