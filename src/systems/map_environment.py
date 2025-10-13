"""
Map and Environment
===================

3D environment, lighting, and map management.
"""

from ursina import *
from ursina.shaders import lit_with_shadows_shader
from config import *

# ===============================================
# === MAP AND ENVIRONMENT =======================
# ===============================================

class MapEnvironment:
    def __init__(self):
        # Main map entity
        self.model_entity = Entity(
            model='./assets/tutorial_map.obj',
            texture='./assets/texture_01.png',
            scale=1,
            collider='mesh',
            position=(0, 0, 0),
            texture_scale=(20, 20),
            shader=lit_with_shadows_shader,
            double_sided=True
        )

        # Lighting setup
        self.directional_light = DirectionalLight(color=color.rgb(50, 50, 50), shadows=True)
        self.ambient_light = AmbientLight(color=color.rgba(50, 50, 50, 0.1))
    
    def show_game(self):
        """Show all game environment elements."""
        self.model_entity.enabled = True
    
    def hide_game(self):
        """Hide all game environment elements."""
        self.model_entity.enabled = False

# Global map environment (will be initialized in main.py)
map_environment = None