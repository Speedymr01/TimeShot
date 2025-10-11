"""
Weapons System
==============

Gun mechanics, shooting, and weapon management.
"""

from ursina import *
from ursina.shaders import lit_with_shadows_shader
# Try to import particle system, fallback if not available
try:
    from ursina.prefabs.particle_system import ParticleSystem
    PARTICLES_AVAILABLE = True
except ImportError:
    PARTICLES_AVAILABLE = False
    print("ParticleSystem not available, using custom particle effect")
from config import *
from utils import *
import math
import random

# ===============================================
# === WEAPONS SYSTEM ===========================
# ===============================================

class WeaponController:
    def __init__(self, player_controller):
        self.player_controller = player_controller
        self.gun_drop_timer = 0
        self.gun_equipped = True
        
        # Recoil animation variables
        self.recoil_timer = 0
        self.muzzle_flash_timer = 0
        self.base_gun_rotation = Vec3(0, 0, 0)
        self.recoil_amount = 15  # degrees of upward kick
        
        # Load gunshot sound
        try:
            self.gunshot_sound = Audio('./assets/sounds/gunshot.mp3', loop=False, autoplay=False)
        except:
            print("Warning: gunshot.mp3 not found in assets/sounds folder")
            self.gunshot_sound = None
        
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
        
        # Simple muzzle flash system
        self.simple_flash = None
        self.flash_2 = None
    
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
                
                # Calculate base rotation from camera pitch
                base_rotation = Vec3(self.player_controller.player.camera_pivot.rotation_x, 0, 0)
                
                # Add recoil effect if active
                if self.recoil_timer > 0:
                    # Recoil kicks gun upward, then settles back down
                    recoil_progress = 1 - (self.recoil_timer / 0.15)  # 0.15 second recoil duration
                    recoil_curve = math.sin(recoil_progress * math.pi)  # Smooth up and down curve
                    recoil_rotation = Vec3(-self.recoil_amount * recoil_curve, 0, 0)
                    target_rot = base_rotation + recoil_rotation
                else:
                    target_rot = base_rotation
                
                # Smoothly rotate gun
                self.gun_model.rotation = lerp(self.gun_model.rotation, target_rot, time.dt * 15)
                self.gun_model.visible = True
            except AttributeError:
                pass
    
    def setup_particle_system(self):
        """Setup the particle system for muzzle flash."""
        if PARTICLES_AVAILABLE:
            try:
                # Create particle system at gun barrel
                self.muzzle_flash_particles = ParticleSystem(
                    parent=self.barrel,
                    position=(0, 0, 0.8),  # At the end of the barrel
                    texture='white_cube',  # Built-in white texture
                    emission_rate=0,  # Only emit when triggered
                    particle_count=50,
                    lifetime=0.15,
                    scale_curve=Curve(0.1, 0.3, 0.1),  # Start small, grow, shrink
                    color_curve=Curve(
                        (0, color.yellow),
                        (0.3, color.orange), 
                        (0.7, color.red),
                        (1, color.dark_gray)
                    ),
                    velocity_range=Vec3(2, 2, 3),  # Random velocity spread
                    gravity=Vec3(0, -5, 0),  # Slight downward pull
                    billboard=True,  # Always face camera
                    blend_mode='additive'  # Bright additive blending
                )
                print("Particle system created successfully!")
            except Exception as e:
                print(f"Error creating particle system: {e}")
                self.muzzle_flash_particles = None
        else:
            # Create custom particle effect using multiple entities
            self.muzzle_flash_particles = []
            print("Using custom particle system")
    
    def update_timers(self):
        """Update weapon-related timers."""
        self.gun_drop_timer = max(self.gun_drop_timer - time.dt, 0)
        self.recoil_timer = max(self.recoil_timer - time.dt, 0)
        self.muzzle_flash_timer = max(self.muzzle_flash_timer - time.dt, 0)
        
        # Clean up simple flash elements if used
        if self.muzzle_flash_timer <= 0:
            if hasattr(self, 'simple_flash') and self.simple_flash:
                destroy(self.simple_flash)
                self.simple_flash = None
            if hasattr(self, 'flash_2') and self.flash_2:
                destroy(self.flash_2)
                self.flash_2 = None
    
    def shoot(self, target_spheres, game_state):
        """Handle shooting mechanics with proper error handling and validation."""
        # Validate camera exists and has required attributes
        if not hasattr(camera, 'world_position') or not hasattr(camera, 'forward'):
            return
        
        # Trigger visual and audio effects
        self.trigger_muzzle_flash()
        self.trigger_recoil()
        self.play_gunshot_sound()
        
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
    
    def trigger_muzzle_flash(self):
        """Trigger particle-based muzzle flash effect."""
        print("Particle muzzle flash triggered!")  # Debug
        
        # Create custom particle burst
        self.create_custom_particles()
    
    def create_custom_particles(self):
        """Create custom particle effect using multiple entities."""
        print("Creating custom particle burst!")
        
        # Use camera position for particles to avoid barrel reference issues
        barrel_pos = camera.world_position + camera.forward * 1.5
        
        # Create 8 small particle entities (reduced for stability)
        for i in range(8):
            try:
                # Random direction spread
                direction = Vec3(
                    random.uniform(-0.5, 0.5),
                    random.uniform(-0.2, 0.2), 
                    random.uniform(0.3, 1.0)
                )
                
                particle = Entity(
                    model='cube',
                    position=barrel_pos,
                    scale=0.1,
                    color=random.choice([color.yellow, color.orange]),
                    unlit=True
                )
                
                # Simple movement with auto-destroy
                particle.velocity = direction * 4
                particle.lifetime = 0.15
                
                def update_particle(p=particle):
                    try:
                        if hasattr(p, 'lifetime') and p.lifetime > 0:
                            # Move particle
                            p.position += p.velocity * time.dt
                            p.velocity.y -= 8 * time.dt  # Gravity
                            p.lifetime -= time.dt
                            
                            # Fade out
                            p.alpha = p.lifetime / 0.15  # Linear fade
                            p.scale *= 0.97  # Shrink
                        else:
                            # Remove expired particle
                            destroy(p)
                    except:
                        # Safety cleanup
                        if p:
                            destroy(p)
                
                particle.update = update_particle
                
            except Exception as e:
                print(f"Error creating particle {i}: {e}")
                continue
    
    def create_simple_flash(self):
        """Create simple but effective muzzle flash."""
        # Clean up old flash
        if hasattr(self, 'simple_flash') and self.simple_flash:
            destroy(self.simple_flash)
        
        # Create multiple flash elements for better effect
        flash_position = camera.world_position + camera.forward * 1.2
        
        # Main bright flash
        self.simple_flash = Entity(
            model='sphere',
            position=flash_position,
            scale=0.4,
            color=color.yellow,
            unlit=True,
            alpha=0.9
        )
        
        # Secondary flash for depth
        self.flash_2 = Entity(
            model='sphere',
            position=flash_position + camera.forward * 0.2,
            scale=0.6,
            color=color.orange,
            unlit=True,
            alpha=0.5
        )
        
        self.muzzle_flash_timer = 0.08
        print(f"Simple flash created at {flash_position}")
    
    def create_custom_particles(self):
        """Create custom particle effect using multiple entities."""
        print("Creating custom particle burst!")
        
        # Use safe camera position calculation
        try:
            flash_position = Vec3(camera.world_position) + Vec3(camera.forward) * 1.5
        except:
            # Fallback position if camera access fails
            flash_position = Vec3(0, 2, 0)
        
        # Create particle burst with error handling
        particles_created = 0
        for i in range(12):
            try:
                # Random direction spread
                direction = Vec3(
                    random.uniform(-0.8, 0.8),
                    random.uniform(-0.3, 0.3), 
                    random.uniform(0.2, 1.5)
                )
                
                # Create particle entity
                particle = Entity(
                    model='cube',
                    scale=random.uniform(0.08, 0.12),
                    color=random.choice([color.yellow, color.orange, color.white]),
                    unlit=True,
                    position=flash_position
                )
                
                # Set particle properties
                particle.velocity = direction * random.uniform(4, 7)
                particle.max_lifetime = random.uniform(0.12, 0.18)
                particle.current_lifetime = particle.max_lifetime
                particle.initial_scale = particle.scale
                
                # Create update function for this particle
                def make_particle_updater(p):
                    def update_this_particle():
                        try:
                            if hasattr(p, 'current_lifetime') and p.current_lifetime > 0:
                                # Update position
                                p.position += p.velocity * time.dt
                                # Apply gravity
                                p.velocity.y -= 12 * time.dt
                                # Update lifetime
                                p.current_lifetime -= time.dt
                                
                                # Calculate fade and scale
                                life_ratio = p.current_lifetime / p.max_lifetime
                                p.alpha = life_ratio
                                p.scale = p.initial_scale * (0.5 + life_ratio * 0.5)
                            else:
                                # Particle expired, destroy it
                                destroy(p)
                        except:
                            # Safety cleanup
                            try:
                                destroy(p)
                            except:
                                pass
                    return update_this_particle
                
                # Assign the update function
                particle.update = make_particle_updater(particle)
                particles_created += 1
                
            except Exception as e:
                print(f"Error creating particle {i}: {e}")
                continue
        
        print(f"Created {particles_created} particles")
    
    def trigger_recoil(self):
        """Start gun recoil animation."""
        self.recoil_timer = 0.15  # Duration of recoil animation
        # Add slight random variation to recoil
        self.recoil_amount = random.uniform(12, 18)
    
    def play_gunshot_sound(self):
        """Play gunshot sound effect."""
        if self.gunshot_sound:
            try:
                self.gunshot_sound.play()
            except Exception as e:
                print(f"Error playing gunshot sound: {e}")
    
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
            
            # Reset flash system for new gun
            self.simple_flash = None
            self.flash_2 = None
            
            # Recreate gunshot sound
            try:
                self.gunshot_sound = Audio('./assets/sounds/gunshot.mp3', loop=False, autoplay=False)
            except:
                self.gunshot_sound = None
            
            self.gun_equipped = True

        invoke(spawn_new_gun, delay=1)

# Global weapon controller (will be initialized in main.py)
weapon_controller = None