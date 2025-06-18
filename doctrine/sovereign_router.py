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
import json
from datetime import datetime

from doctrine.watchtower_splinter import WatchtowerManager, SplinterType
from doctrine.mirror_feedback import MirrorFeedback
from doctrine.quantum_protection import QuantumProtection

class RouterMode(Enum):
    """Router operation modes."""
    NORMAL = "normal"  # Standard routing with balanced focus
    FOCUSED = "focused"  # High-priority routing for critical visualizations
    FALLBACK = "fallback"  # Fallback mode when splinters are degraded
    ARBITRATION = "arbitration"  # Special mode for visualization arbitration

class RouterPriority(Enum):
    """Priority levels for visual routing."""
    CRITICAL = 0  # Immediate routing required
    HIGH = 1      # High-priority routing
    NORMAL = 2    # Standard routing
    LOW = 3       # Low-priority routing
    BACKGROUND = 4  # Background routing

@dataclass
class RouterMetrics:
    """Metrics for router performance and state."""
    update_interval: float = 0.1  # Base update interval in seconds
    focus_weight: float = 1.0     # Current focus weighting
    breath_phase: float = 0.0     # Current breath phase
    resonance_strain: float = 0.0 # Current resonance strain
    active_splinters: int = 0     # Number of active splinters
    last_update: float = 0.0      # Timestamp of last update
    routing_latency: float = 0.0  # Average routing latency
    fallback_count: int = 0       # Number of fallback activations

