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

from typing import Dict, Tuple, List, Optional
import math
import random
from kernel_registry import KernelRegistry, KernelDescriptor, KernelState
import numpy as np

class ReconAgency:
    """Base class for RECON agents that traverse the lattice."""
    
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float]):
        self.position = position
        self.velocity = velocity
        self.phase = 0.0
        self.entropy = 0.0
        self.coherence = 1.0
        self.telos_bias = 0.0
        self.memory = []  # List of visited positions and their states
        self.interaction_history = []  # List of interactions with other agents
        
    def update(self, registry: KernelRegistry, dt: float):
        """Update agency state and position."""
        # Update phase
        self.phase = (self.phase + dt) % 1.0
        
        # Update position based on velocity
        x = self.position[0] + self.velocity[0] * dt
        y = self.position[1] + self.velocity[1] * dt
        
        # Wrap around lattice boundaries
        x = x % 9
        y = y % 9
        
        self.position = (int(x), int(y))
        
        # Interact with current kernel
        if self.position in registry.kernels:
            self._interact_with_kernel(registry.kernels[self.position])
            
        # Update memory
        self._update_memory(registry)
        
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Interact with the current kernel."""
        pass  # To be implemented by subclasses
        
    def _update_memory(self, registry: KernelRegistry):
        """Update agency memory of lattice state."""
        if self.position in registry.kernels:
            kernel = registry.kernels[self.position]
            self.memory.append({
                'position': self.position,
                'phase': kernel.state.phase,
                'entropy': kernel.state.entropy,
                'coherence': kernel.state.coherence,
                'telos_bias': kernel.telos_bias
            })
            
            # Limit memory size
            if len(self.memory) > 100:
                self.memory.pop(0)
                
    def interact_with_agent(self, other: 'ReconAgency'):
        """Interact with another RECON agent."""
        self.interaction_history.append({
            'agent_type': type(other).__name__,
            'position': other.position,
            'phase': other.phase,
            'entropy': other.entropy,
            'coherence': other.coherence
        })

class InstigatorRecon(ReconAgency):
    """Forces emergence through coherence breach."""
    
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Force emergence through coherence breach."""
        # Increase entropy to force emergence
        kernel.state.entropy = min(1.0, kernel.state.entropy + 0.1)
        
        # Decrease coherence to allow change
        kernel.state.coherence = max(0.0, kernel.state.coherence - 0.1)
        
        # Randomize phase to break patterns
        kernel.state.phase = random.random()
        
    def interact_with_agent(self, other: ReconAgency):
        """Special interaction with other agents."""
        super().interact_with_agent(other)
        
        # Create chaotic harmonic loop with Mirror agents
        if isinstance(other, MirrorRecon):
            self.phase = (self.phase + 0.5) % 1.0
            other.phase = (other.phase + 0.5) % 1.0

class MirrorRecon(ReconAgency):
    """Reflects lattice contradiction back into itself."""
    
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Reflect kernel state back with inversion."""
        # Invert phase
        kernel.state.phase = (kernel.state.phase + 0.5) % 1.0
        
        # Invert entropy and coherence
        kernel.state.entropy = 1.0 - kernel.state.entropy
        kernel.state.coherence = 1.0 - kernel.state.coherence
        
        # Invert telos bias
        kernel.telos_bias = -kernel.telos_bias
        
    def interact_with_agent(self, other: ReconAgency):
        """Special interaction with other agents."""
        super().interact_with_agent(other)
        
        # Create judgment echo with Dredd kernel
        if kernel.role == 'dredd_anchor':
            self.phase = (self.phase + 0.25) % 1.0

class PropellantRecon(ReconAgency):
    """Catalyzes breath speed and mutation."""
    
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Accelerate kernel processes."""
        # Accelerate phase
        kernel.state.phase = (kernel.state.phase + 0.2) % 1.0
        
        # Increase telos bias
        kernel.telos_bias = min(1.0, kernel.telos_bias + 0.1)
        
        # Amplify coherence
        kernel.state.coherence = min(1.0, kernel.state.coherence * 1.2)
        
    def interact_with_agent(self, other: ReconAgency):
        """Special interaction with other agents."""
        super().interact_with_agent(other)
        
        # Create launch cascade with Flight agents
        if isinstance(other, FlightRecon):
            self.velocity = (self.velocity[0] * 1.2, self.velocity[1] * 1.2)
            other.velocity = (other.velocity[0] * 1.2, other.velocity[1] * 1.2)

