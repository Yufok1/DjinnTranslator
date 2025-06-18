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
Advanced Visualization Module
Implements sophisticated visualization types for system metrics
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from typing import Dict, List, Optional, Tuple
import seaborn as sns
from datetime import datetime, timedelta

class AdvancedVisualizer(QWidget):
    """Widget for advanced visualization of system metrics"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data = []
        self.current_visualization = None
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Control panel
        control_panel = QHBoxLayout()
        
        # Visualization type selector
        self.viz_type = QComboBox()
        self.viz_type.addItems([
            "Time Series",
            "Heatmap",
            "Histogram",
            "Box Plot",
            "Violin Plot",
            "Scatter Matrix"
        ])
        self.viz_type.currentTextChanged.connect(self.update_visualization)
        control_panel.addWidget(QLabel("Visualization Type:"))
        control_panel.addWidget(self.viz_type)
        
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
        self.metric_selector.currentTextChanged.connect(self.update_visualization)
        control_panel.addWidget(QLabel("Metric:"))
        control_panel.addWidget(self.metric_selector)
        
        layout.addLayout(control_panel)
        
        # Create figure and canvas
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def update_data(self, new_data: List[Dict]):
        """Update the visualization data"""
        self.data = new_data
        self.update_visualization()
    
    def update_visualization(self):
        """Update the current visualization"""
        if not self.data:
            return
        
        self.figure.clear()
        viz_type = self.viz_type.currentText()
        metric = self.metric_selector.currentText()
        
        if viz_type == "Time Series":
            self._plot_time_series(metric)
        elif viz_type == "Heatmap":
            self._plot_heatmap(metric)
        elif viz_type == "Histogram":
            self._plot_histogram(metric)
        elif viz_type == "Box Plot":
            self._plot_box_plot(metric)
        elif viz_type == "Violin Plot":
            self._plot_violin_plot(metric)
        elif viz_type == "Scatter Matrix":
            self._plot_scatter_matrix()
        
        self.canvas.draw()
    
    def _plot_time_series(self, metric: str):
        """Plot time series data"""
        ax = self.figure.add_subplot(111)
        
        # Extract timestamps and values
        timestamps = [datetime.strptime(d['timestamp'], "%Y%m%d_%H%M%S") 
                     for d in self.data]
        values = [self._extract_metric_value(d, metric) for d in self.data]
        
        # Plot data
        ax.plot(timestamps, values, 'b-', label=metric)
        
        # Add trend line
        z = np.polyfit(range(len(values)), values, 1)
        p = np.poly1d(z)
        ax.plot(timestamps, p(range(len(values))), 'r--', 
                label='Trend')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())
        
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
    
    def _plot_heatmap(self, metric: str):
        """Plot heatmap of metric values"""
        ax = self.figure.add_subplot(111)
        
        # Extract values and reshape for heatmap
        values = [self._extract_metric_value(d, metric) for d in self.data]
        values_2d = np.array(values).reshape(-1, 10)  # Reshape into 2D array
        
        # Create heatmap
        sns.heatmap(values_2d, ax=ax, cmap='YlOrRd', 
                   cbar_kws={'label': metric})
        
        # Add labels and title
        ax.set_title(f'{metric} Heatmap')
        
        # Adjust layout
        self.figure.tight_layout()
    
    def _plot_histogram(self, metric: str):
        """Plot histogram of metric values"""
        ax = self.figure.add_subplot(111)
        
        # Extract values
        values = [self._extract_metric_value(d, metric) for d in self.data]
        
        # Create histogram
        sns.histplot(values, ax=ax, kde=True)
        
        # Add labels and title
        ax.set_xlabel(metric)
        ax.set_ylabel('Frequency')
        ax.set_title(f'{metric} Distribution')
        
        # Adjust layout
        self.figure.tight_layout()
    
    def _plot_box_plot(self, metric: str):
        """Plot box plot of metric values"""
        ax = self.figure.add_subplot(111)
        
        # Extract values
        values = [self._extract_metric_value(d, metric) for d in self.data]
        
        # Create box plot
        sns.boxplot(y=values, ax=ax)
        
        # Add labels and title
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} Box Plot')
        
        # Adjust layout
        self.figure.tight_layout()
    
    def _plot_violin_plot(self, metric: str):
        """Plot violin plot of metric values"""
        ax = self.figure.add_subplot(111)
        
        # Extract values
        values = [self._extract_metric_value(d, metric) for d in self.data]
        
        # Create violin plot
        sns.violinplot(y=values, ax=ax)
        
        # Add labels and title
        ax.set_ylabel(metric)
        ax.set_title(f'{metric} Violin Plot')
        
        # Adjust layout
        self.figure.tight_layout()
    
    def _plot_scatter_matrix(self):
        """Plot scatter matrix of all metrics"""
        # Extract all metrics
        metrics = [
            "CPU Usage",
            "Memory Usage",
            "Cycle Times",
            "Error Count",
            "Audio Buffer",
            "Thread Count"
        ]
        
        # Create data matrix
        data_matrix = np.array([
            [self._extract_metric_value(d, m) for m in metrics]
            for d in self.data
        ])
        
        # Create scatter matrix
        fig = plt.figure(figsize=(12, 12))
        sns.pairplot(pd.DataFrame(data_matrix, columns=metrics))
        
        # Adjust layout
        self.figure.tight_layout()
    
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

def main():
    """Test the advanced visualizer"""
    import json
    import glob
    
    # Load some test data
    data = []
    for file in glob.glob("state_dumps/system_state_*.json"):
        try:
            with open(file, 'r') as f:
                data.append(json.load(f))
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    if not data:
        print("No test data found")
        return
    
    # Create and show visualizer
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    visualizer = AdvancedVisualizer()
    visualizer.update_data(data)
    visualizer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 