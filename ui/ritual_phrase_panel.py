"""
Ritual Phrase Panel Module
Provides UI for managing ritual phrases and their bindings
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable
from core.ritual_phrases import RitualPhraseSystem, RitualPhrase

class RitualPhrasePanel(ttk.Frame):
    """Ritual phrase panel widget"""
    
    def __init__(self, parent: tk.Widget, ritual_system: RitualPhraseSystem):
        super().__init__(parent)
        self.ritual_system = ritual_system
        
        # Create main layout
        self._create_layout()
        
        # Initialize state
        self.selected_ritual: Optional[str] = None
        self.filtered_rituals: List[str] = []
        
        # Load initial rituals
        self._refresh_ritual_list()
    
    def _create_layout(self):
        """Create panel layout"""
        # Create filter frame
        filter_frame = ttk.LabelFrame(self, text="Filters")
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        # Action filter
        ttk.Label(filter_frame, text="Action:").pack(side='left', padx=5)
        self.action_var = tk.StringVar()
        self.action_var.trace('w', self._on_filter_change)
        ttk.Combobox(
            filter_frame,
            textvariable=self.action_var,
            values=["chord", "harvest", "mirror", "daemon", "all"]
        ).pack(side='left', padx=5)
        
        # Create ritual list
        list_frame = ttk.LabelFrame(self, text="Ritual Phrases")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview
        self.ritual_tree = ttk.Treeview(
            list_frame,
            columns=("phrase", "action", "bound_id"),
            show="headings"
        )
        
        # Configure columns
        self.ritual_tree.heading("phrase", text="Phrase")
        self.ritual_tree.heading("action", text="Action")
        self.ritual_tree.heading("bound_id", text="Bound To")
        
        self.ritual_tree.column("phrase", width=200)
        self.ritual_tree.column("action", width=100)
        self.ritual_tree.column("bound_id", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.ritual_tree.yview)
        self.ritual_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.ritual_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.ritual_tree.bind('<<TreeviewSelect>>', self._on_ritual_select)
        
        # Create control buttons
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(
            control_frame,
            text="Record New",
            command=self._record_new_ritual
        ).pack(side='left', padx=5)
        
        ttk.Button(
            control_frame,
            text="Delete Selected",
            command=self._delete_selected_ritual
        ).pack(side='left', padx=5)
        
        ttk.Button(
            control_frame,
            text="Refresh",
            command=self._refresh_ritual_list
        ).pack(side='right', padx=5)
    
    def _refresh_ritual_list(self):
        """Refresh the ritual list"""
        # Clear existing items
        for item in self.ritual_tree.get_children():
            self.ritual_tree.delete(item)
        
        # Get all rituals
        rituals = self.ritual_system.ritual_phrases
        
        # Apply filters
        self.filtered_rituals = []
        for ritual_id, ritual in rituals.items():
            if self._matches_filters(ritual):
                self.filtered_rituals.append(ritual_id)
                
                # Add to treeview
                self.ritual_tree.insert(
                    "",
                    "end",
                    iid=ritual_id,
                    values=(
                        ritual.phrase,
                        ritual.bound_action,
                        ritual.bound_id
                    )
                )
    
    def _matches_filters(self, ritual: RitualPhrase) -> bool:
        """Check if ritual matches current filters"""
        # Check action filter
        action_filter = self.action_var.get()
        if action_filter and action_filter != "all" and action_filter != ritual.bound_action:
            return False
        
        return True
    
    def _on_filter_change(self, *args):
        """Handle filter changes"""
        self._refresh_ritual_list()
    
    def _on_ritual_select(self, event):
        """Handle ritual selection"""
        selection = self.ritual_tree.selection()
        if selection:
            self.selected_ritual = selection[0]
        else:
            self.selected_ritual = None
    
    def _record_new_ritual(self):
        """Record a new ritual phrase"""
        # Create recording dialog
        dialog = RitualRecordingDialog(self)
        self.wait_window(dialog)
        
        # Get recorded data
        if dialog.result:
            phrase, vocal_profile, breath_phase, echo_structure = dialog.result
            
            # Get binding info
            binding_dialog = RitualBindingDialog(self)
            self.wait_window(binding_dialog)
            
            if binding_dialog.result:
                bound_action, bound_id = binding_dialog.result
                
                # Register ritual phrase
                self.ritual_system.register_ritual_phrase(
                    phrase=phrase,
                    vocal_profile=vocal_profile,
                    breath_phase=breath_phase,
                    echo_structure=echo_structure,
                    bound_action=bound_action,
                    bound_id=bound_id
                )
                
                # Refresh list
                self._refresh_ritual_list()
    
    def _delete_selected_ritual(self):
        """Delete the selected ritual"""
        if self.selected_ritual:
            # Remove from treeview
            self.ritual_tree.delete(self.selected_ritual)
            
            # Remove from system
            del self.ritual_system.ritual_phrases[self.selected_ritual]
            
            # Save changes
            self.ritual_system._save_ritual_phrases()
            
            # Clear selection
            self.selected_ritual = None

class RitualRecordingDialog(tk.Toplevel):
    """Dialog for recording ritual phrases"""
    
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.title("Record Ritual Phrase")
        
        # Initialize result
        self.result = None
        
        # Create layout
        self._create_layout()
        
        # Center dialog
        self.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
    
    def _create_layout(self):
        """Create dialog layout"""
        # Create main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Instructions
        ttk.Label(
            main_frame,
            text="Speak your ritual phrase when ready.\nThe system will capture your voice profile and resonance."
        ).pack(pady=10)
        
        # Record button
        ttk.Button(
            main_frame,
            text="Start Recording",
            command=self._start_recording
        ).pack(pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.pack(pady=5)
        
        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            command=self.destroy
        ).pack(pady=5)
    
    def _start_recording(self):
        """Start recording ritual phrase"""
        # TODO: Implement recording
        pass

class RitualBindingDialog(tk.Toplevel):
    """Dialog for binding ritual phrases"""
    
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.title("Bind Ritual Phrase")
        
        # Initialize result
        self.result = None
        
        # Create layout
        self._create_layout()
        
        # Center dialog
        self.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
    
    def _create_layout(self):
        """Create dialog layout"""
        # Create main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Action selection
        ttk.Label(main_frame, text="Action:").pack(pady=5)
        self.action_var = tk.StringVar()
        ttk.Combobox(
            main_frame,
            textvariable=self.action_var,
            values=["chord", "harvest", "mirror", "daemon"]
        ).pack(pady=5)
        
        # Bound ID entry
        ttk.Label(main_frame, text="Bound To:").pack(pady=5)
        self.bound_id_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.bound_id_var).pack(pady=5)
        
        # Bind button
        ttk.Button(
            main_frame,
            text="Bind",
            command=self._bind_ritual
        ).pack(pady=5)
        
        # Cancel button
        ttk.Button(
            main_frame,
            text="Cancel",
            command=self.destroy
        ).pack(pady=5)
    
    def _bind_ritual(self):
        """Bind the ritual phrase"""
        action = self.action_var.get()
        bound_id = self.bound_id_var.get()
        
        if action and bound_id:
            self.result = (action, bound_id)
            self.destroy() 