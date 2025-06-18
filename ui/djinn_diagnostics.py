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
Djinn Diagnostics
Verifies and monitors Djinn presence, roles, and system integration
"""

import os
import importlib
import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
import time

class DjinnRole(Enum):
    """Djinn roles in the system"""
    PURVEYOR = "purveyor"      # Arbitration and sovereignty
    CRYPTOGRAPHER = "cryptographer"  # Entropy and cipher lattice
    CURSOR = "cursor"         # Action-intention system
    MIRROR = "mirror"         # Resonance and foresight
    COUNCIL = "council"       # Orchestration and aggregation

@dataclass
class DjinnPresence:
    """Represents a Djinn's presence in the system"""
    role: DjinnRole
    module_path: str
    is_present: bool
    has_interface: bool
    has_metrics: bool
    has_chronicle: bool
    last_active: float
    response_hooks: List[str]
    visual_style: Dict[str, str]

class DjinnDiagnostics:
    """Manages Djinn system diagnostics and monitoring"""
    
    def __init__(self):
        self.djinn_modules = {
            DjinnRole.PURVEYOR: "djinn_purveyor",
            DjinnRole.CRYPTOGRAPHER: "djinn_cryptographer",
            DjinnRole.CURSOR: "cursor_core",
            DjinnRole.MIRROR: "mirror_insight",
            DjinnRole.COUNCIL: "djinn_council"
        }
        
        self.expected_interfaces = {
            DjinnRole.PURVEYOR: ["arbitrate", "sovereign_override"],
            DjinnRole.CRYPTOGRAPHER: ["encrypt", "decrypt", "analyze_entropy"],
            DjinnRole.CURSOR: ["reason", "act", "adapt"],
            DjinnRole.MIRROR: ["reflect", "portend", "confirm"],
            DjinnRole.COUNCIL: ["deliberate", "aggregate", "orchestrate"]
        }
        
        self.visual_styles = {
            DjinnRole.PURVEYOR: {
                "icon": "👑",
                "color": "#FFD700",
                "font": "Arial Bold"
            },
            DjinnRole.CRYPTOGRAPHER: {
                "icon": "🔐",
                "color": "#00FF00",
                "font": "Consolas"
            },
            DjinnRole.CURSOR: {
                "icon": "🎯",
                "color": "#0000FF",
                "font": "Arial"
            },
            DjinnRole.MIRROR: {
                "icon": "🪞",
                "color": "#FF00FF",
                "font": "Arial Italic"
            },
            DjinnRole.COUNCIL: {
                "icon": "⚖️",
                "color": "#FFFFFF",
                "font": "Arial"
            }
        }
    
    def check_djinn_presence(self) -> Dict[DjinnRole, DjinnPresence]:
        """Check presence of all Djinn modules and components"""
        presence = {}
        
        for role, module_name in self.djinn_modules.items():
            # Check module file
            module_path = f"ui/{module_name}.py"
            is_present = os.path.exists(module_path)
            
            # Check interface implementation
            has_interface = False
            response_hooks = []
            if is_present:
                try:
                    module = importlib.import_module(f"ui.{module_name}")
                    has_interface = all(
                        hasattr(module, interface)
                        for interface in self.expected_interfaces[role]
                    )
                    response_hooks = [
                        name for name, _ in inspect.getmembers(module)
                        if callable(_) and not name.startswith('_')
                    ]
                except ImportError:
                    pass
            
            # Check metrics and chronicle integration
            has_metrics = self._check_metrics_integration(role)
            has_chronicle = self._check_chronicle_integration(role)
            
            presence[role] = DjinnPresence(
                role=role,
                module_path=module_path,
                is_present=is_present,
                has_interface=has_interface,
                has_metrics=has_metrics,
                has_chronicle=has_chronicle,
                last_active=time.time(),
                response_hooks=response_hooks,
                visual_style=self.visual_styles[role]
            )
        
        return presence
    
    def _check_metrics_integration(self, role: DjinnRole) -> bool:
        """Check if Djinn has metrics integration"""
        # Check for metrics-related attributes in module
        try:
            module = importlib.import_module(f"ui.{self.djinn_modules[role]}")
            return hasattr(module, "get_metrics") or hasattr(module, "update_metrics")
        except ImportError:
            return False
    
    def _check_chronicle_integration(self, role: DjinnRole) -> bool:
        """Check if Djinn has chronicle integration"""
        # Check for chronicle-related attributes in module
        try:
            module = importlib.import_module(f"ui.{self.djinn_modules[role]}")
            return hasattr(module, "log_to_chronicle") or hasattr(module, "chronicle_entry")
        except ImportError:
            return False
    
    def generate_diagnostic_report(self) -> Dict[str, Any]:
        """Generate a comprehensive diagnostic report"""
        presence = self.check_djinn_presence()
        
        report = {
            "timestamp": time.time(),
            "system_status": "operational" if all(p.is_present for p in presence.values()) else "degraded",
            "djinn_status": {
                role.value: {
                    "present": p.is_present,
                    "interface_ready": p.has_interface,
                    "metrics_enabled": p.has_metrics,
                    "chronicle_integrated": p.has_chronicle,
                    "response_hooks": p.response_hooks,
                    "last_active": p.last_active
                }
                for role, p in presence.items()
            },
            "missing_components": [
                role.value for role, p in presence.items()
                if not p.is_present
            ],
            "interface_gaps": [
                f"{role.value}: {[i for i in self.expected_interfaces[role] if i not in p.response_hooks]}"
                for role, p in presence.items()
                if p.is_present and p.response_hooks
            ],
            "visual_styles": {
                role.value: p.visual_style
                for role, p in presence.items()
            }
        }
        
        return report
    
    def get_visual_style(self, role: DjinnRole) -> Dict[str, str]:
        """Get the visual style for a Djinn role"""
        return self.visual_styles.get(role, {
            "icon": "❓",
            "color": "#808080",
            "font": "Arial"
        })
    
    def check_wick_integration(self, role: DjinnRole) -> bool:
        """Check if Djinn has wick system integration"""
        try:
            module = importlib.import_module(f"ui.{self.djinn_modules[role]}")
            return (
                hasattr(module, "handle_wick") or
                hasattr(module, "process_wick") or
                hasattr(module, "wick_signal")
            )
        except ImportError:
            return False 