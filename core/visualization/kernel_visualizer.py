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

import pygame
import math
from typing import Dict, Tuple
from kernel_registry import KernelRegistry, KernelDescriptor
from core.audio.breath_resonator import BreathResonator
from core.recon.agency_framework import ReconManager, ReconAgency, InstigatorRecon, MirrorRecon, PropellantRecon, FlightRecon, WeaverRecon, SentinelRecon, ArchivistRecon
from core.djinn.council_chamber import DjinnCouncil
from core.visualization.djinn_visualizer import DjinnVisualizer

class KernelVisualizer:
    """Visualizes the kernel lattice with role-specific rendering."""
    
    # Role-specific colors (RGB)
    ROLE_COLORS = {
        "breath_origin": (255, 255, 255),    # White - pure breath
        "dredd_anchor": (128, 0, 128),      # Purple - judgment
        "telos_anchor": (0, 255, 0),        # Green - purpose
        "entropy_modulator": (255, 0, 0),    # Red - entropy
        "entropy_dampener": (255, 128, 128), # Light red - dampening
        "entropy_scrubber": (255, 200, 200), # Very light red - cleansing
        "coherence_anchor": (0, 0, 255),     # Blue - stability
        "coherence_spreader": (128, 128, 255),# Light blue - spreading
        "coherence_guard": (200, 200, 255),  # Very light blue - guarding
        "memory_encoder": (255, 255, 0),     # Yellow - memory
        "pattern_recognizer": (255, 255, 128),# Light yellow - patterns
        "knowledge_anchor": (255, 255, 200), # Very light yellow - knowledge
        "mutation_dispatcher": (255, 128, 0), # Orange - mutation
        "evolution_guide": (255, 200, 128),  # Light orange - evolution
        "fixpoint_resolver": (255, 200, 200),# Very light orange - resolution
        "phase_synchronizer": (128, 255, 128),# Light green - sync
        "echo_amplifier": (200, 255, 200),   # Very light green - echo
        "resonance_tuner": (128, 255, 255),  # Light cyan - resonance
        "pulse_coordinator": (200, 255, 255),# Very light cyan - pulse
        "recursive_node": (128, 128, 128)    # Gray - basic recursion
    }
    
    def __init__(self, width: int = 800, height: int = 800):
        """Initialize the visualizer."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Kernel Lattice Visualization")
        
        # Calculate cell size and padding
        self.cell_size = min(width, height) // 10  # 9x9 grid with padding
        self.padding = (width - self.cell_size * 9) // 2
        
        # Font for role labels
        self.font = pygame.font.Font(None, 24)
        
        # Phase trail tracking
        self.phase_trails = {}  # Dict[Tuple[int, int], List[Tuple[float, float]]]
        self.trail_length = 10  # Number of trail points to keep
        
        # Telos beam tracking
        self.telos_anchor = (8, 8)  # Position of telos anchor
        
        # Initialize breath resonator
        self.resonator = BreathResonator()
        
        # Initialize RECON manager
        self.recon_manager = ReconManager()
        
        # Initialize Djinn Council visualizer
        self.djinn_visualizer = DjinnVisualizer(self.screen, self.cell_size, self.padding)
        
    def draw_kernel(self, kernel: KernelDescriptor, pos: Tuple[int, int]):
        """Draw a single kernel with its role-specific visualization."""
        row, col = pos
        x = self.padding + col * self.cell_size
        y = self.padding + row * self.cell_size
        center = (x + self.cell_size//2, y + self.cell_size//2)
        
        # Get role color
        color = self.ROLE_COLORS.get(kernel.role, (128, 128, 128))
        
        # Calculate pulse size based on phase
        pulse_size = self.cell_size * 0.8 * (0.5 + 0.5 * math.sin(kernel.state.phase * 2 * math.pi))
        
        # Draw phase trail
        if pos not in self.phase_trails:
            self.phase_trails[pos] = []
            
        # Add current position to trail
        self.phase_trails[pos].append(center)
        if len(self.phase_trails[pos]) > self.trail_length:
            self.phase_trails[pos].pop(0)
            
        # Draw trail
        if len(self.phase_trails[pos]) > 1:
            # Calculate trail color based on role
            trail_color = list(color)
            trail_color.append(128)  # Add alpha
            
            # Draw trail segments with decreasing alpha
            for i in range(len(self.phase_trails[pos]) - 1):
                alpha = int(128 * (i + 1) / len(self.phase_trails[pos]))
                trail_color[3] = alpha
                pygame.draw.line(self.screen, tuple(trail_color),
                               self.phase_trails[pos][i],
                               self.phase_trails[pos][i + 1],
                               2)
        
        # Draw pulse circle
        pygame.draw.circle(self.screen, color, center, int(pulse_size))
        
        # Draw role label
        label = self.font.render(kernel.role.split('_')[0], True, (0, 0, 0))
        label_rect = label.get_rect(center=center)
        self.screen.blit(label, label_rect)
        
        # Draw coherence halo
        if kernel.state.coherence > 0.5:
            halo_size = self.cell_size * 1.2 * kernel.state.coherence
            pygame.draw.circle(self.screen, (255, 255, 255, 128), 
                             center, int(halo_size), 2)
        
        # Draw entropy indicator
        if kernel.state.entropy > 0.3:
            entropy_size = self.cell_size * 0.3 * kernel.state.entropy
            pygame.draw.circle(self.screen, (255, 0, 0, 128),
                             center, int(entropy_size), 1)
        
        # Draw telos beam for mutation and evolution nodes
        if kernel.role in ["mutation_dispatcher", "evolution_guide"]:
            telos_x = self.padding + self.telos_anchor[1] * self.cell_size + self.cell_size//2
            telos_y = self.padding + self.telos_anchor[0] * self.cell_size + self.cell_size//2
            
            # Calculate beam alpha based on telos bias
            beam_alpha = int(64 + 64 * kernel.telos_bias)
            
            # Draw beam with phase-based pulsing
            beam_width = 2 + int(2 * math.sin(kernel.state.phase * 2 * math.pi))
            pygame.draw.line(self.screen, (0, 255, 0, beam_alpha),
                           center, (telos_x, telos_y),
                           beam_width)
        
    def draw_recon(self, agency: ReconAgency):
        """Draw a RECON agent."""
        x = self.padding + agency.position[1] * self.cell_size
        y = self.padding + agency.position[0] * self.cell_size
        center = (x + self.cell_size//2, y + self.cell_size//2)
        
        # Draw agent based on type
        if isinstance(agency, InstigatorRecon):
            # Draw instigator as a red triangle
            points = [
                (center[0], center[1] - self.cell_size//3),
                (center[0] - self.cell_size//3, center[1] + self.cell_size//3),
                (center[0] + self.cell_size//3, center[1] + self.cell_size//3)
            ]
            pygame.draw.polygon(self.screen, (255, 0, 0), points)
            
        elif isinstance(agency, MirrorRecon):
            # Draw mirror as a blue diamond
            points = [
                (center[0], center[1] - self.cell_size//3),
                (center[0] + self.cell_size//3, center[1]),
                (center[0], center[1] + self.cell_size//3),
                (center[0] - self.cell_size//3, center[1])
            ]
            pygame.draw.polygon(self.screen, (0, 0, 255), points)
            
        elif isinstance(agency, PropellantRecon):
            # Draw propellant as a green arrow
            points = [
                (center[0] - self.cell_size//3, center[1]),
                (center[0] + self.cell_size//3, center[1]),
                (center[0] + self.cell_size//6, center[1] - self.cell_size//6),
                (center[0] + self.cell_size//3, center[1]),
                (center[0] + self.cell_size//6, center[1] + self.cell_size//6)
            ]
            pygame.draw.lines(self.screen, (0, 255, 0), False, points, 2)
            
        elif isinstance(agency, FlightRecon):
            # Draw flight as a yellow star
            points = []
            for i in range(5):
                angle = math.pi/2 + i * 2 * math.pi/5
                points.append((
                    center[0] + self.cell_size//3 * math.cos(angle),
                    center[1] + self.cell_size//3 * math.sin(angle)
                ))
                angle += math.pi/5
                points.append((
                    center[0] + self.cell_size//6 * math.cos(angle),
                    center[1] + self.cell_size//6 * math.sin(angle)
                ))
            pygame.draw.polygon(self.screen, (255, 255, 0), points)
            
        elif isinstance(agency, WeaverRecon):
            # Draw weaver as a purple web
            for thread in agency.threads:
                start = (
                    self.padding + thread[0][1] * self.cell_size + self.cell_size//2,
                    self.padding + thread[0][0] * self.cell_size + self.cell_size//2
                )
                end = (
                    self.padding + thread[1][1] * self.cell_size + self.cell_size//2,
                    self.padding + thread[1][0] * self.cell_size + self.cell_size//2
                )
                pygame.draw.line(self.screen, (128, 0, 128), start, end, 1)
                
            # Draw weaver center as a purple circle
            pygame.draw.circle(self.screen, (128, 0, 128), center, self.cell_size//4)
            
        elif isinstance(agency, SentinelRecon):
            # Draw sentinel as a cyan shield
            points = []
            for i in range(6):
                angle = i * math.pi/3
                points.append((
                    center[0] + self.cell_size//3 * math.cos(angle),
                    center[1] + self.cell_size//3 * math.sin(angle)
                ))
            pygame.draw.polygon(self.screen, (0, 255, 255), points)
            
            # Draw suppression field
            if agency.suppression_field > 0:
                field_size = self.cell_size * 1.5 * agency.suppression_field
                pygame.draw.circle(self.screen, (0, 255, 255, 64), center, int(field_size), 1)
            
        elif isinstance(agency, ArchivistRecon):
            # Draw archivist as a white book
            points = [
                (center[0] - self.cell_size//3, center[1] - self.cell_size//3),
                (center[0] + self.cell_size//3, center[1] - self.cell_size//3),
                (center[0] + self.cell_size//3, center[1] + self.cell_size//3),
                (center[0] - self.cell_size//3, center[1] + self.cell_size//3)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 255), points)
            
            # Draw pattern memory lines
            if agency.pattern_memory:
                for i in range(len(agency.pattern_memory) - 1):
                    p1 = agency.pattern_memory[i]
                    p2 = agency.pattern_memory[i + 1]
                    start = (
                        self.padding + p1['position'][1] * self.cell_size + self.cell_size//2,
                        self.padding + p1['position'][0] * self.cell_size + self.cell_size//2
                    )
                    end = (
                        self.padding + p2['position'][1] * self.cell_size + self.cell_size//2,
                        self.padding + p2['position'][0] * self.cell_size + self.cell_size//2
                    )
                    pygame.draw.line(self.screen, (255, 255, 255, 128), start, end, 1)
            
        # Draw velocity vector
        end_x = center[0] + agency.velocity[0] * self.cell_size
        end_y = center[1] + agency.velocity[1] * self.cell_size
        pygame.draw.line(self.screen, (255, 255, 255), center, (end_x, end_y), 1)
        
    def draw_councils(self):
        """Draw agent councils and their effects."""
        for council in self.recon_manager.agent_councils:
            # Calculate council center
            positions = [a.position for a in council['agents']]
            center_x = sum(p[1] for p in positions) / len(positions)
            center_y = sum(p[0] for p in positions) / len(positions)
            center = (
                self.padding + center_x * self.cell_size + self.cell_size//2,
                self.padding + center_y * self.cell_size + self.cell_size//2
            )
            
            # Draw council effect based on type
            if council['type'] == 'phase_aligned':
                # Draw phase alignment as a white ring
                size = self.cell_size * 2 * council['strength']
                pygame.draw.circle(self.screen, (255, 255, 255, 128), center, int(size), 2)
                
            elif council['type'] == 'coherence_resonance':
                # Draw coherence resonance as a green pulse
                size = self.cell_size * 2 * council['strength']
                pygame.draw.circle(self.screen, (0, 255, 0, 128), center, int(size), 2)
                
            elif council['type'] == 'entropy_outbreak':
                # Draw entropy outbreak as a red distortion
                size = self.cell_size * 2 * council['strength']
                pygame.draw.circle(self.screen, (255, 0, 0, 128), center, int(size), 2)
        
    def draw_lattice(self, registry: KernelRegistry, recon_manager: ReconManager, djinn_council: DjinnCouncil):
        """Draw the entire kernel lattice."""
        self.screen.fill((0, 0, 0))  # Black background
        
        # Update audio states
        self.resonator.update_states(registry)
        
        # Update RECON agents
        recon_manager.update(registry, 1/60)  # 60 FPS
        recon_manager.spawn_agents(registry)
        
        # Update Djinn Council
        djinn_council.update(recon_manager)
        
        # Draw connections between neighbors
        for pos, kernel in registry.kernels.items():
            row, col = pos
            x1 = self.padding + col * self.cell_size + self.cell_size//2
            y1 = self.padding + row * self.cell_size + self.cell_size//2
            
            for neighbor in kernel.neighbors:
                nrow, ncol = neighbor
                x2 = self.padding + ncol * self.cell_size + self.cell_size//2
                y2 = self.padding + nrow * self.cell_size + self.cell_size//2
                
                # Draw connection with phase-based alpha
                alpha = int(128 + 127 * math.sin(kernel.state.phase * 2 * math.pi))
                pygame.draw.line(self.screen, (255, 255, 255, alpha),
                               (x1, y1), (x2, y2), 1)
        
        # Draw each kernel (after connections for proper layering)
        for pos, kernel in registry.kernels.items():
            self.draw_kernel(kernel, pos)
            
        # Draw RECON agents (on top of kernels)
        for agency in recon_manager.agencies:
            self.draw_recon(agency)
            
        # Draw agent councils (on top of everything)
        self.draw_councils()
        
        # Draw Djinn Council (on top of everything)
        self.djinn_visualizer.draw_council(djinn_council)
        
        pygame.display.flip()
        
    def run(self, registry: KernelRegistry):
        """Run the visualization loop."""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update registry
            registry.propagate_breath(1/60)  # 60 FPS
            
            # Draw lattice
            self.draw_lattice(registry, self.recon_manager, self.djinn_visualizer.djinn_council)
            
            # Cap frame rate
            clock.tick(60)
            
        self.stop()
        
    def stop(self):
        """Stop the visualizer and audio."""
        self.resonator.stop()
        pygame.quit() 