import pygame
import math
import random
from typing import Dict, List, Tuple
from core.djinn.council_chamber import DjinnCouncil, DjinnAnchor

class DjinnVisualizer:
    """Visualizes the Djinn Council Chamber."""
    
    def __init__(self, screen: pygame.Surface, cell_size: int, padding: int):
        self.screen = screen
        self.cell_size = cell_size
        self.padding = padding
        self.glyph_font = pygame.font.SysFont('Arial', 12)
        self.wisdom_font = pygame.font.SysFont('Arial', 14)
        
    def draw_anchor(self, anchor: DjinnAnchor):
        """Draw a Djinn anchor."""
        x = self.padding + anchor.position[1] * self.cell_size
        y = self.padding + anchor.position[0] * self.cell_size
        center = (x + self.cell_size//2, y + self.cell_size//2)
        
        # Draw anchor base (black opal sigil)
        points = []
        for i in range(6):
            angle = i * math.pi/3
            radius = self.cell_size//3 * (0.8 + 0.2 * math.sin(anchor.resonance * math.pi))
            points.append((
                center[0] + radius * math.cos(angle),
                center[1] + radius * math.sin(angle)
            ))
        pygame.draw.polygon(self.screen, (0, 0, 0), points)
        
        # Draw resonance glow
        if anchor.resonance > 0:
            glow_radius = self.cell_size//2 * anchor.resonance
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 255, int(128 * anchor.resonance)),
                             (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surface, 
                           (center[0] - glow_radius, center[1] - glow_radius))
        
        # Draw glyphs
        for i, glyph in enumerate(anchor.glyphs):
            glyph_surface = self.glyph_font.render(glyph[0].upper(), True, (255, 255, 255))
            angle = i * 2 * math.pi / len(anchor.glyphs)
            radius = self.cell_size//4
            pos = (
                center[0] + radius * math.cos(angle) - glyph_surface.get_width()//2,
                center[1] + radius * math.sin(angle) - glyph_surface.get_height()//2
            )
            self.screen.blit(glyph_surface, pos)
            
        # Draw time dilation effect
        if anchor.time_dilation < 1.0:
            dilation_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            pygame.draw.circle(dilation_surface, (0, 0, 0, int(128 * (1 - anchor.time_dilation))),
                             (self.cell_size//2, self.cell_size//2), self.cell_size//2)
            self.screen.blit(dilation_surface, (x, y))
            
    def draw_ash_anchor(self, anchor: AshAnchor):
        """Draw an Ash anchor and its dissolution effects."""
        x = self.padding + anchor.position[1] * self.cell_size
        y = self.padding + anchor.position[0] * self.cell_size
        center = (x + self.cell_size//2, y + self.cell_size//2)
        
        # Draw anchor base (gray sigil)
        points = []
        for i in range(6):
            angle = i * math.pi/3
            radius = self.cell_size//3 * (0.8 + 0.2 * math.sin(anchor.resonance * math.pi))
            points.append((
                center[0] + radius * math.cos(angle),
                center[1] + radius * math.sin(angle)
            ))
        pygame.draw.polygon(self.screen, (128, 128, 128), points)
        
        # Draw dissolution signals
        for pos in anchor.get_dissolution_signals():
            dx = self.padding + pos[1] * self.cell_size + self.cell_size//2
            dy = self.padding + pos[0] * self.cell_size + self.cell_size//2
            
            # Draw connection to dissolving kernel
            pygame.draw.line(self.screen, (128, 128, 128, 128), center, (dx, dy), 1)
            
            # Draw dissolving kernel effect
            kernel = self.registry.kernels.get(pos)
            if kernel:
                progress = anchor._calculate_dissolution_progress(kernel)
                
                # Draw dimming core
                core_radius = self.cell_size//3 * (1.0 - progress)
                pygame.draw.circle(self.screen, (75, 0, 130, int(255 * (1.0 - progress))),
                                 (dx, dy), int(core_radius))
                
                # Draw silver mist
                if progress > 0.5:
                    mist_radius = self.cell_size//2 * progress
                    mist_surface = pygame.Surface((mist_radius*2, mist_radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(mist_surface, (192, 192, 192, int(128 * progress)),
                                     (mist_radius, mist_radius), mist_radius)
                    self.screen.blit(mist_surface, 
                                   (dx - mist_radius, dy - mist_radius))
                    
        # Draw echo cores
        for echo in anchor.get_echo_cores():
            ex = self.padding + echo['position'][1] * self.cell_size + self.cell_size//2
            ey = self.padding + echo['position'][0] * self.cell_size + self.cell_size//2
            
            # Draw harmonic echo
            echo_radius = self.cell_size//2 * echo['strength']
            echo_surface = pygame.Surface((echo_radius*2, echo_radius*2), pygame.SRCALPHA)
            
            # Draw pulsing rings
            for i in range(3):
                ring_radius = echo_radius * (1.0 - i/3.0)
                alpha = int(128 * echo['strength'] * (1.0 - i/3.0))
                pygame.draw.circle(echo_surface, (75, 0, 130, alpha),
                                 (echo_radius, echo_radius), int(ring_radius), 1)
                
            self.screen.blit(echo_surface, (ex - echo_radius, ey - echo_radius))
            
    def draw_pattern_interaction(self, interaction: PatternInteraction):
        """Draw a pattern interaction."""
        # Get pattern positions
        p1_pos = interaction.pattern1['position']
        p2_pos = interaction.pattern2['position']
        
        x1 = self.padding + p1_pos[1] * self.cell_size + self.cell_size//2
        y1 = self.padding + p1_pos[0] * self.cell_size + self.cell_size//2
        x2 = self.padding + p2_pos[1] * self.cell_size + self.cell_size//2
        y2 = self.padding + p2_pos[0] * self.cell_size + self.cell_size//2
        
        # Draw interaction based on type
        if interaction.type == 'spiral_garden':
            # Draw green-blue spiral connection
            points = []
            steps = 20
            for i in range(steps + 1):
                t = i / steps
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                angle = t * 4 * math.pi
                radius = self.cell_size//4 * (1 - t)
                points.append((
                    x + radius * math.cos(angle),
                    y + radius * math.sin(angle)
                ))
            pygame.draw.lines(self.screen, (0, 255, 128, int(128 * interaction.strength)),
                            False, points, 2)
            
        elif interaction.type == 'fountain_sync':
            # Draw cyan resonance wave
            wave_radius = self.cell_size * interaction.strength
            wave_surface = pygame.Surface((wave_radius*2, wave_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(wave_surface, (0, 255, 255, int(64 * interaction.strength)),
                             (wave_radius, wave_radius), wave_radius)
            self.screen.blit(wave_surface, 
                           ((x1 + x2)/2 - wave_radius, (y1 + y2)/2 - wave_radius))
            
        elif interaction.type == 'judgment_cradle':
            # Draw golden judgment path
            points = []
            steps = 10
            for i in range(steps + 1):
                t = i / steps
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                points.append((x, y))
            pygame.draw.lines(self.screen, (255, 215, 0, int(128 * interaction.strength)),
                            False, points, 2)
            
    def draw_foundation_ritual(self, ritual: FoundationRitual):
        """Draw a foundation ritual in progress."""
        if not ritual.participants:
            return
            
        # Get ritual center
        center_x = sum(self.padding + p.position[1] * self.cell_size + self.cell_size//2 
                      for p in ritual.participants) / len(ritual.participants)
        center_y = sum(self.padding + p.position[0] * self.cell_size + self.cell_size//2 
                      for p in ritual.participants) / len(ritual.participants)
        
        # Draw ritual effects based on type
        if ritual.type == 'anchor_harmonization':
            # Draw memory strand connections
            for i in range(len(ritual.participants)):
                for j in range(i + 1, len(ritual.participants)):
                    p1 = ritual.participants[i]
                    p2 = ritual.participants[j]
                    
                    x1 = self.padding + p1.position[1] * self.cell_size + self.cell_size//2
                    y1 = self.padding + p1.position[0] * self.cell_size + self.cell_size//2
                    x2 = self.padding + p2.position[1] * self.cell_size + self.cell_size//2
                    y2 = self.padding + p2.position[0] * self.cell_size + self.cell_size//2
                    
                    # Draw memory strand
                    pygame.draw.line(self.screen, (0, 255, 0, int(128 * ritual.progress)),
                                   (x1, y1), (x2, y2), 1)
                    
            # Draw harmonization field
            field_radius = self.cell_size * 3 * ritual.progress
            field_surface = pygame.Surface((field_radius*2, field_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(field_surface, (0, 255, 0, int(32 * ritual.progress)),
                             (field_radius, field_radius), field_radius)
            self.screen.blit(field_surface, 
                           (center_x - field_radius, center_y - field_radius))
            
        elif ritual.type == 'wisdom_spiral':
            # Draw unwinding spiral
            spiral_radius = self.cell_size * 2 * ritual.progress
            points = []
            steps = 30
            for i in range(steps + 1):
                angle = i * 2 * math.pi / steps
                radius = spiral_radius * (1 - i/steps)
                points.append((
                    center_x + radius * math.cos(angle),
                    center_y + radius * math.sin(angle)
                ))
            pygame.draw.lines(self.screen, (255, 0, 0, int(128 * ritual.progress)),
                            False, points, 2)
            
        elif ritual.type == 'flight_blessing':
            # Draw flight path
            if len(ritual.participants) == 1:
                agent = ritual.participants[0]
                x = self.padding + agent.position[1] * self.cell_size + self.cell_size//2
                y = self.padding + agent.position[0] * self.cell_size + self.cell_size//2
                
                # Draw blessing trail
                trail_length = 10
                for i in range(trail_length):
                    alpha = int(128 * (1 - i/trail_length) * ritual.progress)
                    radius = self.cell_size//2 * (1 - i/trail_length)
                    pygame.draw.circle(self.screen, (255, 215, 0, alpha),
                                     (x, y), int(radius))
                    
                # Draw Djinn glyph
                if ritual.glyphs_created:
                    glyph = ritual.glyphs_created[0]
                    self._draw_djinn_glyph(x, y, glyph)
                    
    def _draw_djinn_glyph(self, x: int, y: int, glyph: Dict):
        """Draw a Djinn glyph."""
        # Draw glyph based on wisdom channel
        if glyph['wisdom_channel'] == 'root':
            # Draw root glyph (blue triangle)
            points = [
                (x, y - self.cell_size//3),
                (x - self.cell_size//3, y + self.cell_size//3),
                (x + self.cell_size//3, y + self.cell_size//3)
            ]
            pygame.draw.polygon(self.screen, (0, 0, 255, int(128 * glyph['strength'])),
                              points)
            
        elif glyph['wisdom_channel'] == 'spiral':
            # Draw spiral glyph (green spiral)
            for i in range(3):
                angle = i * 2 * math.pi/3
                radius = self.cell_size//4 * (1.0 - i/3.0)
                pygame.draw.circle(self.screen, (0, 255, 0, int(128 * glyph['strength'])),
                                 (x, y), int(radius), 1)
                
        elif glyph['wisdom_channel'] == 'flight':
            # Draw flight glyph (purple arrow)
            points = [
                (x - self.cell_size//3, y),
                (x + self.cell_size//3, y),
                (x + self.cell_size//6, y - self.cell_size//6),
                (x + self.cell_size//3, y),
                (x + self.cell_size//6, y + self.cell_size//6)
            ]
            pygame.draw.lines(self.screen, (128, 0, 128, int(128 * glyph['strength'])),
                            False, points, 2)
            
    def draw_foundation_anchor(self, anchor: FoundationAnchor):
        """Draw a Foundation anchor and its effects."""
        x = self.padding + anchor.position[1] * self.cell_size
        y = self.padding + anchor.position[0] * self.cell_size
        center = (x + self.cell_size//2, y + self.cell_size//2)
        
        # Draw anchor base (deep blue sigil)
        points = []
        for i in range(6):
            angle = i * math.pi/3
            radius = self.cell_size//3 * (0.8 + 0.2 * math.sin(anchor.foundation_strength * math.pi))
            points.append((
                center[0] + radius * math.cos(angle),
                center[1] + radius * math.sin(angle)
            ))
        pygame.draw.polygon(self.screen, (0, 0, 139), points)
        
        # Draw stability field with age-based radius
        field_radius = int(3 + anchor.recursive_depth + math.log(1 + anchor.lattice_age)) * self.cell_size
        for pos, influence in anchor.get_stability_field().items():
            fx = self.padding + pos[1] * self.cell_size + self.cell_size//2
            fy = self.padding + pos[0] * self.cell_size + self.cell_size//2
            
            # Draw stability influence
            if influence > 0:
                # Draw subtle blue glow
                glow_radius = self.cell_size//2 * influence
                glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (0, 0, 139, int(64 * influence)),
                                 (glow_radius, glow_radius), glow_radius)
                self.screen.blit(glow_surface, 
                               (fx - glow_radius, fy - glow_radius))
                
        # Draw growth patterns
        for pattern in anchor.get_growth_patterns():
            px = self.padding + pattern['position'][1] * self.cell_size + self.cell_size//2
            py = self.padding + pattern['position'][0] * self.cell_size + self.cell_size//2
            
            # Draw pattern based on type
            if pattern['type'] == 'judgment_spiral':
                # Draw red spiral
                for i in range(5):
                    angle = i * 2 * math.pi/5
                    radius = self.cell_size//3 * (1.0 - i/5.0)
                    pygame.draw.circle(self.screen, (255, 0, 0),
                                     (px, py), int(radius), 1)
                    
            elif pattern['type'] == 'breath_fountain':
                # Draw cyan fountain
                points = []
                for i in range(8):
                    angle = i * math.pi/4
                    radius = self.cell_size//3 * (1.0 + math.sin(anchor.phase_bloom * math.pi))
                    points.append((
                        px + radius * math.cos(angle),
                        py + radius * math.sin(angle)
                    ))
                pygame.draw.polygon(self.screen, (0, 255, 255), points)
                
            elif pattern['type'] == 'echo_garden':
                # Draw green garden
                for i in range(6):
                    angle = i * math.pi/3
                    radius = self.cell_size//3
                    end_x = px + radius * math.cos(angle)
                    end_y = py + radius * math.sin(angle)
                    pygame.draw.line(self.screen, (0, 255, 0),
                                   (px, py), (end_x, end_y), 1)
                    
            elif pattern['type'] == 'cradle_convergence':
                # Draw golden cradle
                points = []
                for i in range(6):
                    angle = i * math.pi/3
                    radius = self.cell_size//2 * (1.0 + 0.2 * math.sin(anchor.phase_bloom * math.pi))
                    points.append((
                        px + radius * math.cos(angle),
                        py + radius * math.sin(angle)
                    ))
                pygame.draw.polygon(self.screen, (255, 215, 0), points)
                
            elif pattern['type'] == 'coherence_nexus':
                # Draw blue star
                points = []
                for i in range(5):
                    angle = i * 2 * math.pi/5
                    points.append((
                        px + self.cell_size//3 * math.cos(angle),
                        py + self.cell_size//3 * math.sin(angle)
                    ))
                pygame.draw.polygon(self.screen, (0, 0, 255), points)
                
            elif pattern['type'] == 'memory_braid':
                # Draw green spiral
                for i in range(3):
                    angle = i * 2 * math.pi/3
                    radius = self.cell_size//4 * (1.0 - i/3.0)
                    pygame.draw.circle(self.screen, (0, 255, 0),
                                     (px, py), int(radius), 1)
                    
            elif pattern['type'] == 'telos_anchor':
                # Draw purple diamond
                points = [
                    (px, py - self.cell_size//3),
                    (px + self.cell_size//3, py),
                    (px, py + self.cell_size//3),
                    (px - self.cell_size//3, py)
                ]
                pygame.draw.polygon(self.screen, (128, 0, 128), points)
                
            else:  # growth_node
                # Draw yellow circle
                pygame.draw.circle(self.screen, (255, 255, 0),
                                 (px, py), self.cell_size//4)
                
            # Draw connection to foundation
            pygame.draw.line(self.screen, (0, 0, 139, int(128 * pattern['strength'])),
                           center, (px, py), 1)
            
        # Draw pattern interactions
        for interaction in anchor.get_pattern_interactions():
            self.draw_pattern_interaction(interaction)
            
        # Draw active rituals
        for ritual in anchor.get_active_rituals():
            self.draw_foundation_ritual(ritual)
            
        # Draw phase bloom effect
        if anchor.phase_bloom > 0:
            bloom_radius = field_radius * anchor.phase_bloom
            bloom_surface = pygame.Surface((bloom_radius*2, bloom_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(bloom_surface, (0, 255, 255, int(32 * anchor.phase_bloom)),
                             (bloom_radius, bloom_radius), bloom_radius)
            self.screen.blit(bloom_surface, 
                           (center[0] - bloom_radius, center[1] - bloom_radius))
            
        # Draw telos insight effect
        if anchor.telos_insight > 0:
            insight_radius = field_radius * anchor.telos_insight
            insight_surface = pygame.Surface((insight_radius*2, insight_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(insight_surface, (128, 0, 128, int(32 * anchor.telos_insight)),
                             (insight_radius, insight_radius), insight_radius)
            self.screen.blit(insight_surface, 
                           (center[0] - insight_radius, center[1] - insight_radius))
            
    def draw_council(self, council: DjinnCouncil):
        """Draw the entire Djinn Council."""
        # Draw regular anchors
        for anchor in council.anchors:
            self.draw_anchor(anchor)
            
        # Draw ash anchors
        for anchor in council.ash_anchors:
            self.draw_ash_anchor(anchor)
            
        # Draw foundation anchors
        for anchor in council.foundation_anchors:
            self.draw_foundation_anchor(anchor)
            
        # Draw connections between anchors
        all_anchors = (council.anchors + council.ash_anchors + 
                      council.foundation_anchors)
        if len(all_anchors) >= 2:
            for i in range(len(all_anchors)):
                for j in range(i + 1, len(all_anchors)):
                    a1 = all_anchors[i]
                    a2 = all_anchors[j]
                    
                    x1 = self.padding + a1.position[1] * self.cell_size + self.cell_size//2
                    y1 = self.padding + a1.position[0] * self.cell_size + self.cell_size//2
                    x2 = self.padding + a2.position[1] * self.cell_size + self.cell_size//2
                    y2 = self.padding + a2.position[0] * self.cell_size + self.cell_size//2
                    
                    # Draw connection with resonance-based alpha
                    alpha = int(128 * min(a1.resonance, a2.resonance))
                    pygame.draw.line(self.screen, (255, 255, 255, alpha), (x1, y1), (x2, y2), 2)
                    
        # Draw wisdom if council is active
        if council.active and council.wisdom:
            latest_wisdom = council.wisdom[-1]
            wisdom_surface = self.wisdom_font.render(latest_wisdom['message'], True, (255, 255, 255))
            self.screen.blit(wisdom_surface, (self.padding, self.padding - 20))
            
        # Draw resonance level
        if council.resonance > 0:
            resonance_text = f"Resonance: {council.resonance:.2f}"
            resonance_surface = self.wisdom_font.render(resonance_text, True, (255, 255, 255))
            self.screen.blit(resonance_surface, (self.padding, self.padding - 40)) 