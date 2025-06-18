"""
Voice Memory Visualizer Module

Provides visualization of voice memory patterns and breath cycles,
honoring Scarab and Jester's RAP-5 invocation.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional
from datetime import datetime
import json
from .breath_cycle_visualizer import BreathCycleVisualizer
from .visualization import BaseVisualizer

class VoiceMemoryVisualizer(ttk.Frame):
    """Visualizes voice memory patterns and breath cycles."""
    
    def __init__(self, parent: Optional[ttk.Frame] = None):
        """Initialize the voice memory visualizer.
        
        Args:
            parent: Optional parent frame
        """
        super().__init__(parent)
        self.breath_visualizer = BreathCycleVisualizer()
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
        """Create visualization widgets."""
        # Create chart container
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create controls
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add control buttons
        self.clear_button = ttk.Button(
            self.controls_frame,
            text="Clear",
            command=self.clear
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.export_button = ttk.Button(
            self.controls_frame,
            text="Export",
            command=self.export_data
        )
        self.export_button.pack(side=tk.LEFT, padx=5)
        
    def _create_layout(self):
        """Create the visualization layout."""
        # Create chart container
        self.chart_container = ttk.Frame(self.chart_frame)
        self.chart_container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize chart
        self._initialize_chart()
        
    def _initialize_chart(self):
        """Initialize the Chart.js visualization."""
        # Create HTML container for Chart.js
        self.chart_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <canvas id="breathChart"></canvas>
            <script>
                const ctx = document.getElementById('breathChart').getContext('2d');
                const chart = new Chart(ctx, {json.dumps(self.breath_visualizer.get_chart_config())});
            </script>
        </body>
        </html>
        """
        
        # Create WebView for chart
        self.chart_view = ttk.Frame(self.chart_container)
        self.chart_view.pack(fill=tk.BOTH, expand=True)
        
    def update_state(self, state: Dict[str, Any]) -> None:
        """Update visualization with new state.
        
        Args:
            state: Dictionary containing visualization state
        """
        if 'breath_cycle' in state:
            amplitude = state['breath_cycle'].get('amplitude', 0.0)
            timestamp = state['breath_cycle'].get('timestamp')
            if timestamp:
                timestamp = datetime.fromisoformat(timestamp)
            self.breath_visualizer.update_cycle(amplitude, timestamp)
            self._update_chart()
            
    def _update_chart(self) -> None:
        """Update the chart with current data."""
        # Update chart configuration
        config = self.breath_visualizer.get_chart_config()
        
        # Update chart HTML
        self.chart_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <canvas id="breathChart"></canvas>
            <script>
                const ctx = document.getElementById('breathChart').getContext('2d');
                const chart = new Chart(ctx, {json.dumps(config)});
            </script>
        </body>
        </html>
        """
        
        # Refresh chart view
        self.chart_view.update()
        
    def clear(self) -> None:
        """Clear all visualization data."""
        self.breath_visualizer.clear()
        self._update_chart()
        
    def export_data(self) -> None:
        """Export visualization data."""
        self.breath_visualizer.export_cycle_data('breath_cycle_data.json')
        
    def update_animation(self, anim_id: str, anim_state: Dict[str, Any]) -> None:
        """Update animation state.
        
        Args:
            anim_id: Animation identifier
            anim_state: Animation state data
        """
        if anim_id.startswith('breath_'):
            # Handle breath cycle animations
            if 'amplitude' in anim_state:
                self.breath_visualizer.update_cycle(
                    anim_state['amplitude'],
                    datetime.fromisoformat(anim_state.get('timestamp', datetime.now().isoformat()))
                )
                self._update_chart() 