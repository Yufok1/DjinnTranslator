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

import time
import random
from breath_scheduler import BreathScheduler

def simulate_system_state() -> tuple[float, float]:
    """Simulate system entropy and coherence values."""
    # Simulate some random fluctuations
    entropy = random.uniform(0.3, 0.9)
    coherence = random.uniform(0.4, 0.95)
    
    # Add some correlation between entropy and coherence
    if entropy > 0.7:
        coherence *= 0.8  # High entropy tends to reduce coherence
    elif entropy < 0.4:
        coherence *= 1.2  # Low entropy tends to increase coherence
        
    return entropy, coherence

def visualize_breath_state(phase: float, frequency: float, depth: float, 
                         entropy: float, coherence: float):
    """Visualize the current breath state using ASCII art."""
    # Create phase indicator
    phase_pos = int(phase * 20)
    phase_line = [' '] * 20
    phase_line[phase_pos] = '●'
    
    # Create frequency indicator
    freq_pos = int(frequency * 10)
    freq_line = [' '] * 10
    freq_line[freq_pos] = '↑'
    
    # Create depth indicator
    depth_pos = int(depth * 10)
    depth_line = [' '] * 10
    depth_line[depth_pos] = '↓'
    
    # Create entropy indicator
    entropy_pos = int(entropy * 10)
    entropy_line = [' '] * 10
    entropy_line[entropy_pos] = 'E'
    
    # Create coherence indicator
    coherence_pos = int(coherence * 10)
    coherence_line = [' '] * 10
    coherence_line[coherence_pos] = 'C'
    
    # Print visualization
    print("\nBreath State Visualization:")
    print(f"Phase:    [{'|'.join(phase_line)}]")
    print(f"Freq:     [{'|'.join(freq_line)}]")
    print(f"Depth:    [{'|'.join(depth_line)}]")
    print(f"Entropy:  [{'|'.join(entropy_line)}]")
    print(f"Coherence:[{'|'.join(coherence_line)}]")
    print("-" * 50)

def test_breath_scheduler():
    """Test the breath scheduler with simulated system states."""
    scheduler = BreathScheduler()
    
    print("Testing Breath Scheduler...")
    print("Phase | Frequency | Depth | Entropy | Coherence")
    print("-" * 50)
    
    # Run for 10 seconds of simulated time
    start_time = time.time()
    while time.time() - start_time < 10:
        # Calculate delta time
        current_time = time.time()
        delta_time = current_time - start_time
        
        # Get simulated system state
        entropy, coherence = simulate_system_state()
        
        # Update scheduler
        phase, frequency, depth = scheduler.update(entropy, coherence, delta_time)
        
        # Print current state
        print(f"{phase:.2f} | {frequency:.2f} | {depth:.2f} | {entropy:.2f} | {coherence:.2f}")
        
        # Visualize current state
        visualize_breath_state(phase, frequency, depth, entropy, coherence)
        
        # Get breath pattern
        pattern = scheduler.get_breath_pattern()
        if pattern:
            print("\nBreath Pattern Analysis:")
            print(f"Average Frequency: {pattern['avg_frequency']:.2f}")
            print(f"Average Depth: {pattern['avg_depth']:.2f}")
            print(f"Entropy Trend: {pattern['entropy_trend']:.2f}")
            print(f"Coherence Trend: {pattern['coherence_trend']:.2f}")
            print(f"Breath Count: {pattern['breath_count']}")
            print("-" * 50)
            
        time.sleep(0.5)  # Longer delay to make output readable
        
    print("\nTest Complete")

if __name__ == "__main__":
    test_breath_scheduler() 