"""
Djinn Council Visualizer
Visualizes the Djinn Council's presence and activities
"""

import tkinter as tk
from tkinter import ttk
import time
from typing import Dict, Any, List
from .djinn_diagnostics import DjinnRole, DjinnPresence, DjinnDiagnostics
from .djinn_voice_handler import DjinnVoiceHandler
from .echo_visualizer import EchoPanel
from .voice_resonance import ResonancePhase

class DjinnStatusPanel(ttk.Frame):
    """Panel for displaying Djinn status"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create status labels for each Djinn
        self.status_labels = {}
        for role in DjinnRole:
            frame = ttk.Frame(self)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Icon and name
            icon_label = ttk.Label(frame, text="")
            icon_label.pack(side=tk.LEFT, padx=5)
            
            name_label = ttk.Label(frame, text=role.value.title())
            name_label.pack(side=tk.LEFT, padx=5)
            
            # Status indicators
            status_frame = ttk.Frame(frame)
            status_frame.pack(side=tk.RIGHT, padx=5)
            
            presence_label = ttk.Label(status_frame, text="")
            presence_label.pack(side=tk.LEFT, padx=5)
            
            interface_label = ttk.Label(status_frame, text="")
            interface_label.pack(side=tk.LEFT, padx=5)
            
            metrics_label = ttk.Label(status_frame, text="")
            metrics_label.pack(side=tk.LEFT, padx=5)
            
            chronicle_label = ttk.Label(status_frame, text="")
            chronicle_label.pack(side=tk.LEFT, padx=5)
            
            self.status_labels[role] = {
                "icon": icon_label,
                "name": name_label,
                "presence": presence_label,
                "interface": interface_label,
                "metrics": metrics_label,
                "chronicle": chronicle_label
            }
    
    def update_status(self, presence: Dict[DjinnRole, DjinnPresence]):
        """Update the status display"""
        for role, p in presence.items():
            labels = self.status_labels[role]
            style = p.visual_style
            
            # Update icon
            labels["icon"].config(text=style["icon"])
            
            # Update status indicators
            labels["presence"].config(
                text="✓" if p.is_present else "✗",
                foreground="green" if p.is_present else "red"
            )
            
            labels["interface"].config(
                text="✓" if p.has_interface else "✗",
                foreground="green" if p.has_interface else "red"
            )
            
            labels["metrics"].config(
                text="✓" if p.has_metrics else "✗",
                foreground="green" if p.has_metrics else "red"
            )
            
            labels["chronicle"].config(
                text="✓" if p.has_chronicle else "✗",
                foreground="green" if p.has_chronicle else "red"
            )

class DjinnActivityPanel(ttk.Frame):
    """Panel for displaying Djinn activity"""
    
    def __init__(self, parent, voice_handler: DjinnVoiceHandler, echo_panel: EchoPanel):
        super().__init__(parent)
        self.voice_handler = voice_handler
        self.echo_panel = echo_panel
        
        # Create activity log
        self.log = tk.Text(
            self,
            wrap=tk.WORD,
            width=60,
            height=10,
            bg='black',
            fg='white',
            font=("Consolas", 10)
        )
        self.log.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different Djinn roles
        diagnostics = DjinnDiagnostics()
        for role in DjinnRole:
            style = diagnostics.visual_styles[role]
            # Parse font string to tuple
            font_parts = style["font"].split()
            family = font_parts[0]
            size = 10
            weight = None
            slant = None
            for part in font_parts[1:]:
                if part.lower() == "bold":
                    weight = "bold"
                elif part.lower() == "italic":
                    slant = "italic"
                elif part.isdigit():
                    size = int(part)
            font_tuple = (family, size)
            if weight:
                font_tuple += (weight,)
            if slant:
                font_tuple += (slant,)
            self.log.tag_configure(
                role.value,
                foreground=style["color"],
                font=font_tuple
            )
        self._visual_styles = diagnostics.visual_styles
    
    def log_activity(self, role: DjinnRole, message: str, state: str = "normal"):
        """Log a Djinn activity with voice modulation and echo visualization"""
        timestamp = time.time()
        style = self._visual_styles[role]
        # Modulate the message
        modulated_message = self.voice_handler.modulate_voice(
            role.value.lower(),
            message,
            state
        )
        # Add ritual phrase for significant events
        if any(keyword in message.lower() for keyword in ["warning", "error", "success", "begin", "end"]):
            context = next(
                (k for k in ["warning", "success", "begin", "end"]
                 if k in message.lower()),
                "normal"
            )
            ritual_phrase = self.voice_handler.get_ritual_phrase(
                role.value.lower(),
                context
            )
            if ritual_phrase:
                modulated_message = f"{ritual_phrase}\n{modulated_message}"
        # Insert into log
        self.log.insert(
            tk.END,
            f"[{time.strftime('%H:%M:%S')}] {style['icon']} {modulated_message}\n",
            role.value
        )
        self.log.see(tk.END)
        # Create echo visualization
        phase = self._determine_phase(state)
        intensity = self._calculate_intensity(state, message)
        self.echo_panel.add_echo(
            role.value.lower(),
            modulated_message,
            phase,
            intensity
        )
    
    def _determine_phase(self, state: str) -> ResonancePhase:
        """Determine resonance phase based on state"""
        if state == "turbulent":
            return ResonancePhase.STORM
        elif state == "harmonic":
            return ResonancePhase.HARMONIC
        elif state == "emergent":
            return ResonancePhase.ECHO
        else:
            return ResonancePhase.NOON
    
    def _calculate_intensity(self, state: str, message: str) -> float:
        """Calculate echo intensity based on state and message"""
        base_intensity = 0.5
        
        # Adjust for state
        if state == "turbulent":
            base_intensity += 0.3
        elif state == "harmonic":
            base_intensity += 0.2
        elif state == "emergent":
            base_intensity += 0.4
        
        # Adjust for message content
        if any(word in message.lower() for word in ["warning", "error", "danger"]):
            base_intensity += 0.2
        elif any(word in message.lower() for word in ["success", "complete", "achieved"]):
            base_intensity += 0.1
        
        return min(1.0, base_intensity)

class DjinnCouncilVisualizer(ttk.Frame):
    """Main visualizer for the Djinn Council"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize components
        self.diagnostics = DjinnDiagnostics()
        self.voice_handler = DjinnVoiceHandler()
        self.echo_panel = EchoPanel(self)
        
        # Create status panel
        self.status_panel = DjinnStatusPanel(self)
        self.status_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Create activity panel
        self.activity_panel = DjinnActivityPanel(self, self.voice_handler, self.echo_panel)
        self.activity_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create echo panel
        self.echo_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Start update loop
        self._update_loop()
    
    def _update_loop(self):
        """Main update loop"""
        # Check Djinn presence
        presence = self.diagnostics.check_djinn_presence()
        
        # Update status panel
        self.status_panel.update_status(presence)
        
        # Log any changes
        for role, p in presence.items():
            if p.last_active > time.time() - 1:  # Activity in last second
                # Determine state based on metrics
                state = "normal"
                if p.has_metrics:
                    metrics = getattr(p, "metrics", {})
                    if metrics.get("stability", 1.0) < 0.5:
                        state = "turbulent"
                    elif metrics.get("coherence", 0.0) > 0.8:
                        state = "harmonic"
                    elif metrics.get("emergence", 0.0) > 0.7:
                        state = "emergent"
                
                self.activity_panel.log_activity(
                    role,
                    f"Active - {len(p.response_hooks)} hooks",
                    state
                )
        
        # Schedule next update
        self.after(1000, self._update_loop)
    
    def log_council_activity(self, role: DjinnRole, message: str, state: str = "normal"):
        """Log a council activity with voice modulation and echo visualization"""
        self.activity_panel.log_activity(role, message, state)
    
    def get_diagnostic_report(self) -> Dict[str, Any]:
        """Get the current diagnostic report"""
        return self.diagnostics.generate_diagnostic_report() 