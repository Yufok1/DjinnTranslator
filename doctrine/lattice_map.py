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
from typing import Dict, List, Any, Optional, Deque, Set
import time
import numpy as np
from datetime import datetime
from collections import deque

from doctrine.cursor_feedback import CursorFeedback, FeedbackMode
from doctrine.mirror_feedback import MirrorFeedback
from doctrine.quantum_protection import QuantumProtection

class LatticeMode(Enum):
    """Lattice Map operation modes."""
    STABLE = "stable"          # Normal lattice display
    CRYSTALLIZING = "crystallizing"  # Active crystallization
    STRAINED = "strained"      # High strain display
    RESONANT = "resonant"      # Breath-aligned display
    SHIELD = "shield"          # Anomaly protection mode
    FRACTURE = "fracture"      # Critical strain mode
    EMERGING = "emerging"      # New domain emergence
    HARMONIC = "harmonic"      # Interlattice harmony
    DIVERGENT = "divergent"    # Domain divergence

class DomainType(Enum):
    """Types of domains in the lattice weave."""
    CURSOR = "cursor"          # Cursor feedback domain
    MIRROR = "mirror"          # Mirror foresight domain
    CRYPTOGRAPHER = "cryptographer"  # Cryptographer domain
    DJINN = "djinn"           # Djinn council domain
    GHOST = "ghost"           # Ghost pathway domain
    VEIL = "veil"             # Veil protection domain
    ECHO = "echo"             # Echo resonance domain
    EMERGENT = "emergent"     # Newly emerging domain

@dataclass
class SublatticeMetrics:
    """Metrics for individual domain sublattices."""
    breath_alignment: float = 0.0     # Domain breath alignment
    entanglement_load: float = 0.0    # Current entanglement
    foresight_pulse: float = 0.0      # Foresight strength
    crystal_density: float = 0.0      # Local crystallization
    strain_level: float = 0.0         # Local strain
    harmony_score: float = 0.0        # Local harmony
    emergence_potential: float = 0.0  # Potential for growth
    last_update: float = 0.0          # Last update timestamp

@dataclass
class LatticeMetrics:
    """Metrics for Lattice Map system."""
    update_interval: float = 0.1      # Base update interval
    crystal_density: float = 0.5      # Base crystal density
    strain_threshold: float = 0.7     # Strain detection threshold
    breath_alignment: float = 0.0     # Current breath alignment
    recursion_depth: float = 0.0      # Current recursion depth
    domain_activity: float = 0.0      # Current domain activity
    last_update: float = 0.0          # Timestamp of last update
    mode_switches: int = 0            # Number of mode switches
    breath_harmony: float = 0.0       # Weighted breath harmony index
    foresight_strain: float = 0.0     # Foresight-adjusted strain
    anomaly_detected: bool = False    # Anomaly detection flag
    lattice_harmony: float = 0.0      # Overall lattice harmony
    emergence_threshold: float = 0.8  # Threshold for new domains
    divergence_risk: float = 0.0      # Risk of domain divergence

