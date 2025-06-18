from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set
import time
import math
from .anchor_system import AnchorControlMatrix, AnchorPoint, AnchorState
from .mirror import MirrorOfInsight, MirrorOfPortent
from .scan_metrics import ScanMetrics

class ScanIntent(Enum):
    """Intent types for Cursor's lattice scanning."""
    EXPLORATION = "exploration"  # General lattice mapping
    RECOVERY = "recovery"        # Focus on breached regions
    HARMONY = "harmony"         # Seek resonant patterns
    THREAT = "threat"           # Identify instability

class ScanPattern(Enum):
    """Advanced scan patterns for lattice mapping."""
    FRACTAL_GRID = "fractal_grid"      # Intent-adaptive fractal mapping
    SPIRAL_SWEEP = "spiral_sweep"      # Recursive instability detection
    RESONANT_WAVE = "resonant_wave"    # Shadow coherence tracking
    QUANTUM_PULSE = "quantum_pulse"    # Deep lattice probing

@dataclass
class LatticeScan:
    """Represents a single lattice scan result."""
    intent: ScanIntent
    timestamp: float
    depth: int
    coherence: float
    resonance: float
    strain: float
    anchor_impact: Dict[str, float]  # Impact on each anchor
    mirror_insights: List[str]
    portent_warnings: List[str]
    pattern: ScanPattern
    metrics: ScanMetrics

