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

from typing import Dict, List, Optional, Any, Tuple
import ast
import os
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_compliant: bool
    issues: List[str]
    suggested_fixes: List[str]
    severity: str  # 'safe', 'recoverable', 'critical'

class CodexValidator:
    def __init__(self):
        self._rules = {
            'recursion_depth': self._validate_recursion_depth,
            'state_stability': self._validate_state_stability,
            'codex_alignment': self._validate_codex_alignment,
            'autonomy_boundaries': self._validate_autonomy_boundaries
        }
        self._module_cache: Dict[str, ast.Module] = {}

    def validate_module(self, module_path: str) -> ValidationResult:
        """
        Validate a module for Codex compliance.
        
        Args:
            module_path: Path to the module to validate
            
        Returns:
            ValidationResult containing compliance status and issues
        """
        try:
            with open(module_path, 'r') as f:
                content = f.read()
            
            # Parse the module
            tree = ast.parse(content)
            self._module_cache[module_path] = tree
            
            # Run all validations
            issues = []
            fixes = []
            severity = 'safe'
            
            for rule_name, validator in self._rules.items():
                rule_issues, rule_fixes, rule_severity = validator(tree, module_path)
                issues.extend(rule_issues)
                fixes.extend(rule_fixes)
                severity = self._escalate_severity(severity, rule_severity)
            
            return ValidationResult(
                is_compliant=len(issues) == 0,
                issues=issues,
                suggested_fixes=fixes,
                severity=severity
            )
            
        except Exception as e:
            return ValidationResult(
                is_compliant=False,
                issues=[f"Validation failed: {str(e)}"],
                suggested_fixes=[],
                severity='critical'
            )

    def _validate_recursion_depth(self, tree: ast.Module, module_path: str) -> Tuple[List[str], List[str], str]:
        """Validate recursion depth patterns."""
        issues = []
        fixes = []
        severity = 'safe'
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for proper recursion depth handling
                if any(isinstance(n, ast.Call) for n in ast.walk(node)):
                    if not self._has_depth_check(node):
                        issues.append(f"Missing recursion depth check in {node.name}")
                        fixes.append(f"Add depth parameter and check in {node.name}")
                        severity = 'recoverable'
        
        return issues, fixes, severity

    def _validate_state_stability(self, tree: ast.Module, module_path: str) -> Tuple[List[str], List[str], str]:
        """Validate state stability patterns."""
        issues = []
        fixes = []
        severity = 'safe'
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if 'State' in node.name:
                    if not self._has_stability_check(node):
                        issues.append(f"Missing stability check in {node.name}")
                        fixes.append(f"Add is_stable() method to {node.name}")
                        severity = 'recoverable'
        
        return issues, fixes, severity

    def _validate_codex_alignment(self, tree: ast.Module, module_path: str) -> Tuple[List[str], List[str], str]:
        """Validate Codex alignment patterns."""
        issues = []
        fixes = []
        severity = 'safe'
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not self._has_codex_validation(node):
                    issues.append(f"Missing Codex validation in {node.name}")
                    fixes.append(f"Add validate_codex_compliance() method to {node.name}")
                    severity = 'recoverable'
        
        return issues, fixes, severity

    def _validate_autonomy_boundaries(self, tree: ast.Module, module_path: str) -> Tuple[List[str], List[str], str]:
        """Validate autonomy boundary patterns."""
        issues = []
        fixes = []
        severity = 'safe'
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not self._has_boundary_check(node):
                    issues.append(f"Missing boundary check in {node.name}")
                    fixes.append(f"Add check_boundaries() method to {node.name}")
                    severity = 'recoverable'
        
        return issues, fixes, severity

    def _has_depth_check(self, node: ast.FunctionDef) -> bool:
        """Check if a function has proper depth checking."""
        return any(
            isinstance(n, ast.If) and 
            any(isinstance(c, ast.Compare) for c in ast.walk(n))
            for n in ast.walk(node)
        )

    def _has_stability_check(self, node: ast.ClassDef) -> bool:
        """Check if a class has stability checking."""
        return any(
            isinstance(n, ast.FunctionDef) and 
            n.name == 'is_stable'
            for n in ast.walk(node)
        )

    def _has_codex_validation(self, node: ast.ClassDef) -> bool:
        """Check if a class has Codex validation."""
        return any(
            isinstance(n, ast.FunctionDef) and 
            'codex' in n.name.lower()
            for n in ast.walk(node)
        )

    def _has_boundary_check(self, node: ast.ClassDef) -> bool:
        """Check if a class has boundary checking."""
        return any(
            isinstance(n, ast.FunctionDef) and 
            'boundary' in n.name.lower()
            for n in ast.walk(node)
        )

    def _escalate_severity(self, current: str, new: str) -> str:
        """Escalate severity level if needed."""
        severity_levels = {'safe': 0, 'recoverable': 1, 'critical': 2}
        return max(current, new, key=lambda x: severity_levels[x])

    def apply_fixes(self, module_path: str, fixes: List[str]) -> bool:
        """
        Apply suggested fixes to a module.
        
        Args:
            module_path: Path to the module to fix
            fixes: List of fixes to apply
            
        Returns:
            bool indicating success
        """
        try:
            with open(module_path, 'r') as f:
                content = f.read()
            
            # Apply fixes (implementation depends on fix type)
            for fix in fixes:
                # Implement fix application logic
                pass
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to apply fixes: {str(e)}")
            return False 