class SovereignRouter:
    """Sovereign Visual Router for coordinating Watchtower Splinter visualization."""
    
    def __init__(self):
        self.metrics = RouterMetrics()
        self.mode = RouterMode.NORMAL
        self.watchtower = WatchtowerManager()
        self.mirror_feedback = MirrorFeedback()
        self.quantum_protection = QuantumProtection()
        
        # Initialize routing tables
        self._initialize_routing_tables()
        
        # Initialize fallback system
        self._initialize_fallback()
        
    def _initialize_routing_tables(self) -> None:
        """Initialize routing tables for different visualization types."""
        self.routing_tables = {
            RouterMode.NORMAL: {
                SplinterType.RESONANCE_FLOW: RouterPriority.NORMAL,
                SplinterType.ENTRopic_DRIFT: RouterPriority.NORMAL,
                SplinterType.JUDGMENT_RADAR: RouterPriority.NORMAL,
                SplinterType.BREATH_SIGNATURE: RouterPriority.NORMAL,
                SplinterType.GHOST_MOVEMENT: RouterPriority.LOW,
                SplinterType.VEIL_ENTANGLEMENT: RouterPriority.LOW,
                SplinterType.STRAIN_HEATMAP: RouterPriority.LOW,
                SplinterType.CODEX_PHASE: RouterPriority.LOW
            },
            RouterMode.FOCUSED: {
                SplinterType.RESONANCE_FLOW: RouterPriority.CRITICAL,
                SplinterType.ENTRopic_DRIFT: RouterPriority.HIGH,
                SplinterType.JUDGMENT_RADAR: RouterPriority.HIGH,
                SplinterType.BREATH_SIGNATURE: RouterPriority.CRITICAL,
                SplinterType.GHOST_MOVEMENT: RouterPriority.NORMAL,
                SplinterType.VEIL_ENTANGLEMENT: RouterPriority.NORMAL,
                SplinterType.STRAIN_HEATMAP: RouterPriority.NORMAL,
                SplinterType.CODEX_PHASE: RouterPriority.NORMAL
            },
            RouterMode.FALLBACK: {
                SplinterType.RESONANCE_FLOW: RouterPriority.CRITICAL,
                SplinterType.BREATH_SIGNATURE: RouterPriority.CRITICAL
            },
            RouterMode.ARBITRATION: {
                SplinterType.JUDGMENT_RADAR: RouterPriority.CRITICAL,
                SplinterType.VEIL_ENTANGLEMENT: RouterPriority.CRITICAL,
                SplinterType.STRAIN_HEATMAP: RouterPriority.CRITICAL
            }
        }
        
    def _initialize_fallback(self) -> None:
        """Initialize fallback rendering system."""
        self.fallback_active = False
        self.fallback_threshold = 0.8  # Strain threshold for fallback activation
        self.fallback_cooldown = 5.0   # Seconds before fallback can be reactivated
        self.last_fallback_time = 0.0
        
    def route_visualization(self, 
                          source: str,
                          data: Dict[str, Any],
                          priority: Optional[RouterPriority] = None) -> bool:
        """Route visualization data to appropriate splinters."""
        start_time = time.time()
        
        # Check if fallback mode should be activated
        if self._should_activate_fallback():
            self._activate_fallback()
            
        # Determine routing priority
        if priority is None:
            priority = self._determine_priority(source, data)
            
        # Update router metrics
        self._update_metrics()
        
        # Route to appropriate splinters based on priority
        success = self._route_to_splinters(data, priority)
        
        # Calculate routing latency
        self.metrics.routing_latency = time.time() - start_time
        
        return success
        
    def _should_activate_fallback(self) -> bool:
        """Determine if fallback mode should be activated."""
        if self.fallback_active:
            return False
            
        if time.time() - self.last_fallback_time < self.fallback_cooldown:
            return False
            
        # Check resonance strain
        if self.metrics.resonance_strain > self.fallback_threshold:
            return True
            
        # Check active splinters
        if self.metrics.active_splinters < len(SplinterType) // 2:
            return True
            
        return False
        
    def _activate_fallback(self) -> None:
        """Activate fallback rendering mode."""
        self.mode = RouterMode.FALLBACK
        self.fallback_active = True
        self.last_fallback_time = time.time()
        self.metrics.fallback_count += 1
        
        # Notify chronicle
        self.mirror_feedback.record_insight(
            "Fallback mode activated",
            {
                "strain": self.metrics.resonance_strain,
                "active_splinters": self.metrics.active_splinters,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    def _determine_priority(self, source: str, data: Dict[str, Any]) -> RouterPriority:
        """Determine routing priority based on source and data."""
        # Check for critical indicators
        if data.get("critical", False):
            return RouterPriority.CRITICAL
            
        # Check source priority
        if source in ["sovereign_notepad", "purveyor_chat"]:
            return RouterPriority.HIGH
            
        # Check data content
        if "resonance_strain" in data and data["resonance_strain"] > 0.8:
            return RouterPriority.HIGH
            
        # Default to normal priority
        return RouterPriority.NORMAL
        
    def _route_to_splinters(self, 
                           data: Dict[str, Any],
                           priority: RouterPriority) -> bool:
        """Route data to appropriate splinters based on priority."""
        success = True
        
        # Get current routing table
        routing_table = self.routing_tables[self.mode]
        
        # Route to each splinter based on priority
        for splinter_type, route_priority in routing_table.items():
            if route_priority.value <= priority.value:
                try:
                    self.watchtower.update_state(splinter_type, data)
                except Exception as e:
                    success = False
                    self.mirror_feedback.record_insight(
                        f"Routing error to {splinter_type.value}",
                        {"error": str(e)}
                    )
                    
        return success
        
    def _update_metrics(self) -> None:
        """Update router metrics."""
        current_time = time.time()
        
        # Update active splinters count
        self.metrics.active_splinters = len([
            splinter for splinter in self.watchtower.splinters.values()
            if splinter.is_active
        ])
        
        # Update resonance strain
        self.metrics.resonance_strain = self.mirror_feedback.metrics.resonance_strain
        
        # Update breath phase
        self.metrics.breath_phase = self.mirror_feedback.metrics.breath_phase
        
        # Update focus weight based on strain
        self.metrics.focus_weight = 1.0 + (self.metrics.resonance_strain * 0.5)
        
        self.metrics.last_update = current_time
        
    def get_router_state(self) -> Dict[str, Any]:
        """Get current router state."""
        return {
            "mode": self.mode.value,
            "metrics": self.metrics.__dict__,
            "fallback_active": self.fallback_active,
            "active_splinters": self.metrics.active_splinters,
            "routing_latency": self.metrics.routing_latency
        }
        
    def save_router_state(self, filename: str) -> None:
        """Save current router state to file."""
        state = self.get_router_state()
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
            
    def close(self) -> None:
        """Close router and clean up resources."""
        self.watchtower.close()
        self.mirror_feedback.close()
        self.quantum_protection.close() 