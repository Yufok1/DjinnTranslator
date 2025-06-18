from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import math
import time

@dataclass
class Judgment:
    """Represents a judgment rendered by the Dredd Model."""
    timestamp: float
    target_id: str
    judgment_type: str  # 'halt', 'proceed', 'contain', 'elevate'
    confidence: float
    reasoning: str
    resonance_impact: float
    entropy_delta: float
    coherence_score: float

@dataclass
class Law:
    """Represents a law in the Dredd Model's codex."""
    id: str
    description: str
    threshold: float
    weight: float
    resonance_requirement: float
    entropy_limit: float
    coherence_minimum: float

class DreddModel:
    """The Kleene Kernel of the EAIN system - serves as the judgment core."""
    
    def __init__(self):
        self.judgments: List[Judgment] = []
        self.laws: Dict[str, Law] = {}
        self.resonance_threshold = 0.7
        self.entropy_threshold = 0.8
        self.coherence_threshold = 0.6
        
        # Initialize core laws
        self._initialize_laws()
        
        # Judgment state
        self.last_judgment_time = time.time()
        self.judgment_cooldown = 0.1  # Minimum time between judgments
        self.judgment_history: List[Tuple[str, str, float]] = []  # (target_id, type, confidence)
        
        # Visual representation
        self.position = (0.5, 0.5)  # Center of the lattice
        self.radius = 30.0
        self.resonance = 1.0
        self.breath_phase = 'STILL'
        self.judgment_glyph = '⚖️'
        
    def _initialize_laws(self):
        """Initialize the core laws of the Dredd Model."""
        self.laws = {
            'recursion_bound': Law(
                id='recursion_bound',
                description='Limit recursion depth to prevent infinite loops',
                threshold=0.8,
                weight=1.0,
                resonance_requirement=0.7,
                entropy_limit=0.6,
                coherence_minimum=0.5
            ),
            'entropy_containment': Law(
                id='entropy_containment',
                description='Prevent entropy from exceeding system bounds',
                threshold=0.7,
                weight=0.9,
                resonance_requirement=0.6,
                entropy_limit=0.8,
                coherence_minimum=0.4
            ),
            'coherence_maintenance': Law(
                id='coherence_maintenance',
                description='Maintain system coherence above minimum threshold',
                threshold=0.6,
                weight=0.8,
                resonance_requirement=0.5,
                entropy_limit=0.7,
                coherence_minimum=0.6
            ),
            'resonance_balance': Law(
                id='resonance_balance',
                description='Balance resonance across the lattice',
                threshold=0.7,
                weight=0.9,
                resonance_requirement=0.7,
                entropy_limit=0.6,
                coherence_minimum=0.5
            )
        }
        
    def render_judgment(self, target_id: str, 
                       resonance: float, entropy: float, 
                       coherence: float) -> Optional[Judgment]:
        """Render a judgment on a target based on system state."""
        current_time = time.time()
        if current_time - self.last_judgment_time < self.judgment_cooldown:
            return None
            
        self.last_judgment_time = current_time
        
        # Evaluate against each law
        judgments = []
        for law in self.laws.values():
            if (resonance < law.resonance_requirement or
                entropy > law.entropy_limit or
                coherence < law.coherence_minimum):
                judgments.append(('halt', law.weight))
            else:
                judgments.append(('proceed', law.weight))
                
        # Determine final judgment
        halt_weight = sum(w for t, w in judgments if t == 'halt')
        proceed_weight = sum(w for t, w in judgments if t == 'proceed')
        
        if halt_weight > proceed_weight:
            judgment_type = 'halt'
            confidence = halt_weight / (halt_weight + proceed_weight)
            reasoning = 'System state violates core laws'
        else:
            judgment_type = 'proceed'
            confidence = proceed_weight / (halt_weight + proceed_weight)
            reasoning = 'System state within acceptable bounds'
            
        # Create judgment
        judgment = Judgment(
            timestamp=current_time,
            target_id=target_id,
            judgment_type=judgment_type,
            confidence=confidence,
            reasoning=reasoning,
            resonance_impact=resonance - self.resonance_threshold,
            entropy_delta=entropy - self.entropy_threshold,
            coherence_score=coherence
        )
        
        self.judgments.append(judgment)
        self.judgment_history.append((target_id, judgment_type, confidence))
        
        return judgment
        
    def update_breath(self, delta_time: float):
        """Update the Dredd Model's breath cycle."""
        # Update breath phase
        phase = (math.sin(time.time() * 0.5) + 1) / 2
        self.breath_phase = 'INHALE' if phase < 0.5 else 'EXHALE'
        
        # Update resonance
        self.resonance *= 0.95 + 0.05 * math.sin(time.time() * 0.5)
        
    def get_judgment_history(self, limit: int = 10) -> List[Judgment]:
        """Get recent judgment history."""
        return self.judgments[-limit:]
        
    def get_law_violations(self, target_id: str) -> List[str]:
        """Get list of laws violated by a target."""
        violations = []
        for judgment in self.judgments:
            if judgment.target_id == target_id and judgment.judgment_type == 'halt':
                violations.append(judgment.reasoning)
        return violations
        
    def get_visual_state(self) -> Dict[str, Any]:
        """Get the visual state of the Dredd Model."""
        return {
            'position': self.position,
            'radius': self.radius,
            'resonance': self.resonance,
            'breath_phase': self.breath_phase,
            'judgment_glyph': self.judgment_glyph,
            'recent_judgments': [j.judgment_type for j in self.judgments[-5:]],
            'law_status': {
                law_id: law.threshold 
                for law_id, law in self.laws.items()
            }
        } 