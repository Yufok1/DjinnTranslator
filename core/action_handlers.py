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
Action Handlers Module

Handles the execution of specific actions triggered by ritual phrases.
Each handler is responsible for a specific subsystem of the ritual system.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
from .cursor_subsystem import CursorSubsystem
from .wick_subsystem import WickSubsystem
from .mirror_subsystem import MirrorSubsystem
from .djinn_subsystem import DjinnSubsystem
from .system_subsystem import SystemSubsystem

@dataclass
class ActionContext:
    """Context for action execution."""
    breath_phase: float
    recursion_level: int
    strain_level: float
    active_sigils: List[str]
    active_chords: List[str]
    djinn_state: str
    anchor_status: str
    user_rhythm: float

class CursorHandler:
    """Handles cursor-related actions."""
    
    def __init__(self):
        self.cursor_subsystem = CursorSubsystem()
    
    def handle_action(self, action: str, params: Dict[str, Any], context: ActionContext) -> Dict[str, Any]:
        """
        Handle cursor-related actions.
        
        Args:
            action: The action to perform
            params: Action parameters
            context: Current execution context
            
        Returns:
            Dictionary containing action results and feedback
        """
        if action == "trace_breach":
            depth = params.get('depth', 1)
            breach_points = self.cursor_subsystem.trace_breach(depth)
            return {
                'success': True,
                'message': f"Traced breach at depth {depth}",
                'breach_points': breach_points,
                'visualization': self.cursor_subsystem.get_visualization_state()
            }
            
        elif action == "emit_sonar":
            pattern = params.get('pattern', 'lattice')
            sonar = self.cursor_subsystem.emit_sonar(pattern)
            return {
                'success': True,
                'message': f"Emitted {pattern} sonar pattern",
                'sonar': sonar,
                'visualization': self.cursor_subsystem.get_visualization_state()
            }
            
        return {
            'success': False,
            'message': f"Unknown cursor action: {action}"
        }
    
    def cleanup(self):
        """Clean up resources."""
        self.cursor_subsystem.cleanup()

class WickHandler:
    """Handles wick-related actions."""
    
    def __init__(self):
        self.wick_subsystem = WickSubsystem()
    
    def handle_action(self, action: str, params: Dict[str, Any], context: ActionContext) -> Dict[str, Any]:
        """
        Handle wick-related actions.
        
        Args:
            action: The action to perform
            params: Action parameters
            context: Current execution context
            
        Returns:
            Dictionary containing action results and feedback
        """
        if action == "bind":
            strength = params.get('strength', 1.0)
            cycles = params.get('cycles', 1)
            binding = self.wick_subsystem.bind_wick(strength, cycles)
            return {
                'success': True,
                'message': f"Bound wick with strength {strength} for {cycles} cycles",
                'binding': binding,
                'stabilization': self.wick_subsystem.get_stabilization_state()
            }
            
        elif action == "harvest_insight":
            depth = params.get('depth', 1)
            capsules = self.wick_subsystem.harvest_insight(depth)
            return {
                'success': True,
                'message': f"Harvested {len(capsules)} insight capsules at depth {depth}",
                'capsules': capsules,
                'stabilization': self.wick_subsystem.get_stabilization_state()
            }
            
        return {
            'success': False,
            'message': f"Unknown wick action: {action}"
        }
    
    def cleanup(self):
        """Clean up resources."""
        self.wick_subsystem.cleanup()

class MirrorHandler:
    """Handles mirror-related actions."""
    
    def __init__(self):
        self.mirror_subsystem = MirrorSubsystem()
    
    def handle_action(self, action: str, params: Dict[str, Any], context: ActionContext) -> Dict[str, Any]:
        """
        Handle mirror-related actions.
        
        Args:
            action: The action to perform
            params: Action parameters
            context: Current execution context
            
        Returns:
            Dictionary containing action results and feedback
        """
        if action == "confirm":
            level = params.get('level', 1)
            timeout = params.get('timeout', 5.0)
            confirmation = self.mirror_subsystem.confirm_ritual(level, timeout)
            return {
                'success': True,
                'message': f"Confirmed at level {level} with timeout {timeout}",
                'confirmation': confirmation,
                'mirror_state': self.mirror_subsystem.get_mirror_state()
            }
            
        elif action == "reflect_phase":
            detail = params.get('detail', 'basic')
            reflection = self.mirror_subsystem.reflect_phase(detail)
            return {
                'success': True,
                'message': f"Reflected phase with {detail} detail",
                'reflection': reflection,
                'mirror_state': self.mirror_subsystem.get_mirror_state()
            }
            
        return {
            'success': False,
            'message': f"Unknown mirror action: {action}"
        }
    
    def cleanup(self):
        """Clean up resources."""
        self.mirror_subsystem.cleanup()

