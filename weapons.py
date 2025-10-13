"""
Weapons System
==============

Gun mechanics, shooting, and weapon management.
"""

from ursina import *
from ursina.shaders import lit_with_shadows_shader
from config import *
from utils import *

# ===============================================
# === WEAPONS SYSTEM ===========================
# ===============================================

class WeaponController:
    def __init__(self, player_controller):
        self.player_controller = player_controller
        self.gun_drop_timer = 0
        self.gun_equipped = True
        
        # Create gun model
        self.gun_model = Entity(
            model='./assets/gun3.obj',
            position=(0, 1.3, 2),
            scale=0.1,
            collider=None,
            shader=lit_with_shadows_shader,
            double_sided=True,
            parent=player_controller.player
        )
        self.gun_model.texture = './assets/textures/gun3_texture.png'
        
        # Gun barrel reference point
        self.barrel = Entity(
            parent=self.gun_model,
            position=(0, 0.1, 2.2),
            scale=0.02,
            visible=False
        )
    
    def update_gun_position(self):
        """Update gun model position and rotation to follow camera movement."""
        if self.gun_model and hasattr(self.gun_model, 'world_position'):
            try:
                # Position gun relative to camera
                self.gun_model.world_position = (
                    camera.world_position +
                    camera.forward * GUN_OFFSET.z +
                    camera.right * GUN_OFFSET.x +
                    camera.up * GUN_OFFSET.y
                )
                # Smoothly rotate gun to match camera pitch
                target_rot = Vec3(self.player_controller.player.camera_pivot.rotation_x, 0, 0)
                self.gun_model.rotation = lerp(self.gun_model.rotation, target_rot, time.dt * 10)
                self.gun_model.visible = True
            except AttributeError:
                pass
    
    def update_timers(self):
        """Update weapon-related timers."""
        self.gun_drop_timer = max(self.gun_drop_timer - time.dt, 0)
    
    def shoot(self, target_spheres, game_state):
        """Handle shooting mechanics with proper error handling and validation."""
        # Validate camera exists and has required attributes
        if not hasattr(camera, 'world_position') or not hasattr(camera, 'forward'):
            return
        
        game_state.shots_fired += 1

        try:
            hit_info = raycast(
                origin=camera.world_position,  # Shoot from camera position (eye level)
                direction=camera.forward,
                distance=9999,
                ignore=[self.player_controller.player, self.player_controller.player_model]
            )
            
            # Validate hit and target
            if (hit_info and hit_info.hit and hit_info.entity and 
                hasattr(hit_info.entity, 'name') and hit_info.entity.name == 'target'):
                
                # Safely remove from target list
                if hit_info.entity in target_spheres:
                    target_spheres.remove(hit_info.entity)
                
                # Destroy the target entity
                destroy(hit_info.entity)

                # Update score in timed mode
                if game_state.is_timed_mode:
                    game_state.score += 1
                    game_state.hits += 1
                    if hasattr(game_state.score_text, 'text'):
                        game_state.score_text.text = f"Score: {game_state.score}"

            # Update accuracy display
            if game_state.is_timed_mode and hasattr(game_state.accuracy_text, 'text'):
                accuracy = (game_state.hits / game_state.shots_fired * 100) if game_state.shots_fired > 0 else 0
                game_state.accuracy_text.text = f"Accuracy: {accuracy:.1f}%"
                
        except Exception as e:
            print(f"Error in shoot function: {e}")
    
    def drop_and_respawn_gun(self):
        """Drop current gun and spawn a new one after delay."""
        self.gun_equipped = False

        # Drop the current gun
        dropped_gun = Entity(
            model=self.gun_model.model,
            texture=self.gun_model.texture,
            position=self.gun_model.world_position,
            rotation=self.gun_model.world_rotation,
            scale=self.gun_model.scale,
            collider='box',
            shader=lit_with_shadows_shader,
            double_sided=True
        )

        # Initial velocity: pop up + some of player's horizontal velocity
        horiz = Vec3(self.player_controller.measured_player_velocity.x, 0, self.player_controller.measured_player_velocity.z)
        dropped_gun.velocity = horiz * 0.9
        dropped_gun.velocity.y = GUN_POP_FORCE

        # Gravity + movement for dropped gun
        def dropped_update(e=dropped_gun):
            if e.y > -10:
                e.position += e.velocity * time.dt
                e.velocity.y -= GUN_GRAVITY * time.dt
            else:
                e.y = -10
        dropped_gun.update = dropped_update

        # Spawn replacement gun after 1 sec
        def spawn_new_gun():
            self.gun_model = Entity(
                model='./assets/gun3.obj',
                position=(0, 1.3, 2),
                scale=0.1,
                collider=None,
                shader=lit_with_shadows_shader,
                double_sided=True,
                parent=self.player_controller.player
            )
            self.gun_model.texture = './assets/textures/gun3_texture.png'
            self.barrel.parent = self.gun_model
            self.barrel.position = (0, 0.1, 2.2)
            self.gun_equipped = True

        invoke(spawn_new_gun, delay=1)

# Global weapon controller (will be initialized in main.py)
weapon_controller = None