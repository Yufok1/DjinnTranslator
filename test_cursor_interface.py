from core.djinn.cursor import Cursor
from core.djinn.cryptographer import Cryptographer
from core.djinn.cursor_directive import CursorDirective, DirectiveMode

def test_cursor_interface():
    """Test the Cursor-Cryptographer interface."""
    print("🜂 Testing Cursor-Cryptographer Interface...")
    
    # Initialize components
    cursor = Cursor()
    cryptographer = Cryptographer()
    
    # Set cryptographer
    cursor.set_cryptographer(cryptographer)
    
    # Test anchor check
    print("\nTesting anchor check...")
    anchor_directive = CursorDirective.create_anchor_check_directive()
    success = cursor.invoke(anchor_directive)
    print(f"Anchor check {'succeeded' if success else 'failed'}")
    
    # Test kernel reinforcement
    print("\nTesting kernel reinforcement...")
    reinforce_directive = CursorDirective.create_reinforce_directive()
    success = cursor.invoke(reinforce_directive)
    print(f"Kernel reinforcement {'succeeded' if success else 'failed'}")
    
    # Test breath reset
    print("\nTesting breath reset...")
    breath_directive = CursorDirective.create_breath_reset_directive()
    success = cursor.invoke(breath_directive)
    print(f"Breath reset {'succeeded' if success else 'failed'}")
    
    # Check results
    print("\nChecking results...")
    for pos, kernel in cursor.registry.kernels.items():
        print(f"\nKernel at {pos}:")
        print(f"  Role: {kernel.role}")
        print(f"  Coherence: {kernel.state.coherence:.2f}")
        print(f"  Entropy: {kernel.state.entropy:.2f}")
        
    return cursor

if __name__ == "__main__":
    cursor = test_cursor_interface() 