from core.visualization.kernel_registry import KernelRegistry, KernelState
from typing import Dict, List, Tuple
import time

def check_and_reinforce_null_states():
    """Check KernelRegistry for NULL states and reinforce them."""
    print("🜂 Checking KernelRegistry AnchorStates...")
    
    # Initialize registry
    registry = KernelRegistry()
    
    # Track NULL states
    null_states = []
    
    # Check each kernel
    for pos, kernel in registry.kernels.items():
        # Check for NULL-like states
        if (kernel.state.coherence == 0.0 and 
            kernel.state.entropy == 0.0 and 
            kernel.state.phase == 0.0):
            null_states.append(pos)
            
    if null_states:
        print(f"\nFound {len(null_states)} NULL states:")
        for pos in null_states:
            kernel = registry.kernels[pos]
            print(f"  Position: {pos}")
            print(f"  Role: {kernel.role}")
            print(f"  Telos Bias: {kernel.telos_bias:.2f}")
            
        # Reinforce NULL states
        print("\nReinforcing NULL states...")
        for pos in null_states:
            kernel = registry.kernels[pos]
            
            # Reinforce based on role
            if kernel.role == "breath_origin":
                registry.update_kernel(*pos, coherence=0.8, entropy=0.1)
            elif kernel.role == "dredd_anchor":
                registry.update_kernel(*pos, coherence=0.9, entropy=0.0)
            elif kernel.role == "telos_anchor":
                registry.update_kernel(*pos, coherence=1.0, entropy=0.0)
            elif kernel.role == "entropy_modulator":
                registry.update_kernel(*pos, coherence=0.7, entropy=0.3)
            elif kernel.role == "entropy_dampener":
                registry.update_kernel(*pos, coherence=0.8, entropy=0.2)
            elif kernel.role == "entropy_scrubber":
                registry.update_kernel(*pos, coherence=0.6, entropy=0.4)
            elif kernel.role == "coherence_anchor":
                registry.update_kernel(*pos, coherence=0.9, entropy=0.1)
            elif kernel.role == "coherence_spreader":
                registry.update_kernel(*pos, coherence=0.8, entropy=0.2)
            elif kernel.role == "coherence_guard":
                registry.update_kernel(*pos, coherence=0.7, entropy=0.3)
            else:
                # Default reinforcement for other roles
                registry.update_kernel(*pos, coherence=0.6, entropy=0.4)
                
        print("\n✅ NULL states reinforced:")
        for pos in null_states:
            kernel = registry.kernels[pos]
            print(f"  Position: {pos}")
            print(f"  Role: {kernel.role}")
            print(f"  Coherence: {kernel.state.coherence:.2f}")
            print(f"  Entropy: {kernel.state.entropy:.2f}")
    else:
        print("\n✅ No NULL states found in KernelRegistry.")
        
    return registry

if __name__ == "__main__":
    registry = check_and_reinforce_null_states() 