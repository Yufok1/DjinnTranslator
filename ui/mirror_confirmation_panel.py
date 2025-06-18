"""
Mirror Confirmation Panel Module
Provides UI for viewing and managing mirror confirmations
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any
from datetime import datetime
from core.mirror_confirmation import MirrorConfirmationSystem, MirrorConfirmation

class MirrorConfirmationPanel(ttk.Frame):
    """Panel for viewing and managing mirror confirmations"""
    
    def __init__(self, parent, confirmation_system: MirrorConfirmationSystem):
        super().__init__(parent)
        self.confirmation_system = confirmation_system
        
        # Initialize UI
        self._create_layout()
        self._refresh_confirmation_list()
    
    def _create_layout(self):
        """Create the panel layout"""
        # Create filter frame
        filter_frame = ttk.LabelFrame(self, text="Filters")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").grid(row=0, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar(value="")
        self.status_var.trace('w', lambda *args: self._refresh_confirmation_list())
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, values=["", "pending", "confirmed", "rejected"])
        status_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Resonance threshold
        ttk.Label(filter_frame, text="Min Resonance:").grid(row=0, column=2, padx=5, pady=5)
        self.resonance_var = tk.StringVar(value="0.0")
        self.resonance_var.trace('w', lambda *args: self._refresh_confirmation_list())
        ttk.Entry(filter_frame, textvariable=self.resonance_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # Create confirmation list
        list_frame = ttk.LabelFrame(self, text="Confirmation History")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview
        columns = ("timestamp", "ritual_id", "insight", "portent", "validity", "status")
        self.confirmation_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        self.confirmation_tree.heading("timestamp", text="Timestamp")
        self.confirmation_tree.heading("ritual_id", text="Ritual ID")
        self.confirmation_tree.heading("insight", text="Insight Resonance")
        self.confirmation_tree.heading("portent", text="Portent Resonance")
        self.confirmation_tree.heading("validity", text="Harmonic Validity")
        self.confirmation_tree.heading("status", text="Status")
        
        self.confirmation_tree.column("timestamp", width=150)
        self.confirmation_tree.column("ritual_id", width=150)
        self.confirmation_tree.column("insight", width=100)
        self.confirmation_tree.column("portent", width=100)
        self.confirmation_tree.column("validity", width=100)
        self.confirmation_tree.column("status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.confirmation_tree.yview)
        self.confirmation_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.confirmation_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.confirmation_tree.bind('<<TreeviewSelect>>', self._on_confirmation_select)
        
        # Create details frame
        self.details_frame = ttk.LabelFrame(self, text="Confirmation Details")
        self.details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create details widgets
        self.details_widgets = {}
        
        # Ritual ID
        ttk.Label(self.details_frame, text="Ritual ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["ritual_id"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["ritual_id"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Timestamp
        ttk.Label(self.details_frame, text="Timestamp:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["timestamp"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["timestamp"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Insight Resonance
        ttk.Label(self.details_frame, text="Insight Resonance:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["insight"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["insight"].grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Portent Resonance
        ttk.Label(self.details_frame, text="Portent Resonance:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["portent"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["portent"].grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Harmonic Validity
        ttk.Label(self.details_frame, text="Harmonic Validity:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["validity"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["validity"].grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Status
        ttk.Label(self.details_frame, text="Status:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["status"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["status"].grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Feedback
        ttk.Label(self.details_frame, text="Insight Feedback:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["insight_feedback"] = ttk.Label(self.details_frame, text="", wraplength=400)
        self.details_widgets["insight_feedback"].grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.details_frame, text="Portent Feedback:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["portent_feedback"] = ttk.Label(self.details_frame, text="", wraplength=400)
        self.details_widgets["portent_feedback"].grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Echo Depth
        ttk.Label(self.details_frame, text="Echo Depth:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["echo_depth"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["echo_depth"].grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Recursion Level
        ttk.Label(self.details_frame, text="Recursion Level:").grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["recursion"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["recursion"].grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
    
    def _refresh_confirmation_list(self):
        """Refresh the confirmation list based on filters"""
        # Clear current items
        for item in self.confirmation_tree.get_children():
            self.confirmation_tree.delete(item)
        
        # Get filter values
        status_filter = self.status_var.get().lower()
        try:
            min_resonance = float(self.resonance_var.get())
        except ValueError:
            min_resonance = 0.0
        
        # Add filtered items
        for ritual_id, confirmations in self.confirmation_system.confirmation_history.items():
            for confirmation in confirmations:
                # Apply filters
                if status_filter and status_filter != confirmation.confirmation_status.lower():
                    continue
                if confirmation.harmonic_validity < min_resonance:
                    continue
                
                # Format timestamp
                timestamp = datetime.fromtimestamp(confirmation.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                
                # Add to treeview
                self.confirmation_tree.insert("", tk.END, values=(
                    timestamp,
                    ritual_id,
                    f"{confirmation.insight_resonance:.2f}",
                    f"{confirmation.portent_resonance:.2f}",
                    f"{confirmation.harmonic_validity:.2f}",
                    confirmation.confirmation_status
                ), tags=(ritual_id,))
    
    def _on_confirmation_select(self, event):
        """Handle confirmation selection"""
        # Get selected item
        selection = self.confirmation_tree.selection()
        if not selection:
            return
        
        # Get ritual ID and timestamp
        ritual_id = self.confirmation_tree.item(selection[0])["tags"][0]
        timestamp = datetime.strptime(
            self.confirmation_tree.item(selection[0])["values"][0],
            "%Y-%m-%d %H:%M:%S"
        ).timestamp()
        
        # Find confirmation
        confirmation = None
        for c in self.confirmation_system.confirmation_history[ritual_id]:
            if abs(c.timestamp - timestamp) < 1:  # Within 1 second
                confirmation = c
                break
        
        if not confirmation:
            return
        
        # Update details
        self.details_widgets["ritual_id"].config(text=confirmation.ritual_id)
        self.details_widgets["timestamp"].config(
            text=datetime.fromtimestamp(confirmation.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.details_widgets["insight"].config(text=f"{confirmation.insight_resonance:.2f}")
        self.details_widgets["portent"].config(text=f"{confirmation.portent_resonance:.2f}")
        self.details_widgets["validity"].config(text=f"{confirmation.harmonic_validity:.2f}")
        self.details_widgets["status"].config(text=confirmation.confirmation_status)
        self.details_widgets["insight_feedback"].config(text=confirmation.insight_feedback or "N/A")
        self.details_widgets["portent_feedback"].config(text=confirmation.portent_feedback or "N/A")
        self.details_widgets["echo_depth"].config(text=f"{confirmation.echo_depth:.2f}")
        self.details_widgets["recursion"].config(text=str(confirmation.recursion_level))
    
    def cleanup(self):
        """Clean up resources"""
        pass 