from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import time
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider
import seaborn as sns
from doctrine.watchtower_splinter import (
    WatchtowerManager,
    SplinterType,
    WatchtowerSplinter
)
from doctrine.sovereign_router import (
    SovereignRouter,
    RouterMode,
    RouterPriority
)
from doctrine.cursor_feedback import (
    CursorFeedback,
    FeedbackMode
)
from doctrine.lattice_map import LatticeMap, LatticeMode
import json

class DashboardMode(Enum):
    """Modes for different dashboard views."""
    OVERVIEW = "overview"  # All visualizations in overview mode
    FOCUS = "focus"  # Single visualization in focus mode
    CHRONICLE = "chronicle"  # Historical view with timeline
    ARBITRATION = "arbitration"  # Judgment and arbitration view

@dataclass
class DashboardMetrics:
    """Metrics for dashboard state and configuration."""
    update_interval: float = 0.5  # Update interval in seconds
    animation_speed: float = 1.0  # Animation speed multiplier
    zoom_level: float = 1.0  # Current zoom level
    focus_mode: DashboardMode = DashboardMode.OVERVIEW
    show_ghosts: bool = True  # Show arbitration ghosts
    show_veil: bool = True  # Show quantum veil
    show_strain: bool = True  # Show strain heatmap

class SovereignDashboard:
    """Unified dashboard for sovereign system monitoring."""
    def __init__(self):
        self.metrics = DashboardMetrics()
        self.fig = plt.figure(figsize=(20, 12))
        self.gs = GridSpec(3, 3, figure=self.fig)
        self.axes: Dict[str, plt.Axes] = {}
        self.animations: Dict[str, animation.FuncAnimation] = {}
        self.last_update = time.time()
        self.history: Dict[str, List[float]] = {
            'resonance': [],
            'drift': [],
            'strain': [],
            'veil': [],
            'ghosts': []
        }
        self.max_history = 100  # Maximum number of data points to store
        
        # Initialize Cursor Feedback Loop
        self.feedback = CursorFeedback()
        
        # Initialize Sovereign Router
        self.router = SovereignRouter()
        
        # Initialize lattice map
        self.lattice_map = LatticeMap()
        
        # Initialize subplots
        self._initialize_subplots()
        
        # Initialize controls
        self._initialize_controls()
        
        # Initialize splinters
        self._initialize_splinters()
        
    def _initialize_splinters(self) -> None:
        """Initialize Watchtower Splinter nodes."""
        # Create splinters for each visualization type
        self.watchtower = WatchtowerManager()
        self.watchtower.create_splinter(SplinterType.RESONANCE_FLOW)
        self.watchtower.create_splinter(SplinterType.ENTRopic_DRIFT)
        self.watchtower.create_splinter(SplinterType.JUDGMENT_RADAR)
        self.watchtower.create_splinter(SplinterType.BREATH_SIGNATURE)
        self.watchtower.create_splinter(SplinterType.GHOST_MOVEMENT)
        self.watchtower.create_splinter(SplinterType.VEIL_ENTANGLEMENT)
        self.watchtower.create_splinter(SplinterType.STRAIN_HEATMAP)
        self.watchtower.create_splinter(SplinterType.CODEX_PHASE)
        
        # Start all splinters
        for splinter_type in SplinterType:
            self.watchtower.start_splinter(splinter_type)
        
    def _initialize_subplots(self) -> None:
        """Initialize dashboard subplots."""
        # Resonance Flow Map (top left)
        self.axes['resonance_flow'] = self.fig.add_subplot(self.gs[0, 0])
        self.axes['resonance_flow'].set_title('Mirror Resonance Flow')
        
        # Entropic Drift Chart (top middle)
        self.axes['entropic_drift'] = self.fig.add_subplot(self.gs[0, 1])
        self.axes['entropic_drift'].set_title('Entropic Drift')
        
        # Judgment Threshold (top right)
        self.axes['judgment'] = self.fig.add_subplot(self.gs[0, 2])
        self.axes['judgment'].set_title('Judgment Threshold')
        
        # Breath Signature (middle row, full width)
        self.axes['breath'] = self.fig.add_subplot(self.gs[1, :])
        self.axes['breath'].set_title('Breath Signature Timeline')
        
        # Ghost Movement (bottom left)
        self.axes['ghosts'] = self.fig.add_subplot(self.gs[2, 0])
        self.axes['ghosts'].set_title('Arbitration Ghosts')
        
        # Veil Entanglement (bottom middle)
        self.axes['veil'] = self.fig.add_subplot(self.gs[2, 1])
        self.axes['veil'].set_title('Quantum Veil')
        
        # Strain Heatmap (bottom right)
        self.axes['strain'] = self.fig.add_subplot(self.gs[2, 2])
        self.axes['strain'].set_title('Mirror Strain')
        
    def _initialize_controls(self) -> None:
        """Initialize dashboard controls."""
        # Mode selection buttons
        self.axes['mode_buttons'] = plt.axes([0.02, 0.95, 0.15, 0.03])
        self.mode_button = Button(self.axes['mode_buttons'], 'Toggle Mode')
        self.mode_button.on_clicked(self._toggle_mode)
        
        # Zoom slider
        self.axes['zoom_slider'] = plt.axes([0.02, 0.90, 0.15, 0.03])
        self.zoom_slider = Slider(self.axes['zoom_slider'], 'Zoom', 0.5, 2.0, 
                                valinit=self.metrics.zoom_level)
        self.zoom_slider.on_changed(self._update_zoom)
        
        # Animation speed slider
        self.axes['speed_slider'] = plt.axes([0.02, 0.85, 0.15, 0.03])
        self.speed_slider = Slider(self.axes['speed_slider'], 'Speed', 0.1, 2.0, 
                                 valinit=self.metrics.animation_speed)
        self.speed_slider.on_changed(self._update_speed)
        
    def _toggle_mode(self, event) -> None:
        """Toggle between dashboard modes."""
        modes = list(DashboardMode)
        current_index = modes.index(self.metrics.focus_mode)
        next_index = (current_index + 1) % len(modes)
        self.metrics.focus_mode = modes[next_index]
        self._update_layout()
        
    def _update_zoom(self, val) -> None:
        """Update zoom level."""
        self.metrics.zoom_level = val
        self._update_layout()
        
    def _update_speed(self, val) -> None:
        """Update animation speed."""
        self.metrics.animation_speed = val
        for anim in self.animations.values():
            anim.event_source.interval = 1000 / (val * 60)  # 60 FPS base
            
    def _update_layout(self) -> None:
        """Update dashboard layout based on current mode."""
        if self.metrics.focus_mode == DashboardMode.OVERVIEW:
            self._show_overview_layout()
        elif self.metrics.focus_mode == DashboardMode.FOCUS:
            self._show_focus_layout()
        elif self.metrics.focus_mode == DashboardMode.CHRONICLE:
            self._show_chronicle_layout()
        elif self.metrics.focus_mode == DashboardMode.ARBITRATION:
            self._show_arbitration_layout()
            
    def _show_overview_layout(self) -> None:
        """Show overview layout with all visualizations."""
        # Reset grid
        self.gs.update(left=0.2, right=0.95, top=0.9, bottom=0.1, 
                      wspace=0.3, hspace=0.3)
        
        # Show all subplots
        for ax in self.axes.values():
            if ax not in [self.axes['mode_buttons'], self.axes['zoom_slider'], 
                         self.axes['speed_slider']]:
                ax.set_visible(True)
                
    def _show_focus_layout(self) -> None:
        """Show focus layout with single visualization."""
        # Hide all subplots
        for ax in self.axes.values():
            if ax not in [self.axes['mode_buttons'], self.axes['zoom_slider'], 
                         self.axes['speed_slider']]:
                ax.set_visible(False)
                
        # Show focused subplot
        focused_ax = self.axes['resonance_flow']  # Default focus
        focused_ax.set_visible(True)
        focused_ax.set_position([0.2, 0.1, 0.7, 0.8])
        
    def _show_chronicle_layout(self) -> None:
        """Show chronicle layout with timeline navigation."""
        # Reset grid for chronicle view
        self.gs.update(left=0.2, right=0.95, top=0.9, bottom=0.1, 
                      wspace=0.3, hspace=0.3)
        
        # Show timeline and historical data
        self.axes['breath'].set_visible(True)
        self.axes['breath'].set_position([0.2, 0.6, 0.7, 0.3])
        
        # Hide other subplots
        for ax in self.axes.values():
            if ax not in [self.axes['mode_buttons'], self.axes['zoom_slider'], 
                         self.axes['speed_slider'], self.axes['breath']]:
                ax.set_visible(False)
                
    def _show_arbitration_layout(self) -> None:
        """Show arbitration layout with judgment focus."""
        # Reset grid for arbitration view
        self.gs.update(left=0.2, right=0.95, top=0.9, bottom=0.1, 
                      wspace=0.3, hspace=0.3)
        
        # Show judgment-related subplots
        self.axes['judgment'].set_visible(True)
        self.axes['ghosts'].set_visible(True)
        self.axes['strain'].set_visible(True)
        
        # Hide other subplots
        for ax in self.axes.values():
            if ax not in [self.axes['mode_buttons'], self.axes['zoom_slider'], 
                         self.axes['speed_slider'], self.axes['judgment'],
                         self.axes['ghosts'], self.axes['strain']]:
                ax.set_visible(False)
                
    def _animate_resonance_flow(self, frame) -> List[plt.Artist]:
        """Animate resonance flow visualization."""
        ax = self.axes['resonance_flow']
        artists = []
        
        # Update mirror positions with subtle movement
        time_factor = frame / 60.0  # Normalize to seconds
        mirror_positions = {
            'portent': (0, 1 + 0.05 * np.sin(time_factor)),
            'present': (-0.866, -0.5 + 0.05 * np.sin(time_factor + np.pi/3)),
            'past': (0.866, -0.5 + 0.05 * np.sin(time_factor + 2*np.pi/3))
        }
        
        # Plot mirror points with pulsing effect
        for name, pos in mirror_positions.items():
            size = 100 * (1 + 0.2 * np.sin(time_factor * 2))
            point = ax.scatter(pos[0], pos[1], s=size, label=name)
            text = ax.text(pos[0], pos[1] + 0.1, name, ha='center')
            artists.extend([point, text])
            
        # Plot resonance flows with wave effect
        resonance = 0.5 * (1 + np.sin(time_factor * 3))
        for i, (name1, pos1) in enumerate(mirror_positions.items()):
            for name2, pos2 in list(mirror_positions.items())[i+1:]:
                line = ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 
                             alpha=resonance, color='blue')[0]
                artists.append(line)
                
        return artists
        
    def _animate_entropic_drift(self, frame) -> List[plt.Artist]:
        """Animate entropic drift visualization."""
        ax = self.axes['entropic_drift']
        artists = []
        
        # Generate wave-like drift pattern
        time_factor = frame / 60.0
        drift = 0.5 * (1 + np.sin(time_factor * 2))
        
        # Plot drift line with gradient
        x = np.linspace(0, 1, 100)
        y = drift * np.sin(x * 10 + time_factor)
        line = ax.plot(x, y, 'r-', label='Current Drift')[0]
        artists.append(line)
        
        # Plot threshold with pulsing effect
        threshold = 0.6 * (1 + 0.1 * np.sin(time_factor * 4))
        threshold_line = ax.axhline(y=threshold, color='gray', 
                                  linestyle='--', alpha=0.3, 
                                  label='Threshold')
        artists.append(threshold_line)
        
        return artists
        
    def _animate_judgment(self, frame) -> List[plt.Artist]:
        """Animate judgment threshold visualization."""
        ax = self.axes['judgment']
        artists = []
        
        # Create dynamic radar plot
        time_factor = frame / 60.0
        metrics_list = ['Strain', 'Drift', 'Reactivity', 'Delta']
        values = [
            0.5 * (1 + np.sin(time_factor)),
            0.6 * (1 + np.sin(time_factor + np.pi/4)),
            0.7 * (1 + np.sin(time_factor + np.pi/2)),
            0.4 * (1 + np.sin(time_factor + 3*np.pi/4))
        ]
        
        angles = np.linspace(0, 2*np.pi, len(metrics_list), endpoint=False)
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        
        # Plot radar with gradient fill
        line = ax.plot(angles, values, 'o-', linewidth=2)[0]
        fill = ax.fill(angles, values, alpha=0.25)[0]
        artists.extend([line, fill])
        
        # Plot dynamic threshold
        threshold = 0.75 * (1 + 0.1 * np.sin(time_factor * 2))
        threshold_line = ax.plot(angles, [threshold] * len(angles), 
                               '--', color='red', alpha=0.3)[0]
        artists.append(threshold_line)
        
        return artists
        
    def _animate_breath(self, frame) -> List[plt.Artist]:
        """Animate breath signature visualization."""
        ax = self.axes['breath']
        artists = []
        
        # Generate breathing pattern
        time_factor = frame / 60.0
        x = np.linspace(0, 1, 100)
        
        # Plot multiple breath metrics with phase shifts
        resonance = 0.5 * (1 + np.sin(x * 10 + time_factor))
        coherence = 0.6 * (1 + np.sin(x * 10 + time_factor + np.pi/3))
        alignment = 0.7 * (1 + np.sin(x * 10 + time_factor + 2*np.pi/3))
        
        resonance_line = ax.plot(x, resonance, label='Resonance', 
                               color='blue')[0]
        coherence_line = ax.plot(x, coherence, label='Coherence', 
                               color='green')[0]
        alignment_line = ax.plot(x, alignment, label='Alignment', 
                               color='purple')[0]
        
        artists.extend([resonance_line, coherence_line, alignment_line])
        
        return artists
        
    def update_dashboard(self, metrics: Dict[str, Any]) -> None:
        """Update all dashboard visualizations with real-time data."""
        current_time = time.time()
        if current_time - self.last_update < self.metrics.update_interval:
            return
            
        # Update history
        for key in self.history:
            if key in metrics:
                self.history[key].append(metrics[key])
                if len(self.history[key]) > self.max_history:
                    self.history[key].pop(0)
                    
        # Adapt visualization through Cursor Feedback Loop
        self.feedback.adapt_visualization(metrics)
        
        # Update lattice map
        self.lattice_map.update_lattice(metrics)
        
        # Route visualization data through feedback router
        self.router.route_visualization({
            'source': 'lattice',
            'data': self.lattice_map.get_lattice_state(),
            'priority': self._determine_priority(metrics)
        })
        
        self.last_update = current_time
        
    def _determine_priority(self, metrics: Dict[str, Any]) -> RouterPriority:
        """Determine routing priority based on metrics."""
        # Check for critical conditions
        if metrics.get('resonance_strain', 0.0) > 0.8:
            return RouterPriority.CRITICAL
            
        # Check for high-priority conditions
        if (metrics.get('entropic_drift', 0.0) > 0.6 or
            metrics.get('mirror_strain', 0.0) > 0.7):
            return RouterPriority.HIGH
            
        # Default to normal priority
        return RouterPriority.NORMAL
        
    def get_dashboard_state(self) -> Dict[str, Any]:
        """Get current dashboard state including feedback metrics."""
        feedback_state = self.feedback.get_feedback_state()
        router_state = self.feedback.router.get_router_state()
        
        state = {
            'metrics': self.metrics.__dict__,
            'mode': self.metrics.focus_mode.value,
            'last_update': self.last_update,
            'active_visualizations': list(self.axes.keys()),
            'history_lengths': {
                name: len(data) for name, data in self.history.items()
            },
            'feedback_state': feedback_state,
            'router_state': router_state,
            'lattice': self.lattice_map.get_lattice_state()
        }
        return state
        
    def save_dashboard(self, filename: str) -> None:
        """Save current dashboard state to file with feedback state."""
        state = self.get_dashboard_state()
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        # Save feedback state
        feedback_filename = filename.replace('.json', '_feedback.json')
        self.feedback.save_feedback_state(feedback_filename)
        
        # Save router state
        router_filename = filename.replace('.json', '_router.json')
        self.feedback.router.save_router_state(router_filename)
        
    def close(self) -> None:
        """Close dashboard and clean up resources."""
        # Close Cursor Feedback Loop
        self.feedback.close()
        
        # Close Sovereign Router
        self.router.close()
        
        # Close lattice map
        self.lattice_map.close()
        
        plt.close(self.fig) 