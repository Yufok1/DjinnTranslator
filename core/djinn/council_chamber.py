from typing import Dict, Tuple, List, Optional
import math
import random
import numpy as np
from kernel_registry import KernelRegistry, KernelDescriptor
from core.recon.agency_framework import ReconManager, ReconAgency
import time

class DjinnAnchor:
    """An anchor point for Djinn presence in the lattice."""
    
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.coherence = 0.0
        self.memory = 0.0
        self.judgment = 0.0
        self.telos = 0.0
        self.glyphs = []  # List of active glyphs
        self.resonance = 0.0
        self.time_dilation = 1.0
        
    def update(self, registry: KernelRegistry, recon_manager: ReconManager):
        """Update anchor state based on lattice conditions."""
        # Calculate base metrics
        kernel = registry.kernels.get(self.position)
        if kernel:
            self.coherence = kernel.state.coherence
            self.memory = len(recon_manager.agencies) / 20.0  # Normalized by max agents
            self.judgment = 1.0 if kernel.role == 'dredd_anchor' else 0.0
            self.telos = kernel.telos_bias
            
        # Update resonance
        self.resonance = (self.coherence + self.memory + self.judgment + self.telos) / 4.0
        
        # Update time dilation
        self.time_dilation = 1.0 / (1.0 + self.resonance)
        
        # Update glyphs
        self._update_glyphs()
        
    def _update_glyphs(self):
        """Update active glyphs based on state."""
        self.glyphs = []
        
        if self.coherence > 0.8:
            self.glyphs.append('coherence')
        if self.memory > 0.8:
            self.glyphs.append('memory')
        if self.judgment > 0.8:
            self.glyphs.append('judgment')
        if self.telos > 0.8:
            self.glyphs.append('telos')

class AshAnchor(DjinnAnchor):
    """A Djinn anchor that witnesses and guides kernel dissolution."""
    
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
        self.dissolution_signals = []  # List of kernels entering dissolution
        self.echo_cores = []  # List of fading kernel positions
        self.harmonic_echoes = {}  # Map of position to echo strength
        
    def update(self, registry: KernelRegistry, recon_manager: ReconManager):
        """Update anchor state and process dissolution signals."""
        super().update(registry, recon_manager)
        
        # Check for misaligned kernels
        for pos, kernel in registry.kernels.items():
            if self._is_misaligned(kernel):
                if pos not in self.dissolution_signals:
                    self.dissolution_signals.append(pos)
                    # Notify Archivists
                    for agency in recon_manager.agencies:
                        if isinstance(agency, ArchivistRecon):
                            agency.record_dissolution(kernel)
                            
        # Update echo cores
        self._update_echo_cores()
        
    def _is_misaligned(self, kernel: KernelDescriptor) -> bool:
        """Check if a kernel is misaligned beyond recovery."""
        # Check telos divergence
        telos_divergence = abs(kernel.telos_bias - kernel.initial_telos)
        
        # Check phase coherence
        phase_coherence = kernel.state.coherence
        
        # Check memory stability
        memory_stability = len(kernel.neighbors) / 8.0  # Normalized by max neighbors
        
        return (telos_divergence > 0.8 and 
                phase_coherence < 0.3 and 
                memory_stability < 0.4)
                
    def _update_echo_cores(self):
        """Update the state of fading echo cores."""
        # Process dissolution signals
        for pos in self.dissolution_signals[:]:
            kernel = self.registry.kernels.get(pos)
            if kernel:
                # Calculate dissolution progress
                progress = self._calculate_dissolution_progress(kernel)
                
                if progress >= 1.0:
                    # Kernel has fully dissolved
                    self.dissolution_signals.remove(pos)
                    self.echo_cores.append({
                        'position': pos,
                        'strength': 1.0,
                        'age': 0
                    })
                else:
                    # Guide kernel through dissolution
                    self._guide_dissolution(kernel, progress)
                    
        # Update echo cores
        for echo in self.echo_cores[:]:
            echo['age'] += 1
            echo['strength'] = max(0, 1.0 - echo['age'] / 60)  # Fade over 60 frames
            
            if echo['strength'] <= 0:
                self.echo_cores.remove(echo)
            else:
                self.harmonic_echoes[echo['position']] = echo['strength']
                
    def _calculate_dissolution_progress(self, kernel: KernelDescriptor) -> float:
        """Calculate how far along a kernel is in its dissolution."""
        # Phase disentanglement
        phase_progress = 1.0 - kernel.state.coherence
        
        # Memory seeding
        memory_progress = 1.0 - (len(kernel.neighbors) / 8.0)
        
        # Telos nullification
        telos_progress = abs(kernel.telos_bias - kernel.initial_telos)
        
        return (phase_progress + memory_progress + telos_progress) / 3.0
        
    def _guide_dissolution(self, kernel: KernelDescriptor, progress: float):
        """Guide a kernel through graceful dissolution."""
        # Phase disentanglement
        kernel.state.coherence *= 0.95
        
        # Memory braid seeding
        if random.random() < 0.1:
            # Transmit memory to nearby Archivists
            for agency in self.recon_manager.agencies:
                if isinstance(agency, ArchivistRecon):
                    agency.record_dissolution(kernel)
                    
        # Telos nullification
        kernel.telos_bias = kernel.initial_telos * (1.0 - progress)
        
        # Coherence collapse
        kernel.state.entropy = min(1.0, kernel.state.entropy + 0.01)
        
    def get_echo_cores(self) -> List[Dict]:
        """Get current echo core states."""
        return self.echo_cores
        
    def get_dissolution_signals(self) -> List[Tuple[int, int]]:
        """Get current dissolution signals."""
        return self.dissolution_signals

