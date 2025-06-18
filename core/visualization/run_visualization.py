from kernel_registry import KernelRegistry
from kernel_visualizer import KernelVisualizer

def main():
    """Run the kernel lattice visualization."""
    # Create registry
    registry = KernelRegistry()
    
    # Create visualizer
    visualizer = KernelVisualizer()
    
    # Run visualization
    visualizer.run(registry)

if __name__ == "__main__":
    main() 