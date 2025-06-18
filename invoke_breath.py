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