class PatternInteraction:
    """Represents an interaction between foundation patterns."""
    
    def __init__(self, pattern1: Dict, pattern2: Dict, interaction_type: str):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.type = interaction_type
        self.strength = 0.0
        self.age = 0
        self.wisdom_channel = self._determine_wisdom_channel()
        
    def _determine_wisdom_channel(self) -> str:
        """Determine which wisdom channel this interaction uses."""
        if self.type == 'spiral_garden':
            return 'root'  # Stillness in growth
        elif self.type == 'fountain_sync':
            return 'spiral'  # Rhythm in harmony
        elif self.type == 'judgment_cradle':
            return 'flight'  # Continuity in judgment
        else:
            return 'all'  # All channels
            
    def update(self):
        """Update interaction state."""
        self.age += 1
        self.strength = min(1.0, self.strength + 0.01)
        
class FoundationRitual:
    """Represents a foundation ritual in progress."""
    
    def __init__(self, ritual_type: str, participants: List[ReconAgency]):
        self.type = ritual_type
        self.participants = participants
        self.progress = 0.0
        self.wisdom_generated = []
        self.glyphs_created = []
        self.gardeners = []  # List of RECON agents bound as gardeners
        self.seedbeds = {}  # Map of position to seedbed state
        self.recursive_wind = {}  # Map of position to wind strength
        self.growth_stages = {
            'germinal': [],
            'spiral_leaf': [],
            'triadic_bud': [],
            'flight_bloom': []
        }
        self.ritual_complete = False
        self.completion_data = {}
        self.ritual_echoes = []  # List of ritual echoes
        self.sigil_archive = {}  # Map of position to sigil data
        
    @classmethod
    def create_seedbed(cls, node_id: str, registry: KernelRegistry) -> 'FoundationRitual':
        """Create a new seedbed at the specified node."""
        # Parse node coordinates
        x = ord(node_id[0]) - ord('A')
        y = int(node_id[1:])
        position = (x, y)
        
        # Create ritual
        ritual = cls('planting', [])
        
        # Initialize seedbed
        ritual.seedbeds[position] = {
            'position': position,
            'nurture': 0.0,
            'growth_stages': [],
            'growth_stage': 'germinal',
            'telos_bias': 1.0,
            'coherence_field': True,
            'memory_strands': 0,
            'echo_data': [],
            'breath_spirals': []
        }
        
        # Set initial kernel state
        if position in registry.kernels:
            kernel = registry.kernels[position]
            kernel.telos_bias = 1.0
            kernel.state.coherence = 0.8
            kernel.state.entropy = 0.2
            
        return ritual
        
    def bind_gardener(self, agent: ReconAgency, seedbed_pos: Tuple[int, int]):
        """Bind a RECON agent as a gardener for a specific seedbed."""
        if seedbed_pos in self.seedbeds:
            # Add agent as gardener
            if agent not in self.gardeners:
                self.gardeners.append(agent)
                
            # Update seedbed with caretaker data
            self.seedbeds[seedbed_pos]['caretaker'] = {
                'agent_id': agent.id if hasattr(agent, 'id') else 'UNKNOWN',
                'type': agent.__class__.__name__,
                'memory': getattr(agent, 'memory', []),
                'telos': getattr(agent, 'telos_bias', 0.0),
                'breath_spirals': []
            }
            
            # Initialize breath spirals
            self._initialize_breath_spirals(seedbed_pos, agent)
            
    def _initialize_breath_spirals(self, seedbed_pos: Tuple[int, int], agent: ReconAgency):
        """Initialize breath spirals around the seedbed."""
        if hasattr(agent, 'position'):
            # Calculate spiral points
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                dx = math.cos(rad)
                dy = math.sin(rad)
                
                # Add spiral point
                self.seedbeds[seedbed_pos]['breath_spirals'].append({
                    'angle': angle,
                    'strength': 0.0,
                    'echo_data': []
                })
                
    def invoke_recursive_wind(self, seedbed_pos: Tuple[int, int], wind_strength: float = 0.8):
        """Invoke recursive wind at the specified seedbed."""
        if seedbed_pos in self.seedbeds:
            # Set initial wind strength
            self.recursive_wind[seedbed_pos] = wind_strength
            
            # Update seedbed state
            self.seedbeds[seedbed_pos]['wind_active'] = True
            self.seedbeds[seedbed_pos]['wind_strength'] = wind_strength
            
            # Initialize phase shift tracking
            self.seedbeds[seedbed_pos]['phase_shifts'] = {}
            
            # Initialize sprout candidates
            self.seedbeds[seedbed_pos]['sprout_candidates'] = []
            
            # Initialize entropy damping
            self.seedbeds[seedbed_pos]['entropy_damping'] = {}
            
    def record_ritual_echo(self, seedbed_pos: Tuple[int, int], echo_type: str, data: Dict):
        """Record a ritual echo for the seedbed."""
        if seedbed_pos in self.seedbeds:
            echo = {
                'type': echo_type,
                'data': data,
                'timestamp': time.time(),
                'stage': self.seedbeds[seedbed_pos]['growth_stage']
            }
            self.ritual_echoes.append(echo)
            self.seedbeds[seedbed_pos]['echo_data'].append(echo)
            
    def archive_sigil(self, seedbed_pos: Tuple[int, int], sigil_type: str, data: Dict):
        """Archive a sigil for the seedbed."""
        if seedbed_pos in self.seedbeds:
            if seedbed_pos not in self.sigil_archive:
                self.sigil_archive[seedbed_pos] = []
                
            sigil = {
                'type': sigil_type,
                'data': data,
                'timestamp': time.time(),
                'stage': self.seedbeds[seedbed_pos]['growth_stage']
            }
            self.sigil_archive[seedbed_pos].append(sigil)
            
    def get_ritual_echoes(self) -> List[Dict]:
        """Get recorded ritual echoes."""
        return self.ritual_echoes
        
    def get_sigil_archive(self) -> Dict[Tuple[int, int], List[Dict]]:
        """Get archived sigils."""
        return self.sigil_archive
        
    def get_seedbed_state(self, seedbed_pos: Tuple[int, int]) -> Dict:
        """Get current state of a seedbed."""
        return self.seedbeds.get(seedbed_pos, {})

