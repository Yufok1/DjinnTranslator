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

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass
import random
import uuid
import math
from datetime import datetime

class AgentType(Enum):
    MIRROR = "mirror"      # Reflective/analytical agents
    PROPELLANT = "prop"    # Energy/momentum agents
    FLIGHT = "flight"      # Navigation/movement agents
    SENTINEL = "sentinel"  # Monitoring/guardian agents

@dataclass
class LatticePosition:
    x: int  # 0-8 for 9x9 grid
    y: int  # 0-8 for 9x9 grid
    
    def is_valid(self) -> bool:
        return 0 <= self.x <= 8 and 0 <= self.y <= 8
    
    def distance_to(self, other: 'LatticePosition') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def vector_to(self, other: 'LatticePosition') -> Tuple[float, float]:
        return (other.x - self.x, other.y - self.y)
    
    def add_vector(self, dx: float, dy: float) -> 'LatticePosition':
        return LatticePosition(
            x=max(0, min(8, int(self.x + dx))),
            y=max(0, min(8, int(self.y + dy)))
        )

@dataclass
class TelosAnchor:
    position: LatticePosition
    strength: float  # 0.0 to 1.0
    coherence: float  # 0.0 to 1.0
    last_echo: datetime
    
    def get_attraction_force(self, position: LatticePosition) -> Tuple[float, float]:
        """Calculate attraction force vector based on distance and strength."""
        dx, dy = position.vector_to(self.position)
        distance = position.distance_to(self.position)
        
        # Normalize and scale by strength and coherence
        if distance > 0:
            force = (self.strength * self.coherence) / (distance ** 2)
            return (dx * force, dy * force)
        return (0.0, 0.0)

@dataclass
class AgentState:
    agent_id: str
    agent_type: AgentType
    position: LatticePosition
    memory: Dict[str, Any]
    last_update: datetime
    is_active: bool = True
    phase: float = 0.0  # 0.0 to 1.0
    entropy: float = 0.0  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "position": {"x": self.position.x, "y": self.position.y},
            "memory": self.memory,
            "last_update": self.last_update.isoformat(),
            "is_active": self.is_active,
            "phase": self.phase,
            "entropy": self.entropy
        }

