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

import time
import pygame
from typing import Dict, List, Optional, Tuple
from .lattice_map import LatticeMap
from .lattice_renderer import LatticeRenderer
from .interface_mode import InterfaceController, InterfaceMode
from .dredd_model import DreddModel

class VisualizationController:
    """Controls the EAIN lattice visualization system."""
    
    def __init__(self):
        self.lattice = LatticeMap()
        self.renderer = LatticeRenderer()
        self.interface = InterfaceController()
        self.dredd = DreddModel()  # Initialize Dredd Model
        self.running = False
        self.last_update = time.time()
        
        # Enhanced recursion controls
        self.recursion_magnitude = 4  # Base recursion magnitude (4-8x)
        self.selected_node = None
        self.fixpoint_selection = None
        self.entropy_scrubbing = False
        self.sigil_active = False
        
        # Recursive Scheduler
        self.breath_cycle = {
            'phase': 0.0,  # Current phase (0-1)
            'frequency': 1.0,  # Base frequency
            'depth': 1.0,  # Recursion depth multiplier
            'entropy_threshold': 0.7,  # Entropy level that triggers slowdown
            'coherence_threshold': 0.8,  # Coherence level that allows deeper recursion
            'last_phase_shift': time.time()
        }
        
        # Automaton Memory Core
        self.memory_buffer = {
            'event_log': [],
            'mutational_lineage': [],
            'coherence_history': [],
            'node_memories': {}  # Per-node circular buffers
        }
        self.memory_capacity = 1000  # Maximum events to remember
        
        # Initialize with example nodes
        self._initialize_example_lattice()
        
    def _initialize_example_lattice(self):
        """Initialize the lattice with example nodes and connections."""
        # Add module nodes with enhanced recursion
        self.lattice.add_module_node("core", (0.5, 0.5), "central", 1.0)
        self.lattice.add_module_node("perception", (0.3, 0.3), "input", 0.8)
        self.lattice.add_module_node("reasoning", (0.7, 0.3), "processing", 0.8)
        self.lattice.add_module_node("memory", (0.3, 0.7), "storage", 0.8)
        self.lattice.add_module_node("action", (0.7, 0.7), "output", 0.8)
        
        # Add prompt nodes with fixpoints
        self.lattice.add_prompt_node("seed", (0.2, 0.2), "seed", 1.0)
        self.lattice.add_prompt_node("environmental", (0.8, 0.2), "environmental", 0.9)
        self.lattice.add_prompt_node("selection", (0.2, 0.8), "selection", 0.9)
        self.lattice.add_prompt_node("intervention", (0.8, 0.8), "intervention", 0.9)
        
        # Connect modules with enhanced recursion paths
        self._connect_with_recursion("core", "perception", "data", 0.8)
        self._connect_with_recursion("core", "reasoning", "control", 0.8)
        self._connect_with_recursion("core", "memory", "data", 0.8)
        self._connect_with_recursion("core", "action", "control", 0.8)
        
        # Connect prompts with mutation paths
        self._connect_with_recursion("seed", "core", "mutation", 0.6)
        self._connect_with_recursion("environmental", "perception", "data", 0.6)
        self._connect_with_recursion("selection", "reasoning", "control", 0.6)
        self._connect_with_recursion("intervention", "action", "mutation", 0.6)
        
    def _connect_with_recursion(self, source_id: str, target_id: str, 
                              connection_type: str, strength: float):
        """Create a connection with recursive paths."""
        # Create base connection
        self.lattice.connect_nodes(source_id, target_id, connection_type, strength)
        
        # Add recursive paths
        edge = next(e for e in self.lattice.edges 
                   if e.source_id == source_id and e.target_id == target_id)
        
        # Generate recursive paths based on magnitude
        paths = []
        for i in range(self.recursion_magnitude):
            path = [source_id]
            # Add intermediate nodes for recursion
            for j in range(i + 1):
                intermediate = f"{source_id}_rec_{i}_{j}"
                if intermediate not in self.lattice.nodes:
                    pos = self._get_intermediate_position(
                        self.lattice.nodes[source_id].position,
                        self.lattice.nodes[target_id].position,
                        j / (i + 1)
                    )
                    self.lattice.add_module_node(intermediate, pos, "recursive", 0.7)
                path.append(intermediate)
            path.append(target_id)
            paths.append(path)
            
        edge.recursion_paths = paths
        
    def _get_intermediate_position(self, start: Tuple[float, float], 
                                 end: Tuple[float, float], 
                                 t: float) -> Tuple[float, float]:
        """Calculate position for intermediate node with some randomness."""
        import random
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        # Add some randomness to prevent straight lines
        x += random.uniform(-0.1, 0.1)
        y += random.uniform(-0.1, 0.1)
        return (x, y)
        
    def _modulate_breath(self, delta_time: float):
        """Modulate the automaton's breath cycle based on system state."""
        # Calculate system-wide metrics
        total_entropy = sum(node.entropy_buffer for node in self.lattice.nodes.values()) / len(self.lattice.nodes)
        total_coherence = sum(node.coherence_field['local'] for node in self.lattice.nodes.values()) / len(self.lattice.nodes)
        
        # Adjust frequency based on entropy
        if total_entropy > self.breath_cycle['entropy_threshold']:
            # Slow down when entropy is high
            self.breath_cycle['frequency'] *= 0.95
        else:
            # Return to normal speed
            self.breath_cycle['frequency'] = min(1.0, self.breath_cycle['frequency'] * 1.05)
            
        # Adjust recursion depth based on coherence
        if total_coherence > self.breath_cycle['coherence_threshold']:
            # Allow deeper recursion when system is stable
            self.breath_cycle['depth'] = min(2.0, self.breath_cycle['depth'] * 1.1)
        else:
            # Reduce depth when coherence is low
            self.breath_cycle['depth'] = max(0.5, self.breath_cycle['depth'] * 0.9)
            
        # Update phase
        self.breath_cycle['phase'] += delta_time * self.breath_cycle['frequency']
        if self.breath_cycle['phase'] >= 1.0:
            self.breath_cycle['phase'] = 0.0
            self.breath_cycle['last_phase_shift'] = time.time()
            
        # Record breath state
        self._record_event('breath', {
            'phase': self.breath_cycle['phase'],
            'frequency': self.breath_cycle['frequency'],
            'depth': self.breath_cycle['depth'],
            'entropy': total_entropy,
            'coherence': total_coherence
        })
        
        return self.breath_cycle['depth']  # Return current recursion depth

    def run(self):
        """Run the visualization loop."""
        self.running = True
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self._apply_random_mutation()
                    elif event.key == pygame.K_t:
                        self._toggle_interface_mode()
                    elif event.key == pygame.K_UP:
                        self._increase_transparency()
                    elif event.key == pygame.K_DOWN:
                        self._decrease_transparency()
                    elif event.key == pygame.K_r:
                        self._toggle_recursion_magnitude()
                    elif event.key == pygame.K_e:
                        self._toggle_entropy_scrubbing()
                    elif event.key == pygame.K_s:
                        self._toggle_sigil_mode()
                    elif event.key == pygame.K_d:
                        self._toggle_dredd_visibility()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event.pos)
                        
            # Calculate delta time
            current_time = time.time()
            delta_time = current_time - self.last_update
            self.last_update = current_time
            
            # Modulate breath and get recursion depth
            recursion_depth = self._modulate_breath(delta_time)
            
            # Update systems with modulated depth
            self.lattice.update_breath_cycle(delta_time * recursion_depth)
            self.dredd.update_breath(delta_time * recursion_depth)
            self.renderer.update(delta_time)
            
            # Update node representations based on current mode
            self._update_node_representations()
            
            # Apply entropy scrubbing if active
            if self.entropy_scrubbing:
                self._apply_entropy_scrubbing()
                
            # Apply sigil effects if active
            if self.sigil_active:
                self._apply_sigil_effects()
            
            # Apply judgments
            self._apply_dredd_judgments()
            
            # Render frame
            self.renderer.render(self.lattice)
            
            # Cap frame rate
            clock.tick(60)
            
        self.renderer.cleanup()
        
    def _handle_mouse_click(self, pos: Tuple[int, int]):
        """Handle mouse click for node/fixpoint selection."""
        # Convert screen position to lattice coordinates
        x = pos[0] / self.renderer.width
        y = pos[1] / self.renderer.height
        
        # Check for node selection
        for node_id, node in self.lattice.nodes.items():
            node_x, node_y = node.position
            if abs(x - node_x) < 0.05 and abs(y - node_y) < 0.05:
                self.selected_node = node_id
                self.fixpoint_selection = None
                return
                
        # Check for fixpoint selection
        if self.selected_node:
            node = self.lattice.nodes[self.selected_node]
            for i, fixpoint in enumerate(node.fixpoints):
                fix_x, fix_y = fixpoint
                if abs(x - fix_x) < 0.03 and abs(y - fix_y) < 0.03:
                    self.fixpoint_selection = i
                    return
                    
        # Clear selection if clicking empty space
        self.selected_node = None
        self.fixpoint_selection = None
        
    def _toggle_recursion_magnitude(self):
        """Toggle recursion magnitude between 4x and 8x."""
        self.recursion_magnitude = 8 if self.recursion_magnitude == 4 else 4
        print(f"Recursion magnitude: {self.recursion_magnitude}x")
        
    def _toggle_entropy_scrubbing(self):
        """Toggle entropy scrubbing mode."""
        self.entropy_scrubbing = not self.entropy_scrubbing
        print(f"Entropy scrubbing: {'enabled' if self.entropy_scrubbing else 'disabled'}")
        
    def _toggle_sigil_mode(self):
        """Toggle sigil mode for symbolic mutations."""
        self.sigil_active = not self.sigil_active
        print(f"Sigil mode: {'enabled' if self.sigil_active else 'disabled'}")
        
    def _toggle_dredd_visibility(self):
        """Toggle Dredd Model visibility in the visualization."""
        self.dredd.visible = not getattr(self.dredd, 'visible', True)
        print(f"Dredd Model visibility: {'enabled' if self.dredd.visible else 'disabled'}")
        
    def _apply_entropy_scrubbing(self):
        """Apply entropy scrubbing to selected node or high-entropy nodes."""
        if self.selected_node:
            # Scrub selected node
            node = self.lattice.nodes[self.selected_node]
            node.entropy_buffer *= 0.5  # Reduce entropy by 50%
        else:
            # Scrub high-entropy nodes
            for node in self.lattice.nodes.values():
                if node.entropy_buffer > 0.7:  # High entropy threshold
                    node.entropy_buffer *= 0.8  # Reduce entropy by 20%
                    
    def _apply_sigil_effects(self):
        """Apply sigil-based mutations to the lattice."""
        if self.selected_node and self.fixpoint_selection is not None:
            node = self.lattice.nodes[self.selected_node]
            fixpoint = node.fixpoints[self.fixpoint_selection]
            
            # Apply sigil mutation based on fixpoint
            mutation_type = f"sigil_{self.fixpoint_selection}"
            self.lattice.apply_mutation(self.selected_node, mutation_type, 0.2)
            
            # Update fixpoint resonance
            node.resonance *= 1.1  # Increase resonance
            
            # Propagate effects to connected nodes
            for edge in self.lattice.edges:
                if edge.source_id == self.selected_node:
                    target = self.lattice.nodes[edge.target_id]
                    target.resonance *= 1.05
                elif edge.target_id == self.selected_node:
                    source = self.lattice.nodes[edge.source_id]
                    source.resonance *= 1.05
        
    def _apply_dredd_judgments(self):
        """Apply Dredd Model judgments to the lattice."""
        for node_id, node in self.lattice.nodes.items():
            # Get node state
            resonance = node.resonance
            entropy = node.entropy_buffer
            coherence = node.coherence_field['local']
            
            # Render judgment
            judgment = self.dredd.render_judgment(
                node_id, resonance, entropy, coherence
            )
            
            if judgment:
                if judgment.judgment_type == 'halt':
                    # Apply containment
                    node.entropy_buffer *= 0.8  # Reduce entropy
                    node.resonance *= 0.9  # Reduce resonance
                    
                    # Update coherence field
                    node.coherence_field['local'] = max(
                        node.coherence_field['local'],
                        self.dredd.coherence_threshold
                    )
                else:  # proceed
                    # Allow normal operation
                    pass
                    
                # Update node metadata with judgment
                node.metadata['last_judgment'] = {
                    'type': judgment.judgment_type,
                    'confidence': judgment.confidence,
                    'reasoning': judgment.reasoning
                }
                
    def _toggle_interface_mode(self):
        """Toggle between linear and ritual interface modes."""
        new_mode = self.interface.toggle_mode()
        print(f"Switched to {new_mode.value} mode")
        
    def _increase_transparency(self):
        """Increase the transparency level in ritual mode."""
        current = self.interface.transparency_level
        self.interface.set_transparency_level(current + 0.1)
        print(f"Transparency: {self.interface.transparency_level:.1f}")
        
    def _decrease_transparency(self):
        """Decrease the transparency level in ritual mode."""
        current = self.interface.transparency_level
        self.interface.set_transparency_level(current - 0.1)
        print(f"Transparency: {self.interface.transparency_level:.1f}")
        
    def _update_node_representations(self):
        """Update node representations based on current interface mode."""
        for node_id in self.lattice.nodes:
            # Get the appropriate representation
            rep = self.interface.get_node_representation(node_id)
            
            # Update node properties
            node = self.lattice.nodes[node_id]
            if self.interface.current_mode == InterfaceMode.LINEAR:
                node.metadata["display_name"] = rep["function"]
                node.metadata["description"] = rep["description"]
            else:  # RITUAL mode
                node.metadata["display_name"] = rep["symbol"]
                node.metadata["description"] = rep["description"]
                
    def _apply_random_mutation(self):
        """Apply a random mutation to a random node."""
        import random
        
        # Select random node
        node_id = random.choice(list(self.lattice.nodes.keys()))
        node = self.lattice.nodes[node_id]
        
        # Record pre-mutation state
        pre_state = {
            'resonance': node.resonance,
            'entropy': node.entropy_buffer,
            'coherence': node.coherence_field['local']
        }
        
        # Get current state for judgment
        resonance = node.resonance
        entropy = node.entropy_buffer
        coherence = node.coherence_field['local']
        
        # Get judgment before mutation
        judgment = self.dredd.render_judgment(node_id, resonance, entropy, coherence)
        
        if judgment and judgment.judgment_type == 'halt':
            print(f"Mutation prevented: {judgment.reasoning}")
            return
            
        # Select random mutation type
        mutation_types = ["adapt", "evolve", "transform", "merge", "split"]
        mutation_type = random.choice(mutation_types)
        
        # Apply mutation
        self.lattice.apply_mutation(node_id, mutation_type, 
                                  strength=random.uniform(0.1, 0.3))
                                  
        # Record post-mutation state
        post_state = {
            'resonance': node.resonance,
            'entropy': node.entropy_buffer,
            'coherence': node.coherence_field['local']
        }
        
        # Record mutation in memory
        self._record_mutation(node_id, mutation_type, pre_state, post_state)
        
        # Get post-mutation judgment
        post_judgment = self.dredd.render_judgment(
            node_id, node.resonance, node.entropy_buffer, 
            node.coherence_field['local']
        )
        
        if post_judgment and post_judgment.judgment_type == 'halt':
            # Rollback mutation if it violates laws
            node.resonance = resonance
            node.entropy_buffer = entropy
            node.coherence_field['local'] = coherence
            print(f"Mutation rolled back: {post_judgment.reasoning}")
            
            # Record rollback
            self._record_event('rollback', {
                'node_id': node_id,
                'reason': post_judgment.reasoning
            })
        
    def _record_event(self, event_type: str, data: dict):
        """Record an event in the automaton's memory core."""
        timestamp = time.time()
        event = {
            'type': event_type,
            'timestamp': timestamp,
            'data': data
        }
        
        # Add to event log
        self.memory_buffer['event_log'].append(event)
        if len(self.memory_buffer['event_log']) > self.memory_capacity:
            self.memory_buffer['event_log'].pop(0)
            
        # Record in node memory if applicable
        if 'node_id' in data:
            node_id = data['node_id']
            if node_id not in self.memory_buffer['node_memories']:
                self.memory_buffer['node_memories'][node_id] = []
            self.memory_buffer['node_memories'][node_id].append(event)
            if len(self.memory_buffer['node_memories'][node_id]) > 100:  # Per-node capacity
                self.memory_buffer['node_memories'][node_id].pop(0)
                
    def _record_mutation(self, node_id: str, mutation_type: str, 
                        pre_state: dict, post_state: dict):
        """Record a mutation in the automaton's memory core."""
        mutation = {
            'node_id': node_id,
            'type': mutation_type,
            'pre_state': pre_state,
            'post_state': post_state,
            'timestamp': time.time()
        }
        
        self.memory_buffer['mutational_lineage'].append(mutation)
        if len(self.memory_buffer['mutational_lineage']) > self.memory_capacity:
            self.memory_buffer['mutational_lineage'].pop(0)
            
        # Record as event
        self._record_event('mutation', mutation)
        
    def _record_coherence(self, node_id: str, coherence_value: float):
        """Record coherence changes in the automaton's memory core."""
        coherence = {
            'node_id': node_id,
            'value': coherence_value,
            'timestamp': time.time()
        }
        
        self.memory_buffer['coherence_history'].append(coherence)
        if len(self.memory_buffer['coherence_history']) > self.memory_capacity:
            self.memory_buffer['coherence_history'].pop(0)
            
        # Record as event
        self._record_event('coherence', coherence)
        
    def get_lattice_state(self) -> Dict[str, any]:
        """Get the current state of the lattice."""
        state = self.lattice.get_lattice_state()
        state.update(self.interface.get_mode_info())
        return state
        
if __name__ == "__main__":
    controller = VisualizationController()
    controller.run() 