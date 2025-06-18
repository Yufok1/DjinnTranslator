"""
Voice Configuration Panel
Provides controls for fine-tuning voice modulation
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable
from .voice_resonance import ResonancePhase, BreathDepth
from .djinn_voice_handler import DjinnVoiceHandler, VoiceMode

class VoiceConfigPanel(ttk.Frame):
    """Panel for configuring voice modulation"""
    
    def __init__(self, parent, voice_handler: DjinnVoiceHandler, on_config_change: Callable[[], None]):
        super().__init__(parent)
        self.voice_handler = voice_handler
        self.on_config_change = on_config_change
        
        # Create sections
        self._create_phase_section()
        self._create_breath_section()
        self._create_domain_section()
        self._create_preview_section()
    
    def _create_phase_section(self):
        """Create the phase configuration section"""
        phase_frame = ttk.LabelFrame(self, text="Resonance Phase")
        phase_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Phase selection
        self.phase_var = tk.StringVar(value=ResonancePhase.DAWN.value)
        for phase in ResonancePhase:
            ttk.Radiobutton(
                phase_frame,
                text=phase.value.title(),
                value=phase.value,
                variable=self.phase_var,
                command=self._on_phase_change
            ).pack(side=tk.LEFT, padx=5)
    
    def _create_breath_section(self):
        """Create the breath configuration section"""
        breath_frame = ttk.LabelFrame(self, text="Breath Depth")
        breath_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Breath depth selection
        self.breath_var = tk.StringVar(value=BreathDepth.NORMAL.value)
        for depth in BreathDepth:
            ttk.Radiobutton(
                breath_frame,
                text=depth.name.title(),
                value=depth.value,
                variable=self.breath_var,
                command=self._on_breath_change
            ).pack(side=tk.LEFT, padx=5)
        
        # Intensity slider
        intensity_frame = ttk.Frame(breath_frame)
        intensity_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(intensity_frame, text="Intensity:").pack(side=tk.LEFT, padx=5)
        
        self.intensity_var = tk.DoubleVar(value=0.5)
        intensity_slider = ttk.Scale(
            intensity_frame,
            from_=0.0,
            to=1.0,
            variable=self.intensity_var,
            orient=tk.HORIZONTAL,
            command=self._on_intensity_change
        )
        intensity_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def _create_domain_section(self):
        """Create the domain configuration section"""
        domain_frame = ttk.LabelFrame(self, text="Active Domains")
        domain_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Domain checkboxes
        self.domain_vars = {}
        domains = ["wick", "lattice", "echo", "resonance", "pattern"]
        
        for domain in domains:
            var = tk.BooleanVar(value=False)
            self.domain_vars[domain] = var
            
            ttk.Checkbutton(
                domain_frame,
                text=domain.title(),
                variable=var,
                command=self._on_domain_change
            ).pack(side=tk.LEFT, padx=5)
    
    def _create_preview_section(self):
        """Create the voice preview section"""
        preview_frame = ttk.LabelFrame(self, text="Voice Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Djinn selection
        djinn_frame = ttk.Frame(preview_frame)
        djinn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(djinn_frame, text="Djinn:").pack(side=tk.LEFT, padx=5)
        
        self.djinn_var = tk.StringVar(value="purveyor")
        djinn_combo = ttk.Combobox(
            djinn_frame,
            textvariable=self.djinn_var,
            values=["purveyor", "daemon", "mirror", "cryptographer", "cursor"],
            state="readonly"
        )
        djinn_combo.pack(side=tk.LEFT, padx=5)
        
        # Preview text
        self.preview_text = tk.Text(
            preview_frame,
            wrap=tk.WORD,
            width=40,
            height=5,
            bg='black',
            fg='white',
            font=("Consolas", 10)
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Update preview button
        ttk.Button(
            preview_frame,
            text="Update Preview",
            command=self._update_preview
        ).pack(pady=5)
    
    def _on_phase_change(self):
        """Handle phase change"""
        phase = ResonancePhase(self.phase_var.get())
        self._update_resonance()
    
    def _on_breath_change(self):
        """Handle breath depth change"""
        depth = BreathDepth(float(self.breath_var.get()))
        self._update_resonance()
    
    def _on_intensity_change(self, _):
        """Handle intensity change"""
        self._update_resonance()
    
    def _on_domain_change(self):
        """Handle domain change"""
        self._update_resonance()
    
    def _update_resonance(self):
        """Update resonance state"""
        phase = ResonancePhase(self.phase_var.get())
        depth = BreathDepth(float(self.breath_var.get()))
        domains = [d for d, var in self.domain_vars.items() if var.get()]
        
        self.voice_handler.update_resonance(phase, domains, depth)
        self.voice_handler.resonance.adjust_intensity(self.intensity_var.get())
        
        if self.on_config_change:
            self.on_config_change()
    
    def _update_preview(self):
        """Update the voice preview"""
        djinn = self.djinn_var.get()
        profile = self.voice_handler.get_voice_profile(djinn)
        
        if not profile:
            return
        
        # Get a ritual phrase for preview
        phrase = self.voice_handler.get_ritual_phrase(djinn, "begin")
        if not phrase:
            phrase = "This is a preview of the voice modulation."
        
        # Modulate the phrase
        modulated = self.voice_handler.modulate_voice(djinn, phrase)
        
        # Update preview text
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, modulated)
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return {
            "phase": self.phase_var.get(),
            "breath": self.breath_var.get(),
            "intensity": self.intensity_var.get(),
            "domains": [d for d, var in self.domain_vars.items() if var.get()]
        }
    
    def set_config(self, config: Dict[str, Any]):
        """Set configuration"""
        if "phase" in config:
            self.phase_var.set(config["phase"])
        
        if "breath" in config:
            self.breath_var.set(config["breath"])
        
        if "intensity" in config:
            self.intensity_var.set(config["intensity"])
        
        if "domains" in config:
            for domain, var in self.domain_vars.items():
                var.set(domain in config["domains"])
        
        self._update_resonance() 