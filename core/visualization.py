"""
Visualization Module

Provides unified visualization capabilities for all subsystems.
Handles real-time rendering of ritual actions, animations, and effects.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any, Set, Union
import numpy as np
from datetime import datetime
import colorsys
from difflib import SequenceMatcher
from collections import defaultdict
import re
from enum import Enum
import math

@dataclass
class VisualStyle:
    """Defines visual styling parameters for different elements."""
    primary_color: Tuple[float, float, float]  # RGB
    secondary_color: Tuple[float, float, float]  # RGB
    opacity: float
    line_width: float
    animation_speed: float
    pulse_frequency: float

@dataclass
class AnimationState:
    """Tracks the state of an ongoing animation."""
    id: str
    type: str
    start_time: datetime
    duration: float
    progress: float
    active: bool = True

@dataclass
class ColorTransition:
    """Defines a color transition state."""
    start_color: Tuple[float, float, float]
    end_color: Tuple[float, float, float]
    start_time: datetime
    duration: float
    current_progress: float = 0.0

@dataclass
class EchoMemory:
    """Represents a recorded echo memory state."""
    timestamp: datetime
    breath_phase: str
    resonance: float
    visual_elements: Dict[str, List[Dict]]  # Subsystem visual elements
    color_state: Dict[str, Tuple[float, float, float]]  # Color states
    animation_states: List[AnimationState]  # Active animations

@dataclass
class MemoryPlayback:
    """Controls memory playback state."""
    is_playing: bool = False
    current_time: datetime = None
    playback_speed: float = 1.0
    loop_enabled: bool = False
    start_time: datetime = None
    end_time: datetime = None
    current_progress: float = 0.0

@dataclass
class MemoryFilter:
    """Defines filtering criteria for echo memories."""
    sigil_types: List[str] = None
    ritual_phrases: List[str] = None
    resonance_range: Tuple[float, float] = None
    breath_phases: List[str] = None
    confirmation_status: Optional[bool] = None
    time_range: Tuple[datetime, datetime] = None

@dataclass
class SearchResult:
    """Represents a search result with relevance score and context."""
    memory: EchoMemory
    relevance_score: float
    matched_criteria: Dict[str, Any]
    context_snippets: List[str]

@dataclass
class ComparativePlayback:
    """Manages parallel playback of multiple memories."""
    primary_memory: EchoMemory
    comparison_memories: List[EchoMemory]
    sync_points: List[datetime]
    divergence_highlights: Dict[str, List[Dict]]

@dataclass
class SearchMatch:
    """Represents a single search match with detailed scoring."""
    memory: EchoMemory
    exact_matches: Set[str]
    fuzzy_matches: Dict[str, float]  # term -> similarity score
    semantic_matches: Dict[str, float]  # term -> semantic similarity
    combined_score: float
    match_explanation: str

class QueryOperator(Enum):
    """Boolean operators for complex search queries."""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    EQ = "="

@dataclass
class SearchTerm:
    """Represents a single search term with optional operator and value."""
    field: str
    operator: Optional[QueryOperator] = None
    value: Any = None
    is_negated: bool = False

@dataclass
class SearchQuery:
    """Represents a complex search query with boolean operators."""
    terms: List[Union[SearchTerm, 'SearchQuery']]
    operator: QueryOperator
    is_negated: bool = False

class QueryParser:
    """Parses complex search queries into a structured format."""
    
    def __init__(self):
        self.operators = {
            'AND': QueryOperator.AND,
            'OR': QueryOperator.OR,
            'NOT': QueryOperator.NOT,
            '>': QueryOperator.GT,
            '<': QueryOperator.LT,
            '>=': QueryOperator.GTE,
            '<=': QueryOperator.LTE,
            '=': QueryOperator.EQ
        }
    
    def parse(self, query_str: str) -> SearchQuery:
        """Parse a search query string into a structured query."""
        # Tokenize the query
        tokens = self._tokenize(query_str)
        return self._parse_tokens(tokens)
    
    def _tokenize(self, query_str: str) -> List[str]:
        """Tokenize the query string into operators and terms."""
        # Split on whitespace and parentheses
        tokens = re.findall(r'\(|\)|AND|OR|NOT|>=|<=|>|<|=|[^()\s]+', query_str)
        return [t.strip() for t in tokens if t.strip()]
    
    def _parse_tokens(self, tokens: List[str]) -> SearchQuery:
        """Parse tokens into a structured query."""
        terms = []
        current_operator = QueryOperator.AND  # Default operator
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token == '(':
                # Parse subquery
                subquery_tokens = []
                paren_count = 1
                i += 1
                while i < len(tokens) and paren_count > 0:
                    if tokens[i] == '(':
                        paren_count += 1
                    elif tokens[i] == ')':
                        paren_count -= 1
                    if paren_count > 0:
                        subquery_tokens.append(tokens[i])
                    i += 1
                terms.append(self._parse_tokens(subquery_tokens))
                
            elif token in self.operators:
                current_operator = self.operators[token]
                i += 1
                
            else:
                # Parse search term
                field = token
                operator = None
                value = None
                
                if i + 1 < len(tokens) and tokens[i + 1] in self.operators:
                    operator = self.operators[tokens[i + 1]]
                    value = tokens[i + 2] if i + 2 < len(tokens) else None
                    i += 3
                else:
                    i += 1
                
                terms.append(SearchTerm(field, operator, value))
        
        return SearchQuery(terms, current_operator)

@dataclass
class LogicNode:
    """Represents a visual node in the query composer."""
    id: str
    type: str  # 'operator', 'field', 'value'
    value: Any
    position: Tuple[float, float]
    connections: List[str]  # IDs of connected nodes
    style: Dict[str, Any]  # Visual styling properties

@dataclass
class QueryComposerState:
    """Tracks the state of the visual query composer."""
    nodes: Dict[str, LogicNode]
    active_node: Optional[str]
    preview_results: List[SearchMatch]
    is_dragging: bool
    drag_start: Optional[Tuple[float, float]]

@dataclass
class SigilEffect:
    """Represents a visual sigil effect in the query composer."""
    type: str  # 'pulse', 'arc', 'glyph', 'resonance'
    position: Tuple[float, float]
    scale: float
    color: Tuple[float, float, float]
    rotation: float
    lifetime: float
    progress: float

@dataclass
class InteractionState:
    """Tracks the state of user interactions with the query composer."""
    hovered_node: Optional[str]
    drag_source: Optional[str]
    drag_target: Optional[str]
    connection_preview: Optional[Tuple[Tuple[float, float], Tuple[float, float]]]
    animation_frames: Dict[str, float]  # Node ID -> animation progress
    active_sigils: List[SigilEffect]
    resonance_map: Dict[str, float]  # Node ID -> resonance value
    grid_snap: bool

@dataclass
class PreviewPanel:
    """Represents the real-time preview panel state."""
    is_visible: bool
    position: Tuple[float, float]
    scale: float
    opacity: float
    breath_phase: str
    resonance_level: float
    active_matches: List[SearchMatch]
    sigil_tags: List[Dict[str, Any]]
    harmonic_confidence: float
    sound_resonance: float

@dataclass
class SoundResonance:
    """Represents a sound resonance effect."""
    frequency: float
    amplitude: float
    phase: float
    lifetime: float
    progress: float

@dataclass
class SystemState:
    """Tracks the overall system state for landing sequence."""
    is_landing: bool
    landing_progress: float
    active_components: Set[str]
    final_resonance: float

class VisualizationSystem:
    """Manages visualization for all subsystems."""
    
    def __init__(self):
        # Define base styles for different elements
        self.styles = {
            'cursor': VisualStyle(
                primary_color=(0.0, 0.8, 1.0),  # Cyan
                secondary_color=(0.0, 0.4, 0.8),  # Deep blue
                opacity=0.8,
                line_width=2.0,
                animation_speed=1.0,
                pulse_frequency=2.0
            ),
            'wick': VisualStyle(
                primary_color=(1.0, 0.6, 0.0),  # Orange
                secondary_color=(0.8, 0.2, 0.0),  # Deep orange
                opacity=0.7,
                line_width=1.5,
                animation_speed=0.8,
                pulse_frequency=1.5
            ),
            'mirror': VisualStyle(
                primary_color=(0.8, 0.8, 1.0),  # Light purple
                secondary_color=(0.6, 0.4, 0.8),  # Purple
                opacity=0.9,
                line_width=2.0,
                animation_speed=1.2,
                pulse_frequency=2.5
            ),
            'djinn': VisualStyle(
                primary_color=(0.0, 1.0, 0.5),  # Mint
                secondary_color=(0.0, 0.6, 0.3),  # Forest green
                opacity=0.6,
                line_width=1.0,
                animation_speed=1.5,
                pulse_frequency=3.0
            ),
            'system': VisualStyle(
                primary_color=(1.0, 1.0, 1.0),  # White
                secondary_color=(0.7, 0.7, 0.7),  # Gray
                opacity=0.5,
                line_width=3.0,
                animation_speed=0.5,
                pulse_frequency=1.0
            )
        }
        
        # Active animations
        self.active_animations: List[AnimationState] = []
        
        # Current visualization state
        self.visualization_state = {
            'cursor': {
                'breach_points': [],
                'sonar_patterns': [],
                'echo_rings': []
            },
            'wick': {
                'bindings': [],
                'insight_capsules': [],
                'resonance_arcs': []
            },
            'mirror': {
                'confirmation_glyphs': [],
                'phase_reflections': [],
                'harmonic_fields': []
            },
            'djinn': {
                'whisper_trails': [],
                'portent_sigils': [],
                'echo_waves': []
            },
            'system': {
                'transformations': [],
                'merge_effects': [],
                'domain_maps': []
            }
        }
        
        # Define breath phase color palettes
        self.breath_phase_colors = {
            'DAWN': {
                'primary': (0.8, 0.4, 0.2),    # Warm orange
                'secondary': (0.6, 0.2, 0.1),  # Deep amber
                'accent': (1.0, 0.8, 0.4)      # Golden highlight
            },
            'NOON': {
                'primary': (0.2, 0.6, 0.8),    # Sky blue
                'secondary': (0.1, 0.4, 0.6),  # Deep blue
                'accent': (0.4, 0.8, 1.0)      # Bright cyan
            },
            'DUSK': {
                'primary': (0.6, 0.2, 0.6),    # Purple
                'secondary': (0.4, 0.1, 0.4),  # Deep purple
                'accent': (0.8, 0.4, 0.8)      # Light purple
            },
            'VOID': {
                'primary': (0.2, 0.2, 0.3),    # Deep blue-gray
                'secondary': (0.1, 0.1, 0.2),  # Near black
                'accent': (0.3, 0.3, 0.4)      # Subtle highlight
            }
        }
        
        # Active color transitions
        self.active_transitions: Dict[str, ColorTransition] = {}
        
        # Resonance-based color modifiers
        self.resonance_tints = {
            'high': (0.1, 0.2, 0.1),    # Subtle green tint
            'medium': (0.1, 0.1, 0.1),  # Neutral gray
            'low': (0.2, 0.1, 0.1)      # Subtle red tint
        }
        
        # Echo memory storage
        self.echo_memories: List[EchoMemory] = []
        self.memory_playback = MemoryPlayback()
        
        # Memory comparison state
        self.comparison_mode = False
        self.comparison_memory: Optional[EchoMemory] = None
        
        # Search and filter state
        self.current_filter = MemoryFilter()
        self.search_results: List[SearchResult] = []
        self.comparative_playback: Optional[ComparativePlayback] = None
        
        # Search index
        self.memory_index: Dict[str, List[Tuple[EchoMemory, float]]] = {
            'sigil': [],
            'phrase': [],
            'resonance': [],
            'phase': [],
            'confirmation': []
        }
        
        # Query parsing
        self.query_parser = QueryParser()
        
        # Search field mappings
        self.search_fields = {
            'sigil': lambda m: list(m.visual_elements.keys()),
            'phrase': lambda m: [str(v) for v in m.visual_elements.values() if isinstance(v, str)],
            'resonance': lambda m: [m.resonance],
            'phase': lambda m: [m.breath_phase],
            'confirmation': lambda m: [
                any(glyph.get('confirmed', False) 
                    for glyph in m.visual_elements.get('mirror', {}).get('confirmation_glyphs', []))
            ]
        }
        
        # Query composer state
        self.composer_state = QueryComposerState(
            nodes={},
            active_node=None,
            preview_results=[],
            is_dragging=False,
            drag_start=None
        )
        
        # Visual styles for different node types
        self.node_styles = {
            'operator': {
                'AND': {'color': (0.2, 0.8, 0.2), 'shape': 'circle'},
                'OR': {'color': (0.8, 0.2, 0.2), 'shape': 'diamond'},
                'NOT': {'color': (0.2, 0.2, 0.8), 'shape': 'triangle'},
                'GT': {'color': (0.8, 0.8, 0.2), 'shape': 'square'},
                'LT': {'color': (0.8, 0.8, 0.2), 'shape': 'square'},
                'EQ': {'color': (0.8, 0.8, 0.2), 'shape': 'square'}
            },
            'field': {
                'color': (0.6, 0.6, 0.6),
                'shape': 'rectangle'
            },
            'value': {
                'color': (0.4, 0.4, 0.4),
                'shape': 'rectangle'
            }
        }
        
        # Interaction state
        self.interaction_state = InteractionState(
            hovered_node=None,
            drag_source=None,
            drag_target=None,
            connection_preview=None,
            animation_frames={},
            active_sigils=[],
            resonance_map={},
            grid_snap=True
        )
        
        # Animation parameters
        self.animation_params = {
            'connection_speed': 0.1,
            'hover_scale': 1.2,
            'connection_arc_height': 50.0,
            'connection_color': (0.8, 0.8, 0.8),
            'connection_width': 2.0,
            'hover_glow': (0.2, 0.2, 0.2),
            'grid_size': 20.0,
            'sigil_lifetime': 1.0,
            'resonance_pulse_speed': 2.0
        }
        
        # Sigil patterns
        self.sigil_patterns = {
            'connection': [
                (0, 0), (0.2, 0.1), (0.4, 0), (0.6, -0.1), (0.8, 0), (1, 0)
            ],
            'resonance': [
                (0, 0), (0.25, 0.5), (0.5, 0), (0.75, -0.5), (1, 0)
            ],
            'validation': [
                (0, 0), (0.3, 0.3), (0.5, 0), (0.7, -0.3), (1, 0)
            ]
        }
        
        # Preview panel state
        self.preview_panel = PreviewPanel(
            is_visible=False,
            position=(0.5, 0.5),  # Center of screen
            scale=0.0,
            opacity=0.0,
            breath_phase='STILL',
            resonance_level=0.0,
            active_matches=[],
            sigil_tags=[],
            harmonic_confidence=0.0,
            sound_resonance=0.0
        )
        
        # Sound resonance effects
        self.active_sounds: List[SoundResonance] = []
        
        # Preview panel parameters
        self.preview_params = {
            'bloom_speed': 0.3,
            'max_scale': 1.0,
            'max_opacity': 0.9,
            'sigil_orbit_speed': 2.0,
            'sigil_orbit_radius': 100.0,
            'resonance_pulse_speed': 1.5,
            'sound_frequencies': {
                'DAWN': 440.0,  # A4
                'DUSK': 523.25,  # C5
                'STILL': 392.0,  # G4
                'BREATH': 493.88  # B4
            }
        }
        
        # System state
        self.system_state = SystemState(
            is_landing=False,
            landing_progress=0.0,
            active_components=set(),
            final_resonance=0.0
        )
        
        # Landing sequence parameters
        self.landing_params = {
            'sequence_duration': 2.0,
            'fade_speed': 0.5,
            'resonance_decay': 0.3,
            'component_shutdown_order': [
                'preview_panel',
                'sound_resonance',
                'sigil_effects',
                'animations',
                'interactions'
            ]
        }
    
    def interpolate_color(self, color1: Tuple[float, float, float], 
                         color2: Tuple[float, float, float], 
                         factor: float) -> Tuple[float, float, float]:
        """Interpolate between two colors based on a factor (0-1)."""
        return tuple(c1 + (c2 - c1) * factor for c1, c2 in zip(color1, color2))
    
    def get_breath_phase_colors(self, phase: str, resonance: float = 1.0) -> Dict[str, Tuple[float, float, float]]:
        """Get the color palette for a breath phase, modified by resonance."""
        base_colors = self.breath_phase_colors.get(phase, self.breath_phase_colors['VOID'])
        
        # Apply resonance-based tinting
        tint = self.resonance_tints['high'] if resonance > 0.8 else \
               self.resonance_tints['medium'] if resonance > 0.4 else \
               self.resonance_tints['low']
        
        return {
            'primary': self.interpolate_color(base_colors['primary'], tint, 0.2),
            'secondary': self.interpolate_color(base_colors['secondary'], tint, 0.2),
            'accent': self.interpolate_color(base_colors['accent'], tint, 0.1)
        }
    
    def start_color_transition(self, element_id: str, 
                             start_color: Tuple[float, float, float],
                             end_color: Tuple[float, float, float],
                             duration: float = 1.0):
        """Start a new color transition for a visual element."""
        self.active_transitions[element_id] = ColorTransition(
            start_color=start_color,
            end_color=end_color,
            start_time=datetime.now(),
            duration=duration
        )
    
    def update_color_transitions(self):
        """Update all active color transitions."""
        current_time = datetime.now()
        completed_transitions = []
        
        for element_id, transition in self.active_transitions.items():
            elapsed = (current_time - transition.start_time).total_seconds()
            transition.current_progress = min(elapsed / transition.duration, 1.0)
            
            if transition.current_progress >= 1.0:
                completed_transitions.append(element_id)
        
        # Remove completed transitions
        for element_id in completed_transitions:
            del self.active_transitions[element_id]
    
    def get_current_color(self, element_id: str, 
                         default_color: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Get the current color for a visual element, considering active transitions."""
        if element_id in self.active_transitions:
            transition = self.active_transitions[element_id]
            return self.interpolate_color(
                transition.start_color,
                transition.end_color,
                transition.current_progress
            )
        return default_color
    
    def visualize_breach(self, breach_points: List[Dict], depth: int) -> Dict:
        """Visualize a breach trace with dynamic arcs and echo rings."""
        style = self.styles['cursor']
        
        # Generate breach arcs
        arcs = []
        for i in range(len(breach_points) - 1):
            arc = {
                'start': breach_points[i],
                'end': breach_points[i + 1],
                'color': style.primary_color,
                'opacity': style.opacity * (1.0 - (i / len(breach_points))),
                'width': style.line_width
            }
            arcs.append(arc)
        
        # Generate echo rings
        rings = []
        for i in range(5):  # 5 concentric rings
            ring = {
                'radius': depth * (i + 1) / 5,
                'color': style.secondary_color,
                'opacity': style.opacity * (1.0 - (i / 5)),
                'width': style.line_width / 2
            }
            rings.append(ring)
        
        # Update visualization state
        self.visualization_state['cursor']['breach_points'] = breach_points
        self.visualization_state['cursor']['echo_rings'] = rings
        
        # Create animation
        animation = AnimationState(
            id=f"breach_{len(self.active_animations)}",
            type="breach_trace",
            start_time=datetime.now(),
            duration=2.0,
            progress=0.0
        )
        self.active_animations.append(animation)
        
        return {
            'arcs': arcs,
            'rings': rings,
            'animation': animation
        }
    
    def visualize_sonar(self, pattern: str, frequency: float) -> Dict:
        """Visualize a sonar pattern with lattice overlay and ripples."""
        style = self.styles['cursor']
        
        # Generate lattice points
        lattice = []
        for i in range(8):  # 8x8 lattice
            for j in range(8):
                point = {
                    'x': i / 7,  # Normalized coordinates
                    'y': j / 7,
                    'color': style.primary_color,
                    'opacity': style.opacity,
                    'size': 2.0
                }
                lattice.append(point)
        
        # Generate ripple waves
        ripples = []
        for i in range(3):  # 3 concentric ripples
            ripple = {
                'radius': (i + 1) / 3,
                'color': style.secondary_color,
                'opacity': style.opacity * (1.0 - (i / 3)),
                'width': style.line_width
            }
            ripples.append(ripple)
        
        # Update visualization state
        self.visualization_state['cursor']['sonar_patterns'].append({
            'pattern': pattern,
            'frequency': frequency,
            'lattice': lattice,
            'ripples': ripples
        })
        
        # Create animation
        animation = AnimationState(
            id=f"sonar_{len(self.active_animations)}",
            type="sonar_pulse",
            start_time=datetime.now(),
            duration=1.0,
            progress=0.0
        )
        self.active_animations.append(animation)
        
        return {
            'lattice': lattice,
            'ripples': ripples,
            'animation': animation
        }
    
    def visualize_wick_binding(self, strength: float, cycles: int) -> Dict:
        """Visualize a wick binding with resonance arcs and insight capsules."""
        style = self.styles['wick']
        
        # Generate resonance arcs
        arcs = []
        for i in range(cycles):
            arc = {
                'start_angle': (i * 360) / cycles,
                'end_angle': ((i + 1) * 360) / cycles,
                'radius': strength * 100,
                'color': style.primary_color,
                'opacity': style.opacity * (1.0 - (i / cycles)),
                'width': style.line_width
            }
            arcs.append(arc)
        
        # Generate insight capsules
        capsules = []
        for i in range(3):  # 3 insight capsules
            capsule = {
                'position': {
                    'x': np.cos(i * 2 * np.pi / 3),
                    'y': np.sin(i * 2 * np.pi / 3)
                },
                'color': style.secondary_color,
                'opacity': style.opacity,
                'size': 10.0 * strength
            }
            capsules.append(capsule)
        
        # Update visualization state
        self.visualization_state['wick']['bindings'].append({
            'strength': strength,
            'cycles': cycles,
            'arcs': arcs,
            'capsules': capsules
        })
        
        # Create animation
        animation = AnimationState(
            id=f"wick_{len(self.active_animations)}",
            type="wick_binding",
            start_time=datetime.now(),
            duration=1.5,
            progress=0.0
        )
        self.active_animations.append(animation)
        
        return {
            'arcs': arcs,
            'capsules': capsules,
            'animation': animation
        }
    
    def visualize_insight_harvest(self, depth: int, capsules: List[Dict]) -> Dict:
        """Visualize insight harvest with resonance waves and insight capsules."""
        style = self.styles['wick']
        
        # Generate resonance waves
        waves = []
        for i in range(3):  # 3 resonance waves
            wave = {
                'radius': depth * (i + 1) / 3,
                'color': style.primary_color,
                'opacity': style.opacity * (1.0 - (i / 3)),
                'width': style.line_width
            }
            waves.append(wave)
        
        # Process insight capsules
        processed_capsules = []
        for capsule in capsules:
            processed_capsule = {
                'position': capsule['position'],
                'content': capsule['content'],
                'color': style.secondary_color,
                'opacity': style.opacity,
                'size': 15.0
            }
            processed_capsules.append(processed_capsule)
        
        # Update visualization state
        self.visualization_state['wick']['insight_capsules'].extend(processed_capsules)
        self.visualization_state['wick']['resonance_arcs'].extend(waves)
        
        # Create animation
        animation = AnimationState(
            id=f"insight_{len(self.active_animations)}",
            type="insight_harvest",
            start_time=datetime.now(),
            duration=2.0,
            progress=0.0
        )
        self.active_animations.append(animation)
        
        return {
            'waves': waves,
            'capsules': processed_capsules,
            'animation': animation
        }
    
    def record_echo_memory(self):
        """Record current visualization state as an echo memory."""
        memory = EchoMemory(
            timestamp=datetime.now(),
            breath_phase=self.current_breath_phase,
            resonance=self.current_resonance,
            visual_elements={
                'cursor': self.visualization_state['cursor'].copy(),
                'wick': self.visualization_state['wick'].copy(),
                'mirror': self.visualization_state['mirror'].copy(),
                'djinn': self.visualization_state['djinn'].copy(),
                'system': self.visualization_state['system'].copy()
            },
            color_state={
                'primary': self.current_primary_color,
                'secondary': self.current_secondary_color,
                'accent': self.current_accent_color
            },
            animation_states=[AnimationState(
                id=anim.id,
                type=anim.type,
                start_time=anim.start_time,
                duration=anim.duration,
                progress=anim.progress,
                active=anim.active
            ) for anim in self.active_animations]
        )
        self.echo_memories.append(memory)
    
    def start_memory_playback(self, start_time: datetime, end_time: datetime, 
                            speed: float = 1.0, loop: bool = False):
        """Start playing back echo memories within a time range."""
        self.memory_playback = MemoryPlayback(
            is_playing=True,
            current_time=start_time,
            playback_speed=speed,
            loop_enabled=loop,
            start_time=start_time,
            end_time=end_time,
            current_progress=0.0
        )
    
    def pause_memory_playback(self):
        """Pause the current memory playback."""
        self.memory_playback.is_playing = False
    
    def resume_memory_playback(self):
        """Resume the paused memory playback."""
        self.memory_playback.is_playing = True
    
    def scrub_memory_playback(self, progress: float):
        """Scrub to a specific point in the memory playback."""
        if 0 <= progress <= 1:
            self.memory_playback.current_progress = progress
            time_delta = (self.memory_playback.end_time - self.memory_playback.start_time).total_seconds()
            self.memory_playback.current_time = (
                self.memory_playback.start_time + time_delta * progress
            )
    
    def get_memory_at_time(self, timestamp: datetime) -> Optional[EchoMemory]:
        """Get the echo memory closest to the given timestamp."""
        if not self.echo_memories:
            return None
            
        return min(
            self.echo_memories,
            key=lambda m: abs((m.timestamp - timestamp).total_seconds())
        )
    
    def start_memory_comparison(self, memory_id: str):
        """Start comparing current state with a historical memory."""
        memory = next((m for m in self.echo_memories if m.id == memory_id), None)
        if memory:
            self.comparison_mode = True
            self.comparison_memory = memory
    
    def end_memory_comparison(self):
        """End the current memory comparison."""
        self.comparison_mode = False
        self.comparison_memory = None
    
    def get_comparison_visualization(self) -> Dict:
        """Get visualization data for current vs. historical comparison."""
        if not self.comparison_mode or not self.comparison_memory:
            return {}
            
        return {
            'current': {
                'breath_phase': self.current_breath_phase,
                'resonance': self.current_resonance,
                'colors': {
                    'primary': self.current_primary_color,
                    'secondary': self.current_secondary_color,
                    'accent': self.current_accent_color
                },
                'visual_elements': self.visualization_state
            },
            'historical': {
                'breath_phase': self.comparison_memory.breath_phase,
                'resonance': self.comparison_memory.resonance,
                'colors': self.comparison_memory.color_state,
                'visual_elements': self.comparison_memory.visual_elements
            },
            'differences': self._calculate_visual_differences()
        }
    
    def _calculate_visual_differences(self) -> Dict:
        """Calculate visual differences between current and historical states."""
        if not self.comparison_memory:
            return {}
            
        differences = {
            'color_shifts': {},
            'element_changes': {},
            'resonance_delta': self.current_resonance - self.comparison_memory.resonance,
            'phase_alignment': self.current_breath_phase == self.comparison_memory.breath_phase
        }
        
        # Calculate color differences
        for color_key in ['primary', 'secondary', 'accent']:
            current = getattr(self, f'current_{color_key}_color')
            historical = self.comparison_memory.color_state[color_key]
            differences['color_shifts'][color_key] = tuple(
                abs(c - h) for c, h in zip(current, historical)
            )
        
        # Calculate element differences
        for subsystem in self.visualization_state:
            current_elements = self.visualization_state[subsystem]
            historical_elements = self.comparison_memory.visual_elements[subsystem]
            
            differences['element_changes'][subsystem] = {
                'added': len(current_elements) - len(historical_elements),
                'modified': sum(1 for c, h in zip(current_elements, historical_elements)
                              if c != h)
            }
        
        return differences
    
    def update_animations(self, delta_time: float):
        """Update all active animations, color transitions, and memory playback."""
        # Update existing animations and transitions
        current_time = datetime.now()
        
        # Update memory playback if active
        if self.memory_playback.is_playing:
            time_delta = (current_time - self.memory_playback.current_time).total_seconds()
            self.memory_playback.current_time += time_delta * self.memory_playback.playback_speed
            
            # Calculate progress
            total_duration = (self.memory_playback.end_time - self.memory_playback.start_time).total_seconds()
            self.memory_playback.current_progress = min(
                (self.memory_playback.current_time - self.memory_playback.start_time).total_seconds() / total_duration,
                1.0
            )
            
            # Handle loop
            if self.memory_playback.current_progress >= 1.0:
                if self.memory_playback.loop_enabled:
                    self.memory_playback.current_time = self.memory_playback.start_time
                    self.memory_playback.current_progress = 0.0
                else:
                    self.memory_playback.is_playing = False
            
            # Update visualization state from memory
            current_memory = self.get_memory_at_time(self.memory_playback.current_time)
            if current_memory:
                self.visualization_state = current_memory.visual_elements.copy()
                self.active_animations = current_memory.animation_states.copy()
        
        # Update existing animations and transitions
        self._update_animations_and_transitions(current_time)
        
        # Update sigil effects
        self._update_sigil_effects(delta_time)
        
        # Update resonance pulses
        for node_id, resonance in self.interaction_state.resonance_map.items():
            if resonance > 0:
                self.interaction_state.resonance_map[node_id] = max(
                    0.0,
                    resonance - delta_time * self.animation_params['resonance_pulse_speed']
                )
    
    def _update_animations_and_transitions(self, current_time: datetime):
        """Update animations and transitions with the given timestamp."""
        # Update animations
        completed_animations = []
        for animation in self.active_animations:
            if not animation.active:
                continue
                
            elapsed = (current_time - animation.start_time).total_seconds()
            animation.progress = min(elapsed / animation.duration, 1.0)
            
            if animation.progress >= 1.0:
                animation.active = False
                completed_animations.append(animation)
        
        # Remove completed animations
        for animation in completed_animations:
            self.active_animations.remove(animation)
        
        # Update color transitions
        self.update_color_transitions()
    
    def cleanup(self):
        """Clean up resources and reset state."""
        self.visualization_state = {
            'cursor': {
                'breach_points': [],
                'sonar_patterns': [],
                'echo_rings': []
            },
            'wick': {
                'bindings': [],
                'insight_capsules': [],
                'resonance_arcs': []
            },
            'mirror': {
                'confirmation_glyphs': [],
                'phase_reflections': [],
                'harmonic_fields': []
            },
            'djinn': {
                'whisper_trails': [],
                'portent_sigils': [],
                'echo_waves': []
            },
            'system': {
                'transformations': [],
                'merge_effects': [],
                'domain_maps': []
            }
        }
        self.active_animations = []
        self.active_transitions = {}
        self.echo_memories = []
        self.memory_playback = MemoryPlayback()
        self.comparison_mode = False
        self.comparison_memory = None
        self.current_filter = MemoryFilter()
        self.search_results = []
        self.comparative_playback = None
        self.memory_index = {
            'sigil': [],
            'phrase': [],
            'resonance': [],
            'phase': [],
            'confirmation': []
        }
        self.composer_state = QueryComposerState(
            nodes={},
            active_node=None,
            preview_results=[],
            is_dragging=False,
            drag_start=None
        )
        self.interaction_state = InteractionState(
            hovered_node=None,
            drag_source=None,
            drag_target=None,
            connection_preview=None,
            animation_frames={},
            active_sigils=[],
            resonance_map={},
            grid_snap=True
        )
    
    def visualize_phase_reflection(self, phase: str, resonance: float) -> Dict:
        """
        Placeholder method to simulate the visualization of phase reflection.
        This method currently logs the action and returns a dictionary with a placeholder key.
        """
        print("Visualizing phase reflection for phase:", phase, "with resonance:", resonance)
        return {'phase_reflection': 'placeholder'}
    
    def visualize_confirmation_trail(self, memory_anchor: Dict, phase_anchor: Dict, resonance: float) -> Dict:
        """Visualize a confirmation trail between memory and phase anchors."""
        style = self.styles['mirror']
        
        # Generate threaded filaments
        filaments = []
        for i in range(3):  # 3 parallel filaments
            filament = {
                'start': memory_anchor['position'],
                'end': phase_anchor['position'],
                'color': style.primary_color,
                'opacity': style.opacity * resonance * (1.0 - (i * 0.2)),
                'width': style.line_width * (1.0 - (i * 0.1)),
                'curve': 0.1 * (i + 1)  # Increasing curve for each filament
            }
            filaments.append(filament)
        
        # Generate anchor points
        anchors = {
            'memory': {
                'position': memory_anchor['position'],
                'color': style.secondary_color,
                'opacity': style.opacity * resonance,
                'size': 8.0
            },
            'phase': {
                'position': phase_anchor['position'],
                'color': style.secondary_color,
                'opacity': style.opacity * resonance,
                'size': 8.0
            }
        }
        
        # Update visualization state
        self.visualization_state['mirror']['confirmation_glyphs'].append({
            'resonance': resonance,
            'filaments': filaments,
            'anchors': anchors
        })
        
        # Create animation
        animation = AnimationState(
            id=f"confirmation_{len(self.active_animations)}",
            type="confirmation_trail",
            start_time=datetime.now(),
            duration=1.5,
            progress=0.0
        )
        self.active_animations.append(animation)
        
        return {
            'filaments': filaments,
            'anchors': anchors,
            'animation': animation
        }
    
    def visualize_sigil_pulse(self, sigil: str, breath_phase: str) -> Dict:
        """Visualize a sigil pulse with radiant glyphs."""
        style = self.styles['djinn']
        
        # Generate radiant glyph
        glyph = {
            'content': sigil,
            'color': style.primary_color,
            'opacity': style.opacity,
            'size': 30.0,
            'rotation': 0.0,
            'pulse_speed': style.pulse_frequency
        }
        
        # Generate aura rings
        rings = []
        for i in range(3):  # 3 aura rings
            ring = {
                'radius': 40.0 * (i + 1),
                'color': style.secondary_color,
                'opacity': style.opacity * (1.0 - (i / 3)),
                'width': style.line_width * (1.0 + (i * 0.2))
            }
            rings.append(ring)
        
        # Update visualization state
        self.visualization_state['djinn']['portent_sigils'].append({
            'sigil': sigil,
            'breath_phase': breath_phase,
            'glyph': glyph,
            'rings': rings
        })
        
        # Create animation
        animation = AnimationState(
            id=f"sigil_{len(self.active_animations)}",
            type="sigil_pulse",
            start_time=datetime.now(),
            duration=1.0,
            progress=0.0
        )
        self.active_animations.append(animation)
        
        return {
            'glyph': glyph,
            'rings': rings,
            'animation': animation
        }
    
    def visualize_whisper(self, content: str, depth: int) -> Dict:
        """Visualize a whisper with animated oscillation lines."""
        style = self.styles['djinn']
        
        # Generate oscillation lines
        lines = []
        for i in range(5):  # 5 oscillation lines
            line = {
                'points': [
                    {'x': j/10, 'y': np.sin(j * 0.5 + i) * 0.2}
                    for j in range(11)  # 11 points per line
                ],
                'color': style.primary_color,
                'opacity': style.opacity * (1.0 - (i / 5)),
                'width': style.line_width * (1.0 - (i * 0.1)),
                'frequency': style.pulse_frequency * (1.0 + (i * 0.2))
            }
            lines.append(line)
        
        # Generate whisper core
        core = {
            'content': content,
            'color': style.secondary_color,
            'opacity': style.opacity,
            'size': 5.0 * depth
        }
        
        # Update visualization state
        self.visualization_state['djinn']['whisper_trails'].append({
            'content': content,
            'depth': depth,
            'lines': lines,
            'core': core
        })
        
        # Create animation
        animation = AnimationState(
            id=f"whisper_{len(self.active_animations)}",
            type="whisper",
            start_time=datetime.now(),
            duration=1.5,
            progress=0.0
        )
        self.active_animations.append(animation)
        
        return {
            'lines': lines,
            'core': core,
            'animation': animation
        }
    
    def update_memory_index(self):
        """Update the search index with current echo memories."""
        self.memory_index = {
            'sigil': [],
            'phrase': [],
            'resonance': [],
            'phase': [],
            'confirmation': []
        }
        
        for memory in self.echo_memories:
            # Index by sigil types
            for subsystem in memory.visual_elements:
                self.memory_index['sigil'].append((memory, 1.0))
            
            # Index by breath phase
            self.memory_index['phase'].append((memory, 1.0))
            
            # Index by resonance
            self.memory_index['resonance'].append((memory, memory.resonance))
            
            # Index by confirmation status
            if 'mirror' in memory.visual_elements:
                confirmation_status = any(
                    glyph.get('confirmed', False)
                    for glyph in memory.visual_elements['mirror'].get('confirmation_glyphs', [])
                )
                self.memory_index['confirmation'].append((memory, 1.0 if confirmation_status else 0.0))
    
    def apply_filter(self, filter_criteria: MemoryFilter) -> List[EchoMemory]:
        """Apply filtering criteria to echo memories."""
        self.current_filter = filter_criteria
        filtered_memories = self.echo_memories.copy()
        
        if filter_criteria.sigil_types:
            filtered_memories = [
                m for m in filtered_memories
                if any(sigil in m.visual_elements for sigil in filter_criteria.sigil_types)
            ]
        
        if filter_criteria.ritual_phrases:
            filtered_memories = [
                m for m in filtered_memories
                if any(phrase in str(m.visual_elements) for phrase in filter_criteria.ritual_phrases)
            ]
        
        if filter_criteria.resonance_range:
            min_res, max_res = filter_criteria.resonance_range
            filtered_memories = [
                m for m in filtered_memories
                if min_res <= m.resonance <= max_res
            ]
        
        if filter_criteria.breath_phases:
            filtered_memories = [
                m for m in filtered_memories
                if m.breath_phase in filter_criteria.breath_phases
            ]
        
        if filter_criteria.confirmation_status is not None:
            filtered_memories = [
                m for m in filtered_memories
                if any(
                    glyph.get('confirmed', False) == filter_criteria.confirmation_status
                    for glyph in m.visual_elements.get('mirror', {}).get('confirmation_glyphs', [])
                )
            ]
        
        if filter_criteria.time_range:
            start_time, end_time = filter_criteria.time_range
            filtered_memories = [
                m for m in filtered_memories
                if start_time <= m.timestamp <= end_time
            ]
        
        return filtered_memories
    
    def _evaluate_term(self, term: SearchTerm, memory: EchoMemory) -> bool:
        """Evaluate a single search term against a memory."""
        if term.field not in self.search_fields:
            return False
        
        field_values = self.search_fields[term.field](memory)
        
        if term.operator is None:
            # Simple term match
            query_embedding = self._get_phrase_embedding(term.field)
            for value in field_values:
                value_embedding = self._get_phrase_embedding(str(value))
                similarity = self._calculate_cosine_similarity(query_embedding, value_embedding)
                if similarity >= self.semantic_threshold:
                    return not term.is_negated
            return term.is_negated
        
        # Numeric comparison
        if term.operator in [QueryOperator.GT, QueryOperator.LT, 
                           QueryOperator.GTE, QueryOperator.LTE, 
                           QueryOperator.EQ]:
            try:
                value = float(term.value)
                for field_value in field_values:
                    field_value = float(field_value)
                    if term.operator == QueryOperator.GT and field_value > value:
                        return not term.is_negated
                    elif term.operator == QueryOperator.LT and field_value < value:
                        return not term.is_negated
                    elif term.operator == QueryOperator.GTE and field_value >= value:
                        return not term.is_negated
                    elif term.operator == QueryOperator.LTE and field_value <= value:
                        return not term.is_negated
                    elif term.operator == QueryOperator.EQ and field_value == value:
                        return not term.is_negated
            except (ValueError, TypeError):
                return term.is_negated
        
        return term.is_negated
    
    def _evaluate_query(self, query: SearchQuery, memory: EchoMemory) -> bool:
        """Evaluate a complex query against a memory."""
        results = []
        for term in query.terms:
            if isinstance(term, SearchQuery):
                results.append(self._evaluate_query(term, memory))
            else:
                results.append(self._evaluate_term(term, memory))
        
        if query.operator == QueryOperator.AND:
            return all(results) != query.is_negated
        elif query.operator == QueryOperator.OR:
            return any(results) != query.is_negated
        else:
            return results[0] != query.is_negated
    
    def search_memories(self, query_str: str) -> List[SearchMatch]:
        """Search memories using a complex query string."""
        try:
            query = self.query_parser.parse(query_str)
        except Exception as e:
            # Fall back to simple search if parsing fails
            return super().search_memories(query_str)
        
        matches = []
        for memory in self.echo_memories:
            if self._evaluate_query(query, memory):
                # Create a detailed match explanation
                match = SearchMatch(
                    memory=memory,
                    exact_matches=set(),
                    fuzzy_matches={},
                    semantic_matches={},
                    combined_score=1.0,
                    match_explanation=f"Matches query: {query_str}"
                )
                matches.append(match)
        
        return matches
    
    def get_query_suggestions(self, partial_query: str) -> List[str]:
        """Get suggestions for completing a partial query."""
        suggestions = []
        
        # Add operator suggestions
        if partial_query.endswith(' '):
            suggestions.extend(['AND', 'OR', 'NOT'])
        
        # Add field suggestions
        if not any(op in partial_query for op in ['AND', 'OR', 'NOT', '>', '<', '=']):
            suggestions.extend(self.search_fields.keys())
        
        # Add value suggestions for numeric fields
        if '>' in partial_query or '<' in partial_query or '=' in partial_query:
            suggestions.extend(['0.0', '0.5', '0.8', '1.0'])
        
        return suggestions
    
    def start_comparative_playback(self, primary_memory: EchoMemory, 
                                 comparison_memories: List[EchoMemory]):
        """Start parallel playback of multiple memories."""
        # Find sync points (matching breath phases)
        sync_points = []
        for memory in [primary_memory] + comparison_memories:
            if memory.breath_phase == primary_memory.breath_phase:
                sync_points.append(memory.timestamp)
        
        # Calculate divergence highlights
        divergence_highlights = {}
        for subsystem in primary_memory.visual_elements:
            divergence_highlights[subsystem] = []
            for comp_memory in comparison_memories:
                if subsystem in comp_memory.visual_elements:
                    differences = self._calculate_visual_differences(
                        primary_memory.visual_elements[subsystem],
                        comp_memory.visual_elements[subsystem]
                    )
                    if differences:
                        divergence_highlights[subsystem].append({
                            'memory': comp_memory,
                            'differences': differences
                        })
        
        self.comparative_playback = ComparativePlayback(
            primary_memory=primary_memory,
            comparison_memories=comparison_memories,
            sync_points=sync_points,
            divergence_highlights=divergence_highlights
        )
    
    def _calculate_visual_differences(self, current: Dict, historical: Dict) -> Dict:
        """Calculate differences between two visual states."""
        differences = {
            'added': [],
            'removed': [],
            'modified': []
        }
        
        # Compare elements
        current_keys = set(current.keys())
        historical_keys = set(historical.keys())
        
        # Find added and removed elements
        differences['added'] = list(current_keys - historical_keys)
        differences['removed'] = list(historical_keys - current_keys)
        
        # Find modified elements
        common_keys = current_keys & historical_keys
        for key in common_keys:
            if current[key] != historical[key]:
                differences['modified'].append({
                    'key': key,
                    'current': current[key],
                    'historical': historical[key]
                })
        
        return differences
    
    def get_timeline_markers(self) -> List[Dict]:
        """Get timeline markers for search results and sync points."""
        markers = []
        
        # Add search result markers
        for result in self.search_results:
            markers.append({
                'timestamp': result.memory.timestamp,
                'type': 'search_result',
                'relevance': result.relevance_score,
                'context': result.context_snippets[0] if result.context_snippets else ''
            })
        
        # Add sync point markers if in comparative playback
        if self.comparative_playback:
            for sync_point in self.comparative_playback.sync_points:
                markers.append({
                    'timestamp': sync_point,
                    'type': 'sync_point',
                    'description': 'Breath phase alignment'
                })
        
        return sorted(markers, key=lambda m: m['timestamp'])
    
    def create_logic_node(self, node_type: str, value: Any, position: Tuple[float, float]) -> str:
        """Create a new logic node in the query composer."""
        node_id = f"{node_type}_{len(self.composer_state.nodes)}"
        
        style = self.node_styles.get(node_type, {}).get(value, self.node_styles.get(node_type, {}))
        
        node = LogicNode(
            id=node_id,
            type=node_type,
            value=value,
            position=position,
            connections=[],
            style=style
        )
        
        self.composer_state.nodes[node_id] = node
        return node_id
    
    def connect_nodes(self, source_id: str, target_id: str) -> bool:
        """Connect two logic nodes in the query composer."""
        if source_id not in self.composer_state.nodes or target_id not in self.composer_state.nodes:
            return False
        
        source = self.composer_state.nodes[source_id]
        target = self.composer_state.nodes[target_id]
        
        # Validate connection based on node types
        if source.type == 'operator' and target.type in ['field', 'value']:
            source.connections.append(target_id)
            return True
        elif source.type == 'field' and target.type == 'value':
            source.connections.append(target_id)
            return True
        
        return False
    
    def update_node_position(self, node_id: str, position: Tuple[float, float]):
        """Update the position of a logic node."""
        if node_id in self.composer_state.nodes:
            self.composer_state.nodes[node_id].position = position
    
    def build_query_from_nodes(self) -> Optional[SearchQuery]:
        """Build a search query from the current node configuration."""
        # Find root nodes (nodes with no incoming connections)
        root_nodes = []
        for node_id, node in self.composer_state.nodes.items():
            is_root = True
            for other_node in self.composer_state.nodes.values():
                if node_id in other_node.connections:
                    is_root = False
                    break
            if is_root:
                root_nodes.append(node)
        
        if not root_nodes:
            return None
        
        def build_subquery(node: LogicNode) -> Union[SearchTerm, SearchQuery]:
            if node.type == 'operator':
                terms = []
                for connected_id in node.connections:
                    connected_node = self.composer_state.nodes[connected_id]
                    terms.append(build_subquery(connected_node))
                
                return SearchQuery(
                    terms=terms,
                    operator=QueryOperator(node.value),
                    is_negated=(node.value == 'NOT')
                )
            elif node.type == 'field':
                value_node = self.composer_state.nodes[node.connections[0]] if node.connections else None
                return SearchTerm(
                    field=node.value,
                    operator=QueryOperator(value_node.value) if value_node and value_node.type == 'operator' else None,
                    value=value_node.value if value_node and value_node.type == 'value' else None
                )
            else:
                return SearchTerm(field='', value=node.value)
        
        # Build query from root nodes
        if len(root_nodes) == 1:
            return build_subquery(root_nodes[0])
        else:
            # Multiple root nodes are combined with AND
            return SearchQuery(
                terms=[build_subquery(node) for node in root_nodes],
                operator=QueryOperator.AND
            )
    
    def update_query_preview(self):
        """Update the preview results based on the current query."""
        query = self.build_query_from_nodes()
        if query:
            self.composer_state.preview_results = self.search_memories(str(query))
    
    def get_node_visual_elements(self, node_id: str) -> Dict[str, Any]:
        """Get visual elements for rendering a logic node with sigil effects."""
        elements = super().get_node_visual_elements(node_id)
        
        # Add resonance glow
        resonance = self.interaction_state.resonance_map.get(node_id, 0.0)
        if resonance > 0:
            elements['resonance_glow'] = {
                'intensity': resonance,
                'color': elements['color']
            }
        
        # Add active sigils
        node_sigils = [
            sigil for sigil in self.interaction_state.active_sigils
            if abs(sigil.position[0] - elements['position'][0]) < 30 and
               abs(sigil.position[1] - elements['position'][1]) < 30
        ]
        if node_sigils:
            elements['sigils'] = [
                {
                    'type': sigil.type,
                    'points': self._get_sigil_points(sigil.type, sigil.progress),
                    'color': sigil.color,
                    'scale': sigil.scale,
                    'rotation': sigil.rotation
                }
                for sigil in node_sigils
            ]
        
        return elements
    
    def get_composer_visual_state(self) -> Dict[str, Any]:
        """Get the current visual state of the query composer."""
        state = {
            'nodes': {
                node_id: self.get_node_visual_elements(node_id)
                for node_id in self.composer_state.nodes
            },
            'preview_count': len(self.composer_state.preview_results),
            'active_node': self.composer_state.active_node,
            'connection_preview': self.interaction_state.connection_preview,
            'hovered_node': self.interaction_state.hovered_node
        }
        
        # Add connection preview if dragging
        if self.interaction_state.connection_preview:
            state['connection_preview'] = {
                'start': self.interaction_state.connection_preview[0],
                'end': self.interaction_state.connection_preview[1],
                'progress': 0.0
            }
        
        return state
    
    def handle_mouse_hover(self, position: Tuple[float, float]) -> Optional[str]:
        """Handle mouse hover over nodes."""
        hovered_node = None
        for node_id, node in self.composer_state.nodes.items():
            if self._is_point_in_node(position, node):
                hovered_node = node_id
                break
        
        if hovered_node != self.interaction_state.hovered_node:
            self.interaction_state.hovered_node = hovered_node
            if hovered_node:
                self._start_hover_animation(hovered_node)
        
        return hovered_node
    
    def handle_drag_start(self, position: Tuple[float, float]) -> Optional[str]:
        """Handle start of drag operation."""
        for node_id, node in self.composer_state.nodes.items():
            if self._is_point_in_node(position, node):
                self.interaction_state.drag_source = node_id
                self.composer_state.is_dragging = True
                self.composer_state.drag_start = position
                return node_id
        return None
    
    def handle_drag_move(self, position: Tuple[float, float]):
        """Handle drag movement with grid snapping and sigil effects."""
        if not self.composer_state.is_dragging:
            return
        
        # Apply grid snapping
        if self.interaction_state.grid_snap:
            position = (
                round(position[0] / self.animation_params['grid_size']) * self.animation_params['grid_size'],
                round(position[1] / self.animation_params['grid_size']) * self.animation_params['grid_size']
            )
        
        # Update connection preview
        if self.interaction_state.drag_source:
            source_node = self.composer_state.nodes[self.interaction_state.drag_source]
            self.interaction_state.connection_preview = (source_node.position, position)
            
            # Create sigil trail
            self._create_sigil_effect(
                'connection',
                position,
                source_node.style.get('color', (0.5, 0.5, 0.5)),
                0.5
            )
            
            # Check for potential connection target
            for node_id, node in self.composer_state.nodes.items():
                if node_id != self.interaction_state.drag_source and self._is_point_in_node(position, node):
                    self.interaction_state.drag_target = node_id
                    # Create validation sigil
                    self._create_sigil_effect(
                        'validation',
                        node.position,
                        (0.2, 0.8, 0.2),
                        1.0
                    )
                    return
            
            self.interaction_state.drag_target = None
    
    def handle_drag_end(self, position: Tuple[float, float]) -> bool:
        """Handle end of drag operation with sigil effects."""
        if not self.composer_state.is_dragging:
            return False
        
        success = False
        if self.interaction_state.drag_source and self.interaction_state.drag_target:
            success = self.connect_nodes(
                self.interaction_state.drag_source,
                self.interaction_state.drag_target
            )
            if success:
                # Create connection sigil
                source_node = self.composer_state.nodes[self.interaction_state.drag_source]
                target_node = self.composer_state.nodes[self.interaction_state.drag_target]
                mid_point = (
                    (source_node.position[0] + target_node.position[0]) / 2,
                    (source_node.position[1] + target_node.position[1]) / 2
                )
                self._create_sigil_effect(
                    'resonance',
                    mid_point,
                    source_node.style.get('color', (0.5, 0.5, 0.5)),
                    1.5
                )
                
                # Update resonance map
                self.interaction_state.resonance_map[self.interaction_state.drag_source] = \
                    self.interaction_state.resonance_map.get(self.interaction_state.drag_source, 0.0) + 0.1
                self.interaction_state.resonance_map[self.interaction_state.drag_target] = \
                    self.interaction_state.resonance_map.get(self.interaction_state.drag_target, 0.0) + 0.1
        
        # Reset drag state
        self.composer_state.is_dragging = False
        self.composer_state.drag_start = None
        self.interaction_state.drag_source = None
        self.interaction_state.drag_target = None
        self.interaction_state.connection_preview = None
        
        return success
    
    def _is_point_in_node(self, point: Tuple[float, float], node: LogicNode) -> bool:
        """Check if a point is within a node's bounds."""
        node_size = 30.0  # Base size for nodes
        hover_scale = self.animation_params['hover_scale']
        
        # Get current scale based on hover state
        scale = hover_scale if node.id == self.interaction_state.hovered_node else 1.0
        size = node_size * scale
        
        # Check if point is within node bounds
        return (abs(point[0] - node.position[0]) < size/2 and
                abs(point[1] - node.position[1]) < size/2)
    
    def _start_hover_animation(self, node_id: str):
        """Start hover animation for a node."""
        self.interaction_state.animation_frames[node_id] = 0.0
    
    def _start_connection_animation(self, source_id: str, target_id: str):
        """Start connection animation between nodes."""
        anim_id = f"conn_{source_id}_{target_id}"
        self.interaction_state.animation_frames[anim_id] = 0.0
    
    def _create_sigil_effect(self, effect_type: str, position: Tuple[float, float], 
                           color: Tuple[float, float, float], scale: float = 1.0) -> SigilEffect:
        """Create a new sigil effect."""
        effect = SigilEffect(
            type=effect_type,
            position=position,
            scale=scale,
            color=color,
            rotation=0.0,
            lifetime=self.animation_params['sigil_lifetime'],
            progress=0.0
        )
        self.interaction_state.active_sigils.append(effect)
        return effect
    
    def _update_sigil_effects(self, delta_time: float):
        """Update all active sigil effects."""
        for sigil in self.interaction_state.active_sigils[:]:
            sigil.progress += delta_time / sigil.lifetime
            if sigil.progress >= 1.0:
                self.interaction_state.active_sigils.remove(sigil)
    
    def _get_sigil_points(self, sigil_type: str, progress: float) -> List[Tuple[float, float]]:
        """Get points for a sigil pattern at the given progress."""
        pattern = self.sigil_patterns.get(sigil_type, self.sigil_patterns['connection'])
        points = []
        
        for i in range(len(pattern) - 1):
            p1 = pattern[i]
            p2 = pattern[i + 1]
            t = (progress - p1[0]) / (p2[0] - p1[0])
            if 0 <= t <= 1:
                x = p1[0] + (p2[0] - p1[0]) * t
                y = p1[1] + (p2[1] - p1[1]) * t
                points.append((x, y))
        
        return points
    
    def update_animations(self, delta_time: float):
        """Update all active animations and sigil effects."""
        # Update existing animations
        super().update_animations(delta_time)
        
        # Update sigil effects
        self._update_sigil_effects(delta_time)
        
        # Update resonance pulses
        for node_id, resonance in self.interaction_state.resonance_map.items():
            if resonance > 0:
                self.interaction_state.resonance_map[node_id] = max(
                    0.0,
                    resonance - delta_time * self.animation_params['resonance_pulse_speed']
                )
    
    def update_preview_panel(self, delta_time: float, current_phase: str):
        """Update the preview panel state based on breath phase and resonance."""
        # Update visibility based on breath phase
        target_visible = current_phase in ['DAWN', 'DUSK']
        if target_visible != self.preview_panel.is_visible:
            self.preview_panel.is_visible = target_visible
            if target_visible:
                self._start_preview_bloom()
            else:
                self._start_preview_fade()
        
        # Update panel properties
        if self.preview_panel.is_visible:
            # Animate scale and opacity
            self.preview_panel.scale = min(
                self.preview_params['max_scale'],
                self.preview_panel.scale + delta_time * self.preview_params['bloom_speed']
            )
            self.preview_panel.opacity = min(
                self.preview_params['max_opacity'],
                self.preview_panel.opacity + delta_time * self.preview_params['bloom_speed']
            )
            
            # Update breath phase
            self.preview_panel.breath_phase = current_phase
            
            # Update resonance level
            self.preview_panel.resonance_level = self._calculate_resonance_level()
            
            # Update harmonic confidence
            self.preview_panel.harmonic_confidence = self._calculate_harmonic_confidence()
            
            # Update sound resonance
            self._update_sound_resonance(delta_time)
            
            # Update sigil tags
            self._update_sigil_tags(delta_time)
    
    def _start_preview_bloom(self):
        """Start the preview panel bloom animation."""
        self.preview_panel.scale = 0.0
        self.preview_panel.opacity = 0.0
        # Create initial sound resonance
        self._create_sound_resonance(self.preview_params['sound_frequencies'][self.preview_panel.breath_phase])
    
    def _start_preview_fade(self):
        """Start the preview panel fade animation."""
        self.preview_panel.scale = self.preview_params['max_scale']
        self.preview_panel.opacity = self.preview_params['max_opacity']
    
    def _calculate_resonance_level(self) -> float:
        """Calculate the current resonance level based on active matches."""
        if not self.preview_panel.active_matches:
            return 0.0
        
        # Calculate average resonance from matches
        total_resonance = sum(match.combined_score for match in self.preview_panel.active_matches)
        return min(1.0, total_resonance / len(self.preview_panel.active_matches))
    
    def _calculate_harmonic_confidence(self) -> float:
        """Calculate the harmonic confidence based on query structure and matches."""
        # Consider query complexity, match quality, and resonance
        structure_score = self._evaluate_query_structure()
        match_score = self._evaluate_match_quality()
        resonance_score = self.preview_panel.resonance_level
        
        return (structure_score * 0.4 + match_score * 0.3 + resonance_score * 0.3)
    
    def _evaluate_query_structure(self) -> float:
        """Evaluate the structural integrity of the current query."""
        query = self.build_query_from_nodes()
        if not query:
            return 0.0
        
        # Consider number of nodes, connections, and nesting depth
        node_count = len(self.composer_state.nodes)
        connection_count = sum(len(node.connections) for node in self.composer_state.nodes.values())
        max_depth = self._calculate_query_depth(query)
        
        # Normalize scores
        structure_score = min(1.0, (node_count * 0.2 + connection_count * 0.3 + max_depth * 0.5) / 3.0)
        return structure_score
    
    def _evaluate_match_quality(self) -> float:
        """Evaluate the quality of current matches."""
        if not self.preview_panel.active_matches:
            return 0.0
        
        # Consider match scores and diversity
        scores = [match.combined_score for match in self.preview_panel.active_matches]
        return sum(scores) / len(scores)
    
    def _calculate_query_depth(self, query: SearchQuery) -> int:
        """Calculate the maximum nesting depth of a query."""
        if not query.terms:
            return 0
        
        max_depth = 0
        for term in query.terms:
            if isinstance(term, SearchQuery):
                depth = self._calculate_query_depth(term) + 1
                max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _create_sound_resonance(self, frequency: float):
        """Create a new sound resonance effect."""
        sound = SoundResonance(
            frequency=frequency,
            amplitude=0.5,
            phase=0.0,
            lifetime=1.0,
            progress=0.0
        )
        self.active_sounds.append(sound)
    
    def _update_sound_resonance(self, delta_time: float):
        """Update all active sound resonance effects."""
        for sound in self.active_sounds[:]:
            sound.progress += delta_time / sound.lifetime
            if sound.progress >= 1.0:
                self.active_sounds.remove(sound)
            else:
                # Update phase and amplitude
                sound.phase += delta_time * sound.frequency
                sound.amplitude *= 0.95  # Gradual decay
    
    def _update_sigil_tags(self, delta_time: float):
        """Update the orbiting sigil tags."""
        # Generate tags from active matches
        new_tags = []
        for match in self.preview_panel.active_matches:
            # Extract sigil information
            sigil_info = {
                'type': match.memory.visual_elements.get('sigil_type', 'unknown'),
                'resonance': match.combined_score,
                'phase': match.memory.breath_phase,
                'angle': 0.0  # Will be updated for orbiting
            }
            new_tags.append(sigil_info)
        
        # Update existing tags
        for tag in self.preview_panel.sigil_tags:
            tag['angle'] += delta_time * self.preview_params['sigil_orbit_speed']
            if tag['angle'] >= 2 * math.pi:
                tag['angle'] = 0.0
        
        self.preview_panel.sigil_tags = new_tags
    
    def get_preview_panel_state(self) -> Dict[str, Any]:
        """Get the current state of the preview panel for rendering."""
        return {
            'is_visible': self.preview_panel.is_visible,
            'position': self.preview_panel.position,
            'scale': self.preview_panel.scale,
            'opacity': self.preview_panel.opacity,
            'breath_phase': self.preview_panel.breath_phase,
            'resonance_level': self.preview_panel.resonance_level,
            'harmonic_confidence': self.preview_panel.harmonic_confidence,
            'active_matches': [
                {
                    'memory': match.memory,
                    'score': match.combined_score,
                    'explanation': match.match_explanation
                }
                for match in self.preview_panel.active_matches
            ],
            'sigil_tags': [
                {
                    'type': tag['type'],
                    'resonance': tag['resonance'],
                    'phase': tag['phase'],
                    'position': (
                        self.preview_panel.position[0] + 
                        math.cos(tag['angle']) * self.preview_params['sigil_orbit_radius'],
                        self.preview_panel.position[1] + 
                        math.sin(tag['angle']) * self.preview_params['sigil_orbit_radius']
                    )
                }
                for tag in self.preview_panel.sigil_tags
            ],
            'sound_resonance': [
                {
                    'frequency': sound.frequency,
                    'amplitude': sound.amplitude,
                    'phase': sound.phase
                }
                for sound in self.active_sounds
            ]
        } 
    
    def initiate_landing_sequence(self):
        """Initiate the system landing sequence."""
        self.system_state.is_landing = True
        self.system_state.landing_progress = 0.0
        self.system_state.active_components = {
            'preview_panel',
            'sound_resonance',
            'sigil_effects',
            'animations',
            'interactions'
        }
        self.system_state.final_resonance = self.preview_panel.resonance_level
        
        # Start landing sequence
        self._start_landing_sequence()
    
    def _start_landing_sequence(self):
        """Start the landing sequence process."""
        # Fade out preview panel
        self.preview_panel.is_visible = False
        self.preview_panel.opacity = 0.0
        
        # Begin resonance decay
        for node_id in self.interaction_state.resonance_map:
            self.interaction_state.resonance_map[node_id] *= 0.5
        
        # Clear active sounds
        self.active_sounds.clear()
        
        # Clear sigil effects
        self.interaction_state.active_sigils.clear()
    
    def update_landing_sequence(self, delta_time: float):
        """Update the landing sequence state."""
        if not self.system_state.is_landing:
            return
        
        # Update landing progress
        self.system_state.landing_progress += delta_time / self.landing_params['sequence_duration']
        
        # Shutdown components in order
        for component in self.landing_params['component_shutdown_order']:
            if component in self.system_state.active_components:
                self._shutdown_component(component)
        
        # Check if landing is complete
        if self.system_state.landing_progress >= 1.0:
            self._complete_landing_sequence()
    
    def _shutdown_component(self, component: str):
        """Shutdown a specific component during landing sequence."""
        if component == 'preview_panel':
            self.preview_panel.scale *= 0.95
            self.preview_panel.opacity *= 0.95
        elif component == 'sound_resonance':
            for sound in self.active_sounds:
                sound.amplitude *= 0.9
        elif component == 'sigil_effects':
            for sigil in self.interaction_state.active_sigils:
                sigil.scale *= 0.95
        elif component == 'animations':
            for node_id in self.interaction_state.animation_frames:
                self.interaction_state.animation_frames[node_id] *= 0.9
        elif component == 'interactions':
            self.interaction_state.hovered_node = None
            self.interaction_state.drag_source = None
            self.interaction_state.drag_target = None
        
        # Remove component from active set
        self.system_state.active_components.discard(component)
    
    def _complete_landing_sequence(self):
        """Complete the landing sequence and reset system state."""
        # Reset all states
        self.preview_panel = PreviewPanel(
            is_visible=False,
            position=(0.5, 0.5),
            scale=0.0,
            opacity=0.0,
            breath_phase='STILL',
            resonance_level=0.0,
            active_matches=[],
            sigil_tags=[],
            harmonic_confidence=0.0,
            sound_resonance=0.0
        )
        
        self.interaction_state = InteractionState(
            hovered_node=None,
            drag_source=None,
            drag_target=None,
            connection_preview=None,
            animation_frames={},
            active_sigils=[],
            resonance_map={},
            grid_snap=True
        )
        
        self.active_sounds.clear()
        
        # Reset system state
        self.system_state = SystemState(
            is_landing=False,
            landing_progress=0.0,
            active_components=set(),
            final_resonance=0.0
        )
    
    def get_system_state(self) -> Dict[str, Any]:
        """Get the current system state for monitoring."""
        return {
            'is_landing': self.system_state.is_landing,
            'landing_progress': self.system_state.landing_progress,
            'active_components': list(self.system_state.active_components),
            'final_resonance': self.system_state.final_resonance,
            'preview_panel_visible': self.preview_panel.is_visible,
            'active_sounds': len(self.active_sounds),
            'active_sigils': len(self.interaction_state.active_sigils),
            'resonance_level': self.preview_panel.resonance_level
        }