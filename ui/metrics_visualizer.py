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
Metrics Visualization
Visualizes system metrics and reason patterns
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import colorsys
from enum import Enum
import time
from collections import deque
from .reason_patterns import ReasonPatternAnalyzer, PatternType

class ReasonType(Enum):
    """Types of reasoning decisions."""
    STABILIZING = "stabilizing"  # Maintaining harmony
    EXPLORATIVE = "explorative"  # Seeking new patterns
    REACTIVE = "reactive"       # Responding to strain
    HARMONIC = "harmonic"       # Achieving insight
    DEFERRED = "deferred"       # Waiting for better conditions

@dataclass
class ReasonEvent:
    """A reasoning decision event."""
    timestamp: float
    reason_type: ReasonType
    cause: str
    effect: str
    resonance: float
    mirror_confirmed: bool

class SparklineCanvas(tk.Canvas):
    """Canvas for drawing sparkline visualizations."""
    
    def __init__(self, parent, width=200, height=100, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.padding = 10
        self.data: List[float] = []
        self.reason_events: List[ReasonEvent] = []
        self.pattern_analyzer = ReasonPatternAnalyzer()
    
    def update_data(self, data: List[float], reason_events: List[ReasonEvent]):
        """Update the sparkline data and reason events."""
        self.data = data
        self.reason_events = reason_events
        
        # Add events to pattern analyzer
        for event in reason_events:
            self.pattern_analyzer.add_reason_event(event)
        
        self._draw()
    
    def _draw(self):
        """Draw the sparkline with reason events."""
        self.delete("all")
        
        if not self.data:
            return
        
        # Calculate scaling
        data_min = min(self.data)
        data_max = max(self.data)
        data_range = data_max - data_min if data_max > data_min else 1.0
        
        # Draw sparkline
        points = []
        for i, value in enumerate(self.data):
            x = self.padding + (i * (self.width - 2 * self.padding) / (len(self.data) - 1))
            y = self.height - self.padding - ((value - data_min) / data_range * (self.height - 2 * self.padding))
            points.extend([x, y])
        
        # Draw the line
        self.create_line(points, fill="#4a90e2", width=2, smooth=True)
        
        # Draw reason events
        for event in self.reason_events:
            if event.timestamp >= self.data[0] and event.timestamp <= self.data[-1]:
                # Calculate x position
                x = self.padding + ((event.timestamp - self.data[0]) / 
                                  (self.data[-1] - self.data[0]) * 
                                  (self.width - 2 * self.padding))
                
                # Draw reason spark
                self._draw_reason_spark(x, event)
        
        # Draw pattern indicators
        self._draw_pattern_indicators()
    
    def _draw_reason_spark(self, x: float, event: ReasonEvent):
        """Draw a reason event spark."""
        # Draw the spark
        spark_color = {
            ReasonType.STABILIZING: "#4a90e2",  # Blue
            ReasonType.EXPLORATIVE: "#50e3c2",  # Green
            ReasonType.REACTIVE: "#e35050",     # Red
            ReasonType.HARMONIC: "#f5a623",     # Gold
            ReasonType.DEFERRED: "#9b9b9b"      # Gray
        }.get(event.reason_type, "#9b9b9b")
        
        # Draw spark point
        self.create_oval(x-3, self.height/2-3, x+3, self.height/2+3,
                        fill=spark_color, outline="")
        
        # Draw resonance ring if significant
        if event.resonance > 0.7:
            ring_radius = 5 + (event.resonance * 5)
            self.create_oval(x-ring_radius, self.height/2-ring_radius,
                           x+ring_radius, self.height/2+ring_radius,
                           outline=spark_color, width=1)
        
        # Draw mirror confirmation if present
        if event.mirror_confirmed:
            self.create_text(x, self.height/2-10,
                           text="🪞", font=("Arial", 8))
    
    def _draw_pattern_indicators(self):
        """Draw pattern indicators."""
        pattern_summary = self.pattern_analyzer.get_pattern_summary()
        if not pattern_summary:
            return
        
        # Draw pattern bridges
        for pattern in pattern_summary["recent_patterns"]:
            if pattern["mirror_echo"]:
                # Calculate pattern start and end positions
                start_x = self.padding + ((pattern["start_time"] - self.data[0]) / 
                                        (self.data[-1] - self.data[0]) * 
                                        (self.width - 2 * self.padding))
                end_x = self.padding + ((pattern["end_time"] - self.data[0]) / 
                                      (self.data[-1] - self.data[0]) * 
                                      (self.width - 2 * self.padding))
                
                # Draw pattern bridge
                self.create_line(start_x, self.height/2,
                               end_x, self.height/2,
                               fill="#f5a623", width=2, dash=(4, 4))
                
                # Draw pattern type indicator
                self.create_text((start_x + end_x) / 2, self.height/2 - 15,
                               text=pattern["type"][:3].upper(),
                               font=("Arial", 8), fill="#f5a623")

class HeatmapCanvas(tk.Canvas):
    """Canvas for drawing heatmap visualizations."""
    
    def __init__(self, parent, width=200, height=100, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.padding = 10
        self.matrix: List[List[float]] = []
        self.pattern_analyzer = ReasonPatternAnalyzer()
    
    def update_matrix(self, matrix: List[List[float]], pattern_summary: Dict[str, Any]):
        """Update the heatmap matrix and pattern summary."""
        self.matrix = matrix
        self._draw()
    
    def _draw(self):
        """Draw the heatmap with pattern overlays."""
        self.delete("all")
        
        if not self.matrix:
            return
        
        # Calculate cell size
        cell_width = (self.width - 2 * self.padding) / len(self.matrix[0])
        cell_height = (self.height - 2 * self.padding) / len(self.matrix)
        
        # Draw heatmap
        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                x = self.padding + j * cell_width
                y = self.padding + i * cell_height
                
                # Calculate color intensity
                intensity = int(value * 255)
                color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
                
                # Draw cell
                self.create_rectangle(x, y, x + cell_width, y + cell_height,
                                    fill=color, outline="")
        
        # Draw pattern overlays
        self._draw_pattern_overlays()
    
    def _draw_pattern_overlays(self):
        """Draw pattern overlays on the heatmap."""
        pattern_summary = self.pattern_analyzer.get_pattern_summary()
        if not pattern_summary:
            return
        
        # Draw domain activation overlays
        for pattern in pattern_summary["recent_patterns"]:
            for domain, activation in pattern["domain_activation"].items():
                if activation > 0.5:  # Only show significant activations
                    # Calculate overlay position based on domain
                    x = self.padding + {
                        "cryptographer": 0,
                        "arbiter": 1,
                        "mirror": 2,
                        "purveyor": 3
                    }.get(domain, 0) * (self.width - 2 * self.padding) / 4
                    
                    y = self.padding + (pattern["start_time"] % 1) * (self.height - 2 * self.padding)
                    
                    # Draw domain activation indicator
                    self.create_oval(x-5, y-5, x+5, y+5,
                                   fill="#f5a623", outline="")
                    
                    # Draw activation level
                    self.create_text(x, y-10,
                                   text=f"{int(activation*100)}%",
                                   font=("Arial", 8), fill="#f5a623")

class MetricsVisualizer(ttk.Frame):
    """Visualizes system metrics and reason patterns."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.pattern_analyzer = ReasonPatternAnalyzer()
        
        # Create sections
        self._create_anchor_section()
        self._create_phase_section()
        self._create_recovery_section()
        self._create_pattern_section()
    
    def _create_anchor_section(self):
        """Create the anchor load visualization section."""
        frame = ttk.LabelFrame(self, text="Anchor Load")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Core anchor load
        ttk.Label(frame, text="Core Anchor Load").pack()
        self.core_load = SparklineCanvas(frame)
        self.core_load.pack(fill=tk.X, padx=5, pady=5)
        
        # Shadow anchor load
        ttk.Label(frame, text="Shadow Anchor Load").pack()
        self.shadow_load = SparklineCanvas(frame)
        self.shadow_load.pack(fill=tk.X, padx=5, pady=5)
        
        # Coherence matrix
        ttk.Label(frame, text="Coherence Matrix").pack()
        self.coherence_matrix = HeatmapCanvas(frame)
        self.coherence_matrix.pack(fill=tk.X, padx=5, pady=5)
    
    def _create_phase_section(self):
        """Create the phase stress visualization section."""
        frame = ttk.LabelFrame(self, text="Phase Stress")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Phase horizon stress
        ttk.Label(frame, text="Phase Horizon Stress").pack()
        self.phase_stress = SparklineCanvas(frame)
        self.phase_stress.pack(fill=tk.X, padx=5, pady=5)
        
        # Breach activity
        ttk.Label(frame, text="Breach Activity").pack()
        self.breach_activity = SparklineCanvas(frame)
        self.breach_activity.pack(fill=tk.X, padx=5, pady=5)
        
        # Stability matrix
        ttk.Label(frame, text="Stability Matrix").pack()
        self.stability_matrix = HeatmapCanvas(frame)
        self.stability_matrix.pack(fill=tk.X, padx=5, pady=5)
    
    def _create_recovery_section(self):
        """Create the recovery behavior visualization section."""
        frame = ttk.LabelFrame(self, text="Recovery Behavior")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # LOW-RHYTHM cooldown
        ttk.Label(frame, text="LOW-RHYTHM Cooldown").pack()
        self.cooldown = SparklineCanvas(frame)
        self.cooldown.pack(fill=tk.X, padx=5, pady=5)
        
        # Recovery progress
        ttk.Label(frame, text="Recovery Progress").pack()
        self.recovery_progress = SparklineCanvas(frame)
        self.recovery_progress.pack(fill=tk.X, padx=5, pady=5)
        
        # Recovery stability matrix
        ttk.Label(frame, text="Recovery Stability Matrix").pack()
        self.recovery_matrix = HeatmapCanvas(frame)
        self.recovery_matrix.pack(fill=tk.X, padx=5, pady=5)
    
    def _create_pattern_section(self):
        """Create the pattern analysis section."""
        frame = ttk.LabelFrame(self, text="Reason Patterns")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Pattern timeline
        ttk.Label(frame, text="Pattern Timeline").pack()
        self.pattern_timeline = tk.Text(frame, height=5, wrap=tk.WORD)
        self.pattern_timeline.pack(fill=tk.X, padx=5, pady=5)
        
        # Domain activation
        ttk.Label(frame, text="Domain Activation").pack()
        self.domain_activation = SparklineCanvas(frame)
        self.domain_activation.pack(fill=tk.X, padx=5, pady=5)
        
        # Pattern prediction
        ttk.Label(frame, text="Pattern Prediction").pack()
        self.pattern_prediction = ttk.Label(frame, text="")
        self.pattern_prediction.pack(padx=5, pady=5)
    
    def update_metrics(self, metrics: Dict[str, Any]):
        """Update all visualizations with new metrics."""
        # Update anchor load visualizations
        self.core_load.update_data(
            metrics["anchor_load"]["core_load"],
            metrics["reason_events"]
        )
        self.shadow_load.update_data(
            metrics["anchor_load"]["shadow_load"],
            metrics["reason_events"]
        )
        self.coherence_matrix.update_matrix(
            metrics["anchor_load"]["coherence_matrix"],
            self.pattern_analyzer.get_pattern_summary()
        )
        
        # Update phase stress visualizations
        self.phase_stress.update_data(
            metrics["phase_stress"]["horizon_stress"],
            metrics["reason_events"]
        )
        self.breach_activity.update_data(
            metrics["phase_stress"]["breach_activity"],
            metrics["reason_events"]
        )
        self.stability_matrix.update_matrix(
            metrics["phase_stress"]["stability_matrix"],
            self.pattern_analyzer.get_pattern_summary()
        )
        
        # Update recovery visualizations
        self.cooldown.update_data(
            metrics["recovery"]["cooldown"],
            metrics["reason_events"]
        )
        self.recovery_progress.update_data(
            metrics["recovery"]["progress"],
            metrics["reason_events"]
        )
        self.recovery_matrix.update_matrix(
            metrics["recovery"]["stability_matrix"],
            self.pattern_analyzer.get_pattern_summary()
        )
        
        # Update pattern analysis
        self._update_pattern_analysis()
    
    def _update_pattern_analysis(self):
        """Update the pattern analysis section."""
        pattern_summary = self.pattern_analyzer.get_pattern_summary()
        if not pattern_summary:
            return
        
        # Update pattern timeline
        self.pattern_timeline.delete(1.0, tk.END)
        for pattern in pattern_summary["recent_patterns"]:
            self.pattern_timeline.insert(tk.END,
                f"[{pattern['type']}] {pattern['sequence']} "
                f"(Resonance: {pattern['resonance']:.2f}, "
                f"Tightness: {pattern['loop_tightness']:.2f})\n"
            )
        
        # Update domain activation
        domain_data = []
        for domain, trend in pattern_summary["domain_trends"].items():
            domain_data.append(trend["current"])
        self.domain_activation.update_data(domain_data, [])
        
        # Update pattern prediction
        next_pattern = self.pattern_analyzer.predict_next_pattern()
        if next_pattern:
            self.pattern_prediction.config(
                text=f"Next Pattern: {next_pattern.value.upper()}"
            ) 