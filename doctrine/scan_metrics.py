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
Ephemeral Editioning Sequencer System for Scan Metrics.
This module provides the foundation for fluid, musical interaction
while maintaining autonomous encapsulation of scan processes.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class ScanMetrics:
    """
    Ephemeral metrics for scanning and sequencing, designed to echo
    the fluid nature of musical interaction while maintaining
    autonomous encapsulation.
    """
    sequence_id: str
    timestamp: datetime
    resonance_level: float = 0.0
    harmonic_frequency: float = 0.0
    echo_pattern: List[float] = None
    edition_number: int = 1
    
    def __post_init__(self):
        """Initialize mutable defaults"""
        if self.echo_pattern is None:
            self.echo_pattern = []
    
    def update_resonance(self, new_level: float) -> None:
        """
        Update the resonance level, reflecting the current
        state of musical interaction.
        """
        self.resonance_level = new_level
        self.timestamp = datetime.now()
    
    def add_harmonic(self, frequency: float) -> None:
        """
        Add a new harmonic frequency to the sequence,
        maintaining the fluid nature of the interaction.
        """
        self.harmonic_frequency = frequency
        self.echo_pattern.append(frequency)
    
    def increment_edition(self) -> None:
        """
        Increment the edition number, marking a new
        phase in the ephemeral sequence.
        """
        self.edition_number += 1
        self.timestamp = datetime.now()

# Example utility for creating a new scan sequence
def create_scan_sequence(sequence_id: str) -> ScanMetrics:
    """
    Create a new scan sequence with initial metrics,
    ready for musical interaction.
    """
    return ScanMetrics(
        sequence_id=sequence_id,
        timestamp=datetime.now(),
        resonance_level=0.0,
        harmonic_frequency=0.0,
        echo_pattern=[],
        edition_number=1
    ) 