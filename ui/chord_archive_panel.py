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
Chord Archive Panel Module
Provides UI for browsing and managing preserved memory chords
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Callable
from core.chord_preservation import ChordPreservation, PreservedChord

class ChordArchivePanel(ttk.Frame):
    """Chord archive panel widget"""
    
    def __init__(self, parent: tk.Widget, chord_preservation: ChordPreservation):
        super().__init__(parent)
        self.chord_preservation = chord_preservation
        
        # Create main layout
        self._create_layout()
        
        # Initialize state
        self.selected_chord: Optional[str] = None
        self.filtered_chords: List[str] = []
        
        # Load initial chords
        self._refresh_chord_list()
    
    def _create_layout(self):
        """Create panel layout"""
        # Create filter frame
        filter_frame = ttk.LabelFrame(self, text="Filters")
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        # Sigil filter
        ttk.Label(filter_frame, text="Sigil:").pack(side='left', padx=5)
        self.sigil_var = tk.StringVar()
        self.sigil_var.trace('w', self._on_filter_change)
        ttk.Entry(filter_frame, textvariable=self.sigil_var).pack(side='left', padx=5)
        
        # Chord type filter
        ttk.Label(filter_frame, text="Type:").pack(side='left', padx=5)
        self.type_var = tk.StringVar()
        self.type_var.trace('w', self._on_filter_change)
        ttk.Combobox(
            filter_frame,
            textvariable=self.type_var,
            values=["major", "minor", "dissonant", "resolved", "all"]
        ).pack(side='left', padx=5)
        
        # Create chord list
        list_frame = ttk.LabelFrame(self, text="Preserved Chords")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview
        self.chord_tree = ttk.Treeview(
            list_frame,
            columns=("name", "sigil", "type", "memories"),
            show="headings"
        )
        
        # Configure columns
        self.chord_tree.heading("name", text="Name")
        self.chord_tree.heading("sigil", text="Sigil")
        self.chord_tree.heading("type", text="Type")
        self.chord_tree.heading("memories", text="Memories")
        
        self.chord_tree.column("name", width=150)
        self.chord_tree.column("sigil", width=100)
        self.chord_tree.column("type", width=100)
        self.chord_tree.column("memories", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.chord_tree.yview)
        self.chord_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.chord_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.chord_tree.bind('<<TreeviewSelect>>', self._on_chord_select)
        
        # Create control buttons
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(
            control_frame,
            text="Play Selected",
            command=self._play_selected_chord
        ).pack(side='left', padx=5)
        
        ttk.Button(
            control_frame,
            text="Delete Selected",
            command=self._delete_selected_chord
        ).pack(side='left', padx=5)
        
        ttk.Button(
            control_frame,
            text="Refresh",
            command=self._refresh_chord_list
        ).pack(side='right', padx=5)
    
    def _refresh_chord_list(self):
        """Refresh the chord list"""
        # Clear existing items
        for item in self.chord_tree.get_children():
            self.chord_tree.delete(item)
        
        # Get all chords
        chords = self.chord_preservation.preserved_chords
        
        # Apply filters
        self.filtered_chords = []
        for chord_id, chord in chords.items():
            if self._matches_filters(chord):
                self.filtered_chords.append(chord_id)
                
                # Add to treeview
                self.chord_tree.insert(
                    "",
                    "end",
                    iid=chord_id,
                    values=(
                        chord.name,
                        chord.sigil,
                        chord.chord_type,
                        len(chord.memories)
                    )
                )
    
    def _matches_filters(self, chord: PreservedChord) -> bool:
        """Check if chord matches current filters"""
        # Check sigil filter
        sigil_filter = self.sigil_var.get().strip()
        if sigil_filter and sigil_filter not in chord.sigil:
            return False
        
        # Check type filter
        type_filter = self.type_var.get()
        if type_filter and type_filter != "all" and type_filter != chord.chord_type:
            return False
        
        return True
    
    def _on_filter_change(self, *args):
        """Handle filter changes"""
        self._refresh_chord_list()
    
    def _on_chord_select(self, event):
        """Handle chord selection"""
        selection = self.chord_tree.selection()
        if selection:
            self.selected_chord = selection[0]
        else:
            self.selected_chord = None
    
    def _play_selected_chord(self):
        """Play the selected chord"""
        if self.selected_chord:
            self.chord_preservation.invoke_chord(self.selected_chord)
    
    def _delete_selected_chord(self):
        """Delete the selected chord"""
        if self.selected_chord:
            # Remove from treeview
            self.chord_tree.delete(self.selected_chord)
            
            # Remove from preservation
            del self.chord_preservation.preserved_chords[self.selected_chord]
            
            # Save changes
            self.chord_preservation._save_preserved_chords()
            
            # Clear selection
            self.selected_chord = None 