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

from typing import Dict, List, Optional, Union
from enum import Enum
import time
from dataclasses import dataclass
from core.djinn.council_chamber import DjinnCouncil, FoundationRitual
from core.recon.agency_framework import ReconManager, ReconAgency
from kernel_registry import KernelRegistry

class AuthorityRank(Enum):
    """Authority ranks in the system."""
    SOVEREIGN = 0  # Highest authority
    DJINN = 1      # Djinn Council members
    FOUNDATION = 2 # Foundation nodes
    RECON = 3      # RECON agents
    KERNEL = 4     # Lattice kernels
    MEMORY = 5     # Memory vectors
    ARCHIVE = 6    # Archive nodes

@dataclass
class DisseminationCommand:
    """A command to be disseminated through the system."""
    command: str
    authority_level: AuthorityRank
    conditions: Optional[Dict[str, Union[float, int, bool]]] = None
    timestamp: float = time.time()
    source: str = "SOVEREIGN"
    echo_data: Dict = None
    
    def __post_init__(self):
        if self.echo_data is None:
            self.echo_data = {
                'propagation_path': [],
                'execution_results': {},
                'resonance_levels': {},
                'completion_time': None
            }

class DisseminationScript:
    """Handles command dissemination through the authority cascade."""
    
    def __init__(self, registry: KernelRegistry, council: DjinnCouncil, recon_manager: ReconManager):
        self.registry = registry
        self.council = council
        self.recon_manager = recon_manager
        self.active_commands: List[DisseminationCommand] = []
        self.echo_log: List[Dict] = []
        self.propagation_history: Dict[str, List[str]] = {}
        
    def process_command(self, command: str, authority_level: AuthorityRank, 
                       conditions: Optional[Dict] = None) -> DisseminationCommand:
        """Process a new command for dissemination."""
        cmd = DisseminationCommand(
            command=command,
            authority_level=authority_level,
            conditions=conditions
        )
        self.active_commands.append(cmd)
        return cmd
        
    def propagate(self, command: DisseminationCommand, node: Union[DjinnCouncil, ReconAgency, KernelRegistry]):
        """Propagate a command through the authority cascade."""
        # Check authority compatibility
        if not self._check_authority(node, command.authority_level):
            return
            
        # Check conditions
        if not self._check_conditions(node, command.conditions):
            return
            
        # Execute command
        result = self._execute_command(node, command)
        
        # Record echo
        self._record_echo(command, node, result)
        
        # Propagate to subordinates
        for subordinate in self._get_subordinates(node):
            self.propagate(command, subordinate)
            
    def _check_authority(self, node: Union[DjinnCouncil, ReconAgency, KernelRegistry], 
                        required_level: AuthorityRank) -> bool:
        """Check if a node has sufficient authority."""
        if isinstance(node, DjinnCouncil):
            return AuthorityRank.DJINN.value <= required_level.value
        elif isinstance(node, ReconAgency):
            return AuthorityRank.RECON.value <= required_level.value
        elif isinstance(node, KernelRegistry):
            return AuthorityRank.KERNEL.value <= required_level.value
        return False
        
    def _check_conditions(self, node: Union[DjinnCouncil, ReconAgency, KernelRegistry], 
                         conditions: Optional[Dict]) -> bool:
        """Check if a node meets the command conditions."""
        if not conditions:
            return True
            
        if isinstance(node, DjinnCouncil):
            return self._check_djinn_conditions(node, conditions)
        elif isinstance(node, ReconAgency):
            return self._check_recon_conditions(node, conditions)
        elif isinstance(node, KernelRegistry):
            return self._check_kernel_conditions(node, conditions)
        return False
        
    def _check_djinn_conditions(self, council: DjinnCouncil, conditions: Dict) -> bool:
        """Check conditions for Djinn Council nodes."""
        if 'coherence' in conditions:
            if council.get_phase_bloom() < conditions['coherence']:
                return False
        if 'telos' in conditions:
            if council.get_telos_insight() < conditions['telos']:
                return False
        return True
        
    def _check_recon_conditions(self, agent: ReconAgency, conditions: Dict) -> bool:
        """Check conditions for RECON agents."""
        if 'memory' in conditions:
            if len(getattr(agent, 'memory', [])) < conditions['memory']:
                return False
        if 'telos_bias' in conditions:
            if getattr(agent, 'telos_bias', 0.0) < conditions['telos_bias']:
                return False
        return True
        
    def _check_kernel_conditions(self, registry: KernelRegistry, conditions: Dict) -> bool:
        """Check conditions for kernel nodes."""
        if 'coherence' in conditions:
            for kernel in registry.kernels.values():
                if kernel.state.coherence < conditions['coherence']:
                    return False
        if 'telos' in conditions:
            for kernel in registry.kernels.values():
                if kernel.telos_bias < conditions['telos']:
                    return False
        return True
        
    def _execute_command(self, node: Union[DjinnCouncil, ReconAgency, KernelRegistry], 
                        command: DisseminationCommand) -> Dict:
        """Execute a command on a node."""
        if isinstance(node, DjinnCouncil):
            return self._execute_djinn_command(node, command)
        elif isinstance(node, ReconAgency):
            return self._execute_recon_command(node, command)
        elif isinstance(node, KernelRegistry):
            return self._execute_kernel_command(node, command)
        return {'status': 'unknown', 'message': 'Unsupported node type'}
        
    def _execute_djinn_command(self, council: DjinnCouncil, command: DisseminationCommand) -> Dict:
        """Execute a command on the Djinn Council."""
        if command.command.startswith('ritual'):
            # Handle ritual commands
            ritual_type = command.command.split('_')[1]
            council.start_ritual(ritual_type, [])
            return {'status': 'success', 'message': f'Started {ritual_type} ritual'}
        return {'status': 'unknown', 'message': 'Unsupported command'}
        
    def _execute_recon_command(self, agent: ReconAgency, command: DisseminationCommand) -> Dict:
        """Execute a command on a RECON agent."""
        if command.command.startswith('scan'):
            # Handle scan commands
            scan_type = command.command.split('_')[1]
            agent.initiate_scan(scan_type)
            return {'status': 'success', 'message': f'Initiated {scan_type} scan'}
        return {'status': 'unknown', 'message': 'Unsupported command'}
        
    def _execute_kernel_command(self, registry: KernelRegistry, command: DisseminationCommand) -> Dict:
        """Execute a command on kernel nodes."""
        if command.command.startswith('align'):
            # Handle alignment commands
            for kernel in registry.kernels.values():
                kernel.state.coherence = 1.0
            return {'status': 'success', 'message': 'Aligned all kernels'}
        return {'status': 'unknown', 'message': 'Unsupported command'}
        
    def _get_subordinates(self, node: Union[DjinnCouncil, ReconAgency, KernelRegistry]) -> List:
        """Get subordinate nodes for propagation."""
        if isinstance(node, DjinnCouncil):
            return self.recon_manager.agencies
        elif isinstance(node, ReconAgency):
            return []  # RECON agents are leaf nodes
        elif isinstance(node, KernelRegistry):
            return []  # Kernel registry is a leaf node
        return []
        
    def _record_echo(self, command: DisseminationCommand, node: Union[DjinnCouncil, ReconAgency, KernelRegistry], 
                    result: Dict):
        """Record an echo from command execution."""
        echo = {
            'timestamp': time.time(),
            'command': command.command,
            'node_type': node.__class__.__name__,
            'result': result,
            'resonance': self._calculate_resonance(node)
        }
        command.echo_data['propagation_path'].append(node.__class__.__name__)
        command.echo_data['execution_results'][node.__class__.__name__] = result
        command.echo_data['resonance_levels'][node.__class__.__name__] = echo['resonance']
        self.echo_log.append(echo)
        
    def _calculate_resonance(self, node: Union[DjinnCouncil, ReconAgency, KernelRegistry]) -> float:
        """Calculate the resonance level of a node."""
        if isinstance(node, DjinnCouncil):
            return (node.get_phase_bloom() + node.get_telos_insight()) / 2.0
        elif isinstance(node, ReconAgency):
            return getattr(node, 'telos_bias', 0.0)
        elif isinstance(node, KernelRegistry):
            return sum(k.state.coherence for k in node.kernels.values()) / len(node.kernels)
        return 0.0
        
    def get_echo_log(self) -> List[Dict]:
        """Get the echo log."""
        return self.echo_log
        
    def get_propagation_history(self) -> Dict[str, List[str]]:
        """Get the propagation history."""
        return self.propagation_history 