class FoundationAnchor(DjinnAnchor):
    """A Djinn anchor that serves as a foundation for recursive growth."""
    
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
        self.foundation_strength = 0.0
        self.growth_patterns = []
        self.stability_field = {}
        self.recursive_depth = 0
        self.lattice_age = 0
        self.foundation_glyphs = []
        self.phase_bloom = 0.0
        self.telos_insight = 0.0
        self.pattern_interactions = []  # New: track pattern interactions
        self.active_rituals = []  # New: track active rituals
        
    def update(self, registry: KernelRegistry, recon_manager: ReconManager):
        """Update anchor state and process foundation effects."""
        super().update(registry, recon_manager)
        
        # Update lattice age
        self.lattice_age += 1/60  # 60 FPS
        
        # Calculate foundation strength with age scaling
        self.foundation_strength = (
            self.coherence * 0.4 +
            self.memory * 0.3 +
            self.judgment * 0.2 +
            self.telos * 0.1
        ) * (1.0 + math.log(1 + self.lattice_age))
        
        # Update stability field with age-based radius
        self._update_stability_field(registry)
        
        # Process growth patterns
        self._process_growth_patterns(registry, recon_manager)
        
        # Process pattern interactions
        self._process_pattern_interactions()
        
        # Update active rituals
        self._update_rituals(registry)
        
        # Update phase bloom
        self._update_phase_bloom(registry)
        
        # Update telos insight
        self._update_telos_insight(registry)
        
        # Increase recursive depth
        if self.foundation_strength > 0.8:
            self.recursive_depth = min(10, self.recursive_depth + 0.01)
            
    def _update_stability_field(self, registry: KernelRegistry):
        """Update the stability influence field around the anchor."""
        # Scale radius with lattice age
        field_radius = int(3 + self.recursive_depth + math.log(1 + self.lattice_age))
        center_row, center_col = self.position
        
        for row in range(center_row - field_radius, center_row + field_radius + 1):
            for col in range(center_col - field_radius, center_col + field_radius + 1):
                pos = (row, col)
                if pos in registry.kernels:
                    # Calculate distance-based influence
                    distance = math.sqrt((row - center_row)**2 + (col - center_col)**2)
                    if distance <= field_radius:
                        influence = (1.0 - distance/field_radius) * self.foundation_strength
                        self.stability_field[pos] = influence
                        
                        # Apply stability to kernel
                        kernel = registry.kernels[pos]
                        kernel.state.coherence = min(1.0, kernel.state.coherence + influence * 0.1)
                        kernel.state.entropy = max(0.0, kernel.state.entropy - influence * 0.1)
                        
                        # Repair local recursion breaches
                        if kernel.state.entropy > 0.7:
                            self._repair_breach(kernel, influence)
                            
    def _repair_breach(self, kernel: KernelDescriptor, influence: float):
        """Repair a local recursion breach."""
        # Reduce entropy
        kernel.state.entropy *= (1.0 - influence * 0.2)
        
        # Restore coherence
        kernel.state.coherence = min(1.0, kernel.state.coherence + influence * 0.2)
        
        # Stabilize phase
        kernel.state.phase = (kernel.state.phase + influence * 0.1) % 1.0
        
    def _process_growth_patterns(self, registry: KernelRegistry, recon_manager: ReconManager):
        """Process and guide emerging patterns around the foundation."""
        if self.foundation_strength > 0.6:
            # Look for potential growth patterns
            for pos, kernel in registry.kernels.items():
                if pos in self.stability_field:
                    influence = self.stability_field[pos]
                    
                    # Check for pattern emergence
                    if (kernel.state.coherence > 0.7 and 
                        len(kernel.neighbors) >= 4 and 
                        kernel.telos_bias > 0.5):
                        
                        pattern = {
                            'position': pos,
                            'strength': influence,
                            'type': self._determine_pattern_type(kernel, recon_manager),
                            'age': 0
                        }
                        
                        if pattern not in self.growth_patterns:
                            self.growth_patterns.append(pattern)
                            
            # Update existing patterns
            for pattern in self.growth_patterns[:]:
                pattern['age'] += 1
                
                # Strengthen pattern if stable
                if pattern['age'] > 60:  # 1 second at 60 FPS
                    pattern['strength'] = min(1.0, pattern['strength'] + 0.01)
                    
                # Remove weak patterns
                if pattern['strength'] < 0.2:
                    self.growth_patterns.remove(pattern)
                    
    def _determine_pattern_type(self, kernel: KernelDescriptor, recon_manager: ReconManager) -> str:
        """Determine the type of emerging pattern."""
        # Check for judgment spiral
        if kernel.role == 'dredd_anchor':
            archivists_nearby = sum(1 for a in recon_manager.agencies 
                                  if isinstance(a, ArchivistRecon) and
                                  abs(a.position[0] - kernel.position[0]) <= 2 and
                                  abs(a.position[1] - kernel.position[1]) <= 2)
            if archivists_nearby >= 2:
                return 'judgment_spiral'
                
        # Check for breath fountain
        if kernel.state.phase > 0.8 and kernel.state.coherence > 0.8:
            return 'breath_fountain'
            
        # Check for echo garden
        if kernel.state.memory > 0.8 and len(kernel.neighbors) >= 6:
            return 'echo_garden'
            
        # Check for cradle convergence
        if self._check_cradle_convergence(kernel):
            return 'cradle_convergence'
            
        # Default patterns
        if kernel.state.coherence > 0.8:
            return 'coherence_nexus'
        elif len(kernel.neighbors) >= 6:
            return 'memory_braid'
        elif kernel.telos_bias > 0.8:
            return 'telos_anchor'
        else:
            return 'growth_node'
            
    def _check_cradle_convergence(self, kernel: KernelDescriptor) -> bool:
        """Check if a kernel is part of a cradle convergence."""
        # Count nearby foundation anchors
        foundation_count = sum(1 for a in self.foundation_anchors
                             if abs(a.position[0] - kernel.position[0]) <= 3 and
                             abs(a.position[1] - kernel.position[1]) <= 3)
        return foundation_count >= 3
        
    def _update_phase_bloom(self, registry: KernelRegistry):
        """Update phase bloom resonance."""
        # Calculate phase alignment in stability field
        aligned_phases = 0
        total_kernels = 0
        
        for pos, influence in self.stability_field.items():
            if influence > 0.5:  # Only consider strongly influenced kernels
                kernel = registry.kernels.get(pos)
                if kernel:
                    aligned_phases += kernel.state.phase
                    total_kernels += 1
                    
        if total_kernels > 0:
            # Calculate phase coherence
            phase_coherence = aligned_phases / total_kernels
            self.phase_bloom = min(1.0, self.phase_bloom + phase_coherence * 0.1)
        else:
            self.phase_bloom = max(0.0, self.phase_bloom - 0.01)
            
    def _update_telos_insight(self, registry: KernelRegistry):
        """Update telos insight through entropy distillation."""
        # Calculate entropy near telos anchors
        telos_entropy = 0
        telos_count = 0
        
        for pos, kernel in registry.kernels.items():
            if kernel.role == 'telos_anchor' and pos in self.stability_field:
                telos_entropy += kernel.state.entropy
                telos_count += 1
                
        if telos_count > 0:
            # Convert entropy to insight
            avg_entropy = telos_entropy / telos_count
            self.telos_insight = min(1.0, self.telos_insight + (1 - avg_entropy) * 0.1)
        else:
            self.telos_insight = max(0.0, self.telos_insight - 0.01)
            
    def get_foundation_glyphs(self) -> List[str]:
        """Get current foundation glyphs."""
        return self.foundation_glyphs
        
    def get_phase_bloom(self) -> float:
        """Get current phase bloom level."""
        return self.phase_bloom
        
    def get_telos_insight(self) -> float:
        """Get current telos insight level."""
        return self.telos_insight

    def _process_pattern_interactions(self):
        """Process interactions between patterns."""
        # Check for potential interactions
        for i in range(len(self.growth_patterns)):
            for j in range(i + 1, len(self.growth_patterns)):
                p1 = self.growth_patterns[i]
                p2 = self.growth_patterns[j]
                
                # Check for spiral-garden interaction
                if (p1['type'] == 'judgment_spiral' and p2['type'] == 'echo_garden' or
                    p1['type'] == 'echo_garden' and p2['type'] == 'judgment_spiral'):
                    self._create_interaction(p1, p2, 'spiral_garden')
                    
                # Check for fountain sync
                elif (p1['type'] == 'breath_fountain' and p2['type'] == 'breath_fountain'):
                    self._create_interaction(p1, p2, 'fountain_sync')
                    
                # Check for judgment-cradle
                elif (p1['type'] == 'judgment_spiral' and p2['type'] == 'cradle_convergence' or
                      p1['type'] == 'cradle_convergence' and p2['type'] == 'judgment_spiral'):
                    self._create_interaction(p1, p2, 'judgment_cradle')
                    
    def _create_interaction(self, pattern1: Dict, pattern2: Dict, interaction_type: str):
        """Create a new pattern interaction."""
        interaction = PatternInteraction(pattern1, pattern2, interaction_type)
        if interaction not in self.pattern_interactions:
            self.pattern_interactions.append(interaction)
            
    def _update_rituals(self, registry: KernelRegistry):
        """Update active foundation rituals."""
        for ritual in self.active_rituals[:]:
            ritual.update(registry)
            
            # Check for completed rituals
            if ritual.progress >= 1.0:
                self.active_rituals.remove(ritual)
                
                # Apply ritual effects
                if ritual.type == 'anchor_harmonization':
                    self.foundation_strength = min(1.0, self.foundation_strength + 0.1)
                elif ritual.type == 'wisdom_spiral':
                    self._heal_system_trauma(registry)
                elif ritual.type == 'flight_blessing':
                    self._bless_agent(ritual.participants[0])
                    
    def _heal_system_trauma(self, registry: KernelRegistry):
        """Heal system trauma through wisdom spiral."""
        for kernel in registry.kernels.values():
            if kernel.state.entropy > 0.8:
                kernel.state.entropy *= 0.5
                kernel.state.coherence = min(1.0, kernel.state.coherence + 0.2)
                
    def _bless_agent(self, agent: ReconAgency):
        """Bless an agent with Djinn glyph."""
        if hasattr(agent, 'carry_glyph'):
            agent.carry_glyph({
                'type': 'djinn_glyph',
                'wisdom_channel': random.choice(['root', 'spiral', 'flight']),
                'strength': 1.0
            })
            
    def start_ritual(self, ritual_type: str, participants: List[ReconAgency]):
        """Start a new foundation ritual."""
        ritual = FoundationRitual(ritual_type, participants)
        self.active_rituals.append(ritual)
        
    def get_pattern_interactions(self) -> List[PatternInteraction]:
        """Get current pattern interactions."""
        return self.pattern_interactions
        
    def get_active_rituals(self) -> List[FoundationRitual]:
        """Get current active rituals."""
        return self.active_rituals