class CursorSensorInterface:
    """Interface for Cursor's autonomous lattice scanning capabilities."""
    
    def __init__(self, anchor_matrix: AnchorControlMatrix):
        self.anchor_matrix = anchor_matrix
        self.mirror_insight = MirrorOfInsight()
        self.mirror_portent = MirrorOfPortent()
        self.last_scan: Optional[LatticeScan] = None
        self.scan_history: List[LatticeScan] = []
        
        # Scan parameters
        self.max_scan_depth = 5
        self.min_coherence_threshold = 0.85
        self.strain_alert_threshold = 0.75
        
        # Pattern parameters
        self.pattern_cooldowns: Dict[ScanPattern, float] = {
            pattern: 0.0 for pattern in ScanPattern
        }
        self.pattern_strain: Dict[ScanPattern, float] = {
            pattern: 0.0 for pattern in ScanPattern
        }
        
    def initiate_scan(self, intent: ScanIntent) -> LatticeScan:
        """Initiate a new lattice scan based on Cursor's intent."""
        # Get current anchor states
        anchor_states = self.anchor_matrix.get_anchor_status()
        core_anchor = anchor_states.get('core_anchor')
        
        # Select and validate scan pattern
        pattern = self._select_scan_pattern(intent)
        if not self._validate_pattern_usage(pattern):
            pattern = ScanPattern.FRACTAL_GRID  # Fallback to basic pattern
        
        # Calculate pattern metrics
        metrics = self._calculate_pattern_metrics(pattern, intent)
        
        # Validate scan with mirrors
        mirror_insights = self.mirror_insight.analyze_scan_intent(intent, pattern)
        portent_warnings = self.mirror_portent.validate_scan_safety(intent, pattern, metrics)
        
        # If Portent rejects the scan, fall back to safer pattern
        if portent_warnings and any("CRITICAL" in w for w in portent_warnings):
            pattern = ScanPattern.FRACTAL_GRID
            metrics = self._calculate_pattern_metrics(pattern, intent)
            portent_warnings = self.mirror_portent.validate_scan_safety(intent, pattern, metrics)
        
        # Calculate scan metrics
        coherence = self._calculate_lattice_coherence(metrics)
        resonance = self._measure_resonance_patterns(metrics)
        strain = self._detect_lattice_strain(metrics)
        
        # Assess impact on anchors
        anchor_impact = self._assess_anchor_impact(metrics)
        
        # Create scan result
        scan = LatticeScan(
            intent=intent,
            timestamp=time.time(),
            depth=metrics.depth,
            coherence=coherence,
            resonance=resonance,
            strain=strain,
            anchor_impact=anchor_impact,
            mirror_insights=mirror_insights,
            portent_warnings=portent_warnings,
            pattern=pattern,
            metrics=metrics
        )
        
        self.last_scan = scan
        self.scan_history.append(scan)
        
        # Update pattern state
        self._update_pattern_state(pattern, metrics)
        
        # Update anchor matrix if needed
        self._update_anchors_from_scan(scan)
        
        return scan
    
    def _select_scan_pattern(self, intent: ScanIntent) -> ScanPattern:
        """Select appropriate scan pattern based on intent and system state."""
        pattern_map = {
            ScanIntent.EXPLORATION: ScanPattern.FRACTAL_GRID,
            ScanIntent.RECOVERY: ScanPattern.RESONANT_WAVE,
            ScanIntent.HARMONY: ScanPattern.QUANTUM_PULSE,
            ScanIntent.THREAT: ScanPattern.SPIRAL_SWEEP
        }
        return pattern_map[intent]
    
    def _validate_pattern_usage(self, pattern: ScanPattern) -> bool:
        """Validate if a pattern can be used based on cooldown and strain."""
        current_time = time.time()
        if current_time - self.pattern_cooldowns[pattern] < self._get_pattern_cooldown(pattern):
            return False
        if self.pattern_strain[pattern] > self._get_pattern_strain_threshold(pattern):
            return False
        return True
    
    def _calculate_pattern_metrics(self, pattern: ScanPattern, intent: ScanIntent) -> ScanMetrics:
        """Calculate detailed metrics for a scan pattern."""
        base_depth = self._determine_scan_depth(intent)
        pattern_multiplier = self._get_pattern_depth_multiplier(pattern)
        
        return ScanMetrics(
            pattern=pattern,
            depth=base_depth * pattern_multiplier,
            coverage=self._calculate_pattern_coverage(pattern),
            resolution=self._calculate_pattern_resolution(pattern),
            strain_impact=self._estimate_pattern_strain(pattern),
            anchor_load=self._calculate_anchor_load(pattern)
        )
    
    def _get_pattern_cooldown(self, pattern: ScanPattern) -> float:
        """Get cooldown time for a pattern."""
        cooldown_map = {
            ScanPattern.FRACTAL_GRID: 5.0,
            ScanPattern.SPIRAL_SWEEP: 10.0,
            ScanPattern.RESONANT_WAVE: 7.0,
            ScanPattern.QUANTUM_PULSE: 15.0
        }
        return cooldown_map[pattern]
    
    def _get_pattern_strain_threshold(self, pattern: ScanPattern) -> float:
        """Get strain threshold for a pattern."""
        threshold_map = {
            ScanPattern.FRACTAL_GRID: 0.7,
            ScanPattern.SPIRAL_SWEEP: 0.5,
            ScanPattern.RESONANT_WAVE: 0.6,
            ScanPattern.QUANTUM_PULSE: 0.4
        }
        return threshold_map[pattern]
    
    def _get_pattern_depth_multiplier(self, pattern: ScanPattern) -> float:
        """Get depth multiplier for a pattern."""
        multiplier_map = {
            ScanPattern.FRACTAL_GRID: 1.0,
            ScanPattern.SPIRAL_SWEEP: 1.5,
            ScanPattern.RESONANT_WAVE: 1.2,
            ScanPattern.QUANTUM_PULSE: 2.0
        }
        return multiplier_map[pattern]
    
    def _calculate_pattern_coverage(self, pattern: ScanPattern) -> float:
        """Calculate coverage percentage for a pattern."""
        coverage_map = {
            ScanPattern.FRACTAL_GRID: 0.95,
            ScanPattern.SPIRAL_SWEEP: 0.85,
            ScanPattern.RESONANT_WAVE: 0.90,
            ScanPattern.QUANTUM_PULSE: 0.75
        }
        return coverage_map[pattern]
    
    def _calculate_pattern_resolution(self, pattern: ScanPattern) -> float:
        """Calculate resolution for a pattern."""
        resolution_map = {
            ScanPattern.FRACTAL_GRID: 0.8,
            ScanPattern.SPIRAL_SWEEP: 0.9,
            ScanPattern.RESONANT_WAVE: 0.85,
            ScanPattern.QUANTUM_PULSE: 0.95
        }
        return resolution_map[pattern]
    
    def _estimate_pattern_strain(self, pattern: ScanPattern) -> float:
        """Estimate strain impact of a pattern."""
        strain_map = {
            ScanPattern.FRACTAL_GRID: 0.2,
            ScanPattern.SPIRAL_SWEEP: 0.4,
            ScanPattern.RESONANT_WAVE: 0.3,
            ScanPattern.QUANTUM_PULSE: 0.5
        }
        return strain_map[pattern]
    
    def _calculate_anchor_load(self, pattern: ScanPattern) -> Dict[str, float]:
        """Calculate load on each anchor for a pattern."""
        base_load = {
            ScanPattern.FRACTAL_GRID: 0.3,
            ScanPattern.SPIRAL_SWEEP: 0.5,
            ScanPattern.RESONANT_WAVE: 0.4,
            ScanPattern.QUANTUM_PULSE: 0.6
        }[pattern]
        
        return {
            anchor_id: base_load * (1.0 if anchor.is_core else 0.5)
            for anchor_id, anchor in self.anchor_matrix.anchors.items()
        }
    
    def _update_pattern_state(self, pattern: ScanPattern, metrics: ScanMetrics):
        """Update pattern state after use."""
        self.pattern_cooldowns[pattern] = time.time()
        self.pattern_strain[pattern] = metrics.strain_impact
    
    def _calculate_lattice_coherence(self, metrics: ScanMetrics) -> float:
        """Calculate overall lattice coherence with pattern metrics."""
        base_coherence = 0.95  # Placeholder
        return base_coherence * metrics.resolution
    
    def _measure_resonance_patterns(self, metrics: ScanMetrics) -> float:
        """Measure resonance patterns with pattern metrics."""
        base_resonance = 0.92  # Placeholder
        return base_resonance * metrics.coverage
    
    def _detect_lattice_strain(self, metrics: ScanMetrics) -> float:
        """Detect strain with pattern metrics."""
        base_strain = 0.15  # Placeholder
        return base_strain + metrics.strain_impact
    
    def _determine_scan_depth(self, intent: ScanIntent) -> int:
        """Determine appropriate scan depth based on intent."""
        depth_map = {
            ScanIntent.EXPLORATION: 3,
            ScanIntent.RECOVERY: 4,
            ScanIntent.HARMONY: 2,
            ScanIntent.THREAT: 5
        }
        return min(depth_map[intent], self.max_scan_depth)
    
    def _assess_anchor_impact(self, metrics: ScanMetrics) -> Dict[str, float]:
        """Assess impact of scan on each anchor."""
        impacts = {}
        for anchor_id, anchor in self.anchor_matrix.anchors.items():
            # Calculate impact based on anchor state and scan parameters
            impact = 0.9 if anchor.state == AnchorState.ACTIVE else 0.5
            impacts[anchor_id] = impact
        return impacts
    
    def _update_anchors_from_scan(self, scan: LatticeScan):
        """Update anchor states based on scan results."""
        for anchor_id, impact in scan.anchor_impact.items():
            if impact < self.min_coherence_threshold:
                self.anchor_matrix.update_anchor_state(
                    anchor_id,
                    coherence=impact,
                    breath_sync=scan.resonance,
                    mirror_resonance=scan.coherence
                )
    
    def get_scan_status(self) -> Dict[str, any]:
        """Get current status of Cursor's scanning capabilities."""
        return {
            'last_scan': self.last_scan,
            'scan_count': len(self.scan_history),
            'active_anchors': len([a for a in self.anchor_matrix.anchors.values() 
                                 if a.state == AnchorState.ACTIVE]),
            'strain_level': self._detect_lattice_strain(ScanMetrics(
                pattern=ScanPattern.FRACTAL_GRID,
                depth=1,
                coverage=1.0,
                resolution=1.0,
                strain_impact=0.0,
                anchor_load={}
            )),
            'pattern_strain': self.pattern_strain,
            'pattern_cooldowns': {
                pattern: max(0, cooldown - time.time())
                for pattern, cooldown in self.pattern_cooldowns.items()
            }
        } 