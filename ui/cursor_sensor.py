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
from typing import Dict, List, Optional, Tuple

class ScanPattern(Enum):
    """Types of scan patterns for lattice analysis."""
    FRACTAL_GRID = "fractal_grid"         # Grid-based scanning with fractal recursion
    SPIRAL_SWEEP = "spiral_sweep"         # Spiral pattern from center outward
    RESONANT_WAVE = "resonant_wave"       # Wave-like pattern with resonance
    QUANTUM_PULSE = "quantum_pulse"       # Quantum-entangled pulse scanning

class ScanIntent(Enum):
    """Intentions behind lattice scanning."""
    EXPLORATION = "exploration"           # General exploration of lattice
    DIAGNOSTIC = "diagnostic"             # Diagnostic scanning for issues
    RECOVERY = "recovery"                 # Recovery scanning after breach
    ENHANCEMENT = "enhancement"           # Enhancement scanning for optimization
    PROTECTION = "protection"             # Protection scanning for security

@dataclass
class ScanMetrics:
    """Metrics for a lattice scan."""
    depth: float = 0.0                    # Scan depth (0.0 to 5.0)
    coverage: float = 0.0                 # Coverage percentage (0.0 to 1.0)
    anchor_load: Dict[str, float] = None  # Load on each anchor point
    resonance: float = 1.0                # Resonance level (0.0 to 1.0)
    coherence: float = 1.0                # Coherence level (0.0 to 1.0)
    strain: float = 0.0                   # Strain level (0.0 to 1.0)
    portent_warnings: List[str] = None    # List of warning messages

    def __post_init__(self):
        if self.anchor_load is None:
            self.anchor_load = {}
        if self.portent_warnings is None:
            self.portent_warnings = []

@dataclass
class LatticeScan:
    """Represents a scan of the lattice."""
    pattern: ScanPattern
    intent: ScanIntent
    metrics: ScanMetrics
    timestamp: float = 0.0
    position: Tuple[float, float] = (0.0, 0.0)
    rotation: float = 0.0
    scale: float = 1.0
    resonance: float = 1.0
    coherence: float = 1.0
    strain: float = 0.0
    portent_warnings: List[str] = None

    def __post_init__(self):
        if self.portent_warnings is None:
            self.portent_warnings = [] 