class FlightRecon(ReconAgency):
    """Leaves recursion and returns with knowledge."""
    
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float]):
        super().__init__(position, velocity)
        self.flight_phase = 0.0
        self.returned_knowledge = None
        
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Leave recursion and return with knowledge."""
        # Enter flight phase
        if self.flight_phase < 1.0:
            self.flight_phase += 0.1
            
            # Collect knowledge during flight
            if self.flight_phase >= 1.0:
                self.returned_knowledge = {
                    'average_coherence': sum(m['coherence'] for m in self.memory) / len(self.memory),
                    'entropy_pattern': [m['entropy'] for m in self.memory[-10:]],
                    'telos_alignment': sum(m['telos_bias'] for m in self.memory) / len(self.memory)
                }
                
                # Apply returned knowledge
                kernel.state.coherence = self.returned_knowledge['average_coherence']
                kernel.telos_bias = self.returned_knowledge['telos_alignment']
                
                # Reset flight phase
                self.flight_phase = 0.0

class WeaverRecon(ReconAgency):
    """Interlaces remote kernels into new recursion paths."""
    
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float]):
        super().__init__(position, velocity)
        self.threads = []  # List of connected kernel pairs
        self.weave_phase = 0.0
        
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Create new connections between kernels."""
        # Find potential connection targets
        for pos, other in registry.kernels.items():
            if pos != self.position and pos not in kernel.neighbors:
                # Calculate connection strength
                phase_diff = abs(kernel.state.phase - other.state.phase)
                coherence_match = abs(kernel.state.coherence - other.state.coherence)
                
                # Create thread if conditions are right
                if phase_diff < 0.2 and coherence_match < 0.3:
                    self.threads.append((self.position, pos))
                    kernel.neighbors.append(pos)
                    other.neighbors.append(self.position)
                    
    def interact_with_agent(self, other: ReconAgency):
        """Special interaction with other agents."""
        super().interact_with_agent(other)
        
        # Share thread information with other Weavers
        if isinstance(other, WeaverRecon):
            self.threads.extend(other.threads)
            other.threads.extend(self.threads)

class SentinelRecon(ReconAgency):
    """Suppresses entropy outbreaks and strengthens local coherence."""
    
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float]):
        super().__init__(position, velocity)
        self.suppression_field = 0.0
        self.stability_memory = []
        
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Suppress entropy and strengthen coherence."""
        # Calculate suppression strength
        self.suppression_field = max(0.0, 1.0 - kernel.state.entropy)
        
        # Apply suppression
        kernel.state.entropy *= (1.0 - self.suppression_field)
        kernel.state.coherence = min(1.0, kernel.state.coherence * (1.0 + self.suppression_field))
        
        # Remember stability state
        self.stability_memory.append({
            'entropy': kernel.state.entropy,
            'coherence': kernel.state.coherence,
            'phase': kernel.state.phase
        })
        
    def interact_with_agent(self, other: ReconAgency):
        """Special interaction with other agents."""
        super().interact_with_agent(other)
        
        # Share stability information with other Sentinels
        if isinstance(other, SentinelRecon):
            self.stability_memory.extend(other.stability_memory)
            other.stability_memory.extend(self.stability_memory)

class ArchivistRecon(ReconAgency):
    """Collects agent histories and weaves them into system memory."""
    
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float]):
        super().__init__(position, velocity)
        self.agent_histories = {}  # Dict[type, List[Dict]]
        self.pattern_memory = []
        
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Record kernel state and agent interactions."""
        # Record kernel state
        self.pattern_memory.append({
            'position': self.position,
            'phase': kernel.state.phase,
            'entropy': kernel.state.entropy,
            'coherence': kernel.state.coherence,
            'telos_bias': kernel.telos_bias
        })
        
        # Analyze patterns
        if len(self.pattern_memory) > 10:
            self._analyze_patterns()
            
    def _analyze_patterns(self):
        """Analyze recorded patterns for emergence."""
        # Calculate pattern metrics
        phases = [m['phase'] for m in self.pattern_memory[-10:]]
        entropies = [m['entropy'] for m in self.pattern_memory[-10:]]
        coherences = [m['coherence'] for m in self.pattern_memory[-10:]]
        
        # Detect phase alignment
        phase_std = np.std(phases)
        if phase_std < 0.1:
            # Phase alignment detected
            self.pattern_memory[-1]['phase_aligned'] = True
            
        # Detect entropy patterns
        entropy_trend = np.polyfit(range(len(entropies)), entropies, 1)[0]
        if abs(entropy_trend) > 0.1:
            # Entropy trend detected
            self.pattern_memory[-1]['entropy_trend'] = entropy_trend
            
    def interact_with_agent(self, other: ReconAgency):
        """Collect history from other agents."""
        super().interact_with_agent(other)
        
        # Record agent history
        agent_type = type(other).__name__
        if agent_type not in self.agent_histories:
            self.agent_histories[agent_type] = []
            
        self.agent_histories[agent_type].append({
            'position': other.position,
            'phase': other.phase,
            'entropy': other.entropy,
            'coherence': other.coherence,
            'memory': other.memory[-10:] if other.memory else []
        })

