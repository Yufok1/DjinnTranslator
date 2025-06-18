"""
Ritual Trigger Panel
UI for managing ritual triggers and their actions
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any, List
import numpy as np
from core.ritual_trigger import RitualTrigger, TriggerAction, TriggerResult

class RitualTriggerPanel(ttk.Frame):
    """Panel for ritual triggers"""
    
    def __init__(self, parent, ritual_trigger: RitualTrigger):
        super().__init__(parent)
        self.ritual_trigger = ritual_trigger
        
        # Create layout
        self._create_layout()
        
        # Initialize state
        self.current_action: Optional[TriggerAction] = None
        self.current_result: Optional[TriggerResult] = None
    
    def _create_layout(self):
        """Create the panel layout"""
        # Input frame
        input_frame = ttk.LabelFrame(self, text="Ritual Trigger")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Phrase entry
        self.phrase_var = tk.StringVar()
        phrase_entry = ttk.Entry(
            input_frame,
            textvariable=self.phrase_var,
            width=50
        )
        phrase_entry.pack(side=tk.LEFT, padx=5, pady=5)
        phrase_entry.bind("<Return>", self._on_trigger)
        
        # Trigger button
        trigger_btn = ttk.Button(
            input_frame,
            text="Trigger",
            command=self._on_trigger
        )
        trigger_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Action frame
        action_frame = ttk.LabelFrame(self, text="Action")
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Action tree
        self.action_tree = ttk.Treeview(
            action_frame,
            columns=("type", "target", "priority", "confirmation"),
            show="headings",
            height=3
        )
        self.action_tree.heading("type", text="Type")
        self.action_tree.heading("target", text="Target")
        self.action_tree.heading("priority", text="Priority")
        self.action_tree.heading("confirmation", text="Confirmation")
        self.action_tree.column("type", width=100)
        self.action_tree.column("target", width=100)
        self.action_tree.column("priority", width=100)
        self.action_tree.column("confirmation", width=100)
        self.action_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # Result frame
        result_frame = ttk.LabelFrame(self, text="Result")
        result_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Result tree
        self.result_tree = ttk.Treeview(
            result_frame,
            columns=("success", "message", "resonance", "echo"),
            show="headings",
            height=3
        )
        self.result_tree.heading("success", text="Success")
        self.result_tree.heading("message", text="Message")
        self.result_tree.heading("resonance", text="Resonance")
        self.result_tree.heading("echo", text="Echo Depth")
        self.result_tree.column("success", width=50)
        self.result_tree.column("message", width=200)
        self.result_tree.column("resonance", width=100)
        self.result_tree.column("echo", width=100)
        self.result_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # Events frame
        events_frame = ttk.LabelFrame(self, text="Events")
        events_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Events tree
        self.events_tree = ttk.Treeview(
            events_frame,
            columns=("type", "target", "priority", "parameters"),
            show="headings"
        )
        self.events_tree.heading("type", text="Type")
        self.events_tree.heading("target", text="Target")
        self.events_tree.heading("priority", text="Priority")
        self.events_tree.heading("parameters", text="Parameters")
        self.events_tree.column("type", width=100)
        self.events_tree.column("target", width=100)
        self.events_tree.column("priority", width=100)
        self.events_tree.column("parameters", width=200)
        self.events_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pattern frame
        pattern_frame = ttk.LabelFrame(self, text="Trigger Patterns")
        pattern_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Pattern tree
        self.pattern_tree = ttk.Treeview(
            pattern_frame,
            columns=("type", "pattern"),
            show="headings",
            height=5
        )
        self.pattern_tree.heading("type", text="Type")
        self.pattern_tree.heading("pattern", text="Pattern")
        self.pattern_tree.column("type", width=100)
        self.pattern_tree.column("pattern", width=300)
        self.pattern_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # Load patterns
        self._load_patterns()
    
    def _load_patterns(self):
        """Load trigger patterns into the tree"""
        for action_type, patterns in self.ritual_trigger.trigger_patterns.items():
            for pattern in patterns:
                self.pattern_tree.insert(
                    "",
                    "end",
                    values=(action_type, pattern)
                )
    
    def _on_trigger(self, event=None):
        """Handle trigger button click"""
        # Get phrase
        phrase = self.phrase_var.get().strip()
        if not phrase:
            return
        
        # Trigger ritual
        result = self.ritual_trigger.trigger_ritual(phrase)
        
        # Update displays
        self._update_action_display(result.action)
        self._update_result_display(result)
        self._update_events_display(result.linked_events)
    
    def _update_action_display(self, action: Optional[TriggerAction]):
        """Update action display"""
        # Clear current items
        for item in self.action_tree.get_children():
            self.action_tree.delete(item)
        
        if action:
            # Add action
            self.action_tree.insert(
                "",
                "end",
                values=(
                    action.action_type,
                    action.target,
                    str(action.priority),
                    "Required" if action.requires_confirmation else "Optional"
                )
            )
    
    def _update_result_display(self, result: TriggerResult):
        """Update result display"""
        # Clear current items
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # Add result
        self.result_tree.insert(
            "",
            "end",
            values=(
                str(result.success),
                result.message,
                f"{result.resonance_level:.2f}",
                f"{result.echo_depth:.2f}"
            )
        )
    
    def _update_events_display(self, events: Optional[List[Dict[str, Any]]]):
        """Update events display"""
        # Clear current items
        for item in self.events_tree.get_children():
            self.events_tree.delete(item)
        
        if events:
            # Add events
            for event in events:
                self.events_tree.insert(
                    "",
                    "end",
                    values=(
                        event["type"],
                        event["target"],
                        str(event.get("priority", 0)),
                        str(event.get("parameters", {}))
                    )
                )
    
    def cleanup(self):
        """Clean up resources"""
        pass 