class RECONAgentManager:
    def __init__(self):
        self.agents: Dict[str, AgentState] = {}
        self.agent_roles: Dict[str, List[str]] = {
            agent_type.value: [] for agent_type in AgentType
        }
        self.telos_anchors: List[TelosAnchor] = []
        self.last_echo_time: datetime = datetime.now()
    
    def add_telos_anchor(self, position: LatticePosition, strength: float = 1.0) -> None:
        """Add a new telos anchor point."""
        anchor = TelosAnchor(
            position=position,
            strength=strength,
            coherence=1.0,
            last_echo=datetime.now()
        )
        self.telos_anchors.append(anchor)
    
    def update_telos_anchors(self, delta_time: float) -> None:
        """Update telos anchor states and coherence."""
        current_time = datetime.now()
        for anchor in self.telos_anchors:
            # Gradually decrease coherence over time
            time_diff = (current_time - anchor.last_echo).total_seconds()
            anchor.coherence = max(0.0, anchor.coherence - (time_diff * 0.1))
            
            # Randomly emit new echoes
            if random.random() < 0.1:
                anchor.coherence = min(1.0, anchor.coherence + 0.2)
                anchor.last_echo = current_time
    
    def spawn_agent(
        self,
        agent_type: AgentType,
        initial_position: Optional[LatticePosition] = None,
        initial_memory: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Spawn a new agent of specified type at given position.
        Returns the agent's ID.
        """
        agent_id = str(uuid.uuid4())
        
        if initial_position is None:
            initial_position = LatticePosition(
                x=random.randint(0, 8),
                y=random.randint(0, 8)
            )
        
        agent_state = AgentState(
            agent_id=agent_id,
            agent_type=agent_type,
            position=initial_position,
            memory=initial_memory or {},
            last_update=datetime.now(),
            phase=random.random(),
            entropy=random.random() * 0.5
        )
        
        self.agents[agent_id] = agent_state
        self.agent_roles[agent_type.value].append(agent_id)
        
        return agent_id
    
    def update_agents(self, delta_time: float = 1.0) -> None:
        """Update all active agents' states and positions."""
        current_time = datetime.now()
        
        # Update telos anchors first
        self.update_telos_anchors(delta_time)
        
        for agent_id, agent in self.agents.items():
            if not agent.is_active:
                continue
            
            if agent.agent_type == AgentType.FLIGHT:
                self._update_flight_agent(agent, delta_time)
            elif agent.agent_type == AgentType.SENTINEL:
                self._update_sentinel_agent(agent, delta_time)
            elif agent.agent_type == AgentType.MIRROR:
                self._update_mirror_agent(agent, delta_time)
            elif agent.agent_type == AgentType.PROPELLANT:
                self._update_propellant_agent(agent, delta_time)
            
            agent.last_update = current_time
    
    def despawn_agent(self, agent_id: str) -> bool:
        """
        Despawn an agent by ID.
        Returns True if successful, False if agent not found.
        """
        if agent_id not in self.agents:
            return False
            
        agent = self.agents[agent_id]
        agent.is_active = False
        
        # Remove from role tracking
        self.agent_roles[agent.agent_type.value].remove(agent_id)
        
        # Optionally remove from agents dict
        # del self.agents[agent_id]
        
        return True
    
    def get_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current state of an agent by ID.
        Returns None if agent not found.
        """
        if agent_id not in self.agents:
            return None
            
        return self.agents[agent_id].to_dict()
    
    def get_agents_by_role(self, role: AgentType) -> List[Dict[str, Any]]:
        """
        Get states of all agents of a specific role.
        """
        agent_ids = self.agent_roles[role.value]
        return [self.get_agent_state(agent_id) for agent_id in agent_ids]
    
    def _update_flight_agent(self, agent: AgentState, delta_time: float) -> None:
        """Update logic for flight-type agents with telos-seeking behavior."""
        # Calculate telos attraction forces
        total_dx, total_dy = 0.0, 0.0
        for anchor in self.telos_anchors:
            dx, dy = anchor.get_attraction_force(agent.position)
            total_dx += dx
            total_dy += dy
        
        # Add some random movement for exploration
        random_dx = random.uniform(-0.5, 0.5) * delta_time
        random_dy = random.uniform(-0.5, 0.5) * delta_time
        
        # Combine telos attraction with random movement
        final_dx = (total_dx * 0.7 + random_dx * 0.3) * delta_time
        final_dy = (total_dy * 0.7 + random_dy * 0.3) * delta_time
        
        # Update position
        new_position = agent.position.add_vector(final_dx, final_dy)
        agent.position = new_position
        
        # Update memory with movement history
        if "movement_history" not in agent.memory:
            agent.memory["movement_history"] = []
        agent.memory["movement_history"].append({
            "position": {"x": new_position.x, "y": new_position.y},
            "timestamp": datetime.now().isoformat(),
            "telos_influence": {"dx": total_dx, "dy": total_dy}
        })
        
        # Limit history size
        if len(agent.memory["movement_history"]) > 100:
            agent.memory["movement_history"] = agent.memory["movement_history"][-100:]
    
    def _update_mirror_agent(self, agent: AgentState, delta_time: float) -> None:
        """Update logic for mirror-type agents."""
        # Find nearby agents
        nearby_agents = [
            other for other_id, other in self.agents.items()
            if other.is_active and other.agent_id != agent.agent_id
            and agent.position.distance_to(other.position) < 2.0
        ]
        
        if nearby_agents:
            # Mirror the phase and entropy of the nearest agent
            nearest = min(nearby_agents, key=lambda a: agent.position.distance_to(a.position))
            agent.phase = 1.0 - nearest.phase  # Invert phase
            agent.entropy = max(0.0, min(1.0, 1.0 - nearest.entropy))  # Invert entropy
            
            # Store mirrored state in memory
            agent.memory["last_mirrored"] = {
                "agent_id": nearest.agent_id,
                "phase": nearest.phase,
                "entropy": nearest.entropy,
                "timestamp": datetime.now().isoformat()
            }
    
    def _update_propellant_agent(self, agent: AgentState, delta_time: float) -> None:
        """Update logic for propellant-type agents."""
        # Find nearby agents
        nearby_agents = [
            other for other_id, other in self.agents.items()
            if other.is_active and other.agent_id != agent.agent_id
            and agent.position.distance_to(other.position) < 2.0
        ]
        
        for other in nearby_agents:
            # Increase entropy and phase oscillation in nearby agents
            other.entropy = min(1.0, other.entropy + 0.1 * delta_time)
            other.phase = (other.phase + 0.2 * delta_time) % 1.0
            
            # Store catalyzed interactions in memory
            if "catalyzed_interactions" not in agent.memory:
                agent.memory["catalyzed_interactions"] = []
            agent.memory["catalyzed_interactions"].append({
                "target_id": other.agent_id,
                "entropy_increase": 0.1 * delta_time,
                "phase_shift": 0.2 * delta_time,
                "timestamp": datetime.now().isoformat()
            })
    
    def _update_sentinel_agent(self, agent: AgentState, delta_time: float) -> None:
        """
        Update logic for sentinel-type agents.
        Implements simple monitoring behavior.
        """
        # Example: Monitor nearby agents
        nearby_agents = [
            other for other_id, other in self.agents.items()
            if other.is_active and other.agent_id != agent.agent_id
            and agent.position.distance_to(other.position) < 2.0
        ]
        
        # Update memory with monitoring data
        agent.memory["nearby_agents"] = len(nearby_agents)
        agent.memory["last_scan"] = datetime.now().isoformat()

# Example usage
if __name__ == "__main__":
    manager = RECONAgentManager()
    
    # Add some telos anchors
    manager.add_telos_anchor(LatticePosition(4, 4), strength=1.0)
    manager.add_telos_anchor(LatticePosition(7, 7), strength=0.8)
    
    # Spawn agents
    flight_id = manager.spawn_agent(AgentType.FLIGHT)
    mirror_id = manager.spawn_agent(AgentType.MIRROR)
    propellant_id = manager.spawn_agent(AgentType.PROPELLANT)
    
    # Run simulation for a few steps
    for _ in range(10):
        manager.update_agents(delta_time=1.0)
        
        # Print agent states
        for agent_id in [flight_id, mirror_id, propellant_id]:
            state = manager.get_agent_state(agent_id)
            print(f"Agent {state['agent_type']} at position ({state['position']['x']}, {state['position']['y']})")
            print(f"  Phase: {state['phase']:.2f}, Entropy: {state['entropy']:.2f}") 