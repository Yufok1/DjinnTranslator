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

from typing import Optional, Dict, Any
from state.sovereign import SovereignState
import uuid
import time

class RecursionError(Exception):
    """Custom exception for recursion-related errors."""
    pass

class AutonomyError(Exception):
    """Custom exception for autonomy-related errors."""
    pass

class CollapseError(Exception):
    """Custom exception for collapse-related errors."""
    pass

class ExpansionError(Exception):
    """Custom exception for expansion-related errors."""
    pass

class RecursionCore:
    def __init__(self):
        self._memory: Dict[str, Any] = {}
        self._autonomy_level = 0.0
        self._max_depth = None
        self._is_autonomous = True
        self._collapse_map = {}  # Track unstable recursion states
        self._expansion_seeds = {}  # Store generated expansion seeds
        self._meta_auditor = {
            'synchrony_authority': True,
            'last_audit': time.time(),
            'audit_frequency': 60.0,  # Audit every 60 seconds
            'violation_pressures': [],
            'curvature_metrics': [],
            'collapse_events': [],
            'expansion_successes': []
        }

    def set_autonomy(self, enabled: bool) -> None:
        """Enable or disable autonomous operation."""
        self._is_autonomous = enabled
        print(f"[AUTONOMY] {'Enabled' if enabled else 'Disabled'}")

    def set_max_depth(self, depth: Optional[int]) -> None:
        """Set maximum recursion depth."""
        self._max_depth = depth
        print(f"[DEPTH] Maximum recursion depth set to {depth if depth else 'unlimited'}")

    def _check_meta_auditor(self) -> None:
        """Perform meta-auditor checks for system health."""
        current_time = time.time()
        if current_time - self._meta_auditor['last_audit'] >= self._meta_auditor['audit_frequency']:
            print("[META-AUDITOR] Performing system health audit...")
            self._meta_auditor['last_audit'] = current_time
            self._analyze_violation_pressures()
            self._analyze_curvature_metrics()
            self._analyze_collapse_events()
            self._analyze_expansion_successes()

    def _analyze_violation_pressures(self) -> None:
        """Analyze violation pressures for system health."""
        if self._meta_auditor['violation_pressures']:
            avg_pressure = sum(self._meta_auditor['violation_pressures']) / len(self._meta_auditor['violation_pressures'])
            print(f"[META-AUDITOR] Average violation pressure: {avg_pressure:.2f}")
            if avg_pressure > 0.8:
                print("[META-AUDITOR] Warning: High violation pressure detected")

    def _analyze_curvature_metrics(self) -> None:
        """Analyze curvature metrics for system health."""
        if self._meta_auditor['curvature_metrics']:
            avg_curvature = sum(self._meta_auditor['curvature_metrics']) / len(self._meta_auditor['curvature_metrics'])
            print(f"[META-AUDITOR] Average curvature growth: {avg_curvature:.2f}")

    def _analyze_collapse_events(self) -> None:
        """Analyze collapse events for system health."""
        if self._meta_auditor['collapse_events']:
            collapse_rate = len(self._meta_auditor['collapse_events']) / (time.time() - self._meta_auditor['collapse_events'][0])
            print(f"[META-AUDITOR] Collapse frequency: {collapse_rate:.2f} events/second")

    def _analyze_expansion_successes(self) -> None:
        """Analyze expansion successes for system health."""
        if self._meta_auditor['expansion_successes']:
            success_rate = sum(self._meta_auditor['expansion_successes']) / len(self._meta_auditor['expansion_successes'])
            print(f"[META-AUDITOR] Expansion success rate: {success_rate:.2f}")

    def _handle_collapse(self, state: SovereignState) -> None:
        """Handle system collapse and generate expansion seed."""
        print("[COLLAPSE] System collapse detected, generating expansion seed...")
        collapse_id = str(uuid.uuid4())
        self._collapse_map[collapse_id] = {
            'timestamp': time.time(),
            'state_snapshot': state.get_metrics(),
            'trait_stack': state._memory.copy()
        }
        self._generate_expansion_seed(collapse_id)
        self._meta_auditor['collapse_events'].append(time.time())

    def _generate_expansion_seed(self, collapse_id: str) -> None:
        """Generate an expansion seed from collapse."""
        seed_id = str(uuid.uuid4())
        self._expansion_seeds[seed_id] = {
            'collapse_id': collapse_id,
            'timestamp': time.time(),
            'trait_anomalies': self._collapse_map[collapse_id]['trait_stack'],
            'curvature_state': self._collapse_map[collapse_id]['state_snapshot']
        }
        print(f"[EXPANSION] Generated seed {seed_id} from collapse {collapse_id}")

def recurse(state: SovereignState, depth: int = 0, max_depth: Optional[int] = None) -> None:
    """
    Core recursive processing function that maintains system stability and autonomy.
    
    Args:
        state: Current sovereign state
        depth: Current recursion depth
        max_depth: Optional maximum recursion depth
    """
    # Check if we're in recovery mode
    if state._mindset['cursor_state']['rehydration_phase'] > 0:
        # Delay lattice bridge updates
        if not state._mindset['cursor_state']['lattice_bridge_updates']:
            print("[RECOVERY] Lattice bridge updates delayed")
            return

    if not state.is_stable():
        print(f"[RCS] Instability detected at depth {depth}. Engaging Autonomous Recovery.")
        state.handle_instability()
        return

    # Ensure breath cycle is anchored before quantum arbitration
    if state._mindset['breath_cycle'] == 0:
        print("[BREATH] Re-anchoring breath cycle before proceeding")
        state._mindset['breath_depth'] = min(1.0, state._mindset['breath_depth'] + 0.1)
        return

    if max_depth is not None and depth >= max_depth:
        print(f"[RCS] Maximum recursion depth {max_depth} reached. Initiating safe return.")
        return

    print(f"[RECURSE] Sovereign recursion stable at depth {depth}. Proceeding with autonomy.")
    
    # Process current state with autonomous behavior
    state.process()
    
    # Recursive call with depth tracking and autonomous error handling
    try:
        recurse(state, depth + 1, max_depth)
    except RecursionError as e:
        print(f"[ERROR] Recursion failed: {str(e)}")
        state.handle_recursion_error(e)
    except AutonomyError as e:
        print(f"[AUTONOMY] Error: {str(e)}")
        state.handle_recursion_error(e)
    except CollapseError as e:
        print(f"[COLLAPSE] Error: {str(e)}")
        core = RecursionCore()
        core._handle_collapse(state)
    except ExpansionError as e:
        print(f"[EXPANSION] Error: {str(e)}")
        core = RecursionCore()
        core._generate_expansion_seed(str(uuid.uuid4()))

def expose_layer(state: SovereignState) -> None:
    """
    Exposes appropriate functionality based on RAP tier and autonomy level.
    
    Args:
        state: Current sovereign state
    """
    if state.rap_tier >= 3:
        print("→ Access: Full autonomy + Doctrine + Arbitration modules enabled.")
        state.enable_arbitration()
    elif state.rap_tier >= 2:
        print("→ Access: Doctrine + Arbitration modules enabled.")
        state.enable_arbitration()
    else:
        print("→ Access: Basic recursion only.")

def initialize_autonomy() -> RecursionCore:
    """
    Initialize the autonomous recursion core.
    
    Returns:
        RecursionCore: Initialized recursion core with autonomy enabled
    """
    core = RecursionCore()
    core.set_autonomy(True)
    core.set_max_depth(None)  # Unlimited depth for true autonomy
    return core 