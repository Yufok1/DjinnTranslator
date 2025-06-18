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
Kernel Stabilization Module
Handles system stability monitoring and kernel health checks
"""

import os
import time
import json
import logging
import psutil
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from queue import Queue
import numpy as np

@dataclass
class StabilityMetrics:
    """Container for stability metrics"""
    cpu_usage: float
    memory_usage: float
    cycle_time: float
    error_count: int
    audio_buffer_size: int
    thread_count: int
    kernel_uptime: float
    last_error: Optional[str] = None

class KernelStabilizer:
    """Handles kernel stability monitoring and health checks"""
    
    def __init__(self, 
                 state_dump_dir: str = "state_dumps",
                 analysis_dir: str = "analysis",
                 stability_thresholds: Optional[Dict] = None):
        self.state_dump_dir = state_dump_dir
        self.analysis_dir = analysis_dir
        self.metrics_queue = Queue()
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Default stability thresholds
        self.thresholds = stability_thresholds or {
            'cpu_usage': 80.0,  # 80% CPU usage
            'memory_usage': 85.0,  # 85% memory usage
            'cycle_time': 50.0,  # 50ms cycle time
            'error_rate': 0.1,  # 10% error rate
            'audio_buffer': 0.8,  # 80% buffer utilization
            'thread_count': 20  # Maximum thread count
        }
        
        # Initialize logging
        self._setup_logging()
        
        # Create directories if they don't exist
        os.makedirs(state_dump_dir, exist_ok=True)
        os.makedirs(analysis_dir, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('kernel_stability.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('KernelStabilizer')
    
    def start_monitoring(self):
        """Start the stability monitoring thread"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.logger.info("Started kernel stability monitoring")
    
    def stop_monitoring(self):
        """Stop the stability monitoring thread"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.logger.info("Stopped kernel stability monitoring")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_queue.put(metrics)
                
                # Check stability
                stability_status = self._check_stability(metrics)
                if not stability_status['is_stable']:
                    self._handle_instability(stability_status['issues'])
                
                # Generate state dump if needed
                if self._should_dump_state(metrics):
                    self._generate_state_dump(metrics)
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(5)  # Wait before retrying
    
    def _collect_metrics(self) -> StabilityMetrics:
        """Collect current system metrics"""
        process = psutil.Process()
        
        return StabilityMetrics(
            cpu_usage=process.cpu_percent(),
            memory_usage=process.memory_percent(),
            cycle_time=self._get_cycle_time(),
            error_count=self._get_error_count(),
            audio_buffer_size=self._get_audio_buffer_size(),
            thread_count=process.num_threads(),
            kernel_uptime=time.time() - psutil.boot_time(),
            last_error=self._get_last_error()
        )
    
    def _get_cycle_time(self) -> float:
        """Get the current cycle time in milliseconds"""
        # This should be implemented based on your cycle timing mechanism
        return 0.0
    
    def _get_error_count(self) -> int:
        """Get the current error count"""
        # This should be implemented based on your error tracking mechanism
        return 0
    
    def _get_audio_buffer_size(self) -> int:
        """Get the current audio buffer size"""
        # This should be implemented based on your audio buffer mechanism
        return 0
    
    def _get_last_error(self) -> Optional[str]:
        """Get the last error message"""
        # This should be implemented based on your error tracking mechanism
        return None
    
    def _check_stability(self, metrics: StabilityMetrics) -> Dict:
        """Check if the system is stable based on current metrics"""
        issues = []
        
        if metrics.cpu_usage > self.thresholds['cpu_usage']:
            issues.append(f"High CPU usage: {metrics.cpu_usage}%")
        
        if metrics.memory_usage > self.thresholds['memory_usage']:
            issues.append(f"High memory usage: {metrics.memory_usage}%")
        
        if metrics.cycle_time > self.thresholds['cycle_time']:
            issues.append(f"Slow cycle time: {metrics.cycle_time}ms")
        
        if metrics.error_count > 0:
            error_rate = metrics.error_count / metrics.kernel_uptime
            if error_rate > self.thresholds['error_rate']:
                issues.append(f"High error rate: {error_rate:.2%}")
        
        if metrics.audio_buffer_size > self.thresholds['audio_buffer']:
            issues.append(f"Audio buffer utilization high: {metrics.audio_buffer_size}")
        
        if metrics.thread_count > self.thresholds['thread_count']:
            issues.append(f"High thread count: {metrics.thread_count}")
        
        return {
            'is_stable': len(issues) == 0,
            'issues': issues
        }
    
    def _handle_instability(self, issues: List[str]):
        """Handle system instability"""
        for issue in issues:
            self.logger.warning(f"Stability issue detected: {issue}")
        
        # Implement recovery actions based on the issues
        self._attempt_recovery(issues)
    
    def _attempt_recovery(self, issues: List[str]):
        """Attempt to recover from stability issues"""
        for issue in issues:
            if "CPU usage" in issue:
                self._optimize_cpu_usage()
            elif "memory usage" in issue:
                self._optimize_memory_usage()
            elif "cycle time" in issue:
                self._optimize_cycle_time()
            elif "error rate" in issue:
                self._handle_high_error_rate()
            elif "Audio buffer" in issue:
                self._optimize_audio_buffer()
            elif "thread count" in issue:
                self._optimize_thread_count()
    
    def _optimize_cpu_usage(self):
        """Optimize CPU usage"""
        # Implement CPU optimization strategies
        pass
    
    def _optimize_memory_usage(self):
        """Optimize memory usage"""
        # Implement memory optimization strategies
        pass
    
    def _optimize_cycle_time(self):
        """Optimize cycle time"""
        # Implement cycle time optimization strategies
        pass
    
    def _handle_high_error_rate(self):
        """Handle high error rate"""
        # Implement error handling strategies
        pass
    
    def _optimize_audio_buffer(self):
        """Optimize audio buffer"""
        # Implement audio buffer optimization strategies
        pass
    
    def _optimize_thread_count(self):
        """Optimize thread count"""
        # Implement thread count optimization strategies
        pass
    
    def _should_dump_state(self, metrics: StabilityMetrics) -> bool:
        """Determine if a state dump should be generated"""
        # Dump state if there are stability issues or every 5 minutes
        stability_status = self._check_stability(metrics)
        return (not stability_status['is_stable'] or 
                time.time() % 300 < 1)  # Every 5 minutes
    
    def _generate_state_dump(self, metrics: StabilityMetrics):
        """Generate a state dump file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.state_dump_dir, f"system_state_{timestamp}.json")
        
        state_data = {
            'timestamp': timestamp,
            'metrics': {
                'cpu_usage': metrics.cpu_usage,
                'memory_usage': metrics.memory_usage,
                'cycle_time': metrics.cycle_time,
                'error_count': metrics.error_count,
                'audio_buffer_size': metrics.audio_buffer_size,
                'thread_count': metrics.thread_count,
                'kernel_uptime': metrics.kernel_uptime
            },
            'stability_status': self._check_stability(metrics),
            'last_error': metrics.last_error
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(state_data, f, indent=2)
            self.logger.info(f"Generated state dump: {filename}")
        except Exception as e:
            self.logger.error(f"Error generating state dump: {str(e)}")
    
    def get_current_metrics(self) -> Optional[StabilityMetrics]:
        """Get the most recent metrics"""
        try:
            return self.metrics_queue.get_nowait()
        except:
            return None
    
    def is_kernel_stable(self) -> bool:
        """Check if the kernel is currently stable"""
        metrics = self.get_current_metrics()
        if metrics:
            return self._check_stability(metrics)['is_stable']
        return False
    
    def get_stability_report(self) -> Dict:
        """Generate a stability report"""
        metrics = self.get_current_metrics()
        if not metrics:
            return {'status': 'unknown', 'message': 'No metrics available'}
        
        stability_status = self._check_stability(metrics)
        return {
            'status': 'stable' if stability_status['is_stable'] else 'unstable',
            'issues': stability_status['issues'],
            'metrics': {
                'cpu_usage': metrics.cpu_usage,
                'memory_usage': metrics.memory_usage,
                'cycle_time': metrics.cycle_time,
                'error_count': metrics.error_count,
                'audio_buffer_size': metrics.audio_buffer_size,
                'thread_count': metrics.thread_count,
                'kernel_uptime': metrics.kernel_uptime
            }
        }

def main():
    """Main function for testing"""
    stabilizer = KernelStabilizer()
    stabilizer.start_monitoring()
    
    try:
        while True:
            report = stabilizer.get_stability_report()
            print(f"Stability Report: {report['status']}")
            if report['issues']:
                print("Issues:", report['issues'])
            time.sleep(5)
    except KeyboardInterrupt:
        stabilizer.stop_monitoring()
        print("\nKernel stabilization monitoring stopped")

if __name__ == '__main__':
    main() 