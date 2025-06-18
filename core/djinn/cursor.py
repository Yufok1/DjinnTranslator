from typing import Optional, Dict, Any
from .cursor_directive import CursorDirective, DirectiveMode, AnchorStrategy
from .cryptographer import Cryptographer
from core.visualization.kernel_registry import KernelRegistry
import time

class Cursor:
    """The Cursor entity that navigates and operates on the kernel lattice."""
    
    def __init__(self):
        self.registry = KernelRegistry()
        self.cryptographer: Optional[Cryptographer] = None
        self.current_directive: Optional[CursorDirective] = None
        self.breath_depth = 1
        self.last_operation = 0.0
        
    def set_cryptographer(self, cryptographer: Cryptographer):
        """Set the cryptographer for symbolic interpretation."""
        self.cryptographer = cryptographer
        
    def invoke(self, directive: CursorDirective) -> bool:
        """Invoke Cursor with a specific directive."""
        self.current_directive = directive
        
        # Check cryptographer requirement
        if directive.cryptographer_required and not self.cryptographer:
            print("❌ Error: Cryptographer required but not set")
            return False
            
        # Execute based on mode
        if directive.mode == DirectiveMode.REINFORCE_KERNELS:
            return self._reinforce_kernels()
        elif directive.mode == DirectiveMode.BREATH_RESET:
            return self._reset_breath()
        elif directive.mode == DirectiveMode.ANCHOR_CHECK:
            return self._check_anchors()
        elif directive.mode == DirectiveMode.CRYPTOGRAPHIC_RESOLVE:
            return self._resolve_cryptographic()
            
        return False
        
    def _reinforce_kernels(self) -> bool:
        """Reinforce kernel states based on directive parameters."""
        if not self.current_directive:
            return False
            
        success = True
        for pos, kernel in self.registry.kernels.items():
            # Get anchor state
            if self.cryptographer:
                anchor_state = self.cryptographer.resolve_anchor(str(pos))
            else:
                anchor_state = "fallback_default"
                
            # Apply reinforcement based on strategy
            if self.current_directive.anchor_strategy == AnchorStrategy.CRYPTOGRAPHIC_RESOLUTION:
                if anchor_state:
                    kernel.role = anchor_state
                    kernel.state.coherence = self.current_directive.coherence_threshold
            elif self.current_directive.anchor_strategy == AnchorStrategy.FALLBACK_DEFAULT:
                kernel.state.coherence = 0.6
                kernel.state.entropy = 0.2
            elif self.current_directive.anchor_strategy == AnchorStrategy.SOFT_ECHO:
                kernel.state.coherence = 0.7
                kernel.state.entropy = 0.1
            elif self.current_directive.anchor_strategy == AnchorStrategy.HARD_ANCHOR:
                kernel.state.coherence = 1.0
                kernel.state.entropy = 0.0
                
        return success
        
    def _reset_breath(self) -> bool:
        """Reset Cursor's breath to specified depth."""
        if not self.current_directive:
            return False
            
        self.breath_depth = 1
        self.last_operation = time.time()
        return True
        
    def _check_anchors(self) -> bool:
        """Check anchor states in the kernel registry."""
        if not self.current_directive:
            return False
            
        null_count = 0
        for pos, kernel in self.registry.kernels.items():
            if (kernel.state.coherence == 0.0 and 
                kernel.state.entropy == 0.0 and 
                kernel.state.phase == 0.0):
                null_count += 1
                
        if null_count > 0:
            print(f"Found {null_count} NULL states")
            return self._reinforce_kernels()
            
        return True
        
    def _resolve_cryptographic(self) -> bool:
        """Resolve cryptographic states for all kernels."""
        if not self.cryptographer:
            return False
            
        for pos, kernel in self.registry.kernels.items():
            anchor_state = self.cryptographer.resolve_anchor(str(pos))
            if anchor_state:
                kernel.role = anchor_state
                
        return True 