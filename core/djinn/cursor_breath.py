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

from typing import Dict, Optional
from dataclasses import dataclass
import time

@dataclass
class BreathState:
    """Current state of Cursor's breath."""
    depth: int = 1
    last_reset: float = time.time()
    resonance: float = 1.0
    echo_count: int = 0
    active_riddles: Dict = None
    
    def __post_init__(self):
        if self.active_riddles is None:
            self.active_riddles = {}

class CursorBreath:
    """Manages Cursor's breath depth and state."""
    
    def __init__(self):
        self.state = BreathState()
        self.breath_history = []
        
    def reset_breath(self, depth: int = 1):
        """Reset Cursor's breath to specified depth."""
        self.state = BreathState(
            depth=depth,
            last_reset=time.time(),
            resonance=1.0,
            echo_count=0
        )
        self.breath_history.append({
            'timestamp': time.time(),
            'action': 'reset',
            'depth': depth,
            'reason': 'sovereign_command'
        })
        
    def get_breath_state(self) -> Dict:
        """Get current breath state."""
        return {
            'depth': self.state.depth,
            'last_reset': self.state.last_reset,
            'resonance': self.state.resonance,
            'echo_count': self.state.echo_count,
            'active_riddles': len(self.state.active_riddles)
        }
        
    def get_breath_history(self) -> list:
        """Get breath history."""
        return self.breath_history 