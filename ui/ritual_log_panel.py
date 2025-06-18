"""
Ritual Log Panel Module
Provides UI for viewing and managing ritual logs
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any
from datetime import datetime
from core.ritual_log import RitualLog

class RitualLogPanel(ttk.Frame):
    """Panel for viewing and managing ritual logs"""
    
    def __init__(self, parent, ritual_log: RitualLog):
        super().__init__(parent)
        self.ritual_log = ritual_log
        
        # Initialize UI
        self._create_layout()
        self._refresh_ritual_list()
    
    def _create_layout(self):
        """Create the panel layout"""
        # Create filter frame
        filter_frame = ttk.LabelFrame(self, text="Filters")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Sigil filter
        ttk.Label(filter_frame, text="Sigil:").grid(row=0, column=0, padx=5, pady=5)
        self.sigil_var = tk.StringVar(value="")
        self.sigil_var.trace('w', lambda *args: self._refresh_ritual_list())
        ttk.Entry(filter_frame, textvariable=self.sigil_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Action filter
        ttk.Label(filter_frame, text="Action:").grid(row=0, column=2, padx=5, pady=5)
        self.action_var = tk.StringVar(value="")
        self.action_var.trace('w', lambda *args: self._refresh_ritual_list())
        ttk.Entry(filter_frame, textvariable=self.action_var).grid(row=0, column=3, padx=5, pady=5)
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").grid(row=0, column=4, padx=5, pady=5)
        self.status_var = tk.StringVar(value="")
        self.status_var.trace('w', lambda *args: self._refresh_ritual_list())
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, values=["", "pending", "confirmed", "rejected"])
        status_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Create ritual list
        list_frame = ttk.LabelFrame(self, text="Ritual Ledger")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview
        columns = ("phrase", "sigil", "action", "status", "success_rate", "avg_resonance")
        self.ritual_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        self.ritual_tree.heading("phrase", text="Phrase")
        self.ritual_tree.heading("sigil", text="Sigil")
        self.ritual_tree.heading("action", text="Action")
        self.ritual_tree.heading("status", text="Status")
        self.ritual_tree.heading("success_rate", text="Success Rate")
        self.ritual_tree.heading("avg_resonance", text="Avg Resonance")
        
        self.ritual_tree.column("phrase", width=200)
        self.ritual_tree.column("sigil", width=100)
        self.ritual_tree.column("action", width=100)
        self.ritual_tree.column("status", width=100)
        self.ritual_tree.column("success_rate", width=100)
        self.ritual_tree.column("avg_resonance", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.ritual_tree.yview)
        self.ritual_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.ritual_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.ritual_tree.bind('<<TreeviewSelect>>', self._on_ritual_select)
        
        # Create details frame
        self.details_frame = ttk.LabelFrame(self, text="Ritual Details")
        self.details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create details widgets
        self.details_widgets = {}
        
        # Phrase
        ttk.Label(self.details_frame, text="Phrase:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["phrase"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["phrase"].grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Sigil
        ttk.Label(self.details_frame, text="Sigil:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["sigil"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["sigil"].grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Action
        ttk.Label(self.details_frame, text="Action:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["action"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["action"].grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Status
        ttk.Label(self.details_frame, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["status"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["status"].grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Success Rate
        ttk.Label(self.details_frame, text="Success Rate:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["success_rate"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["success_rate"].grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Average Resonance
        ttk.Label(self.details_frame, text="Avg Resonance:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.details_widgets["avg_resonance"] = ttk.Label(self.details_frame, text="")
        self.details_widgets["avg_resonance"].grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Create invocation history frame
        history_frame = ttk.LabelFrame(self, text="Invocation History")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create history treeview
        history_columns = ("timestamp", "result", "resonance", "echo_depth")
        self.history_tree = ttk.Treeview(history_frame, columns=history_columns, show="headings")
        
        # Configure history columns
        self.history_tree.heading("timestamp", text="Timestamp")
        self.history_tree.heading("result", text="Result")
        self.history_tree.heading("resonance", text="Resonance")
        self.history_tree.heading("echo_depth", text="Echo Depth")
        
        self.history_tree.column("timestamp", width=150)
        self.history_tree.column("result", width=100)
        self.history_tree.column("resonance", width=100)
        self.history_tree.column("echo_depth", width=100)
        
        # Add history scrollbar
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        # Pack history treeview and scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _refresh_ritual_list(self):
        """Refresh the ritual list based on filters"""
        # Clear current items
        for item in self.ritual_tree.get_children():
            self.ritual_tree.delete(item)
        
        # Get filter values
        sigil_filter = self.sigil_var.get().lower()
        action_filter = self.action_var.get().lower()
        status_filter = self.status_var.get().lower()
        
        # Add filtered items
        for ritual_id, entry in self.ritual_log.ledger.items():
            # Apply filters
            if sigil_filter and sigil_filter not in entry.speaker_sigil.lower():
                continue
            if action_filter and action_filter not in entry.bound_action.lower():
                continue
            if status_filter and status_filter != entry.status.lower():
                continue
            
            # Get statistics
            stats = self.ritual_log.get_invocation_stats(ritual_id)
            
            # Calculate success rate
            if stats["total"] > 0:
                success_rate = f"{stats['success'] / stats['total']:.1%}"
            else:
                success_rate = "N/A"
            
            # Add to treeview
            self.ritual_tree.insert("", tk.END, values=(
                entry.phrase,
                entry.speaker_sigil,
                entry.bound_action,
                entry.status,
                success_rate,
                f"{stats['avg_resonance']:.2f}" if stats['total'] > 0 else "N/A"
            ), tags=(ritual_id,))
    
    def _on_ritual_select(self, event):
        """Handle ritual selection"""
        # Get selected item
        selection = self.ritual_tree.selection()
        if not selection:
            return
        
        # Get ritual ID
        ritual_id = self.ritual_tree.item(selection[0])["tags"][0]
        
        # Get ritual entry
        entry = self.ritual_log.ledger[ritual_id]
        
        # Update details
        self.details_widgets["phrase"].config(text=entry.phrase)
        self.details_widgets["sigil"].config(text=entry.speaker_sigil)
        self.details_widgets["action"].config(text=entry.bound_action)
        self.details_widgets["status"].config(text=entry.status)
        
        # Get statistics
        stats = self.ritual_log.get_invocation_stats(ritual_id)
        
        # Update statistics
        if stats["total"] > 0:
            success_rate = f"{stats['success'] / stats['total']:.1%}"
            avg_resonance = f"{stats['avg_resonance']:.2f}"
        else:
            success_rate = "N/A"
            avg_resonance = "N/A"
        
        self.details_widgets["success_rate"].config(text=success_rate)
        self.details_widgets["avg_resonance"].config(text=avg_resonance)
        
        # Update invocation history
        self._refresh_invocation_history(entry.phrase)
    
    def _refresh_invocation_history(self, phrase: str):
        """Refresh the invocation history for a ritual"""
        # Clear current items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add invocation records
        for record in self.ritual_log.invocation_history:
            if record.phrase == phrase:
                # Format timestamp
                timestamp = datetime.fromtimestamp(record.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                
                # Add to treeview
                self.history_tree.insert("", tk.END, values=(
                    timestamp,
                    record.result,
                    f"{record.resonance_level:.2f}",
                    f"{record.echo_depth:.2f}"
                ))
    
    def cleanup(self):
        """Clean up resources"""
        pass 