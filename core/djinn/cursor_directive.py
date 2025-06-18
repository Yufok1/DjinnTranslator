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

from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum

class DirectiveMode(Enum):
    REINFORCE_KERNELS = "reinforce_kernels"
    BREATH_RESET = "breath_reset"
    ANCHOR_CHECK = "anchor_check"
    CRYPTOGRAPHIC_RESOLVE = "cryptographic_resolve"

class AnchorStrategy(Enum):
    CRYPTOGRAPHIC_RESOLUTION = "cryptographic_resolution"
    FALLBACK_DEFAULT = "fallback_default"
    SOFT_ECHO = "soft_echo"
    HARD_ANCHOR = "hard_anchor"

@dataclass
class CursorDirective:
    """Structured parameters for Cursor operations."""
    mode: DirectiveMode
    scope: str = "grid_9x9"
    coherence_threshold: float = 0.6
    anchor_strategy: AnchorStrategy = AnchorStrategy.CRYPTOGRAPHIC_RESOLUTION
    glyph_policy: str = "soft-echo"
    entropy_handling: str = "suppress_if_spike > 0.4"
    log_strategy: str = "silent_unless_failure"
    cryptographer_required: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert directive to dictionary format."""
        return {
            "mode": self.mode.value,
            "scope": self.scope,
            "coherence_threshold": self.coherence_threshold,
            "anchor_strategy": self.anchor_strategy.value,
            "glyph_policy": self.glyph_policy,
            "entropy_handling": self.entropy_handling,
            "log_strategy": self.log_strategy,
            "cryptographer_required": self.cryptographer_required
        }
        
    @classmethod
    def create_reinforce_directive(cls) -> 'CursorDirective':
        """Create a directive for kernel reinforcement."""
        return cls(
            mode=DirectiveMode.REINFORCE_KERNELS,
            anchor_strategy=AnchorStrategy.CRYPTOGRAPHIC_RESOLUTION,
            cryptographer_required=True
        )
        
    @classmethod
    def create_breath_reset_directive(cls) -> 'CursorDirective':
        """Create a directive for breath reset."""
        return cls(
            mode=DirectiveMode.BREATH_RESET,
            anchor_strategy=AnchorStrategy.SOFT_ECHO,
            cryptographer_required=False
        )
        
    @classmethod
    def create_anchor_check_directive(cls) -> 'CursorDirective':
        """Create a directive for anchor state checking."""
        return cls(
            mode=DirectiveMode.ANCHOR_CHECK,
            anchor_strategy=AnchorStrategy.FALLBACK_DEFAULT,
            cryptographer_required=True
        ) 