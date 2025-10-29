"""
Map and Environment
===================

3D environment, lighting, and map management.
"""

from ursina import *
from ursina.shaders import lit_with_shadows_shader
from panda3d.core import Texture
from config import *

# ===============================================
# === MAP AND ENVIRONMENT =======================
# ===============================================

class MapEnvironment:
    def __init__(self):
        # Main map entity with enhanced texture settings
        self.model_entity = Entity(
            model='./assets/tutorial_map.obj',
            #texture='./assets/block_texture.jpg',
            color=color.white,
            scale=1,
            collider='mesh',
            position=(0, 0, 0),
            #texture_scale=(8, 8),
            shader=lit_with_shadows_shader,
            double_sided=True
        )
        
        # Apply texture softening to map if enabled
        if TEXTURE_SOFTENING:
            self.apply_texture_enhancements()

        # Skybox setup
        self.skybox = None
        if SKYBOX_ENABLED:
            self.create_skybox()

        # Lighting setup
        self.directional_light = DirectionalLight(color=color.rgb(50, 50, 50), shadows=True)
        self.ambient_light = AmbientLight(color=color.rgba(50, 50, 50, 0.1))
    
    def create_skybox(self):
        """Create skybox with error handling for missing textures."""
        try:
            # Method 1: Sphere-based skybox (most common and reliable)
            self.skybox = Entity(
                model='sphere',
                texture=SKYBOX_TEXTURE,
                scale=SKYBOX_SCALE,
                color=SKYBOX_COLOR,
                double_sided=True,
                unlit=True,  # Skybox shouldn't be affected by lighting
                render_queue=-1,  # Render behind everything else
                always_on_top=False
            )
            
            # Make skybox follow camera position (but not rotation)
            def update_skybox():
                if self.skybox and camera:
                    self.skybox.position = camera.world_position
            
            self.skybox.update = update_skybox
            
        except Exception as e:
            print(f"Warning: Could not create skybox with texture {SKYBOX_TEXTURE}: {e}")
            # Fallback: Create a simple gradient skybox
            self.create_fallback_skybox()
    
    def create_fallback_skybox(self):
        """Create a simple gradient skybox as fallback."""
        try:
            self.skybox = Entity(
                model='sphere',
                scale=SKYBOX_SCALE,
                color=color.rgb(135, 206, 235),  # Sky blue
                double_sided=True,
                unlit=True,
                render_queue=-1
            )
            
            def update_skybox():
                if self.skybox and camera:
                    self.skybox.position = camera.world_position
            
            self.skybox.update = update_skybox
            
        except Exception as e:
            print(f"Warning: Could not create fallback skybox: {e}")
            self.skybox = None
    
    def apply_texture_enhancements(self):
        """Apply texture softening and quality enhancements to environment."""
        try:
            if self.model_entity:
                # Try multiple methods to apply texture enhancements
                texture_applied = False
                
                # Method 1: Direct texture access
                if hasattr(self.model_entity, 'texture') and self.model_entity.texture:
                    try:
                        if TEXTURE_FILTERING == 'linear':
                            # Try different Panda3D API versions
                            texture = self.model_entity.texture
                            
                            # Try newer API first
                            if hasattr(texture, 'setMagfilter'):
                                texture.setMagfilter(Texture.FTLinear)
                                if MIPMAPPING_ENABLED:
                                    texture.setMinfilter(Texture.FTLinearMipmapLinear)
                                else:
                                    texture.setMinfilter(Texture.FTLinear)
                                texture_applied = True
                            
                            # Apply anisotropic filtering if available
                            if ANISOTROPIC_FILTERING > 0 and hasattr(texture, 'setAnisotropicDegree'):
                                texture.setAnisotropicDegree(ANISOTROPIC_FILTERING)
                    except:
                        pass
                
                # Method 2: Use Ursina's texture system
                if not texture_applied and hasattr(self.model_entity, 'model'):
                    try:
                        # Apply through Ursina's model system
                        if TEXTURE_FILTERING == 'linear':
                            # Ursina automatically handles texture filtering for models
                            pass
                    except:
                        pass
                
                if texture_applied:
                    print("✅ Enhanced texture filtering applied to environment")
                else:
                    # Global settings are still active, so this is fine
                    pass
                
        except Exception:
            # Texture enhancements are optional - fail silently
            pass
    
    def show_game(self):
        """Show all game environment elements."""
        self.model_entity.enabled = True
        if self.skybox:
            self.skybox.enabled = True
    
    def hide_game(self):
        """Hide all game environment elements."""
        self.model_entity.enabled = False
        if self.skybox:
            self.skybox.enabled = False

# Global map environment (will be initialized in main.py)
map_environment = None