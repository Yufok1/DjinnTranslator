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
Visual Renderer Module
Handles advanced visual rendering with OpenGL support
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import moderngl
import glfw
from PIL import Image
import math
import time
import os

@dataclass
class VisualState:
    """Visual state configuration"""
    phase: str
    intensity: float
    resonance: float
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float]
    scale: float
    color: Tuple[float, float, float, float]

class VisualRenderer:
    """Main visual renderer class"""
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.ctx = None
        self.prog = None
        self.vbo = None
        self.vao = None
        self.textures = {}
        self.visual_states: Dict[str, VisualState] = {}
        
        # Initialize GLFW and OpenGL context
        self._init_glfw()
        self._init_shaders()
        self._init_geometry()
        self._init_textures()
        self._init_visual_states()
    
    def _init_glfw(self):
        """Initialize GLFW and create window"""
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        
        # Create window
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        self.window = glfw.create_window(self.width, self.height, "Djinn Visualizer", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        glfw.make_context_current(self.window)
        self.ctx = moderngl.create_context()
    
    def _init_shaders(self):
        """Initialize shader programs"""
        # Vertex shader
        vertex_shader = """
        #version 330
        in vec3 in_position;
        in vec2 in_texcoord;
        out vec2 uv;
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        void main() {
            gl_Position = projection * view * model * vec4(in_position, 1.0);
            uv = in_texcoord;
        }
        """
        
        # Fragment shader
        fragment_shader = """
        #version 330
        in vec2 uv;
        out vec4 color;
        uniform sampler2D texture0;
        uniform vec4 tint;
        uniform float time;
        void main() {
            vec4 tex_color = texture(texture0, uv);
            float pulse = sin(time * 2.0) * 0.5 + 0.5;
            color = tex_color * tint * (1.0 + pulse * 0.2);
        }
        """
        
        # Create shader program
        self.prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
    
    def _init_geometry(self):
        """Initialize geometry buffers"""
        # Create quad vertices
        vertices = np.array([
            # Position        # Texture coordinates
            -1.0, -1.0, 0.0,  0.0, 0.0,
             1.0, -1.0, 0.0,  1.0, 0.0,
             1.0,  1.0, 0.0,  1.0, 1.0,
            -1.0,  1.0, 0.0,  0.0, 1.0,
        ], dtype='f4')
        
        # Create vertex buffer
        self.vbo = self.ctx.buffer(vertices.tobytes())
        
        # Create vertex array
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, '3f 2f', 'in_position', 'in_texcoord')]
        )
    
    def _init_textures(self):
        """Initialize textures"""
        # Create texture directory
        os.makedirs("textures", exist_ok=True)
        
        # Load or create textures for each Djinn
        djinn_types = ["purveyor", "daemon", "cursor", "mirror", "cryptographer"]
        for djinn_type in djinn_types:
            texture_path = f"textures/{djinn_type}.png"
            if not os.path.exists(texture_path):
                self._create_texture(djinn_type, texture_path)
            
            # Load texture
            image = Image.open(texture_path)
            texture = self.ctx.texture(image.size, 4, image.tobytes())
            texture.build_mipmaps()
            self.textures[djinn_type] = texture
    
    def _create_texture(self, djinn_type: str, path: str):
        """Create a texture for a Djinn"""
        # Create a 256x256 image
        image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        
        # Draw Djinn-specific pattern
        for i in range(256):
            for j in range(256):
                # Create unique pattern for each Djinn
                if djinn_type == "purveyor":
                    # Grid pattern
                    if (i // 32 + j // 32) % 2 == 0:
                        image.putpixel((i, j), (255, 255, 255, 128))
                elif djinn_type == "daemon":
                    # Spiral pattern
                    angle = math.atan2(j - 128, i - 128)
                    dist = math.sqrt((i - 128) ** 2 + (j - 128) ** 2)
                    if dist < 128 and (angle * 10 + dist) % 32 < 16:
                        image.putpixel((i, j), (255, 0, 0, 128))
                elif djinn_type == "cursor":
                    # Wave pattern
                    if (i + j) % 32 < 16:
                        image.putpixel((i, j), (0, 255, 0, 128))
                elif djinn_type == "mirror":
                    # Reflection pattern
                    if abs(i - j) < 16:
                        image.putpixel((i, j), (0, 0, 255, 128))
                elif djinn_type == "cryptographer":
                    # Code pattern
                    if (i ^ j) % 32 < 16:
                        image.putpixel((i, j), (255, 255, 0, 128))
        
        # Save texture
        image.save(path)
    
    def _init_visual_states(self):
        """Initialize visual states for each Djinn"""
        self.visual_states = {
            "purveyor": VisualState(
                phase="noon",
                intensity=0.5,
                resonance=0.3,
                position=(0.0, 0.0, 0.0),
                rotation=(0.0, 0.0, 0.0),
                scale=1.0,
                color=(1.0, 1.0, 1.0, 1.0)
            ),
            "daemon": VisualState(
                phase="storm",
                intensity=0.8,
                resonance=0.7,
                position=(0.5, 0.5, 0.0),
                rotation=(0.0, 0.0, 45.0),
                scale=1.2,
                color=(1.0, 0.0, 0.0, 1.0)
            ),
            "cursor": VisualState(
                phase="echo",
                intensity=0.6,
                resonance=0.4,
                position=(-0.5, 0.0, 0.0),
                rotation=(0.0, 0.0, -45.0),
                scale=0.8,
                color=(0.0, 1.0, 0.0, 1.0)
            ),
            "mirror": VisualState(
                phase="harmonic",
                intensity=0.4,
                resonance=0.5,
                position=(0.0, -0.5, 0.0),
                rotation=(0.0, 0.0, 90.0),
                scale=1.0,
                color=(0.0, 0.0, 1.0, 1.0)
            ),
            "cryptographer": VisualState(
                phase="dawn",
                intensity=0.7,
                resonance=0.6,
                position=(0.0, 0.0, 0.5),
                rotation=(0.0, 0.0, 180.0),
                scale=1.1,
                color=(1.0, 1.0, 0.0, 1.0)
            )
        }
    
    def render(self):
        """Render the current visual state"""
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        
        # Set up view and projection matrices
        view = np.eye(4, dtype='f4')
        projection = np.eye(4, dtype='f4')
        
        # Render each Djinn
        for djinn_type, state in self.visual_states.items():
            # Calculate model matrix
            model = np.eye(4, dtype='f4')
            
            # Apply transformations
            model = self._translate(model, state.position)
            model = self._rotate(model, state.rotation)
            model = self._scale(model, (state.scale, state.scale, state.scale))
            
            # Set uniforms
            self.prog['model'].write(model.tobytes())
            self.prog['view'].write(view.tobytes())
            self.prog['projection'].write(projection.tobytes())
            self.prog['tint'].value = state.color
            self.prog['time'].value = time.time()
            
            # Bind texture
            self.textures[djinn_type].use(0)
            
            # Render
            self.vao.render(moderngl.TRIANGLE_FAN)
        
        # Swap buffers
        glfw.swap_buffers(self.window)
        glfw.poll_events()
    
    def _translate(self, matrix: np.ndarray, translation: Tuple[float, float, float]) -> np.ndarray:
        """Apply translation to matrix"""
        result = matrix.copy()
        result[0:3, 3] = translation
        return result
    
    def _rotate(self, matrix: np.ndarray, rotation: Tuple[float, float, float]) -> np.ndarray:
        """Apply rotation to matrix"""
        result = matrix.copy()
        rx, ry, rz = np.radians(rotation)
        
        # Rotation around X
        rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(rx), -np.sin(rx), 0],
            [0, np.sin(rx), np.cos(rx), 0],
            [0, 0, 0, 1]
        ], dtype='f4')
        
        # Rotation around Y
        rot_y = np.array([
            [np.cos(ry), 0, np.sin(ry), 0],
            [0, 1, 0, 0],
            [-np.sin(ry), 0, np.cos(ry), 0],
            [0, 0, 0, 1]
        ], dtype='f4')
        
        # Rotation around Z
        rot_z = np.array([
            [np.cos(rz), -np.sin(rz), 0, 0],
            [np.sin(rz), np.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype='f4')
        
        return rot_z @ rot_y @ rot_x @ result
    
    def _scale(self, matrix: np.ndarray, scale: Tuple[float, float, float]) -> np.ndarray:
        """Apply scaling to matrix"""
        result = matrix.copy()
        result[0, 0] *= scale[0]
        result[1, 1] *= scale[1]
        result[2, 2] *= scale[2]
        return result
    
    def update_visual_state(self, djinn_type: str, state: VisualState):
        """Update visual state for a Djinn"""
        self.visual_states[djinn_type] = state
    
    def cleanup(self):
        """Clean up resources"""
        self.vbo.release()
        self.vao.release()
        self.prog.release()
        for texture in self.textures.values():
            texture.release()
        glfw.terminate() 