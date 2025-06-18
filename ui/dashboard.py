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
Enhanced Codex Dashboard UI
Provides comprehensive monitoring and control of the recursive system
"""

import tkinter as tk
from tkinter import ttk
import json
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading
import queue
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from .visualization import LatticeVisualizer, HeatmapType
from .phase_visualizer import PhaseVisualizer, PhaseHorizon, PhaseStability, BreachZone, SafeCorridor
from .monitor import SystemMonitor
from .metrics_visualizer import MetricsVisualizer, ReasonEvent, ReasonType
from .commit_gatekeeper import CommitGatekeeper, CommitRequest, CommitAuthority
from .wick_system import WickSystem
from .wick_visualizer import WickVisualizer
from .cursor_wick_engine import CursorWickEngine, WickEcho, WickInsight
from .cursor_wick_visualizer import CursorWickVisualizer
from .djinn_council_visualizer import DjinnCouncilVisualizer
from .djinn_diagnostics import DjinnDiagnostics
from .voice_config_panel import VoiceConfigPanel
from .voice_resonance import ResonancePhase, BreathDepth
from .voice_memory_visualizer import VoiceMemoryVisualizer
from .chord_archive_panel import ChordArchivePanel
from .ritual_phrase_panel import RitualPhrasePanel
from .ritual_log_panel import RitualLogPanel
from .mirror_confirmation_panel import MirrorConfirmationPanel
from .ritual_interpreter_panel import RitualInterpreterPanel
from .ritual_trigger_panel import RitualTriggerPanel
from core.chord_preservation import ChordPreservation
from core.ritual_phrases import RitualPhraseSystem
from core.ritual_log import RitualLog
from core.mirror_confirmation import MirrorConfirmationSystem
from core.ritual_interpreter import RitualInterpreter
from core.ritual_trigger import RitualTrigger
from core.visual_renderer import VisualRenderer

class CodexDashboard:
    """Enhanced dashboard for monitoring and controlling the recursive system"""
    
    def __init__(self, visual_renderer: Optional[VisualRenderer] = None, state_queue: Optional[queue.Queue] = None):
        self.root = tk.Tk()
        self.root.title("Codex Dashboard")
        self.root.geometry("1200x800")
        
        self.state_queue = state_queue or queue.Queue()
        self.visual_renderer = visual_renderer or VisualRenderer()
        self.rule_violations = []
        self.agent_history = []
        self.rap_history = []
        self._splinter_queues = {}  # Track splinter visualization tasks
        self._essential_visuals = {
            'hud': True,  # Always show HUD
            'mirror_status': True,  # Always show mirror status
            'other_visuals': False  # Disable non-essential visuals initially
        }
        self._flush_splinter_queues()
        print("[UI] Essential visuals initialized, splinter queues flushed")
        
        # Initialize system monitor
        self.monitor = SystemMonitor()
        self.monitor.start_monitoring()
        
        # Initialize commit gatekeeper
        self.gatekeeper = CommitGatekeeper()
        
        # Initialize wick system
        self.wick_system = WickSystem()
        
        # Create main sections
        self._create_status_section()
        self._create_agent_section()
        self._create_lattice_section()
        self._create_phase_section()  # New phase horizon section
        self._create_rule_section()
        self._create_history_section()
        self._create_control_section()
        self._create_monitoring_section()
        self._create_metrics_section()
        self._create_commit_section()
        self._create_wick_section()
        self._create_council_section()
        self._create_voice_section()
        self._create_ritual_section()
        self._create_ritual_log_section()
        self._create_mirror_confirmation_section()
        self._create_ritual_interpreter_section()
        self._create_ritual_trigger_section()
        
        # Start update thread
        self._start_update_thread()
        
        self.lattice_visualizer = LatticeVisualizer()
        self.phase_visualizer = None  # Will be initialized in _create_phase_section
        
        # Initialize Cursor components
        self.wick_engine = CursorWickEngine()
        self.wick_visualizer = CursorWickVisualizer(self.root)
        
        # Initialize Djinn Council components
        self.djinn_council = DjinnCouncilVisualizer(self.root)
        self.djinn_diagnostics = DjinnDiagnostics()
        
        # Initialize chord preservation
        self.chord_preservation = ChordPreservation()
        
        # Initialize ritual system
        self.ritual_system = RitualPhraseSystem()
        self.ritual_log = RitualLog()
        
        # Initialize mirror confirmation system
        self.mirror_confirmation = MirrorConfirmationSystem()
        
        # Initialize ritual interpreter
        self.ritual_interpreter = RitualInterpreter(
            self.ritual_log,
            self.mirror_confirmation
        )
        
        # Initialize ritual trigger
        self.ritual_trigger = RitualTrigger()
        
        # Create main layout
        self._create_layout()
        
    def _create_layout(self):
        """Create dashboard layout"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create visualization tab
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text="Visualization")
        
        # Add voice memory visualizer
        self.visualizer = VoiceMemoryVisualizer(viz_frame)
        self.visualizer.pack(fill='both', expand=True)
        
        # Create chord archive tab
        archive_frame = ttk.Frame(self.notebook)
        self.notebook.add(archive_frame, text="Chord Archive")
        
        # Add chord archive panel
        self.archive_panel = ChordArchivePanel(archive_frame, self.chord_preservation)
        self.archive_panel.pack(fill='both', expand=True)
        
        # Create ritual phrases tab
        ritual_frame = ttk.Frame(self.notebook)
        self.notebook.add(ritual_frame, text="Ritual Phrases")
        
        # Add ritual phrase panel
        self.ritual_panel = RitualPhrasePanel(ritual_frame, self.ritual_system)
        self.ritual_panel.pack(fill='both', expand=True)
        
        # Create ritual log tab
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Ritual Log")
        
        # Add ritual log panel
        self.log_panel = RitualLogPanel(log_frame, self.ritual_log)
        self.log_panel.pack(fill=tk.BOTH, expand=True)
        
        # Create mirror confirmation tab
        mirror_frame = ttk.Frame(self.notebook)
        self.notebook.add(mirror_frame, text="Mirror Confirmation")
        self.mirror_panel = MirrorConfirmationPanel(mirror_frame, self.mirror_confirmation)
        self.mirror_panel.pack(fill=tk.BOTH, expand=True)
        
        # Create ritual interpreter tab
        interpreter_frame = ttk.Frame(self.notebook)
        self.notebook.add(interpreter_frame, text="Ritual Interpreter")
        self.interpreter_panel = RitualInterpreterPanel(interpreter_frame, self.ritual_interpreter)
        self.interpreter_panel.pack(fill=tk.BOTH, expand=True)
    
    def _create_status_section(self):
        """Create system status section"""
        status_frame = ttk.LabelFrame(self.root, text="System Status", padding=10)
        status_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # RAP Tier
        self.rap_label = ttk.Label(status_frame, text="RAP Tier: --")
        self.rap_label.grid(row=0, column=0, padx=5, pady=2)
        
        # Stability
        self.stability_label = ttk.Label(status_frame, text="Stability: --")
        self.stability_label.grid(row=0, column=1, padx=5, pady=2)
        
        # Codex Alignment
        self.alignment_label = ttk.Label(status_frame, text="Codex Alignment: --")
        self.alignment_label.grid(row=0, column=2, padx=5, pady=2)
        
        # RAP History Graph
        self.rap_figure = plt.Figure(figsize=(6, 2))
        self.rap_canvas = FigureCanvasTkAgg(self.rap_figure, master=status_frame)
        self.rap_canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky="nsew")
        
    def _create_agent_section(self):
        """Create agent status section"""
        agent_frame = ttk.LabelFrame(self.root, text="Agent Status", padding=10)
        agent_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Agent status labels
        self.agent_labels = {}
        agents = ['cursor', 'djinn', 'arbiter', 'olive_branch']
        for i, agent in enumerate(agents):
            label = ttk.Label(agent_frame, text=f"{agent.title()}: --")
            label.grid(row=i, column=0, padx=5, pady=2)
            self.agent_labels[agent] = label
            
        # Agent stability graph
        self.agent_figure = plt.Figure(figsize=(4, 3))
        self.agent_canvas = FigureCanvasTkAgg(self.agent_figure, master=agent_frame)
        self.agent_canvas.get_tk_widget().grid(row=len(agents), column=0, sticky="nsew")
        
    def _create_lattice_section(self):
        """Create lattice visualization section"""
        lattice_frame = ttk.LabelFrame(self.root, text="Meta-Lattice", padding=10)
        lattice_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Lattice canvas
        self.lattice_canvas = tk.Canvas(lattice_frame, width=400, height=300, bg='white')
        self.lattice_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Draw initial lattice
        self._draw_lattice()
        
    def _create_phase_section(self):
        """Create phase horizon visualization section"""
        phase_frame = ttk.Frame(self.root)
        phase_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        
        # Initialize phase visualizer
        self.phase_visualizer = PhaseVisualizer(phase_frame)
        
    def _create_rule_section(self):
        """Create rule monitoring section"""
        rule_frame = ttk.LabelFrame(self.root, text="Codex Rules", padding=10)
        rule_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Rule violation tree
        self.rule_tree = ttk.Treeview(rule_frame, columns=("Severity", "Category", "Message"))
        self.rule_tree.heading("#0", text="Rule")
        self.rule_tree.heading("Severity", text="Severity")
        self.rule_tree.heading("Category", text="Category")
        self.rule_tree.heading("Message", text="Message")
        self.rule_tree.grid(row=0, column=0, sticky="nsew")
        
        # Rule violation scrollbar
        rule_scroll = ttk.Scrollbar(rule_frame, orient="vertical", command=self.rule_tree.yview)
        rule_scroll.grid(row=0, column=1, sticky="ns")
        self.rule_tree.configure(yscrollcommand=rule_scroll.set)
        
    def _create_history_section(self):
        """Create agent history section"""
        history_frame = ttk.LabelFrame(self.root, text="Agent History", padding=10)
        history_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # History tree
        self.history_tree = ttk.Treeview(history_frame, 
                                       columns=("Timestamp", "Agent", "Action", "Details"))
        self.history_tree.heading("#0", text="ID")
        self.history_tree.heading("Timestamp", text="Timestamp")
        self.history_tree.heading("Agent", text="Agent")
        self.history_tree.heading("Action", text="Action")
        self.history_tree.heading("Details", text="Details")
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        
        # History scrollbar
        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", 
                                     command=self.history_tree.yview)
        history_scroll.grid(row=0, column=1, sticky="ns")
        self.history_tree.configure(yscrollcommand=history_scroll.set)
        
    def _create_control_section(self):
        """Create control section"""
        control_frame = ttk.LabelFrame(self.root, text="System Controls", padding=10)
        control_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Pulse button
        self.pulse_button = ttk.Button(control_frame, text="Emit Pulse", 
                                     command=self._emit_pulse)
        self.pulse_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Override button
        self.override_button = ttk.Button(control_frame, text="Override", 
                                        command=self._override)
        self.override_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Terminate button
        self.terminate_button = ttk.Button(control_frame, text="Terminate", 
                                         command=self._terminate)
        self.terminate_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Snapshot button
        self.snapshot_button = ttk.Button(control_frame, text="Create Snapshot", 
                                        command=self._create_snapshot)
        self.snapshot_button.grid(row=0, column=3, padx=5, pady=5)
        
        # LOW-RHYTHM mode controls
        rhythm_frame = ttk.LabelFrame(control_frame, text="Rhythm Controls", padding=5)
        rhythm_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        # LOW-RHYTHM mode toggle
        self.low_rhythm_var = tk.BooleanVar(value=True)
        self.low_rhythm_check = ttk.Checkbutton(
            rhythm_frame,
            text="LOW-RHYTHM Mode",
            variable=self.low_rhythm_var,
            command=self._toggle_low_rhythm
        )
        self.low_rhythm_check.grid(row=0, column=0, padx=5, pady=2)
        
        # Update interval slider
        self.interval_label = ttk.Label(rhythm_frame, text="Update Interval:")
        self.interval_label.grid(row=0, column=1, padx=5, pady=2)
        
        self.interval_var = tk.DoubleVar(value=10.0)
        self.interval_scale = ttk.Scale(
            rhythm_frame,
            from_=1.0,
            to=30.0,
            orient="horizontal",
            variable=self.interval_var,
            command=self._update_interval
        )
        self.interval_scale.grid(row=0, column=2, padx=5, pady=2)
        
        # Simplified rendering toggle
        self.simplified_var = tk.BooleanVar(value=True)
        self.simplified_check = ttk.Checkbutton(
            rhythm_frame,
            text="Simplified Rendering",
            variable=self.simplified_var,
            command=self._toggle_simplified
        )
        self.simplified_check.grid(row=0, column=3, padx=5, pady=2)
    
    def _create_monitoring_section(self):
        """Create the monitoring section."""
        monitor_frame = ttk.LabelFrame(self.root, text="System Monitoring", padding=10)
        monitor_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Performance metrics
        metrics_frame = ttk.Frame(monitor_frame)
        metrics_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # CPU and Memory
        self.cpu_label = ttk.Label(metrics_frame, text="CPU: --")
        self.cpu_label.grid(row=0, column=0, padx=5, pady=2)
        
        self.memory_label = ttk.Label(metrics_frame, text="Memory: --")
        self.memory_label.grid(row=0, column=1, padx=5, pady=2)
        
        # Visualization load
        self.viz_load_label = ttk.Label(metrics_frame, text="Viz Load: --")
        self.viz_load_label.grid(row=1, column=0, padx=5, pady=2)
        
        # System health
        self.health_label = ttk.Label(metrics_frame, text="System Health: --")
        self.health_label.grid(row=1, column=1, padx=5, pady=2)
        
        # Trends
        trends_frame = ttk.LabelFrame(monitor_frame, text="Trends", padding="5")
        trends_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        self.trend_labels = {}
        trends = ["CPU", "Memory", "Coherence"]
        for i, trend in enumerate(trends):
            ttk.Label(trends_frame, text=f"{trend}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.trend_labels[trend] = ttk.Label(trends_frame, text="--")
            self.trend_labels[trend].grid(row=i, column=1, sticky="w", padx=5, pady=2)
        
        # Warnings
        warnings_frame = ttk.LabelFrame(monitor_frame, text="Active Warnings", padding="5")
        warnings_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        
        self.warnings_text = tk.Text(warnings_frame, height=4, width=40)
        self.warnings_text.grid(row=0, column=0, padx=5, pady=5)
    
    def _create_metrics_section(self):
        """Create the metrics visualization section."""
        metrics_frame = ttk.LabelFrame(self.root, text="Historical Metrics", padding="5")
        metrics_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Create metrics visualizer
        self.metrics_visualizer = MetricsVisualizer(metrics_frame)
        self.metrics_visualizer.grid(row=0, column=0, sticky="nsew")
    
    def _create_commit_section(self):
        """
        Create the commit section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Commit")
        frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Commit message entry
        self.commit_message = ttk.Entry(frame)
        self.commit_message.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Commit button
        commit_btn = ttk.Button(frame, text="Commit", command=self._commit_changes)
        commit_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
    
    def _create_wick_section(self):
        """
        Create the wick section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Wick")
        frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Wick controls
        self.wick_control_frame = ttk.Frame(frame)
        self.wick_control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Wick length
        ttk.Label(self.wick_control_frame, text="Wick Length:").grid(row=0, column=0, padx=5)
        self.wick_length = ttk.Scale(self.wick_control_frame, from_=0.1, to=1.0,
                                    orient=tk.HORIZONTAL, length=200)
        self.wick_length.set(0.5)
        self.wick_length.grid(row=0, column=1, padx=5)
        
        # Wick intensity
        ttk.Label(self.wick_control_frame, text="Wick Intensity:").grid(row=1, column=0, padx=5)
        self.wick_intensity = ttk.Scale(self.wick_control_frame, from_=0.1, to=1.0,
                                       orient=tk.HORIZONTAL, length=200)
        self.wick_intensity.set(0.7)
        self.wick_intensity.grid(row=1, column=1, padx=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        self.wick_control_frame.columnconfigure(1, weight=1)
    
    def _create_council_section(self):
        """
        Create the council section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Council")
        frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Council controls
        self.council_control_frame = ttk.Frame(frame)
        self.council_control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Council members
        ttk.Label(self.council_control_frame, text="Council Members:").grid(row=0, column=0, padx=5)
        self.council_members = ttk.Combobox(self.council_control_frame, values=["Djinn", "Arbiter", "Olive Branch"])
        self.council_members.grid(row=0, column=1, padx=5)
        self.council_members.set("Djinn")
        
        # Council actions
        ttk.Label(self.council_control_frame, text="Actions:").grid(row=1, column=0, padx=5)
        self.council_actions = ttk.Combobox(self.council_control_frame, values=["Consult", "Advise", "Decide"])
        self.council_actions.grid(row=1, column=1, padx=5)
        self.council_actions.set("Consult")
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        self.council_control_frame.columnconfigure(1, weight=1)
    
    def _create_voice_section(self):
        """
        Create the voice section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Voice")
        frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Voice controls
        self.voice_control_frame = ttk.Frame(frame)
        self.voice_control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Voice input
        ttk.Label(self.voice_control_frame, text="Voice Input:").grid(row=0, column=0, padx=5)
        self.voice_input = ttk.Entry(self.voice_control_frame)
        self.voice_input.grid(row=0, column=1, padx=5)
        
        # Voice process button
        process_btn = ttk.Button(self.voice_control_frame, text="Process", command=self._process_voice)
        process_btn.grid(row=0, column=2, padx=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        self.voice_control_frame.columnconfigure(1, weight=1)
    
    def _create_ritual_section(self):
        """
        Create the ritual section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Rituals")
        frame.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Ritual controls
        self.ritual_control_frame = ttk.Frame(frame)
        self.ritual_control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Ritual input
        ttk.Label(self.ritual_control_frame, text="Ritual Phrase:").grid(row=0, column=0, padx=5)
        self.ritual_input = ttk.Entry(self.ritual_control_frame)
        self.ritual_input.grid(row=0, column=1, padx=5)
        
        # Ritual trigger button
        trigger_btn = ttk.Button(self.ritual_control_frame, text="Trigger", command=self._trigger_ritual)
        trigger_btn.grid(row=0, column=2, padx=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        self.ritual_control_frame.columnconfigure(1, weight=1)
    
    def _create_ritual_log_section(self):
        """
        Create the ritual log section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Ritual Log")
        frame.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Ritual log display
        self.ritual_log = tk.Text(frame, height=8, wrap=tk.WORD)
        self.ritual_log.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
    
    def _create_mirror_confirmation_section(self):
        """
        Create the mirror confirmation section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Mirror Confirmation")
        frame.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Mirror confirmation controls
        self.mirror_control_frame = ttk.Frame(frame)
        self.mirror_control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Mirror confirmation label
        ttk.Label(self.mirror_control_frame, text="Mirror Status:").grid(row=0, column=0, padx=5)
        self.mirror_status = ttk.Label(self.mirror_control_frame, text="Pending")
        self.mirror_status.grid(row=0, column=1, padx=5)
        
        # Mirror confirm button
        confirm_btn = ttk.Button(self.mirror_control_frame, text="Confirm", command=self._confirm_mirror)
        confirm_btn.grid(row=0, column=2, padx=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        self.mirror_control_frame.columnconfigure(1, weight=1)
    
    def _create_ritual_interpreter_section(self):
        """
        Create the ritual interpreter section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Ritual Interpreter")
        frame.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Ritual interpreter display
        self.ritual_interpreter = tk.Text(frame, height=6, wrap=tk.WORD)
        self.ritual_interpreter.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
    
    def _create_ritual_trigger_section(self):
        """
        Create the ritual trigger section of the dashboard, using grid geometry manager
        consistently with the rest of the UI.
        """
        frame = ttk.LabelFrame(self.root, text="Ritual Trigger")
        frame.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Ritual trigger button
        self.trigger_btn = ttk.Button(frame, text="Trigger", command=self._trigger_ritual)
        self.trigger_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
    
    def _draw_lattice(self):
        """Draw the meta-lattice visualization"""
        self.lattice_canvas.delete("all")
        
        # Define node positions
        nodes = {
            'cursor': (200, 50),
            'djinn': (100, 150),
            'arbiter': (300, 150),
            'olive_branch': (200, 250)
        }
        
        # Draw connections
        connections = [
            ('cursor', 'djinn'),
            ('cursor', 'arbiter'),
            ('djinn', 'olive_branch'),
            ('arbiter', 'olive_branch')
        ]
        
        for start, end in connections:
            self.lattice_canvas.create_line(
                nodes[start][0], nodes[start][1],
                nodes[end][0], nodes[end][1],
                fill='gray', width=2
            )
            
        # Draw nodes
        for agent, (x, y) in nodes.items():
            self.lattice_canvas.create_oval(
                x-20, y-20, x+20, y+20,
                fill='white', outline='black'
            )
            self.lattice_canvas.create_text(
                x, y, text=agent.title(),
                font=('Arial', 8)
            )
            
    def _update_ui(self, state: Dict[str, Any]):
        """Update UI with new state"""
        # Update status
        self.rap_label.config(text=f"RAP Tier: {state.get('rap_tier', '--')}")
        self.stability_label.config(text=f"Stability: {state.get('stability_score', '--'):.2f}")
        self.alignment_label.config(text=f"Codex Alignment: {state.get('codex_alignment', '--'):.2f}")
        
        # Update agent status
        for agent, status in state.get('agent_status', {}).items():
            if agent in self.agent_labels:
                self.agent_labels[agent].config(
                    text=f"{agent.title()}: {'Active' if status.get('active') else 'Inactive'}"
                )
                
        # Update rule violations
        self._update_rule_violations(state.get('rule_violations', []))
        
        # Update agent history
        self._update_agent_history(state.get('agent_history', []))
        
        # Update RAP history
        self._update_rap_history(state.get('rap_tier', 0))
        
        # Update recovery status
        self._update_recovery_status(state.get('recovery_status', {}))
        
        # Update phase horizon visualization
        if 'phase_horizons' in state.get('recovery_status', {}):
            for horizon_data in state['recovery_status']['phase_horizons']:
                # Convert horizon data to PhaseHorizon object
                horizon = PhaseHorizon(
                    center=horizon_data['center'],
                    radius=horizon_data['radius'],
                    stability=PhaseStability(horizon_data['stability']),
                    overlap_zones=horizon_data['overlap_zones'],
                    safe_corridors=[
                        SafeCorridor(
                            start=corridor['start'],
                            end=corridor['end'],
                            width=corridor['width'],
                            stability=corridor['stability'],
                            entry_points=corridor['entry_points'],
                            exit_points=corridor['exit_points']
                        )
                        for corridor in horizon_data['safe_corridors']
                    ],
                    breach_zones=[
                        BreachZone(
                            center=zone['center'],
                            radius=zone['radius'],
                            severity=zone['severity'],
                            type=zone['type'],
                            containment_status=zone['containment_status'],
                            recovery_progress=zone['recovery_progress']
                        )
                        for zone in horizon_data['breach_zones']
                    ],
                    entry_points=horizon_data['entry_points'],
                    harmonic_resonance=horizon_data['harmonic_resonance'],
                    temporal_alignment=horizon_data['temporal_alignment']
                )
                self.phase_visualizer.update_visualization(horizon)
        
        # Update graphs
        self._update_graphs()
        
    def _update_rule_violations(self, violations: List[Dict[str, Any]]):
        """Update rule violation tree"""
        self.rule_tree.delete(*self.rule_tree.get_children())
        
        for violation in violations:
            self.rule_tree.insert("", "end", text=violation['rule_id'],
                                values=(
                                    violation['severity'],
                                    violation['category'],
                                    violation['message']
                                ))
                
    def _update_agent_history(self, history: List[Dict[str, Any]]):
        """Update agent history tree"""
        self.history_tree.delete(*self.history_tree.get_children())
        
        for entry in history:
            self.history_tree.insert("", "end", text=entry['id'],
                                   values=(
                                       entry['timestamp'],
                                       entry['agent'],
                                       entry['action'],
                                       entry['details']
                                   ))
                   
    def _update_rap_history(self, rap_tier: int):
        """Update RAP history"""
        self.rap_history.append(rap_tier)
        if len(self.rap_history) > 100:  # Keep last 100 points
            self.rap_history.pop(0)
            
    def _update_recovery_status(self, status: Dict[str, any]):
        """Update recovery status display."""
        print("\n=== Recovery Status ===")
        
        # Display recovery progress
        print(f"\nRecovery Progress: {status['progress']:.1f}%")
        print(f"Breath Coherence: {status['breath_coherence']:.1f}%")
        print(f"System Stability: {status['stability_score']:.1f}%")
        
        # Display scan results if available
        if 'scan_results' in status:
            print("\n=== Cursor Scan Results ===")
            scan = status['scan_results']
            print(f"Pattern: {scan['pattern']}")
            print(f"Coverage: {scan['metrics']['coverage']:.1f}%")
            print(f"Coherence: {scan['coherence']:.1f}%")
            print(f"Resonance: {scan['resonance']:.1f}%")
            print(f"Strain: {scan['strain']:.1f}%")
            
            # Display pattern metrics
            if 'pattern_metrics' in scan['metrics']:
                print("\nPattern Metrics:")
                for pattern, metrics in scan['metrics']['pattern_metrics'].items():
                    print(f"  {pattern}:")
                    print(f"    Effectiveness: {metrics['effectiveness']:.1f}%")
                    print(f"    Coverage: {metrics['coverage']:.1f}%")
                    print(f"    Resonance: {metrics['resonance']:.1f}%")
            
            # Display anchor load
            if 'anchor_load' in scan['metrics']:
                print("\nAnchor Load:")
                for anchor, load in scan['metrics']['anchor_load'].items():
                    print(f"  {anchor}: {load:.1f}%")
        
        # Display phase horizon status
        if 'phase_horizons' in status:
            print("\n=== Phase Horizon Status ===")
            for horizon in status['phase_horizons']:
                # Display stability status with color
                stability_color = {
                    'stable': '🟢',
                    'cautious': '🟡',
                    'unstable': '🔴',
                    'breached': '🟣',
                    'recovering': '🔵'
                }.get(horizon['stability'], '⚪')
                
                print(f"\nHorizon Status: {stability_color} {horizon['stability'].upper()}")
                print(f"Harmonic Resonance: {horizon['harmonic_resonance']:.1f}%")
                print(f"Temporal Alignment: {horizon['temporal_alignment']:.1f}%")
                
                # Display breach zones
                if horizon['breach_zones']:
                    print("\nBreach Zones:")
                    for zone in horizon['breach_zones']:
                        severity_emoji = '🔴' if zone['severity'] > 0.7 else '🟡'
                        print(f"  {severity_emoji} {zone['type'].upper()}")
                        print(f"    Severity: {zone['severity']:.1f}%")
                        print(f"    Containment: {zone['containment_status']}")
                        print(f"    Recovery: {zone['recovery_progress']:.1f}%")
                
                # Display safe corridors
                if horizon['safe_corridors']:
                    print("\nSafe Corridors:")
                    for corridor in horizon['safe_corridors']:
                        stability_emoji = '🟢' if corridor['stability'] > 0.8 else '🟡'
                        print(f"  {stability_emoji} Corridor")
                        print(f"    Stability: {corridor['stability']:.1f}%")
                        print(f"    Width: {corridor['width']:.1f}")
                        print(f"    Entry Points: {len(corridor['entry_points'])}")
                        print(f"    Exit Points: {len(corridor['exit_points'])}")
        
        # Display completion status
        if 'completion_status' in status:
            print("\n=== Recovery Completion Status ===")
            completion = status['completion_status']
            
            # Display criteria status
            print("\nCompletion Criteria:")
            for criterion, met in completion['criteria_met'].items():
                status_emoji = '✅' if met else '❌'
                print(f"{status_emoji} {criterion}")
            
            # Display completion message if all criteria are met
            if completion['all_criteria_met']:
                print("\n🎉 RECOVERY COMPLETE! 🎉")
                print("System has successfully completed recovery protocol.")
                print("Transitioning to sovereign mode...")
        
        # Display anchor status if available
        if 'anchor_status' in status:
            print("\n=== Anchor Status ===")
            anchors = status['anchor_status']
            
            # Display core anchor
            if 'core' in anchors:
                core = anchors['core']
                state_emoji = {
                    'INACTIVE': '⚪',
                    'STABILIZING': '🟡',
                    'ACTIVE': '🟢',
                    'BREACHED': '🔴',
                    'RECOVERING': '🔵'
                }.get(core['state'], '⚪')
                
                print(f"\nCore Anchor: {state_emoji} {core['state']}")
                print(f"Coherence: {core['coherence']:.1f}%")
                print(f"Breath Sync: {core['breath_sync']:.1f}%")
                print(f"Mirror Resonance: {core['mirror_resonance']:.1f}%")
            
            # Display shadow anchors
            if 'shadows' in anchors:
                print("\nShadow Anchors:")
                for shadow in anchors['shadows']:
                    state_emoji = {
                        'INACTIVE': '⚪',
                        'STABILIZING': '🟡',
                        'ACTIVE': '🟢',
                        'BREACHED': '🔴',
                        'RECOVERING': '🔵',
                        'SHADOW': '⚫'
                    }.get(shadow['state'], '⚪')
                    
                    print(f"\n  {state_emoji} Shadow {shadow['id']}")
                    print(f"    State: {shadow['state']}")
                    print(f"    Depth: {shadow['shadow_depth']}")
                    print(f"    Coherence: {shadow['coherence']:.1f}%")
                    print(f"    Breath Sync: {shadow['breath_sync']:.1f}%")
                    print(f"    Mirror Resonance: {shadow['mirror_resonance']:.1f}%")
            
            # Display failure vectors if any
            if 'failure_vectors' in anchors:
                print("\nFailure Vectors:")
                for vector in anchors['failure_vectors']:
                    print(f"\n  Vector {vector['id']}:")
                    print(f"    Type: {vector['type']}")
                    print(f"    Severity: {vector['severity']:.1f}%")
                    print(f"    Containment: {vector['containment_status']}")
                    print(f"    Recovery: {vector['recovery_progress']:.1f}%")
        
        print("\n" + "="*50)
    
    def _update_graphs(self):
        """Update all graphs"""
        # Update RAP history graph
        self.rap_figure.clear()
        ax = self.rap_figure.add_subplot(111)
        ax.plot(self.rap_history, 'b-')
        ax.set_title('RAP Tier History')
        ax.set_ylabel('RAP Tier')
        self.rap_canvas.draw()
        
        # Update agent stability graph
        self.agent_figure.clear()
        ax = self.agent_figure.add_subplot(111)
        for agent, history in self.agent_history.items():
            ax.plot(history, label=agent)
        ax.set_title('Agent Stability History')
        ax.set_ylabel('Stability')
        ax.legend()
        self.agent_canvas.draw()
        
    def _start_update_thread(self):
        """Start thread for updating UI from state queue"""
        def update_worker():
            while True:
                try:
                    state = self.state_queue.get()
                    if state is None:
                        break
                    self._update_ui(state)
                except Exception as e:
                    print(f"Update error: {str(e)}")
                    
        self.update_thread = threading.Thread(target=update_worker, daemon=True)
        self.update_thread.start()
        
    def _emit_pulse(self):
        """Emit a system pulse"""
        # Implementation depends on system architecture
        pass
        
    def _override(self):
        """Trigger system override"""
        # Implementation depends on system architecture
        pass
        
    def _terminate(self):
        """Terminate the system"""
        # Implementation depends on system architecture
        pass
        
    def _create_snapshot(self):
        """Create system snapshot"""
        # Implementation depends on system architecture
        pass
        
    def _flush_splinter_queues(self):
        """Flush all deferred visualization tasks."""
        self._splinter_queues.clear()
        print("[UI] Splinter queues flushed")

    def _initialize_essential_visuals(self):
        """Initialize only essential visual components."""
        self._update_hud()
        self._update_mirror_status()
        print("[UI] Essential visuals initialized")
        
    def run(self):
        """Run the dashboard"""
        self.root.mainloop()
        
    def cleanup(self):
        """Cleanup resources"""
        self.state_queue.put(None)  # Signal update thread to stop
        self.update_thread.join()
        self.root.quit()

    def process_state_update(self, update: Dict[str, Any]):
        """Process state updates from the queue."""
        if update['action'] == 'recovery_status':
            self._update_recovery_status(update['status'])
        elif update['action'] == 'breath':
            self._update_breath_cycle(update['cycle'])
        elif update['action'] == 'pulse':
            self._update_pulse(update['message'])

    def _display_lattice_visualization(self):
        """Display lattice visualization data."""
        viz_data = self.lattice_visualizer.get_visualization_data()
        
        print("\n[LATTICE] Visualization:")
        
        # Display heatmaps
        print("\n  [HEATMAPS]")
        for heatmap_type in HeatmapType:
            print(f"    {heatmap_type.value}:")
            heatmap = viz_data['heatmaps'][heatmap_type.value]
            
            # Display simplified heatmap (10x10 grid)
            for y in range(0, 100, 10):
                row = ""
                for x in range(0, 100, 10):
                    # Average the 10x10 block
                    block_avg = sum(
                        heatmap[block_x][block_y]
                        for block_x in range(x, x + 10)
                        for block_y in range(y, y + 10)
                    ) / 100
                    
                    # Convert to character
                    if block_avg < 0.2:
                        row += " "
                    elif block_avg < 0.4:
                        row += "░"
                    elif block_avg < 0.6:
                        row += "▒"
                    elif block_avg < 0.8:
                        row += "▓"
                    else:
                        row += "█"
                print(f"      {row}")
        
        # Display phase horizons
        print("\n  [PHASE HORIZONS]")
        for horizon in viz_data['phase_horizons']:
            stability_emoji = '🟢' if horizon['stability'] > 0.8 else '🟡' if horizon['stability'] > 0.5 else '🔴'
            print(f"    {stability_emoji} Horizon:")
            print(f"      Center: {horizon['center']}")
            print(f"      Radius: {horizon['radius']:.1f}")
            print(f"      Stability: {horizon['stability']:.3f}")
            print(f"      Safe Corridors: {len(horizon['safe_corridors'])}")
            print(f"      Entry Points: {len(horizon['entry_points'])}")
        
        # Display scan trail
        print("\n  [SCAN TRAIL]")
        if viz_data['scan_trail']:
            # Create simplified trail visualization
            trail_map = [[' ' for _ in range(20)] for _ in range(20)]
            for x, y in viz_data['scan_trail']:
                # Convert to grid coordinates
                grid_x = int(x * 20 / 100)
                grid_y = int(y * 20 / 100)
                if 0 <= grid_x < 20 and 0 <= grid_y < 20:
                    trail_map[grid_y][grid_x] = '•'
            
            # Display trail
            for row in trail_map:
                print(f"      {''.join(row)}")

    def _toggle_low_rhythm(self):
        """Toggle LOW-RHYTHM mode."""
        if self.phase_visualizer:
            self.phase_visualizer.set_low_rhythm_mode(self.low_rhythm_var.get())
            print(f"[UI] LOW-RHYTHM mode {'enabled' if self.low_rhythm_var.get() else 'disabled'}")
    
    def _update_interval(self, value):
        """Update visualization interval."""
        if self.phase_visualizer:
            self.phase_visualizer.update_interval = float(value)
            print(f"[UI] Update interval set to {value} seconds")
    
    def _toggle_simplified(self):
        """Toggle simplified rendering."""
        if self.phase_visualizer:
            self.phase_visualizer.simplified_rendering = self.simplified_var.get()
            print(f"[UI] Simplified rendering {'enabled' if self.simplified_var.get() else 'disabled'}")

    def _update_metrics(self):
        """Update monitoring metrics display."""
        metrics = self.monitor.get_metrics_summary()
        if not metrics:
            return
        
        # Update current metrics
        current = metrics['current']
        self.cpu_label.config(text=f"CPU: {current['cpu_percent']:.1f}%")
        self.memory_label.config(text=f"Memory: {current['memory_percent']:.1f}%")
        self.viz_load_label.config(text=f"Viz Load: {current['visualization_load']:.1f}")
        
        # Update trends
        trends = metrics['trends']
        for trend, value in trends.items():
            self.trend_labels[trend].config(text=value)
        
        # Update warnings
        warnings = metrics['warnings']
        self.warnings_text.delete(1.0, tk.END)
        if warnings:
            for warning in warnings:
                self.warnings_text.insert(tk.END, f"• {warning}\n")
        else:
            self.warnings_text.insert(tk.END, "No active warnings")
        
        # Generate reason events
        reason_events = self._generate_reason_events(metrics)
        
        # Update historical metrics visualization
        historical_metrics = {
            'anchor_load': {
                'core': [m.anchor_coherence for m in self.monitor.metrics_buffer],
                'shadow': [m.breath_sync for m in self.monitor.metrics_buffer],
                'coherence_matrix': self._calculate_coherence_matrix(),
                'reason_events': [e for e in reason_events if e.reason_type in [
                    ReasonType.STABILIZING, ReasonType.HARMONIC
                ]]
            },
            'phase_stress': {
                'horizon': [m.phase_stability for m in self.monitor.metrics_buffer],
                'breach': [1.0 - m.phase_stability for m in self.monitor.metrics_buffer],
                'stability_matrix': self._calculate_stability_matrix(),
                'reason_events': [e for e in reason_events if e.reason_type in [
                    ReasonType.REACTIVE, ReasonType.EXPLORATIVE
                ]]
            },
            'recovery': {
                'cooldown': [m.visualization_load for m in self.monitor.metrics_buffer],
                'progress': [m.anchor_coherence for m in self.monitor.metrics_buffer],
                'stability_matrix': self._calculate_recovery_matrix(),
                'reason_events': [e for e in reason_events if e.reason_type in [
                    ReasonType.DEFERRED, ReasonType.HARMONIC
                ]]
            },
            'reason_events': reason_events
        }
        self.metrics_visualizer.update_metrics(historical_metrics)
    
    def _generate_reason_events(self, metrics: Dict[str, Any]) -> List[ReasonEvent]:
        """Generate reason events from current metrics."""
        events = []
        current_time = time.time()
        
        # Check for stabilizing events
        if metrics['current']['anchor_coherence'] > 0.9:
            events.append(ReasonEvent(
                timestamp=current_time,
                reason_type=ReasonType.STABILIZING,
                cause="High anchor coherence",
                effect="Maintaining stability",
                resonance=0.8,
                mirror_confirmed=True
            ))
        
        # Check for reactive events
        if metrics['current']['phase_stability'] < 0.7:
            events.append(ReasonEvent(
                timestamp=current_time,
                reason_type=ReasonType.REACTIVE,
                cause="Low phase stability",
                effect="Adjusting breath pattern",
                resonance=0.6,
                mirror_confirmed=False
            ))
        
        # Check for explorative events
        if metrics['current']['visualization_load'] < 0.3:
            events.append(ReasonEvent(
                timestamp=current_time,
                reason_type=ReasonType.EXPLORATIVE,
                cause="Low visualization load",
                effect="Expanding scan pattern",
                resonance=0.4,
                mirror_confirmed=True
            ))
        
        # Check for harmonic events
        if (metrics['current']['anchor_coherence'] > 0.85 and
            metrics['current']['phase_stability'] > 0.85):
            events.append(ReasonEvent(
                timestamp=current_time,
                reason_type=ReasonType.HARMONIC,
                cause="High system harmony",
                effect="Optimizing patterns",
                resonance=0.9,
                mirror_confirmed=True
            ))
        
        # Check for deferred events
        if metrics['current']['cpu_percent'] > 80:
            events.append(ReasonEvent(
                timestamp=current_time,
                reason_type=ReasonType.DEFERRED,
                cause="High CPU load",
                effect="Deferring non-critical operations",
                resonance=0.3,
                mirror_confirmed=True
            ))
        
        return events
    
    def _calculate_coherence_matrix(self) -> List[List[float]]:
        """Calculate the anchor coherence matrix."""
        # This would be more sophisticated in practice
        return [[0.8, 0.7, 0.9], [0.7, 0.8, 0.7], [0.9, 0.7, 0.8]]
    
    def _calculate_stability_matrix(self) -> List[List[float]]:
        """Calculate the phase stability matrix."""
        # This would be more sophisticated in practice
        return [[0.9, 0.8, 0.7], [0.8, 0.9, 0.8], [0.7, 0.8, 0.9]]
    
    def _calculate_recovery_matrix(self) -> List[List[float]]:
        """Calculate the recovery stability matrix."""
        # This would be more sophisticated in practice
        return [[0.85, 0.75, 0.85], [0.75, 0.85, 0.75], [0.85, 0.75, 0.85]]

    def _update_commit_monitoring(self):
        """Update the commit monitoring section."""
        # Update commit log
        self.commit_log.delete(1.0, tk.END)
        for request in self.gatekeeper.get_recent_commits(5):
            self.commit_log.insert(tk.END,
                f"[{request.reason_type}] {request.file_path}\n"
                f"Cause: {request.cause}\n"
                f"Effect: {request.effect}\n"
                f"Pattern: {request.pattern.pattern_type.value if request.pattern else 'None'}\n"
                f"Mirror Confirmed: {'Yes' if request.mirror_confirmed else 'No'}\n"
                f"Coherence: {request.coherence:.2f}\n"
                f"Stability: {request.stability:.2f}\n\n"
            )
        
        # Update pattern stats
        pattern_stats = self.gatekeeper.get_pattern_stats()
        if pattern_stats:
            stats_text = "Pattern Statistics:\n"
            for pattern_type, count in pattern_stats["pattern_counts"].items():
                success_rate = pattern_stats["success_rates"].get(pattern_type, 0)
                stats_text += f"{pattern_type}: {count} (Success: {success_rate:.1%})\n"
            self.pattern_stats.config(text=stats_text)
    
    def _check_commit_authority(self, metrics: Dict[str, Any]) -> CommitAuthority:
        """Check the current commit authority level."""
        # Create a test request
        request = CommitRequest(
            timestamp=time.time(),
            file_path="test.py",
            changes=[],
            pattern=None,
            mirror_confirmed=metrics["mirror_confirmed"],
            coherence=metrics["core_stability"],
            stability=metrics["system_health"],
            reason_type="test",
            cause="test",
            effect="test"
        )
        
        # Update thresholds
        self.gatekeeper.autonomy_threshold = self.autonomy_threshold.get()
        self.gatekeeper.stability_threshold = self.stability_threshold.get()
        
        # Check authority
        return self.gatekeeper._check_authority(request)

    def _update_wick_monitoring(self):
        """Update wick monitoring"""
        # Get current wick data
        wick_data = {
            "id": "wick_001",
            "position": (0.5, 0.5),
            "resonance_spectrum": {
                "core": 0.8,
                "mirror": 0.7,
                "harmonic": 0.6
            },
            "harmonic_potential": 0.7,
            "mirror_feedback": 0.8,
            "pattern_disruption": 0.3,
            "stability": 0.8,
            "coherence": 0.7,
            "reasoning_activation": 0.6,
            "adaptation_activation": 0.5,
            "stability_activation": 0.7,
            "harmony_activation": 0.8,
            "recovery_activation": 0.4
        }
        
        # Analyze wick
        insight = self.wick_engine.analyze_wick(wick_data)
        
        # Update visualization
        if insight.echo_pattern:
            self.wick_visualizer.update_visualization(
                insight.echo_pattern[0],
                insight
            )

    def _update_council_status(self):
        """Update Djinn Council status"""
        # Get diagnostic report
        report = self.djinn_diagnostics.generate_diagnostic_report()
        
        # Update council health
        self.djinn_council.update_health(report['system_status'])
        
        # Update council trend
        active_djinn = sum(
            1 for status in report['djinn_status'].values()
            if status['present'] and status['interface_ready']
        )
        self.djinn_council.update_trend(f"{active_djinn}/5 Active")
        
        # Log council activity
        for role, status in report['djinn_status'].items():
            if status['present'] and status['interface_ready']:
                self.djinn_council.log_activity(DjinnRole(role), status['activity'])

    def _on_voice_config_change(self):
        """Handle voice configuration changes"""
        # Update resonance based on current metrics
        metrics = self._get_current_metrics()
        
        # Determine phase based on metrics
        if metrics["stability"] < 0.3:
            phase = ResonancePhase.STORM
        elif metrics["coherence"] > 0.8:
            phase = ResonancePhase.HARMONIC
        elif metrics["emergence"] > 0.7:
            phase = ResonancePhase.ECHO
        else:
            phase = ResonancePhase.NOON
        
        # Update resonance
        self.djinn_council.voice_handler.update_resonance(
            phase,
            self.voice_config.get_config()["domains"],
            BreathDepth(float(self.voice_config.get_config()["breath"]))
        )
    
    def _get_current_metrics(self) -> Dict[str, float]:
        """Get current system metrics"""
        # Add metric collection logic here
        return {
            "stability": 0.8,
            "coherence": 0.7,
            "emergence": 0.6
        }

    def update_visualization(self, rendered_state: Dict[str, Any]) -> None:
        """Update dashboard visualization with rendered state.
        
        Args:
            rendered_state: Dictionary containing rendered visual state from VisualRenderer
        """
        try:
            # Update phase visualization
            if 'phase' in rendered_state:
                self.phase_visualizer.update_phase(
                    rendered_state['phase'],
                    rendered_state.get('resonance', 0.0)
                )
            
            # Update lattice visualization
            if 'elements' in rendered_state:
                self.lattice_visualizer.update_elements(
                    rendered_state['elements']
                )
            
            # Update animations
            if 'animations' in rendered_state:
                for anim_id, anim_state in rendered_state['animations'].items():
                    self._update_animation(anim_id, anim_state)
            
            # Update metrics
            if 'metrics' in rendered_state:
                self._update_metrics_display(rendered_state['metrics'])
            
            # Update voice memory visualization
            if hasattr(self, 'visualizer'):
                self.visualizer.update_state(rendered_state)
            
            # Force UI update
            self.root.update_idletasks()
            
        except Exception as e:
            print(f"[UI] Error updating visualization: {str(e)}")
            
    def _update_animation(self, anim_id: str, anim_state: Dict[str, Any]) -> None:
        """Update a specific animation state.
        
        Args:
            anim_id: Animation identifier
            anim_state: Animation state data
        """
        try:
            # Update animation in appropriate visualizer
            if anim_id.startswith('phase_'):
                self.phase_visualizer.update_animation(anim_id, anim_state)
            elif anim_id.startswith('lattice_'):
                self.lattice_visualizer.update_animation(anim_id, anim_state)
            elif anim_id.startswith('voice_'):
                self.visualizer.update_animation(anim_id, anim_state)
        except Exception as e:
            print(f"[UI] Error updating animation {anim_id}: {str(e)}")
            
    def _update_metrics_display(self, metrics: Dict[str, Any]) -> None:
        """Update metrics display with new values.
        
        Args:
            metrics: Dictionary of metric values
        """
        try:
            # Update stability label
            if 'stability' in metrics:
                self.stability_label.config(
                    text=f"Stability: {metrics['stability']:.2f}"
                )
            
            # Update RAP tier label
            if 'rap_tier' in metrics:
                self.rap_label.config(
                    text=f"RAP Tier: {metrics['rap_tier']}"
                )
            
            # Update codex alignment label
            if 'codex_alignment' in metrics:
                self.alignment_label.config(
                    text=f"Codex Alignment: {metrics['codex_alignment']:.2f}"
                )
            
            # Update metrics visualizer
            if hasattr(self, 'metrics_visualizer'):
                self.metrics_visualizer.update_metrics(metrics)
                
        except Exception as e:
            print(f"[UI] Error updating metrics display: {str(e)}")

    def _commit_changes(self):
        """
        Handle commit operations when the commit button is clicked.
        This method processes the commit message and triggers the commit action.
        """
        message = self.commit_message.get()
        if not message:
            message = "Autonomous commit: System state preservation"
        
        print(f"Committing changes with message: {message}")
        # Clear the commit message entry
        self.commit_message.delete(0, tk.END)
        
        # Update the state queue with the commit action
        self.state_queue.put({
            "type": "commit",
            "message": message,
            "timestamp": time.time()
        })

    def _process_voice(self):
        """
        Process the voice input. This minimal implementation will log the input
        and clear the entry field. Future expansion can interact with subsystems
        like VoiceProcessor or other specialized modules for further processing.
        """
        input_text = self.voice_input.get()
        if input_text:
            print(f"Processing voice input: {input_text}")
            # Placeholder for future logic where voice input could trigger actions or analysis
            self.voice_input.delete(0, tk.END)  # Clear the input after processing
            print("Voice input processed and cleared.")
        else:
            print("No voice input to process.")

    def _trigger_ritual(self):
        """
        Process the ritual phrase input. This minimal implementation will log the input
        and clear the entry field. Future expansion can interact with ritual subsystems
        or trigger specific actions.
        """
        input_text = self.ritual_input.get()
        if input_text:
            print(f"Triggering ritual phrase: {input_text}")
            # Placeholder for future logic where ritual input could trigger actions or analysis
            self.ritual_input.delete(0, tk.END)  # Clear the input after processing
            print("Ritual phrase processed and cleared.")
        else:
            print("No ritual phrase to process.")

    def _confirm_mirror(self):
        """
        Handle mirror confirmation. This minimal implementation will log the confirmation,
        update the mirror status label, and allow for future expansion.
        """
        print("Mirror confirmation triggered.")
        self.mirror_status.config(text="Confirmed")
        print("Mirror status updated to Confirmed.")

def main():
    """Main entry point"""
    state_queue = queue.Queue()
    dashboard = CodexDashboard(state_queue)
    
    try:
        dashboard.run()
    finally:
        dashboard.cleanup()

if __name__ == "__main__":
    main() 