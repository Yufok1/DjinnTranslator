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
from typing import Dict, List, Set, Optional, Tuple
import math
import colorsys

@dataclass
class LatticeNode:
    """Represents a node in the EAIN lattice."""
    id: str
    type: str  # 'module', 'prompt', 'interface', 'mutation'
    position: Tuple[float, float]
    radius: float
    resonance: float
    connections: Set[str]
    metadata: Dict[str, any]
    breath_phase: str
    telos_vector: float
    mutation_path: List[str]
    # New fields for enhanced recursion
    fixpoints: List[Tuple[float, float]]  # Multiple fixpoints for lattice-based recursion
    recursion_depth: int  # Current recursion depth (4-8x)
    recursion_branches: List[str]  # IDs of recursive branches
    coherence_field: Dict[str, float]  # Local coherence metrics
    entropy_buffer: float  # Local entropy management
    resonance_halos: List[Tuple[float, float]]  # Resonance field points

@dataclass
class LatticeEdge:
    """Represents a connection between lattice nodes."""
    source_id: str
    target_id: str
    strength: float
    type: str  # 'data', 'control', 'mutation', 'resonance'
    breath_sync: float
    mutation_history: List[Tuple[float, str]]
    # New fields for enhanced recursion
    recursion_paths: List[List[str]]  # Multiple recursive paths
    coherence_metrics: Dict[str, float]  # Edge coherence data
    entropy_flow: float  # Entropy transfer rate
    resonance_coupling: float  # Resonance coupling strength

