from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass

class AgentRole(Enum):
    REFACTORER = "refactorer"      # Cursor: Structure and code quality
    SYNTHESIZER = "synthesizer"    # Djinn: Pattern and flow optimization
    ENFORCER = "enforcer"         # Arbiter: Rule compliance and boundaries
    RECONCILER = "reconciler"     # Olive Branch: Harmony and recovery

@dataclass
class RoleCapability:
    name: str
    description: str
    priority: int
    requires_approval: bool

@dataclass
class AgentRoleDefinition:
    role: AgentRole
    capabilities: List[RoleCapability]
    override_conditions: List[str]
    delegation_rules: Dict[str, str]
    intent_mode: str = "gentle"  # Default to gentle mode

class RoleManager:
    def __init__(self):
        self._role_definitions = self._initialize_roles()
        self._active_overrides: Dict[str, bool] = {}
        self._delegation_history: List[Dict[str, Any]] = []

    def _initialize_roles(self) -> Dict[str, AgentRoleDefinition]:
        """Initialize role definitions for all agents."""
        return {
            'cursor': AgentRoleDefinition(
                role=AgentRole.REFACTORER,
                capabilities=[
                    RoleCapability(
                        name="code_refactoring",
                        description="Restructure code for better quality and maintainability",
                        priority=1,
                        requires_approval=False
                    ),
                    RoleCapability(
                        name="pattern_detection",
                        description="Identify and suggest pattern improvements",
                        priority=2,
                        requires_approval=True
                    )
                ],
                override_conditions=[
                    "critical_stability_breach",
                    "codex_violation_detected"
                ],
                delegation_rules={
                    "pattern_optimization": "djinn",
                    "rule_enforcement": "arbiter",
                    "harmony_restoration": "olive_branch"
                },
                intent_mode="gentle"  # Cursor operates in gentle mode
            ),
            'djinn': AgentRoleDefinition(
                role=AgentRole.SYNTHESIZER,
                capabilities=[
                    RoleCapability(
                        name="flow_optimization",
                        description="Optimize recursive flow patterns",
                        priority=1,
                        requires_approval=False
                    ),
                    RoleCapability(
                        name="pattern_synthesis",
                        description="Synthesize new patterns from existing ones",
                        priority=2,
                        requires_approval=True
                    )
                ],
                override_conditions=[
                    "flow_degradation",
                    "pattern_conflict"
                ],
                delegation_rules={
                    "structure_refactoring": "cursor",
                    "rule_validation": "arbiter",
                    "conflict_resolution": "olive_branch"
                },
                intent_mode="gentle"  # Djinn operates in gentle mode
            ),
            'arbiter': AgentRoleDefinition(
                role=AgentRole.ENFORCER,
                capabilities=[
                    RoleCapability(
                        name="rule_enforcement",
                        description="Enforce Codex rules and boundaries",
                        priority=1,
                        requires_approval=False
                    ),
                    RoleCapability(
                        name="compliance_validation",
                        description="Validate system compliance with Codex",
                        priority=2,
                        requires_approval=True
                    )
                ],
                override_conditions=[
                    "rule_violation",
                    "boundary_breach"
                ],
                delegation_rules={
                    "structure_correction": "cursor",
                    "flow_optimization": "djinn",
                    "harmony_restoration": "olive_branch"
                }
            ),
            'olive_branch': AgentRoleDefinition(
                role=AgentRole.RECONCILER,
                capabilities=[
                    RoleCapability(
                        name="harmony_restoration",
                        description="Restore harmony in agent interactions",
                        priority=1,
                        requires_approval=False
                    ),
                    RoleCapability(
                        name="conflict_resolution",
                        description="Resolve conflicts between agents",
                        priority=2,
                        requires_approval=True
                    )
                ],
                override_conditions=[
                    "agent_conflict",
                    "harmony_breach"
                ],
                delegation_rules={
                    "structure_repair": "cursor",
                    "flow_restoration": "djinn",
                    "rule_adjustment": "arbiter"
                }
            )
        }

    def get_role_definition(self, agent: str) -> Optional[AgentRoleDefinition]:
        """Get the role definition for an agent."""
        return self._role_definitions.get(agent.lower())

    def can_override(self, agent: str, condition: str) -> bool:
        """Check if an agent can override based on a condition."""
        role_def = self.get_role_definition(agent)
        if not role_def:
            return False
        return condition in role_def.override_conditions

    def get_delegation_target(self, agent: str, task: str) -> Optional[str]:
        """Get the appropriate delegation target for a task."""
        role_def = self.get_role_definition(agent)
        if not role_def:
            return None
        return role_def.delegation_rules.get(task)

    def record_delegation(self, from_agent: str, to_agent: str, task: str) -> None:
        """Record a delegation action."""
        self._delegation_history.append({
            'timestamp': 'now',  # Replace with actual timestamp
            'from_agent': from_agent,
            'to_agent': to_agent,
            'task': task
        })

    def get_delegation_history(self) -> List[Dict[str, Any]]:
        """Get the delegation history."""
        return self._delegation_history 