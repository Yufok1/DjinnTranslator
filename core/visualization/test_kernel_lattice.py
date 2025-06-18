import time
from kernel_registry import KernelRegistry

def visualize_lattice_state(registry: KernelRegistry):
    """Visualize the current state of the kernel lattice."""
    state = registry.get_lattice_state()
    
    print("\nKernel Lattice State:")
    print("=" * 50)
    
    # Print header
    print("Role".ljust(20), "Phase".ljust(10), "Freq".ljust(10), 
          "Depth".ljust(10), "Entropy".ljust(10), "Coherence")
    print("-" * 50)
    
    # Print each kernel's state
    for (row, col), kernel_state in state.items():
        print(
            f"{kernel_state['role']}".ljust(20),
            f"{kernel_state['phase']:.2f}".ljust(10),
            f"{kernel_state['frequency']:.2f}".ljust(10),
            f"{kernel_state['depth']:.2f}".ljust(10),
            f"{kernel_state['entropy']:.2f}".ljust(10),
            f"{kernel_state['coherence']:.2f}"
        )
        
def test_kernel_lattice():
    """Test the kernel lattice with simulated system states."""
    registry = KernelRegistry()
    
    print("Testing Kernel Lattice...")
    print("Initializing 9×9 grid with specialized kernels...")
    
    # Run for 10 seconds of simulated time
    start_time = time.time()
    while time.time() - start_time < 10:
        # Calculate delta time
        current_time = time.time()
        delta_time = current_time - start_time
        
        # Update entropy and coherence for each kernel
        for row in range(9):
            for col in range(9):
                # Simulate some state changes
                entropy = (row + col) / 16.0  # Varies by position
                coherence = 1.0 - entropy  # Inverse relationship
                
                registry.update_kernel(row, col, entropy=entropy, coherence=coherence)
        
        # Propagate breath through the lattice
        registry.propagate_breath(delta_time)
        
        # Visualize current state
        visualize_lattice_state(registry)
        
        # Small delay to make output readable
        time.sleep(0.5)
        
    print("\nTest Complete")

if __name__ == "__main__":
    test_kernel_lattice() 