class LatticeMap:
    """Visualizes the EAIN architecture as a living, breathing lattice."""
    
    def __init__(self):
        self.nodes: Dict[str, LatticeNode] = {}
        self.edges: List[LatticeEdge] = []
        self.breath_engine = {
            'phase': 'STILL',
            'cycle': 0,
            'amplitude': 1.0,
            'frequency': 1.0
        }
        self.mutation_field = {
            'entropy': 0.0,
            'stability': 1.0,
            'adaptation_rate': 0.1
        }
        # New fields for enhanced recursion
        self.recursion_config = {
            'magnitude': 4,  # Base recursion magnitude (4-8x)
            'fixpoint_count': 3,  # Number of fixpoints per node
            'coherence_threshold': 0.7,  # Minimum coherence for stability
            'entropy_dampening': 0.8,  # Entropy control factor
            'resonance_coupling': 0.6  # Resonance coupling strength
        }
        self.coherence_mesh = {}  # Global coherence tracking
        self.entropy_controllers = {}  # Entropy management per node
        self.resonance_fields = {}  # Resonance field tracking
        
    def add_module_node(self, module_id: str, position: Tuple[float, float], 
                       module_type: str, resonance: float = 1.0):
        """Add a module node to the lattice with enhanced recursion support."""
        # Generate fixpoints around the main position
        fixpoints = []
        for i in range(self.recursion_config['fixpoint_count']):
            angle = (2 * math.pi * i) / self.recursion_config['fixpoint_count']
            radius = 0.1  # Fixpoint distance from center
            fixpoint_x = position[0] + radius * math.cos(angle)
            fixpoint_y = position[1] + radius * math.sin(angle)
            fixpoints.append((fixpoint_x, fixpoint_y))

        self.nodes[module_id] = LatticeNode(
            id=module_id,
            type='module',
            position=position,
            radius=20.0,
            resonance=resonance,
            connections=set(),
            metadata={
                'module_type': module_type,
                'evolution_stage': 0,
                'mutation_count': 0,
                'fitness_score': 0.0
            },
            breath_phase='STILL',
            telos_vector=0.0,
            mutation_path=[],
            fixpoints=fixpoints,
            recursion_depth=0,
            recursion_branches=[],
            coherence_field={
                'local': 1.0,
                'global': 1.0,
                'resonance': 1.0
            },
            entropy_buffer=0.0,
            resonance_halos=[]
        )
        
        # Initialize entropy controller
        self.entropy_controllers[module_id] = {
            'dampening': self.recursion_config['entropy_dampening'],
            'threshold': 0.8,
            'recovery_rate': 0.1
        }
        
        # Initialize resonance field
        self.resonance_fields[module_id] = {
            'strength': resonance,
            'coupling': self.recursion_config['resonance_coupling'],
            'halos': []
        }
    
    def add_prompt_node(self, prompt_id: str, position: Tuple[float, float],
                       prompt_type: str, telos_vector: float):
        """Add a prompt node to the lattice."""
        self.nodes[prompt_id] = LatticeNode(
            id=prompt_id,
            type='prompt',
            position=position,
            radius=15.0,
            resonance=1.0,
            connections=set(),
            metadata={
                'prompt_type': prompt_type,  # 'seed', 'environmental', 'selection', 'intervention'
                'mutation_history': [],
                'effectiveness': 0.0,
                'adaptation_rate': 0.1
            },
            breath_phase='STILL',
            telos_vector=telos_vector,
            mutation_path=[]
        )
    
    def connect_nodes(self, source_id: str, target_id: str, 
                     connection_type: str, strength: float = 1.0):
        """Create a connection between nodes."""
        if source_id in self.nodes and target_id in self.nodes:
            self.nodes[source_id].connections.add(target_id)
            self.nodes[target_id].connections.add(source_id)
            
            self.edges.append(LatticeEdge(
                source_id=source_id,
                target_id=target_id,
                strength=strength,
                type=connection_type,
                breath_sync=0.0,
                mutation_history=[]
            ))
    
    def update_breath_cycle(self, delta_time: float):
        """Update the breath cycle of the lattice with enhanced recursion."""
        # Update breath phase
        self.breath_engine['cycle'] += delta_time * self.breath_engine['frequency']
        phase = (math.sin(self.breath_engine['cycle']) + 1) / 2
        
        # Update node resonances with enhanced recursion
        for node in self.nodes.values():
            # Update breath phase
            node.breath_phase = 'INHALE' if phase < 0.5 else 'EXHALE'
            
            # Update resonance with recursion depth
            recursion_factor = 1.0 + (node.recursion_depth * 0.1)
            node.resonance *= (0.95 + 0.05 * math.sin(self.breath_engine['cycle'])) * recursion_factor
            
            # Update fixpoints
            for i, fixpoint in enumerate(node.fixpoints):
                angle = (2 * math.pi * i) / len(node.fixpoints)
                radius = 0.1 * (1.0 + 0.2 * math.sin(self.breath_engine['cycle']))
                fixpoint_x = node.position[0] + radius * math.cos(angle)
                fixpoint_y = node.position[1] + radius * math.sin(angle)
                node.fixpoints[i] = (fixpoint_x, fixpoint_y)
            
            # Update coherence field
            self._update_coherence_field(node)
            
            # Update entropy buffer
            self._update_entropy_buffer(node)
            
            # Update resonance halos
            self._update_resonance_halos(node)
            
            # Update position based on breath and fixpoints
            x, y = node.position
            radius = 5.0 * math.sin(self.breath_engine['cycle'])
            angle = math.atan2(y, x)
            new_x = x + radius * math.cos(angle)
            new_y = y + radius * math.sin(angle)
            node.position = (new_x, new_y)
    
    def apply_mutation(self, node_id: str, mutation_type: str, 
                      strength: float = 0.1):
        """Apply a mutation to a node."""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.mutation_path.append(mutation_type)
            node.metadata['mutation_count'] += 1
            
            # Update resonance based on mutation
            node.resonance *= (1.0 + strength)
            
            # Update connected nodes
            for edge in self.edges:
                if edge.source_id == node_id or edge.target_id == node_id:
                    edge.mutation_history.append((self.breath_engine['cycle'], 
                                               mutation_type))
                    edge.strength *= (1.0 + strength * 0.5)
    
    def get_node_color(self, node: LatticeNode) -> Tuple[float, float, float]:
        """Get the color for a node based on its state."""
        # Base hue on node type
        if node.type == 'module':
            hue = 0.6  # Blue
        elif node.type == 'prompt':
            hue = 0.3  # Green
        else:
            hue = 0.0  # Red
            
        # Modulate saturation based on resonance
        saturation = 0.5 + 0.5 * node.resonance
        
        # Modulate value based on breath phase
        value = 0.7 + 0.3 * math.sin(self.breath_engine['cycle'])
        
        return colorsys.hsv_to_rgb(hue, saturation, value)
    
    def get_edge_color(self, edge: LatticeEdge) -> Tuple[float, float, float]:
        """Get the color for an edge based on its state."""
        # Base hue on connection type
        if edge.type == 'data':
            hue = 0.5  # Cyan
        elif edge.type == 'control':
            hue = 0.8  # Purple
        elif edge.type == 'mutation':
            hue = 0.1  # Yellow
        else:
            hue = 0.0  # Red
            
        # Modulate saturation based on strength
        saturation = 0.5 + 0.5 * edge.strength
        
        # Modulate value based on breath sync
        value = 0.7 + 0.3 * math.sin(edge.breath_sync)
        
        return colorsys.hsv_to_rgb(hue, saturation, value)
    
    def get_lattice_state(self) -> Dict[str, any]:
        """Get the current state of the lattice."""
        return {
            'node_count': len(self.nodes),
            'edge_count': len(self.edges),
            'breath_phase': self.breath_engine['phase'],
            'mutation_entropy': self.mutation_field['entropy'],
            'active_mutations': sum(1 for node in self.nodes.values() 
                                  if node.metadata['mutation_count'] > 0),
            'average_resonance': sum(node.resonance for node in self.nodes.values()) 
                               / len(self.nodes) if self.nodes else 0.0
        } 

    def _update_coherence_field(self, node: LatticeNode):
        """Update the coherence field for a node."""
        # Calculate local coherence
        local_coherence = 1.0
        for edge in self.edges:
            if edge.source_id == node.id or edge.target_id == node.id:
                local_coherence *= edge.coherence_metrics.get('local', 1.0)
        
        # Update node coherence field
        node.coherence_field['local'] = local_coherence
        node.coherence_field['global'] = self.coherence_mesh.get(node.id, 1.0)
        node.coherence_field['resonance'] = node.resonance

    def _update_entropy_buffer(self, node: LatticeNode):
        """Update the entropy buffer for a node."""
        controller = self.entropy_controllers[node.id]
        
        # Calculate entropy flow
        entropy_flow = 0.0
        for edge in self.edges:
            if edge.source_id == node.id or edge.target_id == node.id:
                entropy_flow += edge.entropy_flow
        
        # Update buffer with dampening
        node.entropy_buffer = (node.entropy_buffer * controller['dampening'] + 
                             entropy_flow * (1.0 - controller['dampening']))
        
        # Apply recovery if below threshold
        if node.entropy_buffer < controller['threshold']:
            node.entropy_buffer += controller['recovery_rate']

    def _update_resonance_halos(self, node: LatticeNode):
        """Update the resonance halos for a node."""
        field = self.resonance_fields[node.id]
        
        # Generate new halos based on resonance strength
        halos = []
        for i in range(3):  # Three layers of halos
            radius = node.radius * (1.5 + i * 0.5)
            strength = field['strength'] * (1.0 - i * 0.2)
            halos.append((radius, strength))
        
        node.resonance_halos = halos
        field['halos'] = halos 