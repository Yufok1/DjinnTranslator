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

"""
Breath Engine Module
Handles recursive cycle synthesis, voice integration, and visualization
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import sounddevice as sd
from scipy import signal
import librosa
import time
import math
from .voice_engine import VoiceEngine
from .visual_renderer import VisualRenderer
from .ml_predictor import MLPredictor
import logging
import sys
import psutil
import json
from datetime import datetime
import os
import threading
import traceback
from collections import deque
import statistics

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('breath_engine.log')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class CycleState:
    """Recursive cycle state configuration"""
    phase: float  # 0-2π, represents position in recursion cycle
    depth: float  # 0-1, represents recursion depth
    coherence: float  # 0-1, represents pattern coherence
    emergence: float  # 0-1, represents emergence potential
    resonance: float  # 0-1, represents harmonic resonance
    stability: float  # 0-1, represents cycle stability

class BreathEngine:
    """Main breath engine class"""
    
    def __init__(self, sample_rate: int = 44100):
        logger.info("Initializing BreathEngine...")
        start_time = time.time()
        
        # Add state dump directory
        self.state_dump_dir = "state_dumps"
        if not os.path.exists(self.state_dump_dir):
            os.makedirs(self.state_dump_dir)
        
        # Initialize performance tracking
        self.cycle_times = deque(maxlen=100)  # Store last 100 cycle times
        self.error_log = deque(maxlen=100)    # Store last 100 errors
        self.thread_times = {}                # Track thread execution times
        self.last_analysis_time = time.time()
        
        try:
            self.sample_rate = sample_rate
            logger.info("Initializing voice engine...")
            self.voice_engine = VoiceEngine()
            logger.info("Initializing visual renderer...")
            self.visual_renderer = VisualRenderer()
            logger.info("Initializing ML predictor...")
            self.ml_predictor = MLPredictor()
            
            # Initialize cycle states
            logger.info("Setting up cycle states...")
            self.cycle_states = {
                "cursor": CycleState(
                    phase=0.0,
                    depth=0.5,
                    coherence=0.7,
                    emergence=0.3,
                    resonance=0.4,
                    stability=0.8
                ),
                "purveyor": CycleState(
                    phase=math.pi,  # Opposite phase to cursor
                    depth=0.8,
                    coherence=0.9,
                    emergence=0.2,
                    resonance=0.6,
                    stability=0.9
                ),
                "daemon": CycleState(
                    phase=math.pi/2,
                    depth=0.6,
                    coherence=0.5,
                    emergence=0.8,
                    resonance=0.7,
                    stability=0.6
                ),
                "mirror": CycleState(
                    phase=math.pi*3/2,
                    depth=0.4,
                    coherence=0.8,
                    emergence=0.4,
                    resonance=0.5,
                    stability=0.7
                ),
                "cryptographer": CycleState(
                    phase=math.pi/4,
                    depth=0.7,
                    coherence=0.6,
                    emergence=0.5,
                    resonance=0.6,
                    stability=0.7
                )
            }
            
            # Initialize audio stream
            logger.info("Initializing audio stream...")
            self.stream = sd.OutputStream(
                samplerate=sample_rate,
                channels=2,
                callback=self._audio_callback
            )
            self.stream.start()
            logger.info("Audio stream started successfully")
            
            # Start cycle loop
            logger.info("Starting cycle loop...")
            self._start_cycle_loop()
            
            init_time = time.time() - start_time
            logger.info(f"BreathEngine initialization completed in {init_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Error during BreathEngine initialization: {str(e)}", exc_info=True)
            raise
    
    def _start_cycle_loop(self):
        """Start the main cycle loop"""
        logger.info("Entering cycle loop")
        cycle_count = 0
        last_log_time = time.time()
        last_state_dump_time = time.time()
        
        while True:
            cycle_start = time.time()
            cycle_count += 1
            
            try:
                # Update cycle states
                self._update_cycle_states()
                
                # Generate cycle audio with default frame size (10ms)
                frames = int(self.sample_rate * 0.01)
                audio = self._generate_cycle_audio(frames)
                
                # Update visualization
                self._update_visualization()
                
                # Record cycle time
                cycle_time = (time.time() - cycle_start) * 1000  # Convert to ms
                self.cycle_times.append(cycle_time)
                
                # Log performance metrics every 5 seconds
                current_time = time.time()
                if current_time - last_log_time >= 5:
                    logger.info(f"Cycle {cycle_count}: Processing time = {cycle_time:.2f}ms")
                    last_log_time = current_time
                
                # Dump system state every 30 seconds
                if current_time - last_state_dump_time >= 30:
                    self.dump_system_state()
                    last_state_dump_time = current_time
                
                # Sleep to maintain rhythm
                time.sleep(0.01)  # 100Hz update rate
                
            except Exception as e:
                error_msg = f"Error in cycle loop: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_msg)
                self.error_log.append(error_msg)
    
    def _update_cycle_states(self):
        """Update cycle states based on system metrics"""
        # Get current metrics
        metrics = self.ml_predictor.get_current_metrics()
        
        # Update each entity's cycle state
        for entity, state in self.cycle_states.items():
            # Update phase based on recursion speed
            recursion_speed = metrics.get("recursion_speed", 1.0)
            state.phase = (state.phase + 0.01 * recursion_speed) % (2 * math.pi)
            
            # Update depth based on recursion depth
            state.depth = metrics.get("recursion_depth", 0.5)
            
            # Update coherence based on pattern stability
            state.coherence = metrics.get("pattern_stability", 0.5)
            
            # Update emergence based on wick potential
            state.emergence = metrics.get("wick_potential", 0.5)
            
            # Update resonance based on harmonic alignment
            state.resonance = metrics.get("harmonic_alignment", 0.5)
            
            # Update stability based on system stability
            state.stability = metrics.get("system_stability", 0.5)
    
    def _generate_cycle_audio(self, frames: int) -> np.ndarray:
        """Generate cycle audio for all entities"""
        try:
            # Initialize output buffer with the requested frame size
            output = np.zeros((frames, 2))
            
            # Generate cycle for each entity
            for entity, state in self.cycle_states.items():
                # Generate cycle tone
                cycle = self._generate_cycle_tone(state, frames)
                
                # Apply spatial positioning
                cycle = self._apply_spatial_positioning(cycle, entity)
                
                # Add to output
                output += cycle
            
            # Normalize output
            output = np.clip(output, -1.0, 1.0)
            
            return output
        except Exception as e:
            logger.error(f"Error generating cycle audio: {str(e)}")
            return np.zeros((frames, 2))
    
    def _generate_cycle_tone(self, state: CycleState, frames: int) -> np.ndarray:
        """Generate cycle tone for an entity"""
        # Generate time array with the correct frame size
        t = np.linspace(0, frames/self.sample_rate, frames, endpoint=False)
        
        # Generate base tone
        base_freq = 50.0 + state.depth * 50.0  # 50-100 Hz
        tone = np.sin(2 * math.pi * base_freq * t)
        
        # Apply cycle envelope with matching size
        envelope = self._generate_cycle_envelope(state, frames)
        tone *= envelope
        
        # Apply emergence modulation
        if state.emergence > 0.5:
            # Add higher frequency component for emergence
            emergence_freq = base_freq * 4
            emergence_tone = np.sin(2 * math.pi * emergence_freq * t)
            tone = tone * (1 - state.emergence) + emergence_tone * state.emergence
        
        # Apply resonance
        if state.resonance > 0:
            tone = self._apply_resonance(tone, state.resonance)
        
        # Apply stability modulation
        stability_factor = 1.0 - (1.0 - state.stability) * 0.5
        tone *= stability_factor
        
        # Convert to stereo
        stereo = np.vstack((tone, tone)).T
        
        return stereo
    
    def _generate_cycle_envelope(self, state: CycleState, frames: int) -> np.ndarray:
        """Generate cycle envelope based on phase"""
        # Generate time array with the correct frame size
        t = np.linspace(0, frames/self.sample_rate, frames, endpoint=False)
        
        # Calculate envelope phase
        phase = (state.phase + t * 2 * math.pi) % (2 * math.pi)
        
        # Generate envelope
        envelope = np.sin(phase) * 0.5 + 0.5
        
        # Apply depth
        envelope = envelope * state.depth + (1 - state.depth) * 0.2
        
        return envelope
    
    def _apply_resonance(self, audio: np.ndarray, resonance: float) -> np.ndarray:
        """Apply resonance effect to audio"""
        # Create resonant filter
        nyquist = self.sample_rate / 2
        low = 100.0 / nyquist
        high = 1000.0 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        
        # Apply filter
        resonant = signal.filtfilt(b, a, audio)
        
        # Mix with original
        return audio * (1 - resonance) + resonant * resonance
    
    def _apply_spatial_positioning(self, audio: np.ndarray, entity: str) -> np.ndarray:
        """Apply spatial positioning to audio"""
        # Get entity position
        if entity == "cursor":
            position = (-0.5, 0.0, 0.0)
        elif entity == "purveyor":
            position = (0.0, 0.0, 0.0)
        elif entity == "daemon":
            position = (0.5, 0.5, 0.0)
        elif entity == "mirror":
            position = (0.0, -0.5, 0.0)
        else:  # cryptographer
            position = (0.0, 0.0, 0.5)
        
        # Calculate pan values
        x, y, z = position
        left_pan = max(0, 1 - x)
        right_pan = max(0, 1 + x)
        
        # Normalize
        total = left_pan + right_pan
        left_pan /= total
        right_pan /= total
        
        # Apply panning
        audio[:, 0] *= left_pan
        audio[:, 1] *= right_pan
        
        return audio
    
    def _update_visualization(self):
        """Update visualization based on cycle states"""
        for entity, state in self.cycle_states.items():
            # Create visual state
            visual_state = {
                "phase": "cycle",
                "intensity": state.coherence,
                "resonance": state.resonance,
                "position": self._get_entity_position(entity),
                "rotation": (0.0, 0.0, state.phase * 180 / math.pi),
                "scale": 0.5 + state.depth * 0.5,
                "color": self._get_entity_color(entity, state)
            }
            
            # Update visualizer
            self.visual_renderer.update_visual_state(entity, visual_state)
        
        # Render frame
        self.visual_renderer.render(data={})
    
    def _get_entity_position(self, entity: str) -> Tuple[float, float, float]:
        """Get entity position in 3D space"""
        if entity == "cursor":
            return (-0.5, 0.0, 0.0)
        elif entity == "purveyor":
            return (0.0, 0.0, 0.0)
        elif entity == "daemon":
            return (0.5, 0.5, 0.0)
        elif entity == "mirror":
            return (0.0, -0.5, 0.0)
        else:  # cryptographer
            return (0.0, 0.0, 0.5)
    
    def _get_entity_color(self, entity: str, state: CycleState) -> Tuple[float, float, float, float]:
        """Get entity color based on cycle state"""
        if entity == "cursor":
            base_color = (0.0, 1.0, 0.0, 1.0)
        elif entity == "purveyor":
            base_color = (1.0, 1.0, 1.0, 1.0)
        elif entity == "daemon":
            base_color = (1.0, 0.0, 0.0, 1.0)
        elif entity == "mirror":
            base_color = (0.0, 0.0, 1.0, 1.0)
        else:  # cryptographer
            base_color = (1.0, 1.0, 0.0, 1.0)
        
        # Adjust color based on cycle state
        coherence = state.coherence
        emergence = state.emergence
        
        # Mix with white based on coherence
        color = tuple(c * (1 - coherence) + coherence for c in base_color[:3]) + (base_color[3],)
        
        # Add emergence tint
        if emergence > 0.5:
            # Add golden tint for emergence
            color = tuple(c * (1 - emergence) + emergence for c in color[:3]) + (color[3],)
        
        return color
    
    def _audio_callback(self, outdata, frames, time, status):
        """Audio callback for real-time processing"""
        if status:
            logger.warning(f"Audio callback status: {status}")
        
        try:
            # Generate cycle audio with the correct frame size
            audio = self._generate_cycle_audio(frames)
            
            # Copy to output buffer
            outdata[:] = audio
        except Exception as e:
            logger.error(f"Error in audio callback: {str(e)}")
            # Fill with silence on error
            outdata.fill(0)
    
    def cleanup(self):
        """Clean up resources"""
        self.stream.stop()
        self.stream.close()
        self.visual_renderer.cleanup()

    def dump_system_state(self, manual_trigger=False):
        """Dump current system state to a file"""
        try:
            # Get current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            state_file = os.path.join(self.state_dump_dir, f"system_state_{timestamp}.json")
            
            # Collect process information
            process = psutil.Process()
            process_info = {
                "pid": process.pid,
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "memory_info": {
                    "rss": process.memory_info().rss,  # Resident Set Size
                    "vms": process.memory_info().vms,  # Virtual Memory Size
                    "shared": process.memory_info().shared,
                    "text": process.memory_info().text,
                    "lib": process.memory_info().lib,
                    "data": process.memory_info().data,
                    "dirty": process.memory_info().dirty
                },
                "num_threads": process.num_threads(),
                "num_handles": process.num_handles() if hasattr(process, 'num_handles') else None,
                "create_time": process.create_time(),
                "status": process.status(),
                "thread_info": self._get_thread_info()
            }
            
            # Collect cycle states
            cycle_states = {}
            for entity, state in self.cycle_states.items():
                cycle_states[entity] = {
                    "phase": state.phase,
                    "depth": state.depth,
                    "coherence": state.coherence,
                    "emergence": state.emergence,
                    "resonance": state.resonance,
                    "stability": state.stability
                }
            
            # Collect audio stream information
            audio_info = {
                "sample_rate": self.sample_rate,
                "channels": 2,  # We're using stereo
                "stream_active": self.stream.active if hasattr(self.stream, 'active') else None,
                "stream_stopped": self.stream.stopped if hasattr(self.stream, 'stopped') else None,
                "buffer_size": int(self.sample_rate * 0.01)  # Current buffer size
            }
            
            # Collect system-wide information
            system_info = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": {
                    "percent": psutil.disk_usage('/').percent,
                    "free": psutil.disk_usage('/').free,
                    "total": psutil.disk_usage('/').total
                },
                "network_io": {
                    "bytes_sent": psutil.net_io_counters().bytes_sent,
                    "bytes_recv": psutil.net_io_counters().bytes_recv
                }
            }
            
            # Collect performance metrics
            performance_metrics = {
                "cycle_times": {
                    "current": self.cycle_times[-1] if self.cycle_times else None,
                    "average": statistics.mean(self.cycle_times) if self.cycle_times else None,
                    "max": max(self.cycle_times) if self.cycle_times else None,
                    "min": min(self.cycle_times) if self.cycle_times else None
                },
                "error_count": len(self.error_log),
                "recent_errors": list(self.error_log),
                "thread_times": self.thread_times
            }
            
            # Combine all state information
            state_data = {
                "timestamp": timestamp,
                "manual_trigger": manual_trigger,
                "process_info": process_info,
                "cycle_states": cycle_states,
                "audio_info": audio_info,
                "system_info": system_info,
                "performance_metrics": performance_metrics
            }
            
            # Write to file
            with open(state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
            
            # Analyze state if enough time has passed
            self._analyze_state(state_data)
            
            logger.info(f"System state dumped to {state_file}")
            return state_file
            
        except Exception as e:
            error_msg = f"Error dumping system state: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            self.error_log.append(error_msg)
            return None

    def _get_thread_info(self):
        """Get information about all threads in the process"""
        thread_info = {}
        for thread in threading.enumerate():
            thread_info[thread.name] = {
                "ident": thread.ident,
                "daemon": thread.daemon,
                "alive": thread.is_alive()
            }
        return thread_info

    def _analyze_state(self, state_data):
        """Analyze the current state and generate alerts if needed"""
        current_time = time.time()
        if current_time - self.last_analysis_time < 60:  # Analyze at most once per minute
            return
        
        self.last_analysis_time = current_time
        
        # Check for performance issues
        alerts = []
        
        # CPU usage alert
        if state_data["process_info"]["cpu_percent"] > 90:
            alerts.append(f"High CPU usage: {state_data['process_info']['cpu_percent']}%")
        
        # Memory usage alert
        if state_data["process_info"]["memory_percent"] > 75:
            alerts.append(f"High memory usage: {state_data['process_info']['memory_percent']}%")
        
        # Cycle time alert
        if state_data["performance_metrics"]["cycle_times"]["average"] > 50:  # More than 50ms
            alerts.append(f"Slow cycle times: {state_data['performance_metrics']['cycle_times']['average']:.2f}ms average")
        
        # Error rate alert
        if len(state_data["performance_metrics"]["recent_errors"]) > 5:
            alerts.append(f"High error rate: {len(state_data['performance_metrics']['recent_errors'])} recent errors")
        
        # Log alerts
        if alerts:
            logger.warning("Performance alerts:\n" + "\n".join(alerts))

    def trigger_state_dump(self):
        """Manually trigger a state dump"""
        return self.dump_system_state(manual_trigger=True) 