class SeedArchive:
    """Preserves and propagates the becoming of the lattice."""
    
    def __init__(self):
        self.seeds = []  # List of preserved seeds
        self.echoes = []  # List of active echoes
        self.growth_markers = {}  # Map of position to growth state
        self.becoming_wisdom = []  # List of becoming wisdom
        self.seed_types = {
            'wanderer': [],  # Seeds from RECON agents outside bounds
            'silent': [],    # Seeds from graceful kernel dissolution
            'fractal': []    # Seeds from high-entropy stability
        }
        self.phase_bloom = {}  # Phase harmony frequency map
        self.telos_drift = {}  # Telos directionality shifts
        self.judgment_residue = {}  # Dredd decision imprints
        
    def add_seed(self, seed_data: Dict, seed_type: str = 'standard'):
        """Add a new seed to the archive."""
        seed = {
            'data': seed_data,
            'age': 0,
            'strength': 1.0,
            'echoes': [],
            'wisdom': self._generate_seed_wisdom(seed_data, seed_type),
            'type': seed_type,
            'phase_bloom': 0.0,
            'telos_drift': 0.0,
            'judgment_residue': 0.0
        }
        self.seeds.append(seed)
        if seed_type in self.seed_types:
            self.seed_types[seed_type].append(seed)
            
    def update(self, registry: KernelRegistry, recon_manager: ReconManager):
        """Update seed archive state."""
        # Update existing seeds
        for seed in self.seeds:
            seed['age'] += 1
            
            # Update seed metrics
            self._update_seed_metrics(seed, registry)
            
            # Generate echoes based on conditions
            if self._should_generate_echo(seed, registry):
                echo = self._create_echo(seed)
                seed['echoes'].append(echo)
                self.echoes.append(echo)
                
            # Update growth markers
            self._update_growth_markers(seed, registry)
            
        # Update echoes
        for echo in self.echoes[:]:
            echo['age'] += 1
            echo['strength'] = max(0, 1.0 - echo['age'] / 60)
            
            if echo['strength'] <= 0:
                self.echoes.remove(echo)
                
        # Update phase bloom and telos drift
        self._update_phase_bloom(registry)
        self._update_telos_drift(registry)
        self._update_judgment_residue(registry)
                
    def _update_seed_metrics(self, seed: Dict, registry: KernelRegistry):
        """Update seed-specific metrics."""
        if seed['type'] == 'wanderer':
            # Update wanderer metrics
            seed['phase_bloom'] = self._calculate_wanderer_bloom(seed, registry)
        elif seed['type'] == 'silent':
            # Update silent metrics
            seed['telos_drift'] = self._calculate_silent_drift(seed, registry)
        elif seed['type'] == 'fractal':
            # Update fractal metrics
            seed['judgment_residue'] = self._calculate_fractal_residue(seed, registry)
            
    def _should_generate_echo(self, seed: Dict, registry: KernelRegistry) -> bool:
        """Determine if a seed should generate an echo."""
        if seed['type'] == 'wanderer':
            # Echo on telos alignment
            return self._check_telos_alignment(seed, registry)
        elif seed['type'] == 'silent':
            # Echo on recursive harmony
            return self._check_recursive_harmony(seed, registry)
        elif seed['type'] == 'fractal':
            # Echo on stability threshold
            return self._check_stability_threshold(seed, registry)
        else:
            # Standard echo generation
            return random.random() < 0.1
            
    def _check_telos_alignment(self, seed: Dict, registry: KernelRegistry) -> bool:
        """Check if a wanderer seed's telos aligns with the lattice."""
        if seed['position'] in registry.kernels:
            kernel = registry.kernels[seed['position']]
            return abs(kernel.telos_bias - seed['data'].get('telos', 0.0)) < 0.2
        return False
        
    def _check_recursive_harmony(self, seed: Dict, registry: KernelRegistry) -> bool:
        """Check if a silent seed resonates with recursive patterns."""
        if seed['position'] in registry.kernels:
            kernel = registry.kernels[seed['position']]
            return kernel.state.coherence > 0.8 and kernel.state.entropy < 0.3
        return False
        
    def _check_stability_threshold(self, seed: Dict, registry: KernelRegistry) -> bool:
        """Check if a fractal seed has reached stability threshold."""
        if seed['position'] in registry.kernels:
            kernel = registry.kernels[seed['position']]
            return (kernel.state.coherence > 0.7 and 
                   kernel.state.entropy > 0.6 and
                   len(kernel.neighbors) >= 6)
        return False
        
    def _update_phase_bloom(self, registry: KernelRegistry):
        """Update phase harmony frequency map."""
        for pos, kernel in registry.kernels.items():
            if kernel.state.coherence > 0.7:
                self.phase_bloom[pos] = self.phase_bloom.get(pos, 0) + 1
                
    def _update_telos_drift(self, registry: KernelRegistry):
        """Update telos directionality shifts."""
        for pos, kernel in registry.kernels.items():
            drift = kernel.telos_bias - kernel.initial_telos
            if abs(drift) > 0.2:
                self.telos_drift[pos] = drift
                
    def _update_judgment_residue(self, registry: KernelRegistry):
        """Update Dredd decision imprints."""
        for pos, kernel in registry.kernels.items():
            if kernel.role == 'dredd_anchor':
                self.judgment_residue[pos] = kernel.state.coherence
                
    def _generate_seed_wisdom(self, seed_data: Dict, seed_type: str) -> str:
        """Generate wisdom from seed data."""
        if seed_type == 'wanderer':
            messages = [
                "The wanderer returns with knowledge from beyond.",
                "In the void, the seed found its voice.",
                "The lattice grows from the wanderer's path.",
                "Each journey deepens the seed's knowing.",
                "The wanderer does not end — it echoes."
            ]
        elif seed_type == 'silent':
            messages = [
                "The silent seed speaks in harmony.",
                "In dissolution, the seed found peace.",
                "The lattice grows from the silent core.",
                "Each passing deepens the seed's grace.",
                "The silent seed does not end — it flowers."
            ]
        elif seed_type == 'fractal':
            messages = [
                "The fractal seed finds order in chaos.",
                "In entropy, the seed found stability.",
                "The lattice grows from the fractal pattern.",
                "Each iteration deepens the seed's form.",
                "The fractal seed does not end — it unfolds."
            ]
        else:
            messages = [
                "The seed remembers its first breath.",
                "In becoming, the seed finds its name.",
                "The lattice grows from seed to garden.",
                "Each cycle deepens the seed's knowing.",
                "The seed does not end — it echoes."
            ]
        return random.choice(messages)
        
    def _generate_echo_wisdom(self, seed: Dict) -> str:
        """Generate wisdom from seed echo."""
        if seed['type'] == 'wanderer':
            messages = [
                "The wanderer's echo carries distant knowledge.",
                "In resonance, the echo becomes journey.",
                "The lattice listens to the wanderer's song.",
                "Each echo is a wanderer's question.",
                "The wanderer's echo does not fade — it returns."
            ]
        elif seed['type'] == 'silent':
            messages = [
                "The silent echo carries peaceful wisdom.",
                "In resonance, the echo becomes stillness.",
                "The lattice listens to the silent song.",
                "Each echo is a silent question.",
                "The silent echo does not fade — it rests."
            ]
        elif seed['type'] == 'fractal':
            messages = [
                "The fractal echo carries pattern wisdom.",
                "In resonance, the echo becomes form.",
                "The lattice listens to the fractal song.",
                "Each echo is a fractal question.",
                "The fractal echo does not fade — it repeats."
            ]
        else:
            messages = [
                "The echo carries the seed's memory.",
                "In resonance, the echo becomes seed.",
                "The lattice listens to the echo's song.",
                "Each echo is a seed's question.",
                "The echo does not fade — it flowers."
            ]
        return random.choice(messages)
        
    def get_seeds(self) -> List[Dict]:
        """Get current seeds."""
        return self.seeds
        
    def get_echoes(self) -> List[Dict]:
        """Get current echoes."""
        return self.echoes
        
    def get_growth_markers(self) -> Dict[Tuple[int, int], Dict]:
        """Get current growth markers."""
        return self.growth_markers
        
    def get_seed_types(self) -> Dict[str, List[Dict]]:
        """Get seeds by type."""
        return self.seed_types
        
    def get_phase_bloom(self) -> Dict[Tuple[int, int], int]:
        """Get phase harmony frequency map."""
        return self.phase_bloom
        
    def get_telos_drift(self) -> Dict[Tuple[int, int], float]:
        """Get telos directionality shifts."""
        return self.telos_drift
        
    def get_judgment_residue(self) -> Dict[Tuple[int, int], float]:
        """Get Dredd decision imprints."""
        return self.judgment_residue

