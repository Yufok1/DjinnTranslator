"""
Ritual Interpreter Panel
UI for interacting with the ritual interpreter
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any, List
import numpy as np
from core.ritual_interpreter import RitualInterpreter, RitualCommand, RitualResponse

class RitualInterpreterPanel(ttk.Frame):
    """Panel for ritual interpretation"""
    
    def __init__(self, parent, ritual_interpreter: RitualInterpreter):
        super().__init__(parent)
        self.ritual_interpreter = ritual_interpreter
        
        # Create layout
        self._create_layout()
        
        # Initialize state
        self.current_command: Optional[RitualCommand] = None
        self.current_response: Optional[RitualResponse] = None
    
    def _create_layout(self):
        """Create the panel layout"""
        # Input frame
        input_frame = ttk.LabelFrame(self, text="Ritual Phrase")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Phrase entry
        self.phrase_var = tk.StringVar()
        phrase_entry = ttk.Entry(
            input_frame,
            textvariable=self.phrase_var,
            width=50
        )
        phrase_entry.pack(side=tk.LEFT, padx=5, pady=5)
        phrase_entry.bind("<Return>", self._on_interpret)
        
        # Interpret button
        interpret_btn = ttk.Button(
            input_frame,
            text="Interpret",
            command=self._on_interpret
        )
        interpret_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Command frame
        command_frame = ttk.LabelFrame(self, text="Command")
        command_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Command tree
        self.command_tree = ttk.Treeview(
            command_frame,
            columns=("type", "target", "parameters"),
            show="headings",
            height=3
        )
        self.command_tree.heading("type", text="Type")
        self.command_tree.heading("target", text="Target")
        self.command_tree.heading("parameters", text="Parameters")
        self.command_tree.column("type", width=100)
        self.command_tree.column("target", width=100)
        self.command_tree.column("parameters", width=200)
        self.command_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # Response frame
        response_frame = ttk.LabelFrame(self, text="Response")
        response_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Response tree
        self.response_tree = ttk.Treeview(
            response_frame,
            columns=("success", "message", "resonance", "echo"),
            show="headings",
            height=3
        )
        self.response_tree.heading("success", text="Success")
        self.response_tree.heading("message", text="Message")
        self.response_tree.heading("resonance", text="Resonance")
        self.response_tree.heading("echo", text="Echo Depth")
        self.response_tree.column("success", width=50)
        self.response_tree.column("message", width=200)
        self.response_tree.column("resonance", width=100)
        self.response_tree.column("echo", width=100)
        self.response_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # Events frame
        events_frame = ttk.LabelFrame(self, text="Events")
        events_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Events tree
        self.events_tree = ttk.Treeview(
            events_frame,
            columns=("type", "details", "phase", "level"),
            show="headings"
        )
        self.events_tree.heading("type", text="Type")
        self.events_tree.heading("details", text="Details")
        self.events_tree.heading("phase", text="Breath Phase")
        self.events_tree.heading("level", text="Recursion")
        self.events_tree.column("type", width=100)
        self.events_tree.column("details", width=200)
        self.events_tree.column("phase", width=100)
        self.events_tree.column("level", width=100)
        self.events_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Context frame
        context_frame = ttk.LabelFrame(self, text="Context")
        context_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Context tree
        self.context_tree = ttk.Treeview(
            context_frame,
            columns=("key", "value"),
            show="headings",
            height=5
        )
        self.context_tree.heading("key", text="Key")
        self.context_tree.heading("value", text="Value")
        self.context_tree.column("key", width=100)
        self.context_tree.column("value", width=200)
        self.context_tree.pack(fill=tk.X, padx=5, pady=5)
        
        # Update context display
        self._update_context_display()
    
    def _on_interpret(self, event=None):
        """Handle interpret button click"""
        # Get phrase
        phrase = self.phrase_var.get().strip()
        if not phrase:
            return
        
        # Interpret phrase
        response = self.ritual_interpreter.interpret_phrase(phrase)
        
        # Update displays
        self._update_command_display(response.command)
        self._update_response_display(response)
        self._update_events_display(response.linked_events)
        self._update_context_display()
    
    def _update_command_display(self, command: Optional[RitualCommand]):
        """Update command display"""
        # Clear current items
        for item in self.command_tree.get_children():
            self.command_tree.delete(item)
        
        if command:
            # Add command
            self.command_tree.insert(
                "",
                "end",
                values=(
                    command.command_type,
                    command.target,
                    str(command.parameters)
                )
            )
    
    def _update_response_display(self, response: RitualResponse):
        """Update response display"""
        # Clear current items
        for item in self.response_tree.get_children():
            self.response_tree.delete(item)
        
        # Add response
        self.response_tree.insert(
            "",
            "end",
            values=(
                str(response.success),
                response.message,
                f"{response.resonance_level:.2f}",
                f"{response.echo_depth:.2f}"
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
                        str(event.get("details", "")),
                        f"{event.get('breath_phase', 0.0):.2f}",
                        str(event.get("recursion_level", 0))
                    )
                )
    
    def _update_context_display(self):
        """Update context display"""
        # Clear current items
        for item in self.context_tree.get_children():
            self.context_tree.delete(item)
        
        # Add context items
        for key, value in self.ritual_interpreter.context.items():
            if isinstance(value, set):
                value = ", ".join(str(v) for v in value)
            self.context_tree.insert(
                "",
                "end",
                values=(key, str(value))
            )
    
    def cleanup(self):
        """Clean up resources"""
        pass 