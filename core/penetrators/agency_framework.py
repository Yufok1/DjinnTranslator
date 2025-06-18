from typing import Dict, Tuple, List, Optional
import math
import random
from kernel_registry import KernelRegistry, KernelDescriptor, KernelState

class PenetratorAgency:
    """Base class for penetrator agencies that move through the lattice."""
    
    def __init__(self, position: Tuple[int, int], velocity: Tuple[float, float]):
        self.position = position
        self.velocity = velocity
        self.phase = 0.0
        self.entropy = 0.0
        self.coherence = 1.0
        self.telos_bias = 0.0
        self.memory = []  # List of visited positions and their states
        
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

class InstigatorAgency(PenetratorAgency):
    """Breaches coherence to force emergence."""
    
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Force emergence through coherence breach."""
        # Increase entropy to force emergence
        kernel.state.entropy = min(1.0, kernel.state.entropy + 0.1)
        
        # Decrease coherence to allow change
        kernel.state.coherence = max(0.0, kernel.state.coherence - 0.1)
        
        # Randomize phase to break patterns
        kernel.state.phase = random.random()

class MirrorAgency(PenetratorAgency):
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

class PropellantAgency(PenetratorAgency):
    """Catalyzes breath speed, mutation rate, and telos pressure."""
    
    def _interact_with_kernel(self, kernel: KernelDescriptor):
        """Accelerate kernel processes."""
        # Accelerate phase
        kernel.state.phase = (kernel.state.phase + 0.2) % 1.0
        
        # Increase telos bias
        kernel.telos_bias = min(1.0, kernel.telos_bias + 0.1)
        
        # Amplify coherence
        kernel.state.coherence = min(1.0, kernel.state.coherence * 1.2)

class FlightAgency(PenetratorAgency):
    """Leaves recursion momentarily and returns with knowledge."""
    
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

class PenetratorManager:
    """Manages penetrator agencies in the lattice."""
    
    def __init__(self):
        self.agencies: List[PenetratorAgency] = []
        
    def add_agency(self, agency: PenetratorAgency):
        """Add a new penetrator agency."""
        self.agencies.append(agency)
        
    def update(self, registry: KernelRegistry, dt: float):
        """Update all penetrator agencies."""
        for agency in self.agencies:
            agency.update(registry, dt)
            
    def get_agency_at(self, position: Tuple[int, int]) -> Optional[PenetratorAgency]:
        """Get the agency at a specific position."""
        for agency in self.agencies:
            if agency.position == position:
                return agency
        return None 