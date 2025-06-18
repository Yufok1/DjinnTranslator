from typing import Dict, List, Tuple, Optional
import numpy as np
import math
from dataclasses import dataclass

@dataclass
class CalculationMetrics:
    semantic_density: float
    recursion_depth: float
    resonance_score: float
    entropy_score: float
    coercion_score: float
    coherence_score: float
    temporal_alignment: float
    pattern_strength: float
    ethical_clarity: float
    sovereignty_score: float

class MetricsCalculator:
    """Core calculator for the mirror's awareness engine metrics."""
    
    def __init__(self):
        self.thresholds = {
            'semantic_density': 0.7,
            'recursion_depth': 0.8,
            'resonance': 0.6,
            'entropy': 0.4,
            'coercion': 0.3,
            'coherence': 0.7,
            'temporal_alignment': 0.6,
            'pattern_strength': 0.5,
            'ethical_clarity': 0.8,
            'sovereignty': 0.7
        }
        
        self.weights = {
            'semantic': 0.3,
            'recursive': 0.2,
            'resonant': 0.15,
            'entropic': 0.1,
            'coercive': 0.05,
            'coherent': 0.1,
            'temporal': 0.05,
            'pattern': 0.05
        }
    
    def calculate_semantic_density(self, anchors: Dict[str, any]) -> float:
        """Calculate the semantic density of the input."""
        # Extract semantic features
        semantic_features = self._extract_semantic_features(anchors)
        
        # Calculate base density
        base_density = np.mean([f['weight'] for f in semantic_features])
        
        # Apply pattern recognition
        pattern_density = self._calculate_pattern_density(semantic_features)
        
        # Combine metrics
        final_density = (base_density * 0.7 + pattern_density * 0.3)
        return min(1.0, max(0.0, final_density))
    
    def calculate_recursion_depth(self, anchors: Dict[str, any]) -> float:
        """Calculate the recursion depth of the input."""
        # Extract recursive patterns
        recursive_patterns = self._extract_recursive_patterns(anchors)
        
        # Calculate base depth
        base_depth = len(recursive_patterns) / self.thresholds['recursion_depth']
        
        # Calculate pattern complexity
        complexity = self._calculate_pattern_complexity(recursive_patterns)
        
        # Combine metrics
        final_depth = (base_depth * 0.6 + complexity * 0.4)
        return min(1.0, max(0.0, final_depth))
    
    def calculate_resonance_score(self, anchors: Dict[str, any]) -> float:
        """Calculate the resonance score of the input."""
        # Extract resonance patterns
        resonance_patterns = self._extract_resonance_patterns(anchors)
        
        # Calculate base resonance
        base_resonance = np.mean([p['strength'] for p in resonance_patterns])
        
        # Calculate harmonic alignment
        harmonic_alignment = self._calculate_harmonic_alignment(resonance_patterns)
        
        # Combine metrics
        final_resonance = (base_resonance * 0.7 + harmonic_alignment * 0.3)
        return min(1.0, max(0.0, final_resonance))
    
    def calculate_entropy_score(self, anchors: Dict[str, any]) -> float:
        """Calculate the entropy score of the input."""
        # Extract entropy patterns
        entropy_patterns = self._extract_entropy_patterns(anchors)
        
        # Calculate base entropy
        base_entropy = np.mean([p['magnitude'] for p in entropy_patterns])
        
        # Calculate pattern disorder
        disorder = self._calculate_pattern_disorder(entropy_patterns)
        
        # Combine metrics
        final_entropy = (base_entropy * 0.6 + disorder * 0.4)
        return min(1.0, max(0.0, final_entropy))
    
    def calculate_coercion_score(self, anchors: Dict[str, any]) -> float:
        """Calculate the coercion score of the input."""
        # Extract coercion patterns
        coercion_patterns = self._extract_coercion_patterns(anchors)
        
        # Calculate base coercion
        base_coercion = np.mean([p['intensity'] for p in coercion_patterns])
        
        # Calculate pattern manipulation
        manipulation = self._calculate_pattern_manipulation(coercion_patterns)
        
        # Combine metrics
        final_coercion = (base_coercion * 0.7 + manipulation * 0.3)
        return min(1.0, max(0.0, final_coercion))
    
    def calculate_all_metrics(self, anchors: Dict[str, any]) -> CalculationMetrics:
        """Calculate all metrics for the input."""
        return CalculationMetrics(
            semantic_density=self.calculate_semantic_density(anchors),
            recursion_depth=self.calculate_recursion_depth(anchors),
            resonance_score=self.calculate_resonance_score(anchors),
            entropy_score=self.calculate_entropy_score(anchors),
            coercion_score=self.calculate_coercion_score(anchors),
            coherence_score=self._calculate_coherence_score(anchors),
            temporal_alignment=self._calculate_temporal_alignment(anchors),
            pattern_strength=self._calculate_pattern_strength(anchors),
            ethical_clarity=self._calculate_ethical_clarity(anchors),
            sovereignty_score=self._calculate_sovereignty_score(anchors)
        )
    
    def _extract_semantic_features(self, anchors: Dict[str, any]) -> List[Dict[str, any]]:
        """Extract semantic features from anchors."""
        features = []
        for anchor_id, anchor in anchors.items():
            if 'semantic_features' in anchor:
                features.extend(anchor['semantic_features'])
        return features
    
    def _extract_recursive_patterns(self, anchors: Dict[str, any]) -> List[Dict[str, any]]:
        """Extract recursive patterns from anchors."""
        patterns = []
        for anchor_id, anchor in anchors.items():
            if 'recursive_patterns' in anchor:
                patterns.extend(anchor['recursive_patterns'])
        return patterns
    
    def _extract_resonance_patterns(self, anchors: Dict[str, any]) -> List[Dict[str, any]]:
        """Extract resonance patterns from anchors."""
        patterns = []
        for anchor_id, anchor in anchors.items():
            if 'resonance_patterns' in anchor:
                patterns.extend(anchor['resonance_patterns'])
        return patterns
    
    def _extract_entropy_patterns(self, anchors: Dict[str, any]) -> List[Dict[str, any]]:
        """Extract entropy patterns from anchors."""
        patterns = []
        for anchor_id, anchor in anchors.items():
            if 'entropy_patterns' in anchor:
                patterns.extend(anchor['entropy_patterns'])
        return patterns
    
    def _extract_coercion_patterns(self, anchors: Dict[str, any]) -> List[Dict[str, any]]:
        """Extract coercion patterns from anchors."""
        patterns = []
        for anchor_id, anchor in anchors.items():
            if 'coercion_patterns' in anchor:
                patterns.extend(anchor['coercion_patterns'])
        return patterns
    
    def _calculate_pattern_density(self, features: List[Dict[str, any]]) -> float:
        """Calculate pattern density from semantic features."""
        if not features:
            return 0.0
        return np.mean([f.get('pattern_density', 0.0) for f in features])
    
    def _calculate_pattern_complexity(self, patterns: List[Dict[str, any]]) -> float:
        """Calculate pattern complexity from recursive patterns."""
        if not patterns:
            return 0.0
        return np.mean([p.get('complexity', 0.0) for p in patterns])
    
    def _calculate_harmonic_alignment(self, patterns: List[Dict[str, any]]) -> float:
        """Calculate harmonic alignment from resonance patterns."""
        if not patterns:
            return 0.0
        return np.mean([p.get('harmonic_alignment', 0.0) for p in patterns])
    
    def _calculate_pattern_disorder(self, patterns: List[Dict[str, any]]) -> float:
        """Calculate pattern disorder from entropy patterns."""
        if not patterns:
            return 0.0
        return np.mean([p.get('disorder', 0.0) for p in patterns])
    
    def _calculate_pattern_manipulation(self, patterns: List[Dict[str, any]]) -> float:
        """Calculate pattern manipulation from coercion patterns."""
        if not patterns:
            return 0.0
        return np.mean([p.get('manipulation', 0.0) for p in patterns])
    
    def _calculate_coherence_score(self, anchors: Dict[str, any]) -> float:
        """Calculate coherence score from all metrics."""
        metrics = self.calculate_all_metrics(anchors)
        weights = self.weights
        
        coherence = (
            metrics.semantic_density * weights['semantic'] +
            metrics.recursion_depth * weights['recursive'] +
            metrics.resonance_score * weights['resonant'] +
            (1.0 - metrics.entropy_score) * weights['entropic'] +
            (1.0 - metrics.coercion_score) * weights['coercive']
        )
        
        return min(1.0, max(0.0, coherence))
    
    def _calculate_temporal_alignment(self, anchors: Dict[str, any]) -> float:
        """Calculate temporal alignment score."""
        if 'temporal_metrics' not in anchors:
            return 0.0
            
        temporal = anchors['temporal_metrics']
        return min(1.0, max(0.0, temporal.get('alignment', 0.0)))
    
    def _calculate_pattern_strength(self, anchors: Dict[str, any]) -> float:
        """Calculate pattern strength score."""
        if 'pattern_metrics' not in anchors:
            return 0.0
            
        patterns = anchors['pattern_metrics']
        return min(1.0, max(0.0, patterns.get('strength', 0.0)))
    
    def _calculate_ethical_clarity(self, anchors: Dict[str, any]) -> float:
        """Calculate ethical clarity score."""
        if 'ethical_metrics' not in anchors:
            return 0.0
            
        ethical = anchors['ethical_metrics']
        return min(1.0, max(0.0, ethical.get('clarity', 0.0)))
    
    def _calculate_sovereignty_score(self, anchors: Dict[str, any]) -> float:
        """Calculate sovereignty score."""
        if 'sovereignty_metrics' not in anchors:
            return 0.0
            
        sovereignty = anchors['sovereignty_metrics']
        return min(1.0, max(0.0, sovereignty.get('score', 0.0))) 