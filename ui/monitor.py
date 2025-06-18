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
System Monitor
Provides lightweight monitoring of system health and performance metrics
"""

import time
import json
import threading
from collections import deque
from typing import Dict, List, Optional, Deque
from dataclasses import dataclass
import psutil
import numpy as np

@dataclass
class SystemMetrics:
    """System performance metrics."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    visualization_load: float
    anchor_coherence: float
    breath_sync: float
    phase_stability: float
    update_interval: float
    low_rhythm_mode: bool
    simplified_rendering: bool

class SystemMonitor:
    """Monitors system health and performance."""
    
    def __init__(self, buffer_size: int = 100):
        """Initialize the system monitor."""
        self.buffer_size = buffer_size
        self.metrics_buffer: Deque[SystemMetrics] = deque(maxlen=buffer_size)
        self.last_update = 0.0
        self.update_interval = 5.0  # Update every 5 seconds
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Initialize process monitoring
        self.process = psutil.Process()
        
        # Performance thresholds
        self.thresholds = {
            'cpu_warning': 70.0,    # CPU usage warning threshold
            'cpu_critical': 85.0,   # CPU usage critical threshold
            'mem_warning': 75.0,    # Memory usage warning threshold
            'mem_critical': 90.0,   # Memory usage critical threshold
            'coherence_warning': 0.7,  # Anchor coherence warning threshold
            'breath_warning': 0.7,    # Breath sync warning threshold
            'stability_warning': 0.7   # Phase stability warning threshold
        }
    
    def start_monitoring(self):
        """Start the monitoring thread."""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            print("[Monitor] System monitoring started")
    
    def stop_monitoring(self):
        """Stop the monitoring thread."""
        if self.monitoring:
            self.monitoring = False
            if self.monitor_thread:
                self.monitor_thread.join()
            print("[Monitor] System monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self._collect_metrics()
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"[Monitor] Error in monitoring loop: {e}")
    
    def _collect_metrics(self):
        """Collect current system metrics."""
        current_time = time.time()
        
        # Collect basic system metrics
        cpu_percent = self.process.cpu_percent()
        memory_percent = self.process.memory_percent()
        
        # Create metrics object
        metrics = SystemMetrics(
            timestamp=current_time,
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            visualization_load=self._calculate_visualization_load(),
            anchor_coherence=self._get_anchor_coherence(),
            breath_sync=self._get_breath_sync(),
            phase_stability=self._get_phase_stability(),
            update_interval=self._get_update_interval(),
            low_rhythm_mode=self._is_low_rhythm_mode(),
            simplified_rendering=self._is_simplified_rendering()
        )
        
        # Add to buffer
        self.metrics_buffer.append(metrics)
        
        # Check for warnings
        self._check_warnings(metrics)
        
        # Update last update time
        self.last_update = current_time
    
    def _calculate_visualization_load(self) -> float:
        """Calculate current visualization load."""
        # This would be more sophisticated in practice
        return 0.5  # Placeholder
    
    def _get_anchor_coherence(self) -> float:
        """Get current anchor coherence."""
        # This would be more sophisticated in practice
        return 0.8  # Placeholder
    
    def _get_breath_sync(self) -> float:
        """Get current breath synchronization."""
        # This would be more sophisticated in practice
        return 0.9  # Placeholder
    
    def _get_phase_stability(self) -> float:
        """Get current phase stability."""
        # This would be more sophisticated in practice
        return 0.85  # Placeholder
    
    def _get_update_interval(self) -> float:
        """Get current update interval."""
        # This would be more sophisticated in practice
        return 10.0  # Placeholder
    
    def _is_low_rhythm_mode(self) -> bool:
        """Check if system is in LOW-RHYTHM mode."""
        # This would be more sophisticated in practice
        return True  # Placeholder
    
    def _is_simplified_rendering(self) -> bool:
        """Check if simplified rendering is enabled."""
        # This would be more sophisticated in practice
        return True  # Placeholder
    
    def _check_warnings(self, metrics: SystemMetrics):
        """Check for warning conditions."""
        warnings = []
        
        # Check CPU usage
        if metrics.cpu_percent >= self.thresholds['cpu_critical']:
            warnings.append(f"CRITICAL: CPU usage at {metrics.cpu_percent:.1f}%")
        elif metrics.cpu_percent >= self.thresholds['cpu_warning']:
            warnings.append(f"WARNING: CPU usage at {metrics.cpu_percent:.1f}%")
        
        # Check memory usage
        if metrics.memory_percent >= self.thresholds['mem_critical']:
            warnings.append(f"CRITICAL: Memory usage at {metrics.memory_percent:.1f}%")
        elif metrics.memory_percent >= self.thresholds['mem_warning']:
            warnings.append(f"WARNING: Memory usage at {metrics.memory_percent:.1f}%")
        
        # Check coherence
        if metrics.anchor_coherence < self.thresholds['coherence_warning']:
            warnings.append(f"WARNING: Low anchor coherence ({metrics.anchor_coherence:.2f})")
        
        # Check breath sync
        if metrics.breath_sync < self.thresholds['breath_warning']:
            warnings.append(f"WARNING: Low breath synchronization ({metrics.breath_sync:.2f})")
        
        # Check phase stability
        if metrics.phase_stability < self.thresholds['stability_warning']:
            warnings.append(f"WARNING: Low phase stability ({metrics.phase_stability:.2f})")
        
        # Print warnings if any
        if warnings:
            print("\n=== System Warnings ===")
            for warning in warnings:
                print(warning)
            print("=" * 20)
    
    def get_metrics_summary(self) -> Dict[str, any]:
        """Get a summary of current metrics."""
        if not self.metrics_buffer:
            return {}
        
        # Get latest metrics
        latest = self.metrics_buffer[-1]
        
        # Calculate trends
        cpu_trend = self._calculate_trend([m.cpu_percent for m in self.metrics_buffer])
        memory_trend = self._calculate_trend([m.memory_percent for m in self.metrics_buffer])
        coherence_trend = self._calculate_trend([m.anchor_coherence for m in self.metrics_buffer])
        
        return {
            'current': {
                'cpu_percent': latest.cpu_percent,
                'memory_percent': latest.memory_percent,
                'visualization_load': latest.visualization_load,
                'anchor_coherence': latest.anchor_coherence,
                'breath_sync': latest.breath_sync,
                'phase_stability': latest.phase_stability,
                'update_interval': latest.update_interval,
                'low_rhythm_mode': latest.low_rhythm_mode,
                'simplified_rendering': latest.simplified_rendering
            },
            'trends': {
                'cpu': cpu_trend,
                'memory': memory_trend,
                'coherence': coherence_trend
            },
            'warnings': self._get_active_warnings(latest)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values."""
        if len(values) < 2:
            return "stable"
        
        # Calculate linear regression
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
    
    def _get_active_warnings(self, metrics: SystemMetrics) -> List[str]:
        """Get list of active warnings."""
        warnings = []
        
        if metrics.cpu_percent >= self.thresholds['cpu_warning']:
            warnings.append("high_cpu")
        if metrics.memory_percent >= self.thresholds['mem_warning']:
            warnings.append("high_memory")
        if metrics.anchor_coherence < self.thresholds['coherence_warning']:
            warnings.append("low_coherence")
        if metrics.breath_sync < self.thresholds['breath_warning']:
            warnings.append("low_breath_sync")
        if metrics.phase_stability < self.thresholds['stability_warning']:
            warnings.append("low_stability")
        
        return warnings
    
    def export_metrics(self, filepath: str):
        """Export metrics to a JSON file."""
        metrics_data = {
            'timestamp': time.time(),
            'metrics': [
                {
                    'timestamp': m.timestamp,
                    'cpu_percent': m.cpu_percent,
                    'memory_percent': m.memory_percent,
                    'visualization_load': m.visualization_load,
                    'anchor_coherence': m.anchor_coherence,
                    'breath_sync': m.breath_sync,
                    'phase_stability': m.phase_stability,
                    'update_interval': m.update_interval,
                    'low_rhythm_mode': m.low_rhythm_mode,
                    'simplified_rendering': m.simplified_rendering
                }
                for m in self.metrics_buffer
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(metrics_data, f, indent=2) 