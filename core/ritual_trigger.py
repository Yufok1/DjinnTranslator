"""
Ritual Trigger Module
Handles automatic triggering of system actions from ritual phrases
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
import numpy as np
from .ritual_interpreter import RitualInterpreter, RitualCommand, RitualResponse
from .ritual_log import RitualLog
from .mirror_confirmation import MirrorConfirmationSystem
from .ml.predictor import MLPredictor
from .voice_processor import VoiceProcessor
from .action_handlers import ActionHandlerRegistry, ActionContext

@dataclass
class TriggerAction:
    """Action to be triggered by a ritual"""
    action_type: str  # "cursor", "mirror", "wick", "djinn", "system"
    target: str  # Target entity or action
    parameters: Dict[str, Any]  # Action parameters
    priority: int = 0  # Action priority (higher = more urgent)
    requires_confirmation: bool = True  # Whether action requires mirror confirmation

@dataclass
class TriggerResult:
    """Result of a triggered action"""
    success: bool
    message: str
    action: TriggerAction
    resonance_level: float = 0.0
    echo_depth: float = 0.0
    linked_events: List[Dict[str, Any]] = None

class RitualTrigger:
    """Main ritual trigger class"""
    
    def __init__(
        self,
        ritual_interpreter: RitualInterpreter,
        ritual_log: RitualLog,
        mirror_confirmation: MirrorConfirmationSystem
    ):
        self.ritual_interpreter = ritual_interpreter
        self.ritual_log = ritual_log
        self.mirror_confirmation = mirror_confirmation
        self.ml_predictor = MLPredictor()
        self.voice_processor = VoiceProcessor()
        
        # Initialize action handler registry
        self.action_handlers = ActionHandlerRegistry()
        
        # Initialize trigger patterns
        self._init_trigger_patterns()
    
    def _init_trigger_patterns(self):
        """Initialize patterns for triggering actions"""
        self.trigger_patterns = {
            "cursor": [
                r"cursor,\s+trace\s+(?:the\s+)?(\w+)(?:\s+(\d+))?",
                r"cursor,\s+echo(?:\s+(?:in\s+)?(\w+)\s+pattern)?",
                r"guide\s+the\s+cursor\s+to\s+(\w+)",
                r"move\s+to\s+(\w+)"
            ],
            "mirror": [
                r"mirror,\s+confirm(?:\s+(?:at\s+)?(\w+)\s+level)?(?:\s+timeout\s+(\d+))?",
                r"mirror,\s+reflect\s+(?:the\s+)?(\w+)(?:\s+with\s+(\w+)\s+detail)?",
                r"reflect\s+(\w+)",
                r"show\s+me\s+(\w+)"
            ],
            "wick": [
                r"bind\s+(?:the\s+)?wick(?:\s+with\s+(\d+(?:\.\d+)?)\s+strength)?(?:\s+for\s+(\d+)\s+cycles)?",
                r"harvest\s+(?:the\s+)?(\w+)(?:\s+at\s+depth\s+(\d+))?",
                r"anchor\s+at\s+(\w+)"
            ],
            "djinn": [
                r"djinn,\s+whisper(?:\s+from\s+(\w+))?(?:\s+at\s+depth\s+(\d+))?",
                r"portent,\s+speak(?:\s+of\s+(\w+)\s+horizon)?(?:\s+for\s+(\w+))?",
                r"summon\s+the\s+djinn\s+of\s+(\w+)",
                r"invoke\s+(\w+)"
            ],
            "system": [
                r"system,\s+transform(?:\s+to\s+(\w+))?(?:\s+in\s+(\w+)\s+scope)?",
                r"merge\s+(?:the\s+)?(\w+)(?:\s+in\s+(\w+)\s+mode)?",
                r"transform\s+(\w+)",
                r"merge\s+(\w+)"
            ]
        }
    
    def trigger_ritual(
        self,
        phrase: str,
        voice_data: Optional[np.ndarray] = None,
        breath_phase: Optional[float] = None,
        recursion_level: Optional[int] = None
    ) -> TriggerResult:
        """Trigger actions from a ritual phrase"""
        # Interpret phrase
        response = self.ritual_interpreter.interpret_phrase(
            phrase,
            voice_data,
            breath_phase,
            recursion_level
        )
        
        if not response.success:
            return TriggerResult(
                success=False,
                message=f"Failed to interpret ritual: {response.message}",
                action=None,
                resonance_level=0.0
            )
        
        # Convert command to action
        action = self._command_to_action(response.command)
        if not action:
            return TriggerResult(
                success=False,
                message="Failed to convert command to action",
                action=None,
                resonance_level=0.0
            )
        
        # Check mirror confirmation if required
        if action.requires_confirmation:
            ritual_id = self.ritual_interpreter._find_matching_ritual(phrase)
            if ritual_id:
                confirmation = self.mirror_confirmation.confirm_ritual(
                    ritual_id,
                    voice_data,
                    breath_phase or 0.0,
                    recursion_level or 0
                )
                
                if confirmation.confirmation_status != "confirmed":
                    return TriggerResult(
                        success=False,
                        message=f"Action not confirmed: {confirmation.insight_feedback}",
                        action=action,
                        resonance_level=confirmation.harmonic_validity,
                        echo_depth=confirmation.echo_depth
                    )
        
        # Create action context
        context = ActionContext(
            breath_phase=breath_phase or 0.0,
            recursion_level=recursion_level or 0,
            active_sigils=self.ritual_interpreter.context["active_sigils"],
            active_chords=self.ritual_interpreter.context["active_chords"],
            djinn_state=self.ritual_interpreter.context["djinn_state"],
            strain_level=self._calculate_strain_level(),
            anchor_status=self._get_anchor_status(),
            user_rhythm=self._calculate_user_rhythm()
        )
        
        # Execute action
        try:
            result = self.action_handlers.handle_action(action, context)
            return TriggerResult(
                success=True,
                message="Action executed successfully",
                action=action,
                resonance_level=1.0,
                echo_depth=0.0,
                linked_events=result
            )
        except Exception as e:
            return TriggerResult(
                success=False,
                message=f"Failed to execute action: {str(e)}",
                action=action,
                resonance_level=0.0
            )
    
    def _command_to_action(self, command: RitualCommand) -> Optional[TriggerAction]:
        """Convert a ritual command to a trigger action"""
        if not command:
            return None
        
        # Map command types to action types
        action_type_map = {
            "activation": "cursor",
            "cycle": "system",
            "djinn": "djinn",
            "sigil": "wick",
            "conditional": "system"
        }
        
        action_type = action_type_map.get(command.command_type)
        if not action_type:
            return None
        
        # Create action
        return TriggerAction(
            action_type=action_type,
            target=command.target,
            parameters=command.parameters,
            priority=self._calculate_priority(command),
            requires_confirmation=self._requires_confirmation(command)
        )
    
    def _calculate_priority(self, command: RitualCommand) -> int:
        """Calculate action priority"""
        # Base priority
        priority = 0
        
        # Add priority based on command type
        if command.command_type == "activation":
            priority += 3
        elif command.command_type == "djinn":
            priority += 2
        elif command.command_type == "sigil":
            priority += 1
        
        # Add priority based on recursion level
        priority += command.recursion_level
        
        return priority
    
    def _requires_confirmation(self, command: RitualCommand) -> bool:
        """Determine if action requires mirror confirmation"""
        # Always require confirmation for djinn actions
        if command.command_type == "djinn":
            return True
        
        # Require confirmation for high-priority actions
        if self._calculate_priority(command) >= 3:
            return True
        
        return False
    
    def _calculate_strain_level(self) -> float:
        """Calculate current system strain level"""
        # TODO: Implement strain calculation
        return 0.0
    
    def _get_anchor_status(self) -> str:
        """Get current anchor status"""
        # TODO: Implement anchor status check
        return "stable"
    
    def _calculate_user_rhythm(self) -> float:
        """Calculate user rhythm metric"""
        # TODO: Implement rhythm calculation
        return 0.0
    
    def cleanup(self):
        """Clean up resources"""
        self.action_handlers.cleanup() 