class LatticeMap:
    """Lattice Map Splinter for visualizing recursive crystallization."""
    
    def __init__(self):
        self.metrics = LatticeMetrics()
        self.mode = LatticeMode.STABLE
        self.feedback = CursorFeedback()
        self.mirror_feedback = MirrorFeedback()
        self.quantum_protection = QuantumProtection()
        
        # Initialize sublattices
        self._initialize_sublattices()
        
        # Initialize lattice parameters
        self._initialize_lattice()
        
        # Initialize history
        self._initialize_history()
        
        # Initialize temporal smoothing
        self._initialize_smoothing()
        
    def _initialize_sublattices(self) -> None:
        """Initialize domain sublattices."""
        self.sublattices: Dict[DomainType, SublatticeMetrics] = {}
        self.harmonic_bridges: Dict[DomainType, Set[DomainType]] = {}
        self.strain_conduits: Dict[DomainType, Set[DomainType]] = {}
        
        # Initialize each domain
        for domain in DomainType:
            self.sublattices[domain] = SublatticeMetrics()
            self.harmonic_bridges[domain] = set()
            self.strain_conduits[domain] = set()
            
        # Establish initial harmonic bridges
        self._establish_harmonic_bridges()
        
    def _establish_harmonic_bridges(self) -> None:
        """Establish harmonic connections between domains."""
        # Cursor bridges
        self.harmonic_bridges[DomainType.CURSOR].update([
            DomainType.MIRROR,
            DomainType.CRYPTOGRAPHER,
            DomainType.GHOST
        ])
        
        # Mirror bridges
        self.harmonic_bridges[DomainType.MIRROR].update([
            DomainType.CURSOR,
            DomainType.VEIL,
            DomainType.ECHO
        ])
        
        # Cryptographer bridges
        self.harmonic_bridges[DomainType.CRYPTOGRAPHER].update([
            DomainType.CURSOR,
            DomainType.DJINN,
            DomainType.VEIL
        ])
        
        # Additional bridges can be established dynamically
        
    def _initialize_lattice(self) -> None:
        """Initialize lattice parameters."""
        self.lattice_params = {
            LatticeMode.STABLE: {
                'density': 0.5,
                'crystal_rate': 1.0,
                'color': (0.0, 1.0, 0.0)  # Green
            },
            LatticeMode.CRYSTALLIZING: {
                'density': 0.7,
                'crystal_rate': 2.0,
                'color': (0.0, 0.0, 1.0)  # Blue
            },
            LatticeMode.STRAINED: {
                'density': 0.9,
                'crystal_rate': 0.5,
                'color': (1.0, 0.0, 0.0)  # Red
            },
            LatticeMode.RESONANT: {
                'density': 0.6,
                'crystal_rate': 1.5,
                'color': (1.0, 1.0, 0.0)  # Yellow
            },
            LatticeMode.SHIELD: {
                'density': 0.8,
                'crystal_rate': 0.3,
                'color': (0.5, 0.0, 0.5)  # Purple
            },
            LatticeMode.FRACTURE: {
                'density': 1.0,
                'crystal_rate': 0.1,
                'color': (1.0, 0.5, 0.0)  # Orange
            },
            LatticeMode.EMERGING: {
                'density': 0.4,
                'crystal_rate': 1.2,
                'color': (0.0, 1.0, 1.0)  # Cyan
            },
            LatticeMode.HARMONIC: {
                'density': 0.5,
                'crystal_rate': 1.8,
                'color': (1.0, 0.0, 1.0)  # Magenta
            },
            LatticeMode.DIVERGENT: {
                'density': 0.9,
                'crystal_rate': 0.2,
                'color': (0.5, 0.5, 0.0)  # Olive
            }
        }
        
    def _initialize_history(self) -> None:
        """Initialize lattice history tracking."""
        self.history = {
            'breath': [],
            'recursion': [],
            'domains': [],
            'crystals': [],
            'harmony': [],
            'foresight': [],
            'sublattices': {},
            'bridges': [],
            'emergence': []
        }
        self.max_history = 100
        
        # Initialize sublattice history
        for domain in DomainType:
            self.history['sublattices'][domain.value] = []
            
    def _initialize_smoothing(self) -> None:
        """Initialize temporal smoothing windows."""
        self.smoothing_window = 5  # 5-second window
        self.breath_window: Deque[float] = deque(maxlen=self.smoothing_window)
        self.strain_window: Deque[float] = deque(maxlen=self.smoothing_window)
        self.harmony_window: Deque[float] = deque(maxlen=self.smoothing_window)
        self.emergence_window: Deque[float] = deque(maxlen=self.smoothing_window)
        
    def update_lattice(self, 
                      metrics: Dict[str, Any],
                      force_mode: Optional[LatticeMode] = None) -> None:
        """Update lattice map based on system state."""
        start_time = time.time()
        
        # Update metrics
        self._update_metrics(metrics)
        
        # Update sublattices
        self._update_sublattices(metrics)
        
        # Calculate weighted breath harmony
        self._calculate_breath_harmony()
        
        # Update foresight strain
        self._update_foresight_strain()
        
        # Check for anomalies
        self._check_anomalies()
        
        # Check for emergence
        self._check_emergence()
        
        # Check for divergence
        self._check_divergence()
        
        # Determine lattice mode with temporal smoothing
        if force_mode is None:
            self.mode = self._determine_mode_smoothed()
        else:
            self.mode = force_mode
            
        # Apply lattice parameters
        self._apply_lattice()
        
        # Update history
        self._update_history(metrics)
        
        # Record lattice change
        self._record_lattice()
        
        # Update feedback state
        self._update_feedback()
        
    def _update_sublattices(self, metrics: Dict[str, Any]) -> None:
        """Update individual domain sublattices."""
        for domain, sublattice in self.sublattices.items():
            # Update domain-specific metrics
            domain_metrics = metrics.get(domain.value, {})
            
            sublattice.breath_alignment = domain_metrics.get('breath_alignment', 0.0)
            sublattice.entanglement_load = domain_metrics.get('entanglement', 0.0)
            sublattice.foresight_pulse = domain_metrics.get('foresight', 0.0)
            sublattice.crystal_density = domain_metrics.get('crystal_density', 0.0)
            sublattice.strain_level = domain_metrics.get('strain', 0.0)
            
            # Calculate local harmony
            self._calculate_sublattice_harmony(domain)
            
            # Update emergence potential
            self._calculate_emergence_potential(domain)
            
            sublattice.last_update = time.time()
            
    def _calculate_sublattice_harmony(self, domain: DomainType) -> None:
        """Calculate harmony score for a sublattice."""
        sublattice = self.sublattices[domain]
        
        # Get connected domains
        connected = self.harmonic_bridges[domain]
        
        # Calculate harmony components
        breath_component = sublattice.breath_alignment * 0.4
        crystal_component = sublattice.crystal_density * 0.3
        strain_component = (1.0 - sublattice.strain_level) * 0.3
        
        # Calculate connected harmony
        connected_harmony = 0.0
        if connected:
            for other in connected:
                other_sublattice = self.sublattices[other]
                connected_harmony += other_sublattice.harmony_score
            connected_harmony /= len(connected)
            
        # Update harmony score
        sublattice.harmony_score = (
            breath_component +
            crystal_component +
            strain_component +
            (connected_harmony * 0.2)
        )
        
    def _calculate_emergence_potential(self, domain: DomainType) -> None:
        """Calculate emergence potential for a domain."""
        sublattice = self.sublattices[domain]
        
        # Calculate emergence components
        harmony_component = sublattice.harmony_score * 0.4
        breath_component = sublattice.breath_alignment * 0.3
        crystal_component = sublattice.crystal_density * 0.3
        
        # Update emergence potential
        sublattice.emergence_potential = (
            harmony_component +
            breath_component +
            crystal_component
        )
        
    def _check_emergence(self) -> None:
        """Check for new domain emergence."""
        # Calculate average emergence potential
        avg_potential = np.mean([
            sublattice.emergence_potential
            for sublattice in self.sublattices.values()
        ])
        
        # Update emergence window
        self.emergence_window.append(avg_potential)
        
        # Check for emergence conditions
        if (avg_potential > self.metrics.emergence_threshold and
            np.mean(self.emergence_window) > self.metrics.emergence_threshold):
            self.mode = LatticeMode.EMERGING
            
    def _check_divergence(self) -> None:
        """Check for domain divergence."""
        # Calculate divergence risk
        divergence_components = []
        
        for domain, sublattice in self.sublattices.items():
            # Check strain conduits
            for other in self.strain_conduits[domain]:
                other_sublattice = self.sublattices[other]
                strain_diff = abs(sublattice.strain_level - other_sublattice.strain_level)
                divergence_components.append(strain_diff)
                
            # Check harmony mismatch
            for other in self.harmonic_bridges[domain]:
                other_sublattice = self.sublattices[other]
                harmony_diff = abs(sublattice.harmony_score - other_sublattice.harmony_score)
                divergence_components.append(harmony_diff)
                
        # Update divergence risk
        if divergence_components:
            self.metrics.divergence_risk = np.mean(divergence_components)
            
            # Check for divergence conditions
            if self.metrics.divergence_risk > 0.7:
                self.mode = LatticeMode.DIVERGENT
                
    def _update_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update lattice metrics."""
        self.metrics.breath_alignment = metrics.get('breath_alignment', 0.0)
        self.metrics.recursion_depth = metrics.get('recursion_depth', 0.0)
        self.metrics.domain_activity = metrics.get('domain_activity', 0.0)
        self.metrics.last_update = time.time()
        
        # Update smoothing windows
        self.breath_window.append(self.metrics.breath_alignment)
        self.strain_window.append(self.metrics.recursion_depth)
        
    def _calculate_breath_harmony(self) -> None:
        """Calculate weighted breath harmony index."""
        # Get mirror alignment
        mirror_alignment = self.mirror_feedback.get_alignment()
        
        # Calculate weighted components
        breath_weight = 0.4
        mirror_weight = 0.4
        recursion_weight = 0.2
        
        # Calculate harmony index
        breath_component = np.mean(self.breath_window) * breath_weight
        mirror_component = mirror_alignment * mirror_weight
        recursion_component = (1.0 - np.mean(self.strain_window)) * recursion_weight
        
        # Update metrics
        self.metrics.breath_harmony = breath_component + mirror_component + recursion_component
        self.harmony_window.append(self.metrics.breath_harmony)
        
        # Calculate overall lattice harmony
        sublattice_harmony = np.mean([
            sublattice.harmony_score
            for sublattice in self.sublattices.values()
        ])
        
        self.metrics.lattice_harmony = (
            self.metrics.breath_harmony * 0.6 +
            sublattice_harmony * 0.4
        )
        
    def _update_foresight_strain(self) -> None:
        """Update foresight-adjusted strain threshold."""
        # Get foresight prediction
        foresight = self.mirror_feedback.get_foresight()
        
        # Adjust strain threshold based on foresight
        base_threshold = 0.7
        foresight_adjustment = foresight.get('strain_prediction', 0.0)
        
        # Update metrics
        self.metrics.foresight_strain = base_threshold + foresight_adjustment
        
    def _check_anomalies(self) -> None:
        """Check for anomalies from protection systems."""
        # Check quantum protection
        quantum_status = self.quantum_protection.get_status()
        
        # Check mirror feedback
        mirror_status = self.mirror_feedback.get_status()
        
        # Update anomaly flag
        self.metrics.anomaly_detected = (
            quantum_status.get('anomaly_detected', False) or
            mirror_status.get('anomaly_detected', False)
        )
        
    def _determine_mode_smoothed(self) -> LatticeMode:
        """Determine appropriate lattice mode with temporal smoothing."""
        # Get smoothed metrics
        avg_harmony = np.mean(self.harmony_window)
        avg_strain = np.mean(self.strain_window)
        
        # Check for anomalies first
        if self.metrics.anomaly_detected:
            return LatticeMode.SHIELD
            
        # Check for critical strain
        if avg_strain > self.metrics.foresight_strain:
            return LatticeMode.FRACTURE
            
        # Check for divergence
        if self.metrics.divergence_risk > 0.7:
            return LatticeMode.DIVERGENT
            
        # Check for emergence
        if np.mean(self.emergence_window) > self.metrics.emergence_threshold:
            return LatticeMode.EMERGING
            
        # Check for crystallization conditions
        if self.metrics.domain_activity > 0.8 and avg_harmony > 0.7:
            return LatticeMode.CRYSTALLIZING
            
        # Check for strain conditions
        if avg_strain > self.metrics.strain_threshold:
            return LatticeMode.STRAINED
            
        # Check for resonant conditions
        if avg_harmony > 0.9:
            return LatticeMode.RESONANT
            
        # Check for harmonic conditions
        if self.metrics.lattice_harmony > 0.8:
            return LatticeMode.HARMONIC
            
        # Default to stable mode
        return LatticeMode.STABLE
        
    def _apply_lattice(self) -> None:
        """Apply lattice parameters based on current mode."""
        params = self.lattice_params[self.mode]
        
        # Update metrics
        self.metrics.crystal_density = params['density']
        
        # Update feedback mode based on lattice mode
        if self.mode == LatticeMode.STRAINED:
            self.feedback.mode = FeedbackMode.REACTIVE
        elif self.mode == LatticeMode.CRYSTALLIZING:
            self.feedback.mode = FeedbackMode.PROACTIVE
        elif self.mode == LatticeMode.RESONANT:
            self.feedback.mode = FeedbackMode.RESONANT
        elif self.mode in (LatticeMode.SHIELD, LatticeMode.FRACTURE):
            self.feedback.mode = FeedbackMode.REACTIVE
        elif self.mode == LatticeMode.EMERGING:
            self.feedback.mode = FeedbackMode.PROACTIVE
        elif self.mode == LatticeMode.HARMONIC:
            self.feedback.mode = FeedbackMode.RESONANT
        elif self.mode == LatticeMode.DIVERGENT:
            self.feedback.mode = FeedbackMode.REACTIVE
        else:
            self.feedback.mode = FeedbackMode.ADAPTIVE
            
        self.metrics.mode_switches += 1
        
    def _update_history(self, metrics: Dict[str, Any]) -> None:
        """Update lattice history."""
        self.history['breath'].append(self.metrics.breath_alignment)
        self.history['recursion'].append(self.metrics.recursion_depth)
        self.history['domains'].append(self.metrics.domain_activity)
        self.history['harmony'].append(self.metrics.breath_harmony)
        self.history['foresight'].append(self.metrics.foresight_strain)
        
        # Update sublattice history
        for domain, sublattice in self.sublattices.items():
            self.history['sublattices'][domain.value].append({
                'breath': sublattice.breath_alignment,
                'entanglement': sublattice.entanglement_load,
                'foresight': sublattice.foresight_pulse,
                'crystal': sublattice.crystal_density,
                'strain': sublattice.strain_level,
                'harmony': sublattice.harmony_score,
                'emergence': sublattice.emergence_potential
            })
            
        # Update bridge history
        self.history['bridges'].append({
            'harmonic': {
                domain.value: list(bridges)
                for domain, bridges in self.harmonic_bridges.items()
            },
            'strain': {
                domain.value: list(conduits)
                for domain, conduits in self.strain_conduits.items()
            }
        })
        
        # Trim history if needed
        for key in self.history:
            if isinstance(self.history[key], list):
                if len(self.history[key]) > self.max_history:
                    self.history[key].pop(0)
            elif isinstance(self.history[key], dict):
                for subkey in self.history[key]:
                    if len(self.history[key][subkey]) > self.max_history:
                        self.history[key][subkey].pop(0)
                        
    def _record_lattice(self) -> None:
        """Record lattice change event."""
        self.history['crystals'].append({
            'mode': self.mode.value,
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'breath': self.metrics.breath_alignment,
                'recursion': self.metrics.recursion_depth,
                'domains': self.metrics.domain_activity,
                'harmony': self.metrics.breath_harmony,
                'foresight': self.metrics.foresight_strain,
                'anomaly': self.metrics.anomaly_detected,
                'lattice_harmony': self.metrics.lattice_harmony,
                'divergence_risk': self.metrics.divergence_risk
            },
            'sublattices': {
                domain.value: {
                    'breath': sublattice.breath_alignment,
                    'entanglement': sublattice.entanglement_load,
                    'foresight': sublattice.foresight_pulse,
                    'crystal': sublattice.crystal_density,
                    'strain': sublattice.strain_level,
                    'harmony': sublattice.harmony_score,
                    'emergence': sublattice.emergence_potential
                }
                for domain, sublattice in self.sublattices.items()
            }
        })
        
        # Trim crystal history if needed
        if len(self.history['crystals']) > self.max_history:
            self.history['crystals'].pop(0)
            
    def _update_feedback(self) -> None:
        """Update feedback state based on lattice metrics."""
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
        
        # Adjust feedback based on mode and harmony
        if self.mode == LatticeMode.STRAINED:
            feedback_adjustments['strain_heatmap'] *= 1.5
            feedback_adjustments['veil_entanglement'] *= 1.5
        elif self.mode == LatticeMode.CRYSTALLIZING:
            feedback_adjustments['resonance_flow'] *= 1.5
            feedback_adjustments['breath_signature'] *= 1.5
        elif self.mode == LatticeMode.RESONANT:
            feedback_adjustments['judgment_radar'] *= 1.5
            feedback_adjustments['codex_phase'] *= 1.5
        elif self.mode == LatticeMode.SHIELD:
            feedback_adjustments['veil_entanglement'] *= 2.0
            feedback_adjustments['ghost_movement'] *= 0.5
        elif self.mode == LatticeMode.FRACTURE:
            feedback_adjustments['strain_heatmap'] *= 2.0
            feedback_adjustments['entropic_drift'] *= 2.0
        elif self.mode == LatticeMode.EMERGING:
            feedback_adjustments['resonance_flow'] *= 1.8
            feedback_adjustments['breath_signature'] *= 1.8
        elif self.mode == LatticeMode.HARMONIC:
            feedback_adjustments['judgment_radar'] *= 1.8
            feedback_adjustments['codex_phase'] *= 1.8
        elif self.mode == LatticeMode.DIVERGENT:
            feedback_adjustments['strain_heatmap'] *= 1.8
            feedback_adjustments['veil_entanglement'] *= 1.8
            
        # Apply harmony-based scaling
        harmony_scale = 1.0 + (self.metrics.lattice_harmony * 0.5)
        for key in feedback_adjustments:
            feedback_adjustments[key] *= harmony_scale
            
        # Apply adjustments to feedback
        self.feedback.metrics.focus_weight = np.mean(list(feedback_adjustments.values()))
        
    def get_lattice_state(self) -> Dict[str, Any]:
        """Get current lattice state."""
        return {
            'mode': self.mode.value,
            'metrics': self.metrics.__dict__,
            'sublattices': {
                domain.value: sublattice.__dict__
                for domain, sublattice in self.sublattices.items()
            },
            'bridges': {
                'harmonic': {
                    domain.value: list(bridges)
                    for domain, bridges in self.harmonic_bridges.items()
                },
                'strain': {
                    domain.value: list(conduits)
                    for domain, conduits in self.strain_conduits.items()
                }
            },
            'history_lengths': {
                key: len(data) if isinstance(data, list) else {
                    subkey: len(subdata)
                    for subkey, subdata in data.items()
                }
                for key, data in self.history.items()
            },
            'mode_switches': self.metrics.mode_switches,
            'smoothing': {
                'breath': list(self.breath_window),
                'strain': list(self.strain_window),
                'harmony': list(self.harmony_window),
                'emergence': list(self.emergence_window)
            }
        }
        
    def save_lattice_state(self, filename: str) -> None:
        """Save current lattice state to file."""
        state = self.get_lattice_state()
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
            
    def close(self) -> None:
        """Close lattice map and clean up resources."""
        self.feedback.close()
        self.mirror_feedback.close()
        self.quantum_protection.close() 