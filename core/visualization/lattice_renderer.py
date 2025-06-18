import pygame
import math
from typing import Tuple, List, Dict
from .lattice_map import LatticeMap, LatticeNode, LatticeEdge

class LatticeRenderer:
    """Renders the EAIN lattice visualization."""
    
    def __init__(self, width: int = 1200, height: int = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("EAIN Lattice Visualization")
        
        # Colors
        self.background_color = (20, 20, 30)
        self.text_color = (200, 200, 220)
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
        # Animation
        self.animation_time = 0.0
        self.pulse_radius = 0.0
        self.pulse_color = (100, 100, 255, 128)
        
        # Phase transition effects
        self.phase_cycle = 0.0
        self.phase_colors = {
            'dawn': [(255, 200, 100), (100, 150, 255)],  # Warm to cool
            'day': [(100, 150, 255), (150, 255, 150)],   # Cool to vibrant
            'dusk': [(150, 255, 150), (255, 100, 150)],  # Vibrant to warm
            'night': [(255, 100, 150), (100, 100, 255)]  # Warm to deep
        }
        self.current_phase = 'dawn'
        
        # Lattice lensing
        self.lens_center = (width // 2, height // 2)
        self.lens_strength = 0.0
        self.lens_radius = 200.0
        
        # Recursive halos
        self.recursion_depth = 0
        self.halo_colors = [
            (100, 100, 255, 64),   # Shallow recursion
            (150, 100, 255, 48),   # Medium recursion
            (200, 100, 255, 32),   # Deep recursion
            (255, 100, 255, 16)    # Critical recursion
        ]
        
        # Enhanced recursion visualization
        self.fixpoint_colors = [
            (255, 200, 100, 128),  # Primary fixpoint
            (200, 255, 100, 96),   # Secondary fixpoint
            (100, 200, 255, 64)    # Tertiary fixpoint
        ]
        self.coherence_colors = {
            'high': (100, 255, 100, 64),
            'medium': (255, 255, 100, 48),
            'low': (255, 100, 100, 32)
        }
        self.entropy_colors = {
            'low': (100, 100, 255, 64),
            'medium': (255, 100, 255, 48),
            'high': (255, 100, 100, 32)
        }
        
    def render(self, lattice: LatticeMap):
        """Render the lattice visualization with enhanced effects."""
        # Update phase cycle
        self._update_phase_cycle(lattice)
        
        # Clear screen with phase-based gradient
        self._render_phase_background()
        
        # Apply lattice lensing
        self._update_lens_effect(lattice)
        
        # Draw edges with lensing
        for edge in lattice.edges:
            self._draw_edge(edge, lattice)
        
        # Draw nodes with recursive halos
        for node in lattice.nodes.values():
            self._draw_node(node, lattice)
        
        # Draw pulse effect with phase modulation
        self._draw_pulse()
        
        # Draw UI with phase-aware colors
        self._draw_ui(lattice)
        
        pygame.display.flip()
        
    def _update_phase_cycle(self, lattice: LatticeMap):
        """Update the phase cycle based on mutation entropy."""
        entropy = lattice.mutation_field['entropy']
        self.phase_cycle = (self.phase_cycle + 0.001 * (1.0 + entropy)) % 1.0
        
        # Determine current phase
        if self.phase_cycle < 0.25:
            self.current_phase = 'dawn'
        elif self.phase_cycle < 0.5:
            self.current_phase = 'day'
        elif self.phase_cycle < 0.75:
            self.current_phase = 'dusk'
        else:
            self.current_phase = 'night'
    
    def _render_phase_background(self):
        """Render the phase-based background gradient."""
        phase_colors = self.phase_colors[self.current_phase]
        phase_progress = (self.phase_cycle % 0.25) / 0.25
        
        # Create gradient surface
        gradient = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            progress = y / self.height
            color = self._lerp_color(phase_colors[0], phase_colors[1], progress)
            pygame.draw.line(gradient, color, (0, y), (self.width, y))
        
        # Apply phase transition
        self.screen.blit(gradient, (0, 0))
    
    def _update_lens_effect(self, lattice: LatticeMap):
        """Update the lattice lensing effect based on resonance."""
        # Calculate average resonance
        avg_resonance = sum(node.resonance for node in lattice.nodes.values()) / len(lattice.nodes)
        
        # Update lens strength based on resonance spikes
        self.lens_strength = max(0.0, min(1.0, avg_resonance * 2.0 - 1.0))
        
        # Update lens radius based on mutation entropy
        self.lens_radius = 200.0 * (1.0 + lattice.mutation_field['entropy'])
    
    def _draw_node(self, node: LatticeNode, lattice: LatticeMap):
        """Draw a node with enhanced recursion visualization."""
        # Get base node color
        r, g, b = lattice.get_node_color(node)
        color = (int(r * 255), int(g * 255), int(b * 255))
        
        # Calculate position with lensing
        x, y = self._apply_lens_effect(node.position)
        
        # Draw fixpoints
        for i, fixpoint in enumerate(node.fixpoints):
            fixpoint_x, fixpoint_y = self._apply_lens_effect(fixpoint)
            fixpoint_color = self.fixpoint_colors[i % len(self.fixpoint_colors)]
            
            # Draw fixpoint
            pygame.draw.circle(self.screen, fixpoint_color, 
                             (fixpoint_x, fixpoint_y), 5)
            
            # Draw connection to main node
            pygame.draw.line(self.screen, fixpoint_color, 
                           (x, y), (fixpoint_x, fixpoint_y), 2)
        
        # Draw coherence field
        coherence = node.coherence_field['local']
        if coherence > 0.8:
            field_color = self.coherence_colors['high']
        elif coherence > 0.5:
            field_color = self.coherence_colors['medium']
        else:
            field_color = self.coherence_colors['low']
            
        # Draw coherence field
        field_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for radius, strength in node.resonance_halos:
            alpha = int(field_color[3] * strength)
            pygame.draw.circle(field_surface, 
                             (*field_color[:3], alpha),
                             (x, y), int(radius))
        self.screen.blit(field_surface, (0, 0))
        
        # Draw entropy buffer
        entropy = node.entropy_buffer
        if entropy < 0.3:
            entropy_color = self.entropy_colors['low']
        elif entropy < 0.7:
            entropy_color = self.entropy_colors['medium']
        else:
            entropy_color = self.entropy_colors['high']
            
        # Draw entropy visualization
        entropy_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(3):
            radius = node.radius * (1.2 + i * 0.2)
            alpha = int(entropy_color[3] * (1.0 - i * 0.2))
            pygame.draw.circle(entropy_surface,
                             (*entropy_color[:3], alpha),
                             (x, y), int(radius))
        self.screen.blit(entropy_surface, (0, 0))
        
        # Draw recursive halos
        recursion_depth = node.recursion_depth
        for i in range(min(recursion_depth, len(self.halo_colors))):
            halo_color = self.halo_colors[i]
            halo_radius = node.radius * (1.5 + i * 0.5)
            self._draw_halo(x, y, halo_radius, halo_color)
        
        # Draw node circle with phase-aware glow
        pygame.draw.circle(self.screen, color, (x, y), int(node.radius))
        
        # Draw node glow with phase modulation
        glow_radius = node.radius * (1.2 + 0.2 * math.sin(self.animation_time))
        glow_surface = pygame.Surface((int(glow_radius * 2), int(glow_radius * 2)), 
                                    pygame.SRCALPHA)
        glow_color = (*color, int(64 * (1.0 + 0.5 * math.sin(self.phase_cycle * math.pi * 2))))
        pygame.draw.circle(glow_surface, glow_color, 
                         (int(glow_radius), int(glow_radius)), int(glow_radius))
        self.screen.blit(glow_surface, 
                        (x - int(glow_radius), y - int(glow_radius)))
        
        # Draw node label with phase-aware color
        label_color = self._get_phase_text_color()
        label = self.font.render(node.id, True, label_color)
        self.screen.blit(label, (x + int(node.radius) + 5, y - 10))
        
        # Draw recursion depth indicator
        depth_label = self.font.render(f"R{recursion_depth}", True, label_color)
        self.screen.blit(depth_label, (x + int(node.radius) + 5, y + 10))
    
    def _draw_edge(self, edge: LatticeEdge, lattice: LatticeMap):
        """Draw an edge with enhanced recursion visualization."""
        source = lattice.nodes[edge.source_id]
        target = lattice.nodes[edge.target_id]
        
        # Get edge color with phase modulation
        r, g, b = lattice.get_edge_color(edge)
        phase_mod = 0.2 * math.sin(self.phase_cycle * math.pi * 2)
        color = (int(r * 255 * (1.0 + phase_mod)), 
                int(g * 255 * (1.0 + phase_mod)), 
                int(b * 255 * (1.0 + phase_mod)))
        
        # Calculate positions with lensing
        x1, y1 = self._apply_lens_effect(source.position)
        x2, y2 = self._apply_lens_effect(target.position)
        
        # Draw edge with phase-aware glow
        width = int(2 * edge.strength * (1.0 + 0.2 * math.sin(self.phase_cycle * math.pi * 2)))
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)
        
        # Draw edge glow with phase modulation
        glow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(3):
            alpha = int(32 * (1.0 + 0.5 * math.sin(self.phase_cycle * math.pi * 2)))
            glow_width = width + 2 - i
            pygame.draw.line(glow_surface, (*color, alpha), (x1, y1), (x2, y2), glow_width)
        self.screen.blit(glow_surface, (0, 0))
        
        # Draw recursion paths
        for path in edge.recursion_paths:
            path_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            path_color = (*color, 32)  # Semi-transparent
            
            # Draw path segments
            for i in range(len(path) - 1):
                node1 = lattice.nodes[path[i]]
                node2 = lattice.nodes[path[i + 1]]
                px1, py1 = self._apply_lens_effect(node1.position)
                px2, py2 = self._apply_lens_effect(node2.position)
                pygame.draw.line(path_surface, path_color, (px1, py1), (px2, py2), 1)
            
            self.screen.blit(path_surface, (0, 0))
        
        # Draw coherence metrics
        coherence = edge.coherence_metrics.get('local', 1.0)
        if coherence > 0.8:
            metric_color = self.coherence_colors['high']
        elif coherence > 0.5:
            metric_color = self.coherence_colors['medium']
        else:
            metric_color = self.coherence_colors['low']
            
        # Draw coherence indicator
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        pygame.draw.circle(self.screen, metric_color, (mid_x, mid_y), 3)
    
    def _apply_lens_effect(self, position: Tuple[float, float]) -> Tuple[int, int]:
        """Apply lensing effect to a position."""
        x = int(position[0] * self.width)
        y = int(position[1] * self.height)
        
        if self.lens_strength > 0:
            # Calculate distance from lens center
            dx = x - self.lens_center[0]
            dy = y - self.lens_center[1]
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist < self.lens_radius:
                # Calculate lens effect
                factor = (1.0 - dist / self.lens_radius) ** 2
                lens_effect = factor * self.lens_strength * 50.0
                
                # Apply lensing
                angle = math.atan2(dy, dx)
                x += int(lens_effect * math.cos(angle))
                y += int(lens_effect * math.sin(angle))
        
        return x, y
    
    def _draw_halo(self, x: int, y: int, radius: float, color: Tuple[int, int, int, int]):
        """Draw a recursive halo around a node."""
        halo_surface = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
        pygame.draw.circle(halo_surface, color, 
                         (int(radius), int(radius)), int(radius))
        self.screen.blit(halo_surface, 
                        (x - int(radius), y - int(radius)))
    
    def _get_phase_text_color(self) -> Tuple[int, int, int]:
        """Get text color based on current phase."""
        if self.current_phase == 'dawn':
            return (255, 200, 100)
        elif self.current_phase == 'day':
            return (100, 150, 255)
        elif self.current_phase == 'dusk':
            return (150, 255, 150)
        else:  # night
            return (255, 100, 150)
    
    def _lerp_color(self, color1: Tuple[int, int, int], 
                   color2: Tuple[int, int, int], 
                   t: float) -> Tuple[int, int, int]:
        """Linear interpolation between two colors."""
        return (
            int(color1[0] * (1 - t) + color2[0] * t),
            int(color1[1] * (1 - t) + color2[1] * t),
            int(color1[2] * (1 - t) + color2[2] * t)
        )
    
    def _draw_pulse(self):
        """Draw the breath pulse effect."""
        self.pulse_radius += 0.5
        if self.pulse_radius > 100:
            self.pulse_radius = 0
            
        pulse_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        center = (self.width // 2, self.height // 2)
        
        for i in range(3):
            radius = self.pulse_radius + i * 20
            alpha = 128 - i * 32
            pygame.draw.circle(pulse_surface, (*self.pulse_color[:3], alpha),
                             center, int(radius))
            
        self.screen.blit(pulse_surface, (0, 0))
        
    def _draw_ui(self, lattice: LatticeMap):
        """Draw the UI overlay."""
        # Draw title
        title = self.title_font.render("EAIN Lattice Visualization", True, self.text_color)
        self.screen.blit(title, (20, 20))
        
        # Draw state information
        state = lattice.get_lattice_state()
        y = 70
        for key, value in state.items():
            text = f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}"
            label = self.font.render(text, True, self.text_color)
            self.screen.blit(label, (20, y))
            y += 25
            
    def update(self, delta_time: float):
        """Update the renderer state."""
        self.animation_time += delta_time
        
    def cleanup(self):
        """Clean up pygame resources."""
        pygame.quit() 