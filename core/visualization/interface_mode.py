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

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from .high_symbology_mode import HighSymbologyMode, SymbolicState

class InterfaceMode(Enum):
    """Defines the available interface modes."""
    LINEAR = "linear"      # Clear, functional representation
    RITUAL = "ritual"      # Symbolic, resonant representation
    HIGH_SYMBOL = "high_symbol"  # Deep symbolic resonance

@dataclass
class NodeMapping:
    """Maps between interface representations of nodes."""
    linear_id: str
    ritual_id: str
    function: str
    sigil: str
    description: str
    parameters: Dict[str, Any]
    symbolic_element: str  # Reference to HSM element

@dataclass
class EdgeMapping:
    """Maps between interface representations of connections."""
    linear_type: str
    ritual_type: str
    description: str
    visual_style: Dict[str, Any]
    symbolic_style: Dict[str, Any]  # HSM-specific style

class InterfaceController:
    """Manages the multi-model interface system."""
    
    def __init__(self):
        self.current_mode = InterfaceMode.LINEAR
        self.node_mappings: Dict[str, NodeMapping] = {}
        self.edge_mappings: Dict[str, EdgeMapping] = {}
        self.transparency_level = 1.0  # 0.0 to 1.0
        self.hsm = HighSymbologyMode()
        
        # Initialize default mappings
        self._initialize_mappings()
        
    def _initialize_mappings(self):
        """Initialize the default node and edge mappings."""
        # Node mappings
        self.node_mappings = {
            "perception": NodeMapping(
                linear_id="perception",
                ritual_id="sigil_01",
                function="Input Processing",
                sigil="👁️",
                description="Processes and interprets input data",
                parameters={
                    "sensitivity": 0.8,
                    "filter_strength": 0.5
                },
                symbolic_element="perception"
            ),
            "reasoning": NodeMapping(
                linear_id="reasoning",
                ritual_id="sigil_02",
                function="Logical Processing",
                sigil="⚡",
                description="Performs logical operations and decision making",
                parameters={
                    "depth": 3,
                    "confidence_threshold": 0.7
                },
                symbolic_element="reasoning"
            ),
            "memory": NodeMapping(
                linear_id="memory",
                ritual_id="sigil_03",
                function="State Storage",
                sigil="💾",
                description="Stores and retrieves system state",
                parameters={
                    "capacity": 1000,
                    "retention_rate": 0.9
                },
                symbolic_element="memory"
            ),
            "action": NodeMapping(
                linear_id="action",
                ritual_id="sigil_04",
                function="Output Generation",
                sigil="🎯",
                description="Generates system outputs and actions",
                parameters={
                    "precision": 0.8,
                    "response_time": 0.1
                },
                symbolic_element="action"
            )
        }
        
        # Edge mappings
        self.edge_mappings = {
            "data": EdgeMapping(
                linear_type="data",
                ritual_type="resonance",
                description="Data flow between nodes",
                visual_style={
                    "color": (100, 150, 255),
                    "width": 2,
                    "animation": "flow"
                },
                symbolic_style={
                    "motion": "flow",
                    "sound": "wind",
                    "resonance": 0.8
                }
            ),
            "control": EdgeMapping(
                linear_type="control",
                ritual_type="harmony",
                description="Control signal transmission",
                visual_style={
                    "color": (150, 255, 150),
                    "width": 2,
                    "animation": "pulse"
                },
                symbolic_style={
                    "motion": "pulse",
                    "sound": "crystal",
                    "resonance": 0.6
                }
            ),
            "mutation": EdgeMapping(
                linear_type="mutation",
                ritual_type="evolution",
                description="System adaptation and change",
                visual_style={
                    "color": (255, 100, 150),
                    "width": 2,
                    "animation": "spark"
                },
                symbolic_style={
                    "motion": "burst",
                    "sound": "thunder",
                    "resonance": 1.0
                }
            )
        }
    
    def toggle_mode(self):
        """Toggle between linear and ritual modes."""
        self.current_mode = (InterfaceMode.RITUAL 
                           if self.current_mode == InterfaceMode.LINEAR 
                           else InterfaceMode.LINEAR)
        return self.current_mode
    
    def get_node_representation(self, node_id: str) -> Dict[str, Any]:
        """Get the current representation of a node based on mode."""
        mapping = self.node_mappings.get(node_id)
        if not mapping:
            return {"id": node_id, "type": "unknown"}
            
        if self.current_mode == InterfaceMode.LINEAR:
            return {
                "id": mapping.linear_id,
                "type": "module",
                "function": mapping.function,
                "description": mapping.description,
                "parameters": mapping.parameters
            }
        else:  # RITUAL mode
            return {
                "id": mapping.ritual_id,
                "type": "sigil",
                "symbol": mapping.sigil,
                "description": mapping.description,
                "resonance": 0.0  # Will be updated by the visualization
            }
    
    def get_edge_representation(self, edge_type: str) -> Dict[str, Any]:
        """Get the current representation of an edge based on mode."""
        mapping = self.edge_mappings.get(edge_type)
        if not mapping:
            return {"type": edge_type}
            
        if self.current_mode == InterfaceMode.LINEAR:
            return {
                "type": mapping.linear_type,
                "description": mapping.description,
                "style": {
                    "color": mapping.visual_style["color"],
                    "width": mapping.visual_style["width"]
                }
            }
        else:  # RITUAL mode
            return {
                "type": mapping.ritual_type,
                "description": mapping.description,
                "style": mapping.visual_style
            }
    
    def get_transparency_info(self, element_id: str) -> Dict[str, Any]:
        """Get transparency information for an element."""
        if self.current_mode == InterfaceMode.LINEAR:
            return {}  # No additional info needed in linear mode
            
        # Find the mapping
        mapping = None
        for node_map in self.node_mappings.values():
            if node_map.ritual_id == element_id:
                mapping = node_map
                break
                
        if not mapping:
            return {}
            
        return {
            "linear_id": mapping.linear_id,
            "function": mapping.function,
            "parameters": mapping.parameters,
            "description": mapping.description
        }
    
    def set_transparency_level(self, level: float):
        """Set the transparency level for ritual mode."""
        self.transparency_level = max(0.0, min(1.0, level))
        
    def get_mode_info(self) -> Dict[str, Any]:
        """Get information about the current mode."""
        return {
            "mode": self.current_mode.value,
            "transparency": self.transparency_level,
            "node_count": len(self.node_mappings),
            "edge_types": list(self.edge_mappings.keys())
        } 