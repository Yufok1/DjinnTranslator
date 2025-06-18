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
Dashboard Module
Main UI for the breath engine system
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTabWidget,
                            QProgressBar, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt, QTimer
from .breath_engine import BreathEngine
from .state_visualizer import StateVisualizer
from .advanced_visualizer import AdvancedVisualizer
from .kernel_stabilizer import KernelStabilizer
from .recovery_strategies import RecoveryManager
from .report_viewer import ReportViewer

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = BreathEngine()
        self.stabilizer = KernelStabilizer()
        self.recovery_manager = RecoveryManager()
        self.report_viewer = ReportViewer()
        self.init_ui()
        
        # Start update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)  # Update every second
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Breath Engine Dashboard')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Main control tab
        main_tab = QWidget()
        main_layout = QVBoxLayout(main_tab)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_engine)
        control_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_engine)
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)
        
        self.dump_button = QPushButton('Dump State')
        self.dump_button.clicked.connect(self.dump_state)
        control_layout.addWidget(self.dump_button)
        
        self.stabilize_button = QPushButton('Stabilize Kernel')
        self.stabilize_button.clicked.connect(self.stabilize_kernel)
        control_layout.addWidget(self.stabilize_button)
        
        main_layout.addLayout(control_layout)
        
        # Status indicators
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel('Status: Stopped')
        status_layout.addWidget(self.status_label)
        
        self.cycle_label = QLabel('Current Cycle: None')
        status_layout.addWidget(self.cycle_label)
        
        main_layout.addLayout(status_layout)
        
        # Stability indicators
        stability_layout = QVBoxLayout()
        
        # CPU Usage
        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(QLabel('CPU Usage:'))
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        cpu_layout.addWidget(self.cpu_bar)
        stability_layout.addLayout(cpu_layout)
        
        # Memory Usage
        memory_layout = QHBoxLayout()
        memory_layout.addWidget(QLabel('Memory Usage:'))
        self.memory_bar = QProgressBar()
        self.memory_bar.setRange(0, 100)
        memory_layout.addWidget(self.memory_bar)
        stability_layout.addLayout(memory_layout)
        
        # Cycle Time
        cycle_layout = QHBoxLayout()
        cycle_layout.addWidget(QLabel('Cycle Time:'))
        self.cycle_time_label = QLabel('0 ms')
        cycle_layout.addWidget(self.cycle_time_label)
        stability_layout.addLayout(cycle_layout)
        
        # Error Count
        error_layout = QHBoxLayout()
        error_layout.addWidget(QLabel('Error Count:'))
        self.error_count_label = QLabel('0')
        error_layout.addWidget(self.error_count_label)
        stability_layout.addLayout(error_layout)
        
        main_layout.addLayout(stability_layout)
        
        # Add main tab
        tabs.addTab(main_tab, "Controls")
        
        # Add visualization tab
        viz_tab = QWidget()
        viz_layout = QVBoxLayout(viz_tab)
        
        # Create splitter for visualizers
        splitter = QSplitter(Qt.Vertical)
        
        # Basic visualizer
        self.state_visualizer = StateVisualizer()
        splitter.addWidget(self.state_visualizer)
        
        # Advanced visualizer
        self.advanced_visualizer = AdvancedVisualizer()
        splitter.addWidget(self.advanced_visualizer)
        
        viz_layout.addWidget(splitter)
        tabs.addTab(viz_tab, "System State")
        
        # Add error log tab
        error_tab = QWidget()
        error_layout = QVBoxLayout(error_tab)
        self.error_label = QLabel('No errors')
        error_layout.addWidget(self.error_label)
        tabs.addTab(error_tab, "Error Log")
        
        # Add recovery report tab
        recovery_tab = QWidget()
        recovery_layout = QVBoxLayout(recovery_tab)
        self.recovery_label = QLabel('No recovery attempts')
        recovery_layout.addWidget(self.recovery_label)
        tabs.addTab(recovery_tab, "Recovery Report")
        
        # Add report tab
        report_tab = QWidget()
        report_layout = QVBoxLayout(report_tab)
        self.report_viewer.pack(fill=Qt.FillRole, expand=True, padx=5, pady=5)
        tabs.addTab(report_tab, "Reports")
    
    def start_engine(self):
        """Start the breath engine"""
        try:
            self.engine.start()
            self.stabilizer.start_monitoring()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText('Status: Running')
        except Exception as e:
            self.error_label.setText(f'Error starting engine: {str(e)}')
    
    def stop_engine(self):
        """Stop the breath engine"""
        try:
            self.engine.stop()
            self.stabilizer.stop_monitoring()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.status_label.setText('Status: Stopped')
        except Exception as e:
            self.error_label.setText(f'Error stopping engine: {str(e)}')
    
    def dump_state(self):
        """Trigger a state dump"""
        try:
            self.engine.trigger_state_dump(manual_trigger=True)
        except Exception as e:
            self.error_label.setText(f'Error dumping state: {str(e)}')
    
    def stabilize_kernel(self):
        """Stabilize the kernel"""
        try:
            if not self.stabilizer.is_kernel_stable():
                report = self.stabilizer.get_stability_report()
                if report['status'] == 'unstable':
                    # Attempt recovery
                    recovery_metrics = self.recovery_manager.handle_instability(
                        report['metrics']
                    )
                    
                    # Update recovery report
                    self._update_recovery_report()
                    
                    QMessageBox.warning(
                        self,
                        'Kernel Unstable',
                        f'Kernel stability issues detected:\n' + 
                        '\n'.join(report['issues']) +
                        '\n\nRecovery steps taken:\n' +
                        '\n'.join(recovery_metrics.recovery_steps)
                    )
            else:
                QMessageBox.information(
                    self,
                    'Kernel Stable',
                    'The kernel is currently stable.'
                )
        except Exception as e:
            self.error_label.setText(f'Error stabilizing kernel: {str(e)}')
    
    def _update_recovery_report(self):
        """Update the recovery report display"""
        report = self.recovery_manager.get_recovery_report()
        
        report_text = f"""
        Total Recoveries: {report['total_recoveries']}
        Successful Recoveries: {report['successful_recoveries']}
        Average Performance Impact: {report['average_performance_impact']:.2f}
        
        Recent Recovery Steps:
        """
        
        for steps in report['recent_steps']:
            report_text += "\n".join(f"- {step}" for step in steps) + "\n"
        
        self.recovery_label.setText(report_text)
    
    def update_metrics(self):
        """Update dashboard metrics"""
        if self.engine.is_running:
            # Update cycle label
            current_cycle = self.engine.get_current_cycle()
            if current_cycle:
                self.cycle_label.setText(f'Current Cycle: {current_cycle}')
            
            # Update state visualizer
            state_data = self.engine.get_current_state()
            if state_data:
                self.state_visualizer.update_current_state(state_data)
                self.advanced_visualizer.update_data([state_data])
            
            # Update error log
            if self.engine.error_log:
                self.error_label.setText('\n'.join(self.engine.error_log[-5:]))
            
            # Update stability metrics
            metrics = self.stabilizer.get_current_metrics()
            if metrics:
                self.cpu_bar.setValue(int(metrics.cpu_usage))
                self.memory_bar.setValue(int(metrics.memory_usage))
                self.cycle_time_label.setText(f'{metrics.cycle_time:.1f} ms')
                self.error_count_label.setText(str(metrics.error_count))
            
            # Update report viewer
            self.report_viewer.update()

def main():
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 