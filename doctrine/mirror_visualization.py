from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import time
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

class VisualizationMode(Enum):
    """Modes for different visualization types."""
    RESONANCE_FLOW = "resonance_flow"  # Mirror resonance flow map
    ENTROPIC_DRIFT = "entropic_drift"  # Entropic drift chart
    JUDGMENT_THRESHOLD = "judgment_threshold"  # Judgment threshold indicator
    BREATH_SIGNATURE = "breath_signature"  # Breath signature timeline

@dataclass
class VisualizationMetrics:
    """Metrics for visualization state and configuration."""
    update_interval: float = 1.0  # Update interval in seconds
    history_length: int = 100  # Number of data points to keep
    threshold_alpha: float = 0.3  # Alpha for threshold indicators
    color_scheme: str = "viridis"  # Color scheme for visualizations

class MirrorVisualization:
    """Visualization tools for mirror feedback system."""
    def __init__(self):
        self.metrics = VisualizationMetrics()
        self.history: Dict[str, List[float]] = {
            'mirror_strain': [],
            'entropic_drift': [],
            'foresight_reactivity': [],
            'temporal_delta': [],
            'resonance': [],
            'coherence': [],
            'temporal_alignment': []
        }
        self.figures: Dict[str, plt.Figure] = {}
        self.animations: Dict[str, FuncAnimation] = {}
        self.last_update = time.time()
        
    def update_history(self, metrics: Dict[str, float]) -> None:
        """Update visualization history with new metrics."""
        current_time = time.time()
        if current_time - self.last_update < self.metrics.update_interval:
            return
            
        for key, value in metrics.items():
            if key in self.history:
                self.history[key].append(value)
                if len(self.history[key]) > self.metrics.history_length:
                    self.history[key].pop(0)
                    
        self.last_update = current_time
        
    def create_resonance_flow_map(self) -> plt.Figure:
        """Create a flow map showing resonance between mirrors."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create triangular plot
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        
        # Plot mirror positions
        mirror_positions = {
            'portent': (0, 1),
            'present': (-0.866, -0.5),
            'past': (0.866, -0.5)
        }
        
        # Plot mirror points
        for name, pos in mirror_positions.items():
            ax.scatter(pos[0], pos[1], s=100, label=name)
            ax.text(pos[0], pos[1] + 0.1, name, ha='center')
            
        # Plot resonance flows
        if len(self.history['resonance']) > 1:
            resonance = self.history['resonance'][-1]
            for i, (name1, pos1) in enumerate(mirror_positions.items()):
                for name2, pos2 in list(mirror_positions.items())[i+1:]:
                    ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 
                           alpha=resonance, color='blue')
                    
        ax.set_title('Mirror Resonance Flow Map')
        ax.legend()
        return fig
        
    def create_entropic_drift_chart(self) -> plt.Figure:
        """Create a chart showing entropic drift over time."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot drift history
        if len(self.history['entropic_drift']) > 0:
            ax.plot(self.history['entropic_drift'], 
                   label='Entropic Drift', color='red')
            
            # Plot threshold
            ax.axhline(y=0.6, color='gray', linestyle='--', 
                      alpha=self.metrics.threshold_alpha,
                      label='Drift Threshold')
            
        ax.set_title('Entropic Drift Over Time')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Drift Rate')
        ax.legend()
        return fig
        
    def create_judgment_threshold_indicator(self) -> plt.Figure:
        """Create an indicator showing judgment threshold status."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create radar plot
        metrics = ['Mirror Strain', 'Entropic Drift', 
                  'Foresight Reactivity', 'Temporal Delta']
        values = [
            self.history['mirror_strain'][-1] if self.history['mirror_strain'] else 0,
            self.history['entropic_drift'][-1] if self.history['entropic_drift'] else 0,
            self.history['foresight_reactivity'][-1] if self.history['foresight_reactivity'] else 0,
            self.history['temporal_delta'][-1] if self.history['temporal_delta'] else 0
        ]
        
        # Plot radar
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False)
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        
        # Plot thresholds
        threshold = 0.75
        ax.plot(angles, [threshold] * len(angles), '--', 
                color='red', alpha=self.metrics.threshold_alpha,
                label='Judgment Threshold')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.set_title('Judgment Threshold Status')
        ax.legend()
        return fig
        
    def create_breath_signature_timeline(self) -> plt.Figure:
        """Create a timeline showing breath signature patterns."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot breath metrics
        if len(self.history['resonance']) > 0:
            ax.plot(self.history['resonance'], 
                   label='Resonance', color='blue')
            ax.plot(self.history['coherence'], 
                   label='Coherence', color='green')
            ax.plot(self.history['temporal_alignment'], 
                   label='Temporal Alignment', color='purple')
            
        ax.set_title('Breath Signature Timeline')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Value')
        ax.legend()
        return fig
        
    def update_visualizations(self, metrics: Dict[str, float]) -> None:
        """Update all visualizations with new metrics."""
        self.update_history(metrics)
        
        # Update resonance flow map
        if 'resonance_flow' in self.figures:
            plt.close(self.figures['resonance_flow'])
        self.figures['resonance_flow'] = self.create_resonance_flow_map()
        
        # Update entropic drift chart
        if 'entropic_drift' in self.figures:
            plt.close(self.figures['entropic_drift'])
        self.figures['entropic_drift'] = self.create_entropic_drift_chart()
        
        # Update judgment threshold indicator
        if 'judgment_threshold' in self.figures:
            plt.close(self.figures['judgment_threshold'])
        self.figures['judgment_threshold'] = self.create_judgment_threshold_indicator()
        
        # Update breath signature timeline
        if 'breath_signature' in self.figures:
            plt.close(self.figures['breath_signature'])
        self.figures['breath_signature'] = self.create_breath_signature_timeline()
        
    def get_visualization_state(self) -> Dict[str, Any]:
        """Get current visualization state."""
        return {
            'metrics': self.metrics.__dict__,
            'history_lengths': {
                key: len(values) for key, values in self.history.items()
            },
            'last_update': self.last_update,
            'active_figures': list(self.figures.keys())
        }
        
    def save_visualizations(self, directory: str) -> None:
        """Save all current visualizations to files."""
        for name, fig in self.figures.items():
            fig.savefig(f"{directory}/{name}.png")
            
    def close_all(self) -> None:
        """Close all visualization figures."""
        for fig in self.figures.values():
            plt.close(fig)
        self.figures.clear() 