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

from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
import time
import hashlib

@dataclass
class GlyphState:
    """Represents the state of a cryptographic glyph."""
    symbol: str
    resonance: float = 0.0
    echo_count: int = 0
    last_resolved: float = 0.0
    anchor_state: Optional[str] = None
    
class Cryptographer:
    """Handles symbolic interpretation and glyph resolution for Cursor."""
    
    def __init__(self):
        self.glyph_index: Dict[str, GlyphState] = {}
        self.echo_memory: List[Tuple[str, float]] = []
        self.resolution_cache: Dict[str, str] = {}
        self.last_sweep: float = 0.0
        
    def resolve_anchor(self, kernel_id: str) -> Optional[str]:
        """Resolve the anchor state for a kernel using cryptographic methods."""
        # Check cache first
        if kernel_id in self.resolution_cache:
            return self.resolution_cache[kernel_id]
            
        # Generate glyph for kernel
        glyph = self._generate_glyph(kernel_id)
        
        # Check if glyph exists in index
        if glyph in self.glyph_index:
            state = self.glyph_index[glyph]
            state.last_resolved = time.time()
            state.echo_count += 1
            return state.anchor_state
            
        # Create new glyph state
        state = GlyphState(
            symbol=glyph,
            resonance=0.0,
            echo_count=0,
            last_resolved=time.time()
        )
        
        # Determine anchor state based on glyph properties
        anchor_state = self._determine_anchor_state(glyph)
        state.anchor_state = anchor_state
        
        # Cache and store
        self.glyph_index[glyph] = state
        self.resolution_cache[kernel_id] = anchor_state
        
        return anchor_state
        
    def _generate_glyph(self, kernel_id: str) -> str:
        """Generate a cryptographic glyph for a kernel."""
        # Use SHA-256 for deterministic glyph generation
        hash_obj = hashlib.sha256(kernel_id.encode())
        return hash_obj.hexdigest()[:16]  # Use first 16 chars as glyph
        
    def _determine_anchor_state(self, glyph: str) -> str:
        """Determine appropriate anchor state based on glyph properties."""
        # Simple heuristic based on glyph properties
        if glyph.startswith('0'):
            return "breath_origin"
        elif glyph.startswith('1'):
            return "dredd_anchor"
        elif glyph.startswith('2'):
            return "telos_anchor"
        elif glyph.startswith('3'):
            return "entropy_modulator"
        elif glyph.startswith('4'):
            return "coherence_anchor"
        else:
            return "recursive_node"
            
    def sweep_echoes(self):
        """Sweep and clean old echoes."""
        current_time = time.time()
        if current_time - self.last_sweep < 60:  # Sweep every minute
            return
            
        # Remove old echoes
        self.echo_memory = [
            (echo, timestamp) for echo, timestamp in self.echo_memory
            if current_time - timestamp < 300  # Keep last 5 minutes
        ]
        
        # Update resonance based on echo density
        for glyph, state in self.glyph_index.items():
            recent_echoes = sum(1 for _, ts in self.echo_memory 
                              if current_time - ts < 60)
            state.resonance = min(1.0, recent_echoes / 10.0)
            
        self.last_sweep = current_time
        
    def get_glyph_state(self, glyph: str) -> Optional[GlyphState]:
        """Get the current state of a glyph."""
        return self.glyph_index.get(glyph)
        
    def record_echo(self, glyph: str):
        """Record an echo for a glyph."""
        self.echo_memory.append((glyph, time.time()))
        if glyph in self.glyph_index:
            self.glyph_index[glyph].echo_count += 1 