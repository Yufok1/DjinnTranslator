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
Enhanced Logging System
Provides structured logging and real-time monitoring capabilities
"""

import logging
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import threading
import queue
import os

@dataclass
class LogEntry:
    """Represents a structured log entry"""
    timestamp: str
    level: str
    component: str
    message: str
    details: Dict[str, Any]
    trace_id: Optional[str] = None

class EnhancedLogger:
    """Enhanced logging system with structured logging and real-time monitoring"""
    
    def __init__(self, 
                 log_dir: str = "logs",
                 system_log: str = "system.log",
                 pulse_log: str = "pulse.log",
                 max_log_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        
        self.log_dir = Path(log_dir)
        self.system_log = self.log_dir / system_log
        self.pulse_log = self.log_dir / pulse_log
        self.max_log_size = max_log_size
        self.backup_count = backup_count
        
        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize loggers
        self._setup_loggers()
        
        # Initialize monitoring queue
        self.monitor_queue = queue.Queue()
        self._start_monitor_thread()
        
    def _setup_loggers(self):
        """Setup system and pulse loggers"""
        # System logger
        self.system_logger = logging.getLogger('system')
        self.system_logger.setLevel(logging.INFO)
        
        system_handler = logging.handlers.RotatingFileHandler(
            self.system_log,
            maxBytes=self.max_log_size,
            backupCount=self.backup_count
        )
        system_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.system_logger.addHandler(system_handler)
        
        # Pulse logger
        self.pulse_logger = logging.getLogger('pulse')
        self.pulse_logger.setLevel(logging.INFO)
        
        pulse_handler = logging.handlers.RotatingFileHandler(
            self.pulse_log,
            maxBytes=self.max_log_size,
            backupCount=self.backup_count
        )
        pulse_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.pulse_logger.addHandler(pulse_handler)
        
    def _start_monitor_thread(self):
        """Start monitoring thread for real-time updates"""
        def monitor_worker():
            while True:
                try:
                    entry = self.monitor_queue.get()
                    if entry is None:
                        break
                    self._process_monitor_entry(entry)
                except Exception as e:
                    self.system_logger.error(f"Monitor error: {str(e)}")
                    
        self.monitor_thread = threading.Thread(target=monitor_worker, daemon=True)
        self.monitor_thread.start()
        
    def _process_monitor_entry(self, entry: LogEntry):
        """Process monitoring entry"""
        # Convert to JSON for real-time monitoring
        entry_json = json.dumps(asdict(entry))
        
        # Log to appropriate file
        if entry.component == 'pulse':
            self.pulse_logger.info(entry_json)
        else:
            self.system_logger.info(entry_json)
            
    def log_system(self, 
                  level: str,
                  component: str,
                  message: str,
                  details: Dict[str, Any] = None,
                  trace_id: Optional[str] = None):
        """Log system event"""
        entry = LogEntry(
            timestamp=datetime.utcnow().isoformat(),
            level=level,
            component=component,
            message=message,
            details=details or {},
            trace_id=trace_id
        )
        
        self.monitor_queue.put(entry)
        
    def log_pulse(self,
                 level: str,
                 component: str,
                 message: str,
                 details: Dict[str, Any] = None,
                 trace_id: Optional[str] = None):
        """Log pulse event"""
        entry = LogEntry(
            timestamp=datetime.utcnow().isoformat(),
            level=level,
            component=component,
            message=message,
            details=details or {},
            trace_id=trace_id
        )
        
        self.monitor_queue.put(entry)
        
    def get_recent_logs(self, 
                       component: Optional[str] = None,
                       level: Optional[str] = None,
                       limit: int = 100) -> List[LogEntry]:
        """Get recent log entries with optional filtering"""
        entries = []
        
        # Read system log
        if os.path.exists(self.system_log):
            with open(self.system_log, 'r') as f:
                for line in f:
                    try:
                        entry = self._parse_log_line(line)
                        if self._matches_filter(entry, component, level):
                            entries.append(entry)
                    except Exception:
                        continue
                        
        # Read pulse log
        if os.path.exists(self.pulse_log):
            with open(self.pulse_log, 'r') as f:
                for line in f:
                    try:
                        entry = self._parse_log_line(line)
                        if self._matches_filter(entry, component, level):
                            entries.append(entry)
                    except Exception:
                        continue
                        
        # Sort by timestamp and limit
        entries.sort(key=lambda x: x.timestamp, reverse=True)
        return entries[:limit]
        
    def _parse_log_line(self, line: str) -> LogEntry:
        """Parse log line into LogEntry"""
        try:
            data = json.loads(line.split(' - ', 2)[-1])
            return LogEntry(**data)
        except Exception:
            raise ValueError("Invalid log line format")
            
    def _matches_filter(self, 
                       entry: LogEntry,
                       component: Optional[str],
                       level: Optional[str]) -> bool:
        """Check if entry matches filter criteria"""
        if component and entry.component != component:
            return False
        if level and entry.level != level:
            return False
        return True
        
    def export_logs(self, output_dir: str):
        """Export logs to specified directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export system log
        if os.path.exists(self.system_log):
            with open(self.system_log, 'r') as src, \
                 open(output_path / "system.log", 'w') as dst:
                dst.write(src.read())
                
        # Export pulse log
        if os.path.exists(self.pulse_log):
            with open(self.pulse_log, 'r') as src, \
                 open(output_path / "pulse.log", 'w') as dst:
                dst.write(src.read())
                
        # Create log manifest
        manifest = {
            'export_timestamp': datetime.utcnow().isoformat(),
            'system_log_size': os.path.getsize(self.system_log) if os.path.exists(self.system_log) else 0,
            'pulse_log_size': os.path.getsize(self.pulse_log) if os.path.exists(self.pulse_log) else 0,
            'log_entries': len(self.get_recent_logs())
        }
        
        with open(output_path / "log_manifest.yaml", 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False)
            
    def cleanup(self):
        """Cleanup resources"""
        self.monitor_queue.put(None)  # Signal monitor thread to stop
        self.monitor_thread.join()
        
        # Close loggers
        for handler in self.system_logger.handlers:
            handler.close()
        for handler in self.pulse_logger.handlers:
            handler.close()

def main():
    """Command-line interface for log management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Log Management")
    parser.add_argument("--list", action="store_true", help="List recent logs")
    parser.add_argument("--component", help="Filter by component")
    parser.add_argument("--level", help="Filter by level")
    parser.add_argument("--limit", type=int, default=100, help="Limit number of entries")
    parser.add_argument("--export", help="Export logs to directory")
    
    args = parser.parse_args()
    logger = EnhancedLogger()
    
    try:
        if args.list:
            entries = logger.get_recent_logs(
                component=args.component,
                level=args.level,
                limit=args.limit
            )
            
            for entry in entries:
                print(f"\nTimestamp: {entry.timestamp}")
                print(f"Level: {entry.level}")
                print(f"Component: {entry.component}")
                print(f"Message: {entry.message}")
                if entry.details:
                    print("Details:", json.dumps(entry.details, indent=2))
                if entry.trace_id:
                    print(f"Trace ID: {entry.trace_id}")
                    
        elif args.export:
            logger.export_logs(args.export)
            print(f"Logs exported to: {args.export}")
            
    finally:
        logger.cleanup()

if __name__ == "__main__":
    main() 