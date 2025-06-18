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
Configuration Manager Module
Handles system configuration and threshold settings
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

@dataclass
class SystemThresholds:
    """System threshold configurations"""
    # CPU thresholds
    cpu_warning: float = 70.0
    cpu_critical: float = 85.0
    cpu_recovery_target: float = 60.0
    
    # Memory thresholds
    memory_warning: float = 75.0
    memory_critical: float = 85.0
    memory_recovery_target: float = 65.0
    
    # Cycle time thresholds (ms)
    cycle_warning: float = 40.0
    cycle_critical: float = 50.0
    cycle_recovery_target: float = 30.0
    
    # Error rate thresholds
    error_rate_warning: float = 0.05  # 5%
    error_rate_critical: float = 0.10  # 10%
    error_rate_recovery_target: float = 0.02  # 2%
    
    # Audio buffer thresholds
    buffer_warning: float = 0.8  # 80%
    buffer_critical: float = 0.9  # 90%
    buffer_recovery_target: float = 0.7  # 70%
    
    # Thread count thresholds
    thread_warning: int = 15
    thread_critical: int = 20
    thread_recovery_target: int = 10

@dataclass
class RecoveryConfig:
    """Recovery strategy configurations"""
    # Memory optimization
    memory_optimization_enabled: bool = True
    memory_optimization_interval: int = 60  # seconds
    aggressive_memory_cleanup: bool = False
    
    # Cycle time optimization
    cycle_optimization_enabled: bool = True
    cycle_optimization_interval: int = 30  # seconds
    dynamic_cycle_adjustment: bool = True
    
    # Error mitigation
    error_mitigation_enabled: bool = True
    error_retry_count: int = 3
    error_retry_delay: float = 1.0  # seconds
    
    # Recovery tracking
    recovery_history_size: int = 100
    performance_impact_threshold: float = 0.1  # 10% improvement required

@dataclass
class VisualizationConfig:
    """Visualization configurations"""
    # Update intervals
    basic_update_interval: int = 1000  # ms
    advanced_update_interval: int = 5000  # ms
    
    # Chart configurations
    time_series_window: int = 3600  # 1 hour
    heatmap_resolution: int = 10  # minutes
    histogram_bins: int = 20
    
    # Display options
    show_trend_lines: bool = True
    show_confidence_intervals: bool = True
    show_outliers: bool = True
    
    # Export options
    auto_export_interval: int = 3600  # 1 hour
    export_format: str = "png"
    export_directory: str = "analysis"

@dataclass
class SystemConfig:
    """Complete system configuration"""
    thresholds: SystemThresholds
    recovery: RecoveryConfig
    visualization: VisualizationConfig
    
    @classmethod
    def default(cls) -> 'SystemConfig':
        """Create default configuration"""
        return cls(
            thresholds=SystemThresholds(),
            recovery=RecoveryConfig(),
            visualization=VisualizationConfig()
        )

class ConfigManager:
    """Manages system configuration"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.logger = logging.getLogger('ConfigManager')
    
    def _load_config(self) -> SystemConfig:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return SystemConfig(
                        thresholds=SystemThresholds(**data['thresholds']),
                        recovery=RecoveryConfig(**data['recovery']),
                        visualization=VisualizationConfig(**data['visualization'])
                    )
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
        
        # Return default config if loading fails
        return SystemConfig.default()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    'thresholds': asdict(self.config.thresholds),
                    'recovery': asdict(self.config.recovery),
                    'visualization': asdict(self.config.visualization)
                }, f, indent=2)
            self.logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")
    
    def update_thresholds(self, new_thresholds: Dict[str, Any]):
        """Update threshold configurations"""
        for key, value in new_thresholds.items():
            if hasattr(self.config.thresholds, key):
                setattr(self.config.thresholds, key, value)
        self.save_config()
    
    def update_recovery_config(self, new_config: Dict[str, Any]):
        """Update recovery configurations"""
        for key, value in new_config.items():
            if hasattr(self.config.recovery, key):
                setattr(self.config.recovery, key, value)
        self.save_config()
    
    def update_visualization_config(self, new_config: Dict[str, Any]):
        """Update visualization configurations"""
        for key, value in new_config.items():
            if hasattr(self.config.visualization, key):
                setattr(self.config.visualization, key, value)
        self.save_config()
    
    def get_threshold_level(self, metric: str, value: float) -> str:
        """Get threshold level for a metric value"""
        thresholds = self.config.thresholds
        
        if metric == 'cpu':
            if value >= thresholds.cpu_critical:
                return 'critical'
            elif value >= thresholds.cpu_warning:
                return 'warning'
        elif metric == 'memory':
            if value >= thresholds.memory_critical:
                return 'critical'
            elif value >= thresholds.memory_warning:
                return 'warning'
        elif metric == 'cycle_time':
            if value >= thresholds.cycle_critical:
                return 'critical'
            elif value >= thresholds.cycle_warning:
                return 'warning'
        elif metric == 'error_rate':
            if value >= thresholds.error_rate_critical:
                return 'critical'
            elif value >= thresholds.error_rate_warning:
                return 'warning'
        elif metric == 'buffer':
            if value >= thresholds.buffer_critical:
                return 'critical'
            elif value >= thresholds.buffer_warning:
                return 'warning'
        elif metric == 'threads':
            if value >= thresholds.thread_critical:
                return 'critical'
            elif value >= thresholds.thread_warning:
                return 'warning'
        
        return 'normal'
    
    def get_recovery_target(self, metric: str) -> float:
        """Get recovery target for a metric"""
        thresholds = self.config.thresholds
        
        if metric == 'cpu':
            return thresholds.cpu_recovery_target
        elif metric == 'memory':
            return thresholds.memory_recovery_target
        elif metric == 'cycle_time':
            return thresholds.cycle_recovery_target
        elif metric == 'error_rate':
            return thresholds.error_rate_recovery_target
        elif metric == 'buffer':
            return thresholds.buffer_recovery_target
        elif metric == 'threads':
            return thresholds.thread_recovery_target
        
        return 0.0

def main():
    """Test the configuration manager"""
    # Create config manager
    manager = ConfigManager()
    
    # Print current configuration
    print("Current Configuration:")
    print(json.dumps({
        'thresholds': asdict(manager.config.thresholds),
        'recovery': asdict(manager.config.recovery),
        'visualization': asdict(manager.config.visualization)
    }, indent=2))
    
    # Test threshold levels
    test_values = {
        'cpu': 80.0,
        'memory': 85.0,
        'cycle_time': 45.0,
        'error_rate': 0.08,
        'buffer': 0.85,
        'threads': 18
    }
    
    print("\nThreshold Levels:")
    for metric, value in test_values.items():
        level = manager.get_threshold_level(metric, value)
        print(f"{metric}: {value} -> {level}")
    
    # Test recovery targets
    print("\nRecovery Targets:")
    for metric in test_values.keys():
        target = manager.get_recovery_target(metric)
        print(f"{metric}: {target}")

if __name__ == '__main__':
    main() 