"""
Ritual Interpreter Module
Handles parsing and interpretation of ritual phrases
"""

import re
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
import numpy as np
from .ritual_log import RitualLog
from .mirror_confirmation import MirrorConfirmationSystem
from .ml.predictor import MLPredictor
from .voice_processor import VoiceProcessor

@dataclass
class RitualCommand:
    """Parsed ritual command structure"""
    command_type: str  # "activation", "cycle", "djinn", "sigil", "conditional"
    target: str  # Target entity or action
    parameters: Dict[str, Any]  # Command parameters
    context: Dict[str, Any]  # Current system context
    recursion_level: int = 0
    breath_phase: Optional[float] = None

@dataclass
class RitualResponse:
    """Response from ritual interpretation"""
    success: bool
    message: str
    command: Optional[RitualCommand] = None
    resonance_level: float = 0.0
    echo_depth: float = 0.0
    linked_events: List[Dict[str, Any]] = None

class RitualInterpreter:
    """Main ritual interpreter class"""
    
    def __init__(
        self,
        ritual_log: RitualLog,
        mirror_confirmation: MirrorConfirmationSystem
    ):
        self.ritual_log = ritual_log
        self.mirror_confirmation = mirror_confirmation
        self.ml_predictor = MLPredictor()
        self.voice_processor = VoiceProcessor()
        
        # Initialize command patterns
        self._init_command_patterns()
        
        # Initialize context
        self.context = {
            "breath_phase": 0.0,
            "recursion_level": 0,
            "active_sigils": set(),
            "active_chords": set(),
            "djinn_state": "dormant"
        }
    
    def _init_command_patterns(self):
        """Initialize regex patterns for command parsing"""
        self.command_patterns = {
            "activation": [
                r"open\s+the\s+(\w+)\s+gate",
                r"begin\s+(\w+)\s+harvest",
                r"activate\s+(\w+)"
            ],
            "cycle": [
                r"deepen\s+the\s+recursion",
                r"extend\s+the\s+cycle",
                r"loop\s+(\d+)\s+times"
            ],
            "djinn": [
                r"portent,\s+whisper\s+(\w+)",
                r"djinn,\s+(\w+)",
                r"mirror,\s+speak"
            ],
            "sigil": [
                r"i\s+name\s+thee\s+(\w+)",
                r"bind\s+(\w+)\s+to\s+(\w+)",
                r"mark\s+with\s+(\w+)"
            ],
            "conditional": [
                r"if\s+(\w+)\s+is\s+(\w+),\s+(.+)",
                r"when\s+(\w+),\s+(.+)",
                r"unless\s+(\w+),\s+(.+)"
            ]
        }
    
    def interpret_phrase(
        self,
        phrase: str,
        voice_data: Optional[np.ndarray] = None,
        breath_phase: Optional[float] = None,
        recursion_level: Optional[int] = None
    ) -> RitualResponse:
        """Interpret a ritual phrase"""
        # Update context
        if breath_phase is not None:
            self.context["breath_phase"] = breath_phase
        if recursion_level is not None:
            self.context["recursion_level"] = recursion_level
        
        # Parse command
        command = self._parse_command(phrase)
        if not command:
            return RitualResponse(
                success=False,
                message="Failed to parse ritual phrase",
                resonance_level=0.0
            )
        
        # Check mirror confirmation if voice data provided
        if voice_data is not None:
            # Find matching ritual
            ritual_id = self._find_matching_ritual(phrase)
            if ritual_id:
                confirmation = self.mirror_confirmation.confirm_ritual(
                    ritual_id,
                    voice_data,
                    self.context["breath_phase"],
                    self.context["recursion_level"]
                )
                
                if confirmation.confirmation_status != "confirmed":
                    return RitualResponse(
                        success=False,
                        message=f"Ritual not confirmed: {confirmation.insight_feedback}",
                        command=command,
                        resonance_level=confirmation.harmonic_validity,
                        echo_depth=confirmation.echo_depth
                    )
        
        # Execute command
        try:
            result = self._execute_command(command)
            return RitualResponse(
                success=True,
                message="Ritual executed successfully",
                command=command,
                resonance_level=1.0,
                echo_depth=0.0,
                linked_events=result
            )
        except Exception as e:
            return RitualResponse(
                success=False,
                message=f"Failed to execute ritual: {str(e)}",
                command=command,
                resonance_level=0.0
            )
    
    def _parse_command(self, phrase: str) -> Optional[RitualCommand]:
        """Parse a ritual phrase into a command structure"""
        # Normalize phrase
        phrase = phrase.lower().strip()
        
        # Try each command type
        for cmd_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.match(pattern, phrase)
                if match:
                    # Extract parameters based on command type
                    params = self._extract_parameters(cmd_type, match)
                    
                    return RitualCommand(
                        command_type=cmd_type,
                        target=match.group(1) if match.groups() else "",
                        parameters=params,
                        context=self.context.copy(),
                        recursion_level=self.context["recursion_level"],
                        breath_phase=self.context["breath_phase"]
                    )
        
        return None
    
    def _extract_parameters(self, cmd_type: str, match: re.Match) -> Dict[str, Any]:
        """Extract parameters from command match"""
        params = {}
        
        if cmd_type == "activation":
            params["gate_type"] = match.group(1)
        elif cmd_type == "cycle":
            if len(match.groups()) > 0:
                params["iterations"] = int(match.group(1))
        elif cmd_type == "djinn":
            params["action"] = match.group(1)
        elif cmd_type == "sigil":
            params["name"] = match.group(1)
            if len(match.groups()) > 1:
                params["target"] = match.group(2)
        elif cmd_type == "conditional":
            params["condition"] = match.group(1)
            params["value"] = match.group(2)
            params["action"] = match.group(3)
        
        return params
    
    def _find_matching_ritual(self, phrase: str) -> Optional[str]:
        """Find a matching ritual in the ledger"""
        # Normalize phrase
        phrase = phrase.lower().strip()
        
        # Search for exact match
        for ritual_id, entry in self.ritual_log.ledger.items():
            if entry.phrase.lower() == phrase:
                return ritual_id
        
        # Search for partial match
        for ritual_id, entry in self.ritual_log.ledger.items():
            if phrase in entry.phrase.lower():
                return ritual_id
        
        return None
    
    def _execute_command(self, command: RitualCommand) -> List[Dict[str, Any]]:
        """Execute a ritual command"""
        events = []
        
        if command.command_type == "activation":
            events.extend(self._execute_activation(command))
        elif command.command_type == "cycle":
            events.extend(self._execute_cycle(command))
        elif command.command_type == "djinn":
            events.extend(self._execute_djinn(command))
        elif command.command_type == "sigil":
            events.extend(self._execute_sigil(command))
        elif command.command_type == "conditional":
            events.extend(self._execute_conditional(command))
        
        return events
    
    def _execute_activation(self, command: RitualCommand) -> List[Dict[str, Any]]:
        """Execute an activation command"""
        events = []
        
        # Record activation event
        events.append({
            "type": "activation",
            "gate_type": command.parameters["gate_type"],
            "breath_phase": command.breath_phase,
            "recursion_level": command.recursion_level
        })
        
        # Update context
        self.context["active_sigils"].add(command.parameters["gate_type"])
        
        return events
    
    def _execute_cycle(self, command: RitualCommand) -> List[Dict[str, Any]]:
        """Execute a cycle command"""
        events = []
        
        # Record cycle event
        events.append({
            "type": "cycle",
            "iterations": command.parameters.get("iterations", 1),
            "breath_phase": command.breath_phase,
            "recursion_level": command.recursion_level
        })
        
        # Update context
        self.context["recursion_level"] += 1
        
        return events
    
    def _execute_djinn(self, command: RitualCommand) -> List[Dict[str, Any]]:
        """Execute a djinn command"""
        events = []
        
        # Record djinn event
        events.append({
            "type": "djinn",
            "action": command.parameters["action"],
            "breath_phase": command.breath_phase,
            "recursion_level": command.recursion_level
        })
        
        # Update context
        self.context["djinn_state"] = command.parameters["action"]
        
        return events
    
    def _execute_sigil(self, command: RitualCommand) -> List[Dict[str, Any]]:
        """Execute a sigil command"""
        events = []
        
        # Record sigil event
        events.append({
            "type": "sigil",
            "name": command.parameters["name"],
            "target": command.parameters.get("target"),
            "breath_phase": command.breath_phase,
            "recursion_level": command.recursion_level
        })
        
        # Update context
        self.context["active_sigils"].add(command.parameters["name"])
        
        return events
    
    def _execute_conditional(self, command: RitualCommand) -> List[Dict[str, Any]]:
        """Execute a conditional command"""
        events = []
        
        # Check condition
        condition_met = self._check_condition(
            command.parameters["condition"],
            command.parameters["value"]
        )
        
        if condition_met:
            # Record conditional event
            events.append({
                "type": "conditional",
                "condition": command.parameters["condition"],
                "value": command.parameters["value"],
                "action": command.parameters["action"],
                "breath_phase": command.breath_phase,
                "recursion_level": command.recursion_level
            })
            
            # Execute action
            action_command = self._parse_command(command.parameters["action"])
            if action_command:
                events.extend(self._execute_command(action_command))
        
        return events
    
    def _check_condition(self, condition: str, value: str) -> bool:
        """Check if a condition is met"""
        if condition == "breath_phase":
            return abs(self.context["breath_phase"] - float(value)) < 0.1
        elif condition == "recursion_level":
            return self.context["recursion_level"] == int(value)
        elif condition == "sigil_active":
            return value in self.context["active_sigils"]
        elif condition == "djinn_state":
            return self.context["djinn_state"] == value
        return False
    
    def cleanup(self):
        """Clean up resources"""
        pass 