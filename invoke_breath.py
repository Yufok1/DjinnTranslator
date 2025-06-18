from core.djinn.cursor_breath import CursorBreath

def invoke_breath_reset():
    """Invoke Cursor breath reset."""
    print("🜂 Invoking Cursor Breath Reset...")
    
    # Initialize breath manager
    breath = CursorBreath()
    
    # Reset to depth 1
    breath.reset_breath(depth=1)
    
    # Get current state
    state = breath.get_breath_state()
    
    print("\n✅ Breath Reset Complete:")
    print(f"  Depth: {state['depth']}")
    print(f"  Resonance: {state['resonance']:.2f}")
    print(f"  Echo Count: {state['echo_count']}")
    print(f"  Active Riddles: {state['active_riddles']}")
    
    return breath

if __name__ == "__main__":
    breath = invoke_breath_reset() 