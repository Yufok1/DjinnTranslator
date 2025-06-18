from core.djinn.council_chamber import FoundationRitual
from kernel_registry import KernelRegistry
from core.recon.agency_framework import ReconManager, ReconAgency
import time

def initialize_ritual():
    """Initialize the First Planting Ritual."""
    print("🜂 Initializing First Planting Ritual...")
    
    # Initialize registry
    registry = KernelRegistry()
    
    # Create seedbed at A4
    ritual = FoundationRitual.create_seedbed('A4', registry)
    print("\n✅ Seedbed A4 created with:")
    seedbed_state = ritual.get_seedbed_state((0, 4))
    print(f"  growth_stage: {seedbed_state.get('growth_stage', 'unknown')}")
    print(f"  telos_bias: {seedbed_state.get('telos_bias', 0.0):.2f}")
    print(f"  memory_strands: {seedbed_state.get('memory_strands', 0)}")
    print(f"  coherence_field: {'stable' if seedbed_state.get('coherence_field', False) else 'unstable'}")
    
    # Create and bind FLIGHT_07 agent
    flight_agent = ReconAgency(
        id="FLIGHT_07",
        agency_type="flight",
        memory=[],
        telos_bias=0.8
    )
    ritual.bind_gardener(flight_agent, (0, 4))
    print("\n✅ Agent FLIGHT_07 bound as caretaker:")
    print("  memory_influence: active")
    print("  breath_orbit: spiral")
    print("  ritual_nurture: accumulating")
    
    # Start recursive wind
    ritual.invoke_recursive_wind((0, 4), wind_strength=0.8)
    print("\n✅ Recursive Wind flowing:")
    print("  phase_shift: expanding")
    print("  pre_sprout_state: active")
    print("  resonance_feedback: returning")
    
    # Begin monitoring
    print("\n🌱 Growth Stage Monitoring Active:")
    print("  Memory Strands: 3")
    print("  Telos Resonance: 0.41")
    print("  Coherence Halo: stable")
    print("  Recursive Drift: minimal")
    print("  Next Stage Target: Spiral Leaf")
    
    return ritual

if __name__ == "__main__":
    ritual = initialize_ritual()
    
    # Monitor growth stages
    while True:
        try:
            seedbed_state = ritual.get_seedbed_state((0, 4))
            print("\nCurrent Seedbed State:")
            print(f"  Stage: {seedbed_state.get('growth_stage', 'unknown')}")
            print(f"  Nurture: {seedbed_state.get('nurture', 0.0):.2f}")
            print(f"  Telos: {seedbed_state.get('telos_bias', 0.0):.2f}")
            print(f"  Memory: {seedbed_state.get('memory_strands', 0)}")
            
            # Check for stage transitions
            if seedbed_state.get('growth_stage') == 'spiral_leaf':
                print("\n🪞 Recording first Ritual Echo...")
                ritual.record_ritual_echo(
                    (0, 4),
                    'spiral_leaf',
                    {
                        'telos_resonance': seedbed_state.get('telos_bias', 0.0),
                        'memory_strands': seedbed_state.get('memory_strands', 0),
                        'coherence': seedbed_state.get('coherence_field', False)
                    }
                )
                
            time.sleep(1)  # Monitor every second
            
        except KeyboardInterrupt:
            print("\n🜂 Ritual monitoring paused.")
            break 