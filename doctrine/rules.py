"""
Codex Compliance Rules
Defines and enforces the core principles of the recursive system
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import ast
import hashlib
from datetime import datetime

@dataclass
class CodexRule:
    """Represents a Codex compliance rule"""
    id: str
    name: str
    description: str
    severity: str  # 'critical', 'warning', 'info'
    validator: Callable[[Any], bool]
    error_message: str
    category: str  # 'structure', 'flow', 'security', 'stability'

class CodexValidator:
    """Validates system state against Codex rules"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
        
    def _initialize_rules(self) -> Dict[str, CodexRule]:
        """Initialize Codex compliance rules"""
        return {
            # Structure Rules
            'STRUCT_001': CodexRule(
                id='STRUCT_001',
                name='Recursive Pattern Preservation',
                description='Recursive patterns must maintain their structural integrity',
                severity='critical',
                validator=self._validate_recursive_pattern,
                error_message='Recursive pattern integrity compromised',
                category='structure'
            ),
            
            'STRUCT_002': CodexRule(
                id='STRUCT_002',
                name='Module Boundary Respect',
                description='Module boundaries must be respected and maintained',
                severity='critical',
                validator=self._validate_module_boundaries,
                error_message='Module boundary violation detected',
                category='structure'
            ),
            
            # Flow Rules
            'FLOW_001': CodexRule(
                id='FLOW_001',
                name='Recursive Flow Integrity',
                description='Recursive flow must maintain its integrity and direction',
                severity='critical',
                validator=self._validate_recursive_flow,
                error_message='Recursive flow integrity compromised',
                category='flow'
            ),
            
            'FLOW_002': CodexRule(
                id='FLOW_002',
                name='Pattern Evolution Stability',
                description='Pattern evolution must maintain system stability',
                severity='warning',
                validator=self._validate_pattern_evolution,
                error_message='Pattern evolution causing instability',
                category='flow'
            ),
            
            # Security Rules
            'SEC_001': CodexRule(
                id='SEC_001',
                name='State Preservation',
                description='System state must be preserved and protected',
                severity='critical',
                validator=self._validate_state_preservation,
                error_message='State preservation compromised',
                category='security'
            ),
            
            'SEC_002': CodexRule(
                id='SEC_002',
                name='Boundary Protection',
                description='System boundaries must be protected',
                severity='critical',
                validator=self._validate_boundary_protection,
                error_message='Boundary protection compromised',
                category='security'
            ),
            
            # Stability Rules
            'STAB_001': CodexRule(
                id='STAB_001',
                name='Recursive Stability',
                description='Recursive operations must maintain system stability',
                severity='critical',
                validator=self._validate_recursive_stability,
                error_message='Recursive stability compromised',
                category='stability'
            ),
            
            'STAB_002': CodexRule(
                id='STAB_002',
                name='Pattern Harmony',
                description='Patterns must maintain harmony with each other',
                severity='warning',
                validator=self._validate_pattern_harmony,
                error_message='Pattern harmony compromised',
                category='stability'
            )
        }
        
    def _validate_recursive_pattern(self, state: Any) -> bool:
        """Validate recursive pattern integrity"""
        # Check pattern structure
        if not hasattr(state, 'pattern'):
            return False
            
        # Verify pattern components
        pattern = state.pattern
        required_components = ['structure', 'flow', 'boundaries']
        if not all(comp in pattern for comp in required_components):
            return False
            
        # Check pattern stability
        if not hasattr(pattern, 'stability_score'):
            return False
        if pattern.stability_score < 0.8:  # Minimum stability threshold
            return False
            
        return True
        
    def _validate_module_boundaries(self, state: Any) -> bool:
        """Validate module boundary integrity"""
        # Check module structure
        if not hasattr(state, 'modules'):
            return False
            
        # Verify module boundaries
        for module in state.modules:
            if not hasattr(module, 'boundaries'):
                return False
            if not module.boundaries.get('protected', False):
                return False
                
        return True
        
    def _validate_recursive_flow(self, state: Any) -> bool:
        """Validate recursive flow integrity"""
        # Check flow structure
        if not hasattr(state, 'flow'):
            return False
            
        # Verify flow components
        flow = state.flow
        required_components = ['direction', 'depth', 'stability']
        if not all(comp in flow for comp in required_components):
            return False
            
        # Check flow stability
        if flow.stability < 0.8:  # Minimum stability threshold
            return False
            
        return True
        
    def _validate_pattern_evolution(self, state: Any) -> bool:
        """Validate pattern evolution stability"""
        # Check evolution state
        if not hasattr(state, 'evolution'):
            return False
            
        # Verify evolution stability
        evolution = state.evolution
        if not hasattr(evolution, 'stability_score'):
            return False
        if evolution.stability_score < 0.7:  # Minimum stability threshold
            return False
            
        return True
        
    def _validate_state_preservation(self, state: Any) -> bool:
        """Validate state preservation"""
        # Check state structure
        if not hasattr(state, 'preservation'):
            return False
            
        # Verify preservation components
        preservation = state.preservation
        required_components = ['hash', 'timestamp', 'integrity']
        if not all(comp in preservation for comp in required_components):
            return False
            
        # Check integrity
        if not preservation.integrity:
            return False
            
        return True
        
    def _validate_boundary_protection(self, state: Any) -> bool:
        """Validate boundary protection"""
        # Check boundary structure
        if not hasattr(state, 'boundaries'):
            return False
            
        # Verify boundary protection
        boundaries = state.boundaries
        if not boundaries.get('protected', False):
            return False
        if not boundaries.get('monitored', False):
            return False
            
        return True
        
    def _validate_recursive_stability(self, state: Any) -> bool:
        """Validate recursive stability"""
        # Check stability metrics
        if not hasattr(state, 'stability'):
            return False
            
        # Verify stability components
        stability = state.stability
        required_components = ['score', 'metrics', 'thresholds']
        if not all(comp in stability for comp in required_components):
            return False
            
        # Check stability score
        if stability.score < 0.8:  # Minimum stability threshold
            return False
            
        return True
        
    def _validate_pattern_harmony(self, state: Any) -> bool:
        """Validate pattern harmony"""
        # Check harmony state
        if not hasattr(state, 'harmony'):
            return False
            
        # Verify harmony components
        harmony = state.harmony
        required_components = ['score', 'conflicts', 'resolution']
        if not all(comp in harmony for comp in required_components):
            return False
            
        # Check harmony score
        if harmony.score < 0.7:  # Minimum harmony threshold
            return False
            
        return True
        
    def validate_state(self, state: Any) -> Dict[str, Any]:
        """Validate system state against all rules"""
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'valid': True,
            'violations': [],
            'warnings': [],
            'info': []
        }
        
        for rule_id, rule in self.rules.items():
            try:
                if not rule.validator(state):
                    violation = {
                        'rule_id': rule_id,
                        'name': rule.name,
                        'description': rule.description,
                        'error_message': rule.error_message,
                        'category': rule.category
                    }
                    
                    if rule.severity == 'critical':
                        results['valid'] = False
                        results['violations'].append(violation)
                    elif rule.severity == 'warning':
                        results['warnings'].append(violation)
                    else:
                        results['info'].append(violation)
                        
            except Exception as e:
                results['valid'] = False
                results['violations'].append({
                    'rule_id': rule_id,
                    'name': rule.name,
                    'description': rule.description,
                    'error_message': f'Validation error: {str(e)}',
                    'category': rule.category
                })
                
        return results
        
    def get_rule(self, rule_id: str) -> Optional[CodexRule]:
        """Get rule by ID"""
        return self.rules.get(rule_id)
        
    def list_rules(self, category: Optional[str] = None) -> List[CodexRule]:
        """List all rules, optionally filtered by category"""
        if category:
            return [rule for rule in self.rules.values() if rule.category == category]
        return list(self.rules.values())
        
    def add_rule(self, rule: CodexRule):
        """Add a new rule"""
        self.rules[rule.id] = rule
        
    def remove_rule(self, rule_id: str):
        """Remove a rule"""
        if rule_id in self.rules:
            del self.rules[rule_id]

def main():
    """Command-line interface for rule management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Codex Rule Management")
    parser.add_argument("--list", action="store_true", help="List all rules")
    parser.add_argument("--category", help="Filter rules by category")
    parser.add_argument("--rule", help="Get specific rule")
    
    args = parser.parse_args()
    validator = CodexValidator()
    
    if args.list:
        rules = validator.list_rules(args.category)
        for rule in rules:
            print(f"\nRule ID: {rule.id}")
            print(f"Name: {rule.name}")
            print(f"Description: {rule.description}")
            print(f"Severity: {rule.severity}")
            print(f"Category: {rule.category}")
            
    elif args.rule:
        rule = validator.get_rule(args.rule)
        if rule:
            print(f"\nRule ID: {rule.id}")
            print(f"Name: {rule.name}")
            print(f"Description: {rule.description}")
            print(f"Severity: {rule.severity}")
            print(f"Category: {rule.category}")
            print(f"Error Message: {rule.error_message}")
        else:
            print(f"Rule not found: {args.rule}")

if __name__ == "__main__":
    main() 