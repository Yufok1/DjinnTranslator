"""
Commit Gatekeeper
Manages commit permissions and pattern analysis for autonomous code changes
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional
from collections import deque

class CommitAuthority(Enum):
    """Levels of commit authority"""
    RESTRICTED = 0  # No autonomous commits
    SUPERVISED = 1  # Commits require explicit approval
    AUTONOMOUS = 2  # Full autonomous commit capability

class PatternType(Enum):
    """Types of reasoning patterns"""
    BREAKTHROUGH = "breakthrough"  # Novel solution patterns
    TURBULENCE = "turbulence"      # System stress patterns
    HARMONY = "harmony"           # Stable operation patterns
    EXPLORATION = "exploration"    # Learning/adaptation patterns
    RECOVERY = "recovery"         # System recovery patterns

@dataclass
class Pattern:
    """Represents a detected reasoning pattern"""
    pattern_type: PatternType
    start_time: float
    end_time: float
    events: List[Any]  # List of reason events
    resonance: float
    mirror_confirmed: bool
    domain_activation: Dict[str, float]

@dataclass
class CommitRequest:
    """Represents a request to commit changes"""
    timestamp: float
    file_path: str
    changes: List[Any]
    pattern: Optional[Pattern]
    mirror_confirmed: bool
    coherence: float
    stability: float
    reason_type: str
    cause: str
    effect: str

class CommitGatekeeper:
    """Manages commit permissions and pattern analysis"""
    
    def __init__(self):
        self.autonomy_threshold = 0.95  # Threshold for autonomous commits
        self.stability_threshold = 0.90  # Threshold for system stability
        self.pattern_buffer = deque(maxlen=100)  # Recent patterns
        self.commit_history = deque(maxlen=50)   # Recent commits
        self.pattern_templates = self._init_pattern_templates()
    
    def _init_pattern_templates(self) -> Dict[PatternType, Dict[str, Any]]:
        """Initialize pattern templates for detection"""
        return {
            PatternType.BREAKTHROUGH: {
                "min_resonance": 0.8,
                "min_mirror_confirmation": True,
                "required_domains": ["reasoning", "adaptation"]
            },
            PatternType.TURBULENCE: {
                "max_stability": 0.7,
                "min_events": 3,
                "required_domains": ["stress", "recovery"]
            },
            PatternType.HARMONY: {
                "min_stability": 0.9,
                "min_resonance": 0.7,
                "required_domains": ["coherence", "stability"]
            },
            PatternType.EXPLORATION: {
                "min_events": 2,
                "max_stability": 0.8,
                "required_domains": ["learning", "adaptation"]
            },
            PatternType.RECOVERY: {
                "min_stability": 0.6,
                "min_resonance": 0.5,
                "required_domains": ["recovery", "stability"]
            }
        }
    
    def add_pattern(self, pattern: Pattern):
        """Add a new pattern to the buffer"""
        self.pattern_buffer.append(pattern)
        self._analyze_patterns()
    
    def _analyze_patterns(self):
        """Analyze patterns for insights"""
        if len(self.pattern_buffer) < 2:
            return
        
        # Calculate pattern statistics
        pattern_counts = {}
        success_rates = {}
        
        for pattern in self.pattern_buffer:
            pattern_type = pattern.pattern_type
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
            
            # Calculate success rate based on mirror confirmation and resonance
            if pattern.mirror_confirmed and pattern.resonance > 0.7:
                success_rates[pattern_type] = success_rates.get(pattern_type, 0) + 1
        
        # Normalize success rates
        for pattern_type in success_rates:
            success_rates[pattern_type] /= pattern_counts[pattern_type]
    
    def get_pattern_stats(self) -> Optional[Dict[str, Any]]:
        """Get current pattern statistics"""
        if not self.pattern_buffer:
            return None
        
        pattern_counts = {}
        success_rates = {}
        
        for pattern in self.pattern_buffer:
            pattern_type = pattern.pattern_type
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
            
            if pattern.mirror_confirmed and pattern.resonance > 0.7:
                success_rates[pattern_type] = success_rates.get(pattern_type, 0) + 1
        
        # Normalize success rates
        for pattern_type in success_rates:
            success_rates[pattern_type] /= pattern_counts[pattern_type]
        
        return {
            "pattern_counts": pattern_counts,
            "success_rates": success_rates
        }
    
    def get_recent_commits(self, count: int = 5) -> List[CommitRequest]:
        """Get recent commit requests"""
        return list(self.commit_history)[-count:]
    
    def request_commit(self, request: CommitRequest) -> CommitAuthority:
        """Process a commit request and determine authority level"""
        # Add to history
        self.commit_history.append(request)
        
        # Check authority
        authority = self._check_authority(request)
        
        # Update pattern analysis if commit was made
        if request.pattern:
            self.add_pattern(request.pattern)
        
        return authority
    
    def _check_authority(self, request: CommitRequest) -> CommitAuthority:
        """Check the authority level for a commit request"""
        # Check stability threshold
        if request.stability < self.stability_threshold:
            return CommitAuthority.RESTRICTED
        
        # Check autonomy conditions
        if (request.mirror_confirmed and 
            request.coherence >= self.autonomy_threshold and 
            request.stability >= self.stability_threshold):
            return CommitAuthority.AUTONOMOUS
        
        # Default to supervised
        return CommitAuthority.SUPERVISED
    
    def predict_next_pattern(self) -> Optional[PatternType]:
        """Predict the next likely pattern type"""
        if not self.pattern_buffer:
            return None
        
        # Count recent patterns
        recent_patterns = list(self.pattern_buffer)[-10:]
        pattern_counts = {}
        
        for pattern in recent_patterns:
            pattern_type = pattern.pattern_type
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        # Find most common pattern
        if pattern_counts:
            return max(pattern_counts.items(), key=lambda x: x[1])[0]
        
        return None 