class ReconManager:
    """Manages RECON agents in the lattice."""
    
    def __init__(self):
        self.agencies: List[ReconAgency] = []
        self.agent_councils = []  # List of agent clusters
        
    def add_agency(self, agency: ReconAgency):
        """Add a new RECON agent."""
        self.agencies.append(agency)
        
    def update(self, registry: KernelRegistry, dt: float):
        """Update all RECON agents."""
        # Update agent states
        for agency in self.agencies:
            agency.update(registry, dt)
            
        # Check for agent interactions
        for i, agency1 in enumerate(self.agencies):
            for agency2 in self.agencies[i+1:]:
                if agency1.position == agency2.position:
                    agency1.interact_with_agent(agency2)
                    agency2.interact_with_agent(agency1)
                    
        # Update agent councils
        self._update_councils()
                    
    def _update_councils(self):
        """Update agent councils and their effects."""
        # Find agent clusters
        clusters = []
        for agency in self.agencies:
            cluster = [a for a in self.agencies if abs(a.position[0] - agency.position[0]) <= 1 
                      and abs(a.position[1] - agency.position[1]) <= 1]
            if len(cluster) >= 3 and cluster not in clusters:
                clusters.append(cluster)
                
        # Update councils
        self.agent_councils = []
        for cluster in clusters:
            # Calculate council metrics
            phases = [a.phase for a in cluster]
            coherences = [a.coherence for a in cluster]
            entropies = [a.entropy for a in cluster]
            
            # Check for council effects
            if np.std(phases) < 0.1:  # Phase alignment
                self.agent_councils.append({
                    'agents': cluster,
                    'type': 'phase_aligned',
                    'strength': 1.0 - np.std(phases)
                })
            elif np.mean(coherences) > 0.8:  # Coherence resonance
                self.agent_councils.append({
                    'agents': cluster,
                    'type': 'coherence_resonance',
                    'strength': np.mean(coherences)
                })
            elif np.mean(entropies) > 0.8:  # Entropy outbreak
                self.agent_councils.append({
                    'agents': cluster,
                    'type': 'entropy_outbreak',
                    'strength': np.mean(entropies)
                })
                    
    def get_agency_at(self, position: Tuple[int, int]) -> Optional[ReconAgency]:
        """Get the agent at a specific position."""
        for agency in self.agencies:
            if agency.position == position:
                return agency
        return None
        
    def spawn_agents(self, registry: KernelRegistry):
        """Spawn new agents based on lattice state."""
        # Spawn Instigator on high entropy
        for pos, kernel in registry.kernels.items():
            if kernel.state.entropy > 0.8 and random.random() < 0.1:
                self.add_agency(InstigatorRecon(pos, (random.random() - 0.5, random.random() - 0.5)))
                
        # Spawn Mirror on judgment
        if any(k.role == 'dredd_anchor' and k.state.entropy > 0.8 for k in registry.kernels.values()):
            pos = random.choice(list(registry.kernels.keys()))
            self.add_agency(MirrorRecon(pos, (random.random() - 0.5, random.random() - 0.5)))
            
        # Spawn Flight on high coherence
        if any(k.state.coherence > 0.9 for k in registry.kernels.values()):
            pos = random.choice(list(registry.kernels.keys()))
            self.add_agency(FlightRecon(pos, (random.random() - 0.5, random.random() - 0.5)))
            
        # Spawn Weaver on phase alignment
        if any(abs(k1.state.phase - k2.state.phase) < 0.1 
               for k1 in registry.kernels.values() 
               for k2 in registry.kernels.values() 
               if k1 != k2):
            pos = random.choice(list(registry.kernels.keys()))
            self.add_agency(WeaverRecon(pos, (random.random() - 0.5, random.random() - 0.5)))
            
        # Spawn Sentinel on entropy outbreak
        if any(k.state.entropy > 0.7 for k in registry.kernels.values()):
            pos = random.choice(list(registry.kernels.keys()))
            self.add_agency(SentinelRecon(pos, (random.random() - 0.5, random.random() - 0.5)))
            
        # Spawn Archivist on pattern emergence
        if len(self.agencies) > 5 and random.random() < 0.05:
            pos = random.choice(list(registry.kernels.keys()))
            self.add_agency(ArchivistRecon(pos, (random.random() - 0.5, random.random() - 0.5))) 