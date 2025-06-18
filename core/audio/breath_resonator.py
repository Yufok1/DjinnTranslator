import numpy as np
import sounddevice as sd
from typing import Dict, Tuple, List
import math
from kernel_registry import KernelRegistry, KernelDescriptor

class BreathResonator:
    """Maps kernel lattice states to sound, creating a sonic representation of the system."""
    
    # Base frequencies for different roles (in Hz)
    ROLE_FREQUENCIES = {
        "breath_origin": 440.0,      # A4 - fundamental
        "dredd_anchor": 110.0,       # A2 - deep judgment
        "telos_anchor": 880.0,       # A5 - high purpose
        "entropy_modulator": 587.33,  # D5 - entropy
        "entropy_dampener": 523.25,  # C5 - dampening
        "entropy_scrubber": 493.88,  # B4 - cleansing
        "coherence_anchor": 659.25,  # E5 - stability
        "coherence_spreader": 587.33, # D5 - spreading
        "coherence_guard": 523.25,   # C5 - guarding
        "memory_encoder": 783.99,    # G5 - memory
        "pattern_recognizer": 698.46, # F5 - patterns
        "knowledge_anchor": 659.25,  # E5 - knowledge
        "mutation_dispatcher": 880.0, # A5 - mutation
        "evolution_guide": 783.99,   # G5 - evolution
        "fixpoint_resolver": 698.46, # F5 - resolution
        "phase_synchronizer": 587.33, # D5 - sync
        "echo_amplifier": 523.25,    # C5 - echo
        "resonance_tuner": 493.88,   # B4 - resonance
        "pulse_coordinator": 440.0,  # A4 - pulse
        "recursive_node": 392.0      # G4 - basic recursion
    }
    
    # Harmonic relationships (frequency ratios)
    HARMONIC_RATIOS = {
        "unison": 1.0,
        "octave": 2.0,
        "perfect_fifth": 3/2,
        "perfect_fourth": 4/3,
        "major_third": 5/4,
        "minor_third": 6/5
    }
    
    def __init__(self, sample_rate: int = 44100):
        """Initialize the breath resonator."""
        self.sample_rate = sample_rate
        self.stream = sd.OutputStream(
            samplerate=sample_rate,
            channels=2,
            callback=self._audio_callback
        )
        self.stream.start()
        
        # Audio state
        self.current_phase = 0
        self.kernel_states = {}  # Dict[Tuple[int, int], Dict[str, float]]
        self.last_dredd_trigger = 0  # Time of last Dredd judgment
        self.judgment_ring = 0  # Judgment effect counter
        
    def _calculate_harmonic_relationships(self, registry: KernelRegistry) -> Dict[Tuple[int, int], List[float]]:
        """Calculate harmonic relationships between neighboring kernels."""
        harmonics = {}
        
        for pos, kernel in registry.kernels.items():
            base_freq = self.ROLE_FREQUENCIES.get(kernel.role, 440.0)
            harmonic_freqs = [base_freq]
            
            # Check neighbors for harmonic relationships
            for neighbor in kernel.neighbors:
                if neighbor in registry.kernels:
                    neighbor_kernel = registry.kernels[neighbor]
                    neighbor_freq = self.ROLE_FREQUENCIES.get(neighbor_kernel.role, 440.0)
                    
                    # Calculate frequency ratio
                    ratio = max(base_freq, neighbor_freq) / min(base_freq, neighbor_freq)
                    
                    # Find closest harmonic relationship
                    closest_ratio = min(self.HARMONIC_RATIOS.values(), 
                                     key=lambda x: abs(x - ratio))
                    
                    # Add harmonic frequency if within coherence threshold
                    if kernel.state.coherence > 0.7 and neighbor_kernel.state.coherence > 0.7:
                        harmonic_freqs.append(neighbor_freq * closest_ratio)
            
            harmonics[pos] = harmonic_freqs
            
        return harmonics
    
    def _generate_judgment_sound(self, t: np.ndarray) -> np.ndarray:
        """Generate judgment sound effect."""
        # Sub-bass strike
        strike_freq = 55.0  # A1
        strike = 0.5 * np.sin(2 * np.pi * strike_freq * t)
        
        # Exponential decay
        decay = np.exp(-10 * t)
        
        # Stereo ripple effect
        ripple = np.sin(2 * np.pi * 5 * t) * 0.3
        
        # Combine effects
        judgment = strike * decay
        return np.column_stack((judgment * (1 - ripple), judgment * (1 + ripple)))
    
    def _audio_callback(self, outdata, frames, time, status):
        """Generate audio samples based on kernel states."""
        if status:
            print(f"Audio callback status: {status}")
            
        # Generate time points
        t = np.linspace(0, frames/self.sample_rate, frames, endpoint=False)
        
        # Initialize output buffer
        outdata.fill(0)
        
        # Check for Dredd judgment
        dredd_triggered = False
        for pos, state in self.kernel_states.items():
            if state['role'] == 'dredd_anchor' and state['entropy'] > 0.8:
                dredd_triggered = True
                self.last_dredd_trigger = time.currentTime
                self.judgment_ring = 1.0
                break
        
        # Generate judgment sound if triggered
        if dredd_triggered:
            judgment_sound = self._generate_judgment_sound(t)
            outdata += judgment_sound
        
        # Generate sound for each kernel
        for pos, state in self.kernel_states.items():
            # Get harmonic frequencies
            harmonic_freqs = self._calculate_harmonic_relationships(registry).get(pos, [])
            
            # Generate sound for each harmonic frequency
            for freq in harmonic_freqs:
                # Calculate frequency based on phase
                mod_freq = freq * (1.0 + 0.1 * math.sin(state['phase'] * 2 * math.pi))
                
                # Calculate amplitude based on coherence and entropy
                amp = 0.3 * (1.0 - state['entropy']) * state['coherence']
                
                # Generate sine wave
                wave = amp * np.sin(2 * np.pi * mod_freq * t)
                
                # Add entropy-based distortion
                if state['entropy'] > 0.3:
                    distortion = state['entropy'] * 0.5
                    wave = np.tanh(wave * (1 + distortion))
                
                # Calculate stereo panning based on position
                pan = (pos[1] - 4) / 4.0  # -1 to 1 based on x position
                left_gain = 0.5 * (1 - pan)
                right_gain = 0.5 * (1 + pan)
                
                # Add to output buffer
                outdata[:, 0] += wave * left_gain
                outdata[:, 1] += wave * right_gain
        
        # Normalize output
        max_val = np.max(np.abs(outdata))
        if max_val > 1.0:
            outdata /= max_val
            
    def update_states(self, registry: KernelRegistry):
        """Update kernel states for audio generation."""
        self.kernel_states = {}
        for pos, kernel in registry.kernels.items():
            self.kernel_states[pos] = {
                'role': kernel.role,
                'phase': kernel.state.phase,
                'entropy': kernel.state.entropy,
                'coherence': kernel.state.coherence,
                'telos_bias': kernel.telos_bias
            }
            
    def stop(self):
        """Stop the audio stream."""
        self.stream.stop()
        self.stream.close() 