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
Report Viewer Module
Provides a UI component for viewing and managing analysis reports
"""

import os
import glob
from datetime import datetime
import webbrowser
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, filedialog
import logging
import pdfkit
import pandas as pd
import json
from .analysis_reporter import AnalysisReporter

class ReportViewer(ttk.Frame):
    """Report viewer component for the dashboard"""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.logger = logging.getLogger('ReportViewer')
        
        # Initialize reporter
        self.reporter = AnalysisReporter()
        
        # Create UI elements
        self._create_widgets()
        
        # Load available reports
        self._load_reports()
    
    def _create_widgets(self):
        """Create the UI widgets"""
        # Control panel
        control_frame = ttk.LabelFrame(self, text="Report Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Time range selection
        ttk.Label(control_frame, text="Time Range:").pack(side=tk.LEFT, padx=5)
        self.time_range = ttk.Combobox(
            control_frame,
            values=["24h", "7d", "30d"],
            state="readonly",
            width=10
        )
        self.time_range.set("24h")
        self.time_range.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        self.generate_btn = ttk.Button(
            control_frame,
            text="Generate Report",
            command=self._generate_report
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        self.refresh_btn = ttk.Button(
            control_frame,
            text="Refresh",
            command=self._load_reports
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        self.export_btn = ttk.Button(
            control_frame,
            text="Export",
            command=self._show_export_menu
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Create export menu
        self.export_menu = tk.Menu(self, tearoff=0)
        self.export_menu.add_command(label="Export as PDF", command=self._export_pdf)
        self.export_menu.add_command(label="Export as CSV", command=self._export_csv)
        
        # Report list
        list_frame = ttk.LabelFrame(self, text="Available Reports")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview
        self.report_tree = ttk.Treeview(
            list_frame,
            columns=("date", "time", "range", "size"),
            show="headings"
        )
        
        # Configure columns
        self.report_tree.heading("date", text="Date")
        self.report_tree.heading("time", text="Time")
        self.report_tree.heading("range", text="Time Range")
        self.report_tree.heading("size", text="Size")
        
        self.report_tree.column("date", width=100)
        self.report_tree.column("time", width=100)
        self.report_tree.column("range", width=100)
        self.report_tree.column("size", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.report_tree.yview
        )
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.report_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.report_tree.bind("<Double-1>", self._open_report)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)
    
    def _show_export_menu(self):
        """Show export menu"""
        try:
            # Get selected item
            selection = self.report_tree.selection()
            if not selection:
                self.status_var.set("Please select a report to export")
                return
            
            # Show menu at button position
            x = self.export_btn.winfo_rootx()
            y = self.export_btn.winfo_rooty() + self.export_btn.winfo_height()
            self.export_menu.post(x, y)
        except Exception as e:
            self.logger.error(f"Error showing export menu: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
    
    def _export_pdf(self):
        """Export selected report as PDF"""
        try:
            # Get selected item
            selection = self.report_tree.selection()
            if not selection:
                return
            
            # Get file path from tags
            file_path = self.report_tree.item(selection[0])["tags"][0]
            
            # Ask for save location
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if not save_path:
                return
            
            # Convert HTML to PDF
            pdfkit.from_file(file_path, save_path)
            
            self.status_var.set(f"Report exported as PDF: {os.path.basename(save_path)}")
        except Exception as e:
            self.logger.error(f"Error exporting PDF: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
    
    def _export_csv(self):
        """Export selected report data as CSV"""
        try:
            # Get selected item
            selection = self.report_tree.selection()
            if not selection:
                return
            
            # Get file path from tags
            file_path = self.report_tree.item(selection[0])["tags"][0]
            
            # Ask for save location
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=f"report_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not save_path:
                return
            
            # Load report data
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame
            df = pd.DataFrame(data['metrics'])
            
            # Save as CSV
            df.to_csv(save_path, index=False)
            
            self.status_var.set(f"Report data exported as CSV: {os.path.basename(save_path)}")
        except Exception as e:
            self.logger.error(f"Error exporting CSV: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
    
    def _load_reports(self):
        """Load available reports into the treeview"""
        # Clear existing items
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Get report files
        report_files = glob.glob(os.path.join(self.reporter.report_dir, "*.html"))
        
        # Add reports to treeview
        for file in sorted(report_files, reverse=True):
            try:
                # Parse filename
                filename = os.path.basename(file)
                if filename.startswith("analysis_report_"):
                    # Extract timestamp
                    timestamp = filename[15:-5]  # Remove prefix and extension
                    dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                    
                    # Get file size
                    size = os.path.getsize(file)
                    size_str = f"{size/1024:.1f} KB"
                    
                    # Add to treeview
                    self.report_tree.insert(
                        "",
                        "end",
                        values=(
                            dt.strftime("%Y-%m-%d"),
                            dt.strftime("%H:%M:%S"),
                            "Unknown",  # Time range not stored in filename
                            size_str
                        ),
                        tags=(file,)  # Store full path in tags
                    )
            except Exception as e:
                self.logger.error(f"Error loading report {file}: {str(e)}")
        
        self.status_var.set(f"Loaded {len(report_files)} reports")
    
    def _generate_report(self):
        """Generate a new report"""
        try:
            # Disable generate button
            self.generate_btn.configure(state="disabled")
            self.status_var.set("Generating report...")
            
            # Generate report
            report_path = self.reporter.generate_report(
                time_range=self.time_range.get()
            )
            
            # Reload reports
            self._load_reports()
            
            # Open the new report
            self._open_report_by_path(report_path)
            
            self.status_var.set("Report generated successfully")
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
        finally:
            # Re-enable generate button
            self.generate_btn.configure(state="normal")
    
    def _open_report(self, event):
        """Open the selected report"""
        # Get selected item
        selection = self.report_tree.selection()
        if not selection:
            return
        
        # Get file path from tags
        file_path = self.report_tree.item(selection[0])["tags"][0]
        self._open_report_by_path(file_path)
    
    def _open_report_by_path(self, file_path: str):
        """Open a report by its file path"""
        try:
            # Open in default browser
            webbrowser.open(f"file://{os.path.abspath(file_path)}")
            self.status_var.set(f"Opened report: {os.path.basename(file_path)}")
        except Exception as e:
            self.logger.error(f"Error opening report {file_path}: {str(e)}")
            self.status_var.set(f"Error opening report: {str(e)}")
    
    def update(self):
        """Update the report viewer"""
        self._load_reports()

def main():
    """Test the report viewer"""
    root = tk.Tk()
    root.title("Report Viewer Test")
    
    viewer = ReportViewer(root)
    viewer.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    root.mainloop()

if __name__ == '__main__':
    main() 