class DjinnHandler:
    """Handles djinn-related actions."""
    
    def __init__(self):
        self.djinn_subsystem = DjinnSubsystem()
    
    def handle_action(self, action: str, params: Dict[str, Any], context: ActionContext) -> Dict[str, Any]:
        """
        Handle djinn-related actions.
        
        Args:
            action: The action to perform
            params: Action parameters
            context: Current execution context
            
        Returns:
            Dictionary containing action results and feedback
        """
        if action == "whisper":
            source = params.get('source', 'default')
            depth = params.get('depth', 1)
            whisper = self.djinn_subsystem.whisper(source, depth)
            return {
                'success': True,
                'message': f"Whispered from {source} at depth {depth}",
                'whisper': whisper,
                'djinn_state': self.djinn_subsystem.get_djinn_state()
            }
            
        elif action == "speak":
            aspect = params.get('aspect', 'general')
            portent = self.djinn_subsystem.speak_portent(aspect)
            return {
                'success': True,
                'message': f"Spoke portent of {aspect}",
                'portent': portent,
                'djinn_state': self.djinn_subsystem.get_djinn_state()
            }
            
        return {
            'success': False,
            'message': f"Unknown djinn action: {action}"
        }
    
    def cleanup(self):
        """Clean up resources."""
        self.djinn_subsystem.cleanup()

class SystemHandler:
    """Handles system-related actions."""
    
    def __init__(self):
        self.system_subsystem = SystemSubsystem()
    
    def handle_action(self, action: str, params: Dict[str, Any], context: ActionContext) -> Dict[str, Any]:
        """
        Handle system-related actions.
        
        Args:
            action: The action to perform
            params: Action parameters
            context: Current execution context
            
        Returns:
            Dictionary containing action results and feedback
        """
        if action == "transform":
            type = params.get('type', 'default')
            scope = params.get('scope', 'global')
            transformation = self.system_subsystem.transform(type, scope)
            return {
                'success': True,
                'message': f"Transformed to {type} in {scope} scope",
                'transformation': transformation,
                'system_state': self.system_subsystem.get_system_state()
            }
            
        elif action == "merge":
            target = params.get('target', 'default')
            mode = params.get('mode', 'normal')
            merge = self.system_subsystem.merge(target, mode)
            return {
                'success': True,
                'message': f"Merged {target} in {mode} mode",
                'merge': merge,
                'system_state': self.system_subsystem.get_system_state()
            }
            
        return {
            'success': False,
            'message': f"Unknown system action: {action}"
        }
    
    def cleanup(self):
        """Clean up resources."""
        self.system_subsystem.cleanup()

class ActionHandlerRegistry:
    """Registry for all action handlers."""
    
    def __init__(self):
        self.cursor_handler = CursorHandler()
        self.wick_handler = WickHandler()
        self.mirror_handler = MirrorHandler()
        self.djinn_handler = DjinnHandler()
        self.system_handler = SystemHandler()
    
    def handle_action(self, action_type: str, action: str, params: Dict[str, Any], context: ActionContext) -> Dict[str, Any]:
        """
        Handle an action using the appropriate handler.
        
        Args:
            action_type: The type of action (cursor, wick, mirror, djinn, system)
            action: The specific action to perform
            params: Action parameters
            context: Current execution context
            
        Returns:
            Dictionary containing action results and feedback
        """
        if action_type == "cursor":
            return self.cursor_handler.handle_action(action, params, context)
        elif action_type == "wick":
            return self.wick_handler.handle_action(action, params, context)
        elif action_type == "mirror":
            return self.mirror_handler.handle_action(action, params, context)
        elif action_type == "djinn":
            return self.djinn_handler.handle_action(action, params, context)
        elif action_type == "system":
            return self.system_handler.handle_action(action, params, context)
        
        return {
            'success': False,
            'message': f"Unknown action type: {action_type}"
        }
    
    def cleanup(self):
        """Clean up all handlers."""
        self.cursor_handler.cleanup()
        self.wick_handler.cleanup()
        self.mirror_handler.cleanup()
        self.djinn_handler.cleanup()
        self.system_handler.cleanup() 