"""
Weapons System
==============

Gun mechanics, shooting, and weapon management.
"""

from ursina import *
from ursina.shaders import lit_with_shadows_shader
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

from config import *
from utils import *
import random

# ===============================================
# === WEAPONS SYSTEM ===========================
# ===============================================

class WeaponController:
    def __init__(self, player_controller):
        self.player_controller = player_controller
        self.gun_drop_timer = 0
        self.gun_equipped = True
        
        # Recoil system
        self.recoil_timer = 0
        self.recoil_offset = Vec3(0, 0, 0)
        self.base_camera_rotation = Vec3(0, 0, 0)
        
        # Grappling hook system
        self.grapple_active = False
        self.grapple_point = None
        self.grapple_line = None
        self.grapple_timer = 0
        self.grapple_hook_entity = None
        
        # Load gunshot sound with validation
        try:
            from pathlib import Path
            sound_path = Path(GUNSHOT_SOUND).resolve()
            current_dir = Path.cwd()
            
            # Validate sound file path
            if str(sound_path).startswith(str(current_dir)) and sound_path.exists():
                self.gunshot_sound = Audio(GUNSHOT_SOUND, loop=False, autoplay=False)
            else:
                print(f"Warning: Invalid or missing sound file: {GUNSHOT_SOUND}")
                self.gunshot_sound = None
        except Exception as e:
            print(f"Warning: Could not load gunshot sound: {e}")
            self.gunshot_sound = None
        
        # Create gun model
        self.gun_model = Entity(
            model=GUN_MODEL_PATH,
            position=(0, 1.3, 2),
            scale=GUN_SCALE,
            collider=None,
            shader=lit_with_shadows_shader,
            double_sided=True,
            parent=player_controller.player
        )
        self.gun_model.texture = GUN_TEXTURE_PATH
        
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
        self.grapple_timer = max(self.grapple_timer - time.dt, 0)
        self.update_recoil()
        self.update_grapple()
    
    def update_recoil(self):
        """Update recoil recovery over time."""
        if self.recoil_timer > 0:
            self.recoil_timer -= time.dt
            
            # Calculate recovery factor (0 to 1, where 1 is full recovery)
            recovery_factor = 1 - (self.recoil_timer / RECOIL_DURATION)
            recovery_factor = max(0, min(1, recovery_factor))
            
            # Apply smooth recovery using lerp
            current_offset = lerp(self.recoil_offset, Vec3(0, 0, 0), recovery_factor * RECOIL_RECOVERY_SPEED * time.dt)
            
            # Apply recoil to camera
            if hasattr(self.player_controller.player, 'camera_pivot'):
                self.player_controller.player.camera_pivot.rotation_x += current_offset.x * time.dt * 60
                self.player_controller.player.rotation_y += current_offset.y * time.dt * 60
            
            # Reduce recoil offset
            self.recoil_offset = lerp(self.recoil_offset, Vec3(0, 0, 0), RECOIL_RECOVERY_SPEED * time.dt)
            
            # End recoil when timer expires
            if self.recoil_timer <= 0:
                self.recoil_offset = Vec3(0, 0, 0)
    
    def apply_recoil(self):
        """Apply recoil effect to camera."""
        if not RECOIL_ENABLED:
            return
            
        # Determine recoil multiplier based on player state
        recoil_multiplier = RECOIL_MULTIPLIER_STANDING
        if hasattr(self.player_controller, 'is_sliding') and self.player_controller.is_sliding:
            recoil_multiplier = RECOIL_MULTIPLIER_CROUCHING
        elif hasattr(self.player_controller, 'measured_player_velocity'):
            velocity_magnitude = self.player_controller.measured_player_velocity.length()
            if velocity_magnitude > 1.0:  # Player is moving
                recoil_multiplier = RECOIL_MULTIPLIER_MOVING
        
        # Generate recoil pattern
        if RECOIL_PATTERN_ENABLED:
            # Predictable recoil pattern (could be expanded with pattern arrays)
            vertical_recoil = RECOIL_VERTICAL * recoil_multiplier
            horizontal_recoil = RECOIL_HORIZONTAL * recoil_multiplier * (1 if random.random() > 0.5 else -1)
        else:
            # Random recoil pattern
            vertical_recoil = (RECOIL_VERTICAL + random.uniform(-0.5, 0.5)) * recoil_multiplier
            horizontal_recoil = random.uniform(-RECOIL_HORIZONTAL, RECOIL_HORIZONTAL) * recoil_multiplier
        
        # Set recoil offset and timer
        self.recoil_offset = Vec3(-vertical_recoil, horizontal_recoil, 0)
        self.recoil_timer = RECOIL_DURATION
        
        # Immediate camera kick
        if hasattr(self.player_controller.player, 'camera_pivot'):
            self.player_controller.player.camera_pivot.rotation_x -= vertical_recoil * 0.3
            self.player_controller.player.rotation_y += horizontal_recoil * 0.3
    
    def shoot(self, target_spheres, game_state):
        """Handle shooting mechanics with proper error handling and validation."""
        # Check if shooting is enabled
        if not SHOOTING_ENABLED:
            return
            
        # Validate camera exists and has required attributes
        if not hasattr(camera, 'world_position') or not hasattr(camera, 'forward'):
            return
        
        # Play gunshot sound
        try:
            if (self.gunshot_sound and 
                hasattr(self, 'gunshot_sound') and 
                SFX_VOLUME > 0):
                self.gunshot_sound.volume = min(1.0, max(0.0, SFX_VOLUME * MASTER_VOLUME))
                self.gunshot_sound.play()
        except AttributeError:
            pass  # Sound not available
        except Exception as e:
            print(f"Error playing gunshot sound: {e}")
        
        # Apply recoil effect
        self.apply_recoil()
        
        game_state.shots_fired += 1

        try:
            hit_info = raycast(
                origin=camera.world_position,  # Shoot from camera position (eye level)
                direction=camera.forward,
                distance=BULLET_RANGE,
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
                    points_awarded = POINTS_PER_TARGET
                    if SCORE_MULTIPLIER != 1.0:
                        points_awarded = int(points_awarded * SCORE_MULTIPLIER)
                    
                    game_state.score += points_awarded
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

        # Spawn replacement gun after configured delay
        def spawn_new_gun():
            self.gun_model = Entity(
                model=GUN_MODEL_PATH,
                position=(0, 1.3, 2),
                scale=GUN_SCALE,
                collider=None,
                shader=lit_with_shadows_shader,
                double_sided=True,
                parent=self.player_controller.player
            )
            self.gun_model.texture = GUN_TEXTURE_PATH
            self.barrel.parent = self.gun_model
            self.barrel.position = (0, 0.1, 2.2)
            
            # Reset recoil state for new gun
            self.recoil_timer = 0
            self.recoil_offset = Vec3(0, 0, 0)
            
            self.gun_equipped = True

        invoke(spawn_new_gun, delay=GUN_RESPAWN_TIME)
    
    def fire_grapple(self):
        """Fire grappling hook in the direction the player is looking."""
        if not GRAPPLE_ENABLED or self.grapple_timer > 0:
            return False
        
        # Don't fire if grapple is already active
        if self.grapple_active:
            return False
        
        # Raycast to find grapple target
        try:
            hit_info = raycast(
                origin=camera.world_position,
                direction=camera.forward,
                distance=GRAPPLE_RANGE,
                ignore=[self.player_controller.player, self.player_controller.player_model]
            )
            
            if hit_info and hit_info.hit and hit_info.entity:
                # Valid grapple target found
                self.grapple_point = hit_info.point
                self.grapple_active = True
                self.create_grapple_line()
                self.grapple_timer = GRAPPLE_COOLDOWN
                print(f"Grapple attached at distance: {distance(camera.world_position, self.grapple_point):.1f}")
                return True
            else:
                # No valid target
                print("No grapple target found")
                return False
                
        except Exception as e:
            print(f"Error firing grapple: {e}")
            return False
    
    def create_grapple_line(self):
        """Create visual grapple line from gun to grapple point."""
        try:
            if self.grapple_point:
                # Create grapple line entity
                self.grapple_line = Entity(
                    model='cube',
                    color=GRAPPLE_LINE_COLOR,
                    scale=(GRAPPLE_LINE_THICKNESS, GRAPPLE_LINE_THICKNESS, 1),
                    unlit=True
                )
                
                # Create grapple hook point indicator
                self.grapple_hook_entity = Entity(
                    model='sphere',
                    color=GRAPPLE_LINE_COLOR,
                    scale=0.2,
                    position=self.grapple_point,
                    unlit=True
                )
                
        except Exception as e:
            print(f"Error creating grapple line: {e}")
    
    def update_grapple(self):
        """Update grapple line position and apply grapple physics."""
        if not self.grapple_active or not self.grapple_point:
            return
        
        try:
            # Update grapple line visual
            if self.grapple_line:
                # Calculate line position and rotation
                gun_pos = self.gun_model.world_position if self.gun_model else camera.world_position
                grapple_pos = self.grapple_point
                
                # Position line at midpoint
                midpoint = (gun_pos + grapple_pos) / 2
                self.grapple_line.position = midpoint
                
                # Scale line to match distance
                line_distance = distance(gun_pos, grapple_pos)
                self.grapple_line.scale = (GRAPPLE_LINE_THICKNESS, GRAPPLE_LINE_THICKNESS, line_distance)
                
                # Rotate line to point from gun to grapple point
                self.grapple_line.look_at(grapple_pos)
            
            # Apply grapple physics to player
            self.apply_grapple_physics()
            
        except Exception as e:
            print(f"Error updating grapple: {e}")
            self.release_grapple()
    
    def apply_grapple_physics(self):
        """Apply physics forces when grappling."""
        if not self.grapple_active or not self.grapple_point:
            return
        
        try:
            player_pos = self.player_controller.player.position
            grapple_distance = distance(player_pos, self.grapple_point)
            
            # Calculate direction from player to grapple point
            direction = (self.grapple_point - player_pos).normalized()
            
            # Apply pull force towards grapple point
            pull_force = direction * GRAPPLE_PULL_FORCE * time.dt
            
            # Add to player's movement velocity
            self.player_controller.movement_velocity += pull_force
            
            # Add some upward force to counteract remaining gravity while grappling
            if direction.y > 0:  # Only if grappling upward
                # Compensate for reduced but not eliminated gravity
                gravity_compensation = (1.0 - GRAPPLE_GRAVITY_REDUCTION) * 9.8 * PLAYER_GRAVITY * time.dt
                self.player_controller.movement_velocity.y += gravity_compensation
                # Add additional upward pull force
                self.player_controller.movement_velocity.y += abs(direction.y) * GRAPPLE_PULL_FORCE * 0.3 * time.dt
            
            # Limit maximum grapple distance (cable physics)
            max_cable_length = GRAPPLE_RANGE * 0.8  # 80% of max range
            if grapple_distance > max_cable_length:
                # Pull player back if they get too far
                constraint_force = direction * (grapple_distance - max_cable_length) * 2
                self.player_controller.movement_velocity += constraint_force * time.dt
            
        except Exception as e:
            print(f"Error applying grapple physics: {e}")
    
    def release_grapple(self):
        """Release the grappling hook and clean up."""
        try:
            self.grapple_active = False
            self.grapple_point = None
            
            # Clean up visual elements
            if self.grapple_line:
                destroy(self.grapple_line)
                self.grapple_line = None
            
            if self.grapple_hook_entity:
                destroy(self.grapple_hook_entity)
                self.grapple_hook_entity = None
            
            print("Grapple released")
            
        except Exception as e:
            print(f"Error releasing grapple: {e}")

# Global weapon controller (will be initialized in main.py)
weapon_controller = None