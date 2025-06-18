"""
State Visualizer Module
Handles visualization and analysis of system state dumps
"""

import json
import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel
import numpy as np
from typing import Dict, List, Optional, Tuple

class StateVisualizer(QWidget):
    """Widget for visualizing system state data"""
    
    def __init__(self, state_dump_dir: str = "state_dumps"):
        super().__init__()
        self.state_dump_dir = state_dump_dir
        self.current_data = None
        self.historical_data = []
        
        # Initialize UI
        self._init_ui()
        
        # Load historical data
        self._load_historical_data()
        
        # Start update timer
        self._start_update_timer()
    
    def _init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        
        # Control panel
        control_panel = QHBoxLayout()
        
        # Metric selector
        self.metric_selector = QComboBox()
        self.metric_selector.addItems([
            "CPU Usage",
            "Memory Usage",
            "Cycle Times",
            "Error Count",
            "Audio Buffer",
            "Thread Count"
        ])
        self.metric_selector.currentTextChanged.connect(self._update_plot)
        control_panel.addWidget(QLabel("Metric:"))
        control_panel.addWidget(self.metric_selector)
        
        # Time range selector
        self.time_range = QComboBox()
        self.time_range.addItems([
            "Last 5 minutes",
            "Last 15 minutes",
            "Last hour",
            "Last 24 hours",
            "All time"
        ])
        self.time_range.currentTextChanged.connect(self._update_plot)
        control_panel.addWidget(QLabel("Time Range:"))
        control_panel.addWidget(self.time_range)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._load_historical_data)
        control_panel.addWidget(refresh_btn)
        
        layout.addLayout(control_panel)
        
        # Create figure and canvas
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)
        
        # Alert panel
        self.alert_label = QLabel()
        self.alert_label.setStyleSheet("color: red;")
        layout.addWidget(self.alert_label)
        
        self.setLayout(layout)
    
    def _load_historical_data(self):
        """Load historical state data from dump files"""
        self.historical_data = []
        
        # Get all state dump files
        dump_files = glob.glob(os.path.join(self.state_dump_dir, "system_state_*.json"))
        dump_files.sort()  # Sort by filename (which includes timestamp)
        
        for file in dump_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    self.historical_data.append(data)
            except Exception as e:
                print(f"Error loading {file}: {e}")
    
    def _start_update_timer(self):
        """Start timer for periodic updates"""
        from PyQt5.QtCore import QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_plot)
        self.timer.start(5000)  # Update every 5 seconds
    
    def _update_plot(self):
        """Update the plot with current data"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Get selected metric and time range
        metric = self.metric_selector.currentText()
        time_range = self.time_range.currentText()
        
        # Filter data based on time range
        filtered_data = self._filter_data_by_time_range(time_range)
        
        if not filtered_data:
            ax.text(0.5, 0.5, "No data available", 
                   horizontalalignment='center',
                   verticalalignment='center')
            self.canvas.draw()
            return
        
        # Extract timestamps and values
        timestamps = []
        values = []
        alerts = []
        
        for data in filtered_data:
            # Convert timestamp string to datetime
            timestamp = datetime.strptime(data['timestamp'], "%Y%m%d_%H%M%S")
            timestamps.append(timestamp)
            
            # Extract value based on selected metric
            value = self._extract_metric_value(data, metric)
            values.append(value)
            
            # Check for alerts
            if data.get('alerts'):
                alerts.append((timestamp, data['alerts']))
        
        # Plot data
        ax.plot(timestamps, values, 'b-', label=metric)
        
        # Plot alerts if any
        if alerts:
            alert_times = [t for t, _ in alerts]
            alert_values = [values[timestamps.index(t)] for t in alert_times]
            ax.plot(alert_times, alert_values, 'ro', label='Alerts')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        # Add labels and title
        ax.set_xlabel('Time')
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} Over Time')
        
        # Rotate x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Add legend
        ax.legend()
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Update canvas
        self.canvas.draw()
        
        # Update alert label if there are recent alerts
        if alerts:
            latest_alerts = alerts[-1][1]
            self.alert_label.setText(f"Latest Alerts: {', '.join(latest_alerts)}")
        else:
            self.alert_label.setText("")
    
    def _filter_data_by_time_range(self, time_range: str) -> List[Dict]:
        """Filter historical data based on selected time range"""
        if not self.historical_data:
            return []
        
        now = datetime.now()
        
        if time_range == "Last 5 minutes":
            cutoff = now.timestamp() - 300
        elif time_range == "Last 15 minutes":
            cutoff = now.timestamp() - 900
        elif time_range == "Last hour":
            cutoff = now.timestamp() - 3600
        elif time_range == "Last 24 hours":
            cutoff = now.timestamp() - 86400
        else:  # All time
            return self.historical_data
        
        return [
            data for data in self.historical_data
            if datetime.strptime(data['timestamp'], "%Y%m%d_%H%M%S").timestamp() > cutoff
        ]
    
    def _extract_metric_value(self, data: Dict, metric: str) -> float:
        """Extract the value for the selected metric from state data"""
        if metric == "CPU Usage":
            return data['process_info']['cpu_percent']
        elif metric == "Memory Usage":
            return data['process_info']['memory_percent']
        elif metric == "Cycle Times":
            return data['performance_metrics']['cycle_times']['average']
        elif metric == "Error Count":
            return data['performance_metrics']['error_count']
        elif metric == "Audio Buffer":
            return data['audio_info']['buffer_size']
        elif metric == "Thread Count":
            return data['process_info']['num_threads']
        else:
            return 0.0
    
    def update_current_state(self, state_data: Dict):
        """Update the visualization with new state data"""
        self.current_data = state_data
        self._update_plot()

def analyze_state_dumps(dump_dir: str = "state_dumps", output_dir: str = "analysis"):
    """Analyze state dumps and generate summary plots"""
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load all state dumps
    dump_files = glob.glob(os.path.join(dump_dir, "system_state_*.json"))
    dump_files.sort()
    
    if not dump_files:
        print("No state dumps found")
        return
    
    # Load data
    data = []
    for file in dump_files:
        try:
            with open(file, 'r') as f:
                data.append(json.load(f))
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    if not data:
        print("No valid state data found")
        return
    
    # Generate summary plots
    metrics = [
        ("CPU Usage", "process_info", "cpu_percent"),
        ("Memory Usage", "process_info", "memory_percent"),
        ("Cycle Times", "performance_metrics", "cycle_times", "average"),
        ("Error Count", "performance_metrics", "error_count"),
        ("Thread Count", "process_info", "num_threads")
    ]
    
    for metric_name, *path in metrics:
        plt.figure(figsize=(12, 6))
        
        # Extract timestamps and values
        timestamps = [datetime.strptime(d['timestamp'], "%Y%m%d_%H%M%S") for d in data]
        values = []
        for d in data:
            value = d
            for p in path:
                value = value[p]
            values.append(value)
        
        # Plot data
        plt.plot(timestamps, values, 'b-', label=metric_name)
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        
        # Add labels and title
        plt.xlabel('Time')
        plt.ylabel(metric_name)
        plt.title(f'{metric_name} Over Time')
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        
        # Add legend
        plt.legend()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot
        plt.savefig(os.path.join(output_dir, f"{metric_name.lower().replace(' ', '_')}.png"))
        plt.close()
    
    print(f"Analysis complete. Plots saved to {output_dir}")

if __name__ == "__main__":
    # Example usage
    analyze_state_dumps() 