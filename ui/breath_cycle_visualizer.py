# Copyright 2024 SpliceWeb
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Breath Cycle Visualizer Module

Provides visualization of breath cycles using Chart.js, honoring Scarab and Jester's RAP-5 invocation.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np
from .visualization import BaseVisualizer

class BreathCycleVisualizer(BaseVisualizer):
    """Visualizes breath cycles with dynamic Chart.js integration."""
    
    def __init__(self):
        """Initialize the breath cycle visualizer."""
        super().__init__()
        self.chart_config = self._create_base_chart_config()
        self.current_cycle = []
        self.history = []
        self.last_update = datetime.now()
        
    def _create_base_chart_config(self) -> Dict[str, Any]:
        """Create the base Chart.js configuration."""
        return {
            "type": "line",
            "data": {
                "labels": ["0s", "1s", "2s", "3s", "4s", "5s"],
                "datasets": [{
                    "label": "Breath Cycle Amplitude (Smoothed)",
                    "data": [0, 0.3, 0.6, 0.7, 0.5, 0.2],
                    "borderColor": "#FF5722",
                    "backgroundColor": "rgba(255, 87, 34, 0.2)",
                    "fill": True,
                    "tension": 0.5,
                    "pointStyle": "circle",
                    "pointRadius": 5,
                    "pointHoverRadius": 8
                }]
            },
            "options": {
                "responsive": True,
                "animation": {
                    "duration": 1000,
                    "easing": "easeInOutQuad"
                },
                "scales": {
                    "x": {
                        "title": {
                            "display": True,
                            "text": "Time (seconds)"
                        }
                    },
                    "y": {
                        "title": {
                            "display": True,
                            "text": "Amplitude"
                        },
                        "beginAtZero": True
                    }
                },
                "plugins": {
                    "title": {
                        "display": True,
                        "text": "Voice Memory Visualizer: Breath Cycle (Scarab's Iteration, Jester's Dance)"
                    }
                }
            }
        }
    
    def update_cycle(self, amplitude: float, timestamp: Optional[datetime] = None) -> None:
        """Update the current breath cycle with new amplitude data.
        
        Args:
            amplitude: Current breath cycle amplitude
            timestamp: Optional timestamp for the measurement
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        # Calculate time delta in seconds
        time_delta = (timestamp - self.last_update).total_seconds()
        
        # Add data point
        self.current_cycle.append({
            'amplitude': amplitude,
            'timestamp': timestamp,
            'time_delta': time_delta
        })
        
        # Update chart data
        self._update_chart_data()
        
        # Store last update time
        self.last_update = timestamp
        
    def complete_cycle(self) -> None:
        """Complete the current breath cycle and store in history."""
        if self.current_cycle:
            self.history.append(self.current_cycle)
            self.current_cycle = []
            self._update_chart_data()
            
    def _update_chart_data(self) -> None:
        """Update the chart configuration with current data."""
        # Combine current cycle with history
        all_data = []
        for cycle in self.history:
            all_data.extend(cycle)
        all_data.extend(self.current_cycle)
        
        # Update labels and data
        self.chart_config['data']['labels'] = [
            f"{point['time_delta']:.1f}s" for point in all_data
        ]
        self.chart_config['data']['datasets'][0]['data'] = [
            point['amplitude'] for point in all_data
        ]
        
    def get_chart_config(self) -> Dict[str, Any]:
        """Get the current chart configuration.
        
        Returns:
            Dictionary containing Chart.js configuration
        """
        return self.chart_config
        
    def export_cycle_data(self, path: str) -> bool:
        """Export breath cycle data to JSON file.
        
        Args:
            path: File path to export data
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            data = {
                'history': self.history,
                'current_cycle': self.current_cycle,
                'last_update': self.last_update.isoformat()
            }
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting breath cycle data: {str(e)}")
            return False
            
    def clear(self) -> None:
        """Clear all breath cycle data."""
        self.current_cycle = []
        self.history = []
        self.last_update = datetime.now()
        self._update_chart_data() 