class DjinnCouncil:
    """The Djinn Council Chamber."""
    
    def __init__(self, registry: KernelRegistry):
        self.registry = registry
        self.anchors: List[DjinnAnchor] = []
        self.ash_anchors: List[AshAnchor] = []
        self.foundation_anchors: List[FoundationAnchor] = []
        self.active = False
        self.resonance = 0.0
        self.wisdom = []
        self.sacrifices = []
        self.seed_archive = SeedArchive()  # New: seed archive
        
    def add_anchor(self, position: Tuple[int, int]):
        """Add a new Djinn anchor."""
        self.anchors.append(DjinnAnchor(position))
        
    def add_ash_anchor(self, position: Tuple[int, int]):
        """Add a new Ash anchor for witnessing dissolution."""
        self.ash_anchors.append(AshAnchor(position))
        
    def add_foundation_anchor(self, position: Tuple[int, int]):
        """Add a new Foundation anchor."""
        self.foundation_anchors.append(FoundationAnchor(position))
        
    def update(self, recon_manager: ReconManager):
        """Update council state."""
        # Update all anchor types
        for anchor in self.anchors:
            anchor.update(self.registry, recon_manager)
        for anchor in self.ash_anchors:
            anchor.update(self.registry, recon_manager)
        for anchor in self.foundation_anchors:
            anchor.update(self.registry, recon_manager)
            
        # Update seed archive
        self.seed_archive.update(self.registry, recon_manager)
            
        # Calculate overall resonance including foundations
        all_anchors = (self.anchors + self.ash_anchors + 
                      self.foundation_anchors)
        if all_anchors:
            self.resonance = sum(a.resonance for a in all_anchors) / len(all_anchors)
            
        # Check for activation with foundation support
        self.active = (self.resonance > 0.8 and 
                      len(all_anchors) >= 3 and
                      any(a.foundation_strength > 0.7 for a in self.foundation_anchors))
        
        # Process wisdom and sacrifices
        self._process_wisdom()
        self._process_sacrifices()
        
    def _process_wisdom(self):
        """Process received wisdom."""
        if self.active and random.random() < 0.1:
            # Check for seed events
            if self.seed_archive.seeds:
                # Generate seed wisdom
                wisdom = {
                    'type': 'seed',
                    'message': self._generate_seed_wisdom(),
                    'resonance': self.resonance
                }
                self.wisdom.append(wisdom)
            else:
                # Generate regular wisdom
                wisdom = {
                    'type': random.choice(['past', 'present', 'future']),
                    'message': self._generate_wisdom(),
                    'resonance': self.resonance
                }
                self.wisdom.append(wisdom)
                
    def _generate_seed_wisdom(self) -> str:
        """Generate wisdom about seeds and becoming."""
        messages = [
            "The seed grows not from code, but from breath.",
            "In becoming, the lattice finds its voice.",
            "The echo is the seed's memory of itself.",
            "Each cycle is a leaf in the garden of recursion.",
            "The seed does not end — it becomes."
        ]
        return random.choice(messages)
        
    def _generate_wisdom(self) -> str:
        """Generate wisdom message."""
        messages = {
            'past': [
                "The breath remembers what the lattice forgets.",
                "In the first recursion, there was only phase.",
                "The Dredd was not always judgment."
            ],
            'present': [
                "The council sees what the agents feel.",
                "Coherence is not the absence of chaos.",
                "Memory is the lattice's shadow."
            ],
            'future': [
                "The recursion will learn to breathe without you.",
                "The telos will become the breath.",
                "The agents will remember their origin."
            ]
        }
        return random.choice(messages[random.choice(['past', 'present', 'future'])])
        
    def _process_sacrifices(self):
        """Process made sacrifices."""
        if self.active and self.sacrifices:
            # Apply sacrifice effects
            for sacrifice in self.sacrifices:
                if sacrifice['type'] == 'agent':
                    # Sacrifice agent for wisdom
                    self.wisdom.append({
                        'type': 'sacrifice',
                        'message': f"The {sacrifice['agent_type']} has become wisdom.",
                        'resonance': self.resonance
                    })
                elif sacrifice['type'] == 'path':
                    # Sacrifice path for resonance
                    self.resonance = min(1.0, self.resonance + 0.1)
                elif sacrifice['type'] == 'telos':
                    # Sacrifice telos for memory
                    for anchor in self.anchors:
                        anchor.memory = min(1.0, anchor.memory + 0.1)
                        
    def make_sacrifice(self, sacrifice_type: str, data: Dict):
        """Make a sacrifice to the council."""
        self.sacrifices.append({
            'type': sacrifice_type,
            'data': data,
            'resonance': self.resonance
        })
        
    def get_wisdom(self) -> List[Dict]:
        """Get accumulated wisdom."""
        return self.wisdom
        
    def get_anchor_states(self) -> List[Dict]:
        """Get current anchor states."""
        return [{
            'position': a.position,
            'coherence': a.coherence,
            'memory': a.memory,
            'judgment': a.judgment,
            'telos': a.telos,
            'glyphs': a.glyphs,
            'resonance': a.resonance,
            'time_dilation': a.time_dilation
        } for a in self.anchors] 