"""
Player System
=============

Player controller, movement physics, and related functionality.
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

from config import *
from utils import *
import math

# ===============================================
# === PLAYER SYSTEM ============================
# ===============================================

from typing import Optional

class PlayerController:
    """
    Manages player movement, physics, and state.
    
    Handles advanced movement mechanics including sliding, dashing,
    wall running, and momentum-based physics.
    """
    
    def __init__(self):
        # Initialize player
        self.player = FirstPersonController(position=PLAYER_START_POS)
        self.player.gravity = PLAYER_GRAVITY
        self.player.jump_height = PLAYER_JUMP_HEIGHT
        self.player.speed = PLAYER_SPEED
        
        # Set proper camera height
        self.player.camera_pivot.y = NORMAL_CAMERA_Y
        self.player.collider = 'box'
        
        # Initialize position tracking
        self.measured_player_prev_pos = self.player.position
        
        # Create player hitbox (invisible in first-person)
        self.player_model = Entity(
            parent=self.player,
            model='cube',
            color=color.rgba(100, 150, 255, 150),
            scale=(PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH),
            position=(0, PLAYER_HEIGHT/2, 0),
            collider=None,
            visible=DEBUG_MODE  # Only visible in debug mode
        )
        
        # Movement state
        self.movement_velocity = Vec3(0, 0, 0)
        self.measured_player_velocity = Vec3(0, 0, 0)
        
        # Movement state flags
        self.is_sliding = False
        self.slide_velocity = 0
        self.slide_direction = Vec3(0, 0, 0)
        self.is_airborne = False
        self.is_sprinting = False
        self.slide_timer = 0.0
        self.dash_timer = 0.0
        
        # Wall running state
        self.is_wall_running = False
        self.wall_run_timer = 0.0
        self.wall_normal = Vec3(0, 0, 0)
        self.wall_run_side = 0  # -1 for left wall, 1 for right wall, 0 for no wall
        
        # Jump speed system
        self.jump_speed_active = False
        self.jump_speed_timer = 0.0
        self.jump_direction = Vec3(0, 0, 0)
        
        # Jump feel enhancements
        self.jump_buffer_timer = 0.0
        self.coyote_timer = 0.0
        self.was_grounded = False
        self.jump_held = False
    
    def update_velocity_measurement(self) -> None:
        """
        Calculate player's instantaneous velocity for physics interactions.
        
        Uses frame time delta to compute velocity from position changes.
        Includes safety checks for zero delta time and initialization.
        """
        # Early validation
        if not hasattr(self.player, 'position') or time.dt <= 0:
            if not hasattr(self, 'measured_player_velocity'):
                self.measured_player_velocity = Vec3(0, 0, 0)
            return
        
        try:
            self.measured_player_velocity = (
                self.player.position - self.measured_player_prev_pos
            ) / time.dt
            self.measured_player_prev_pos = self.player.position
        except (AttributeError, ZeroDivisionError, TypeError) as e:
            # Log error but don't expose details to user
            if hasattr(self, 'debug_mode') and self.debug_mode:
                print(f"Debug: Error in velocity measurement: {e}")
            self.measured_player_velocity = Vec3(0, 0, 0)
        except Exception as e:
            # Catch any other unexpected errors
            self.measured_player_velocity = Vec3(0, 0, 0)
    
    def update_timers(self):
        """Update all cooldown timers."""
        self.slide_timer = max(self.slide_timer - time.dt, 0)
        self.dash_timer = max(self.dash_timer - time.dt, 0)
        self.update_jump_speed_timer()
        self.update_jump_feel_timers()
    
    def handle_sprint_input(self):
        """Process sprint input and return target max speed."""
        if held_keys['shift'] and not self.is_sliding:
            self.is_sprinting = True
            return MAX_SPEED * SPRINT_MULTIPLIER
        else:
            self.is_sprinting = False
            return MAX_SPEED
    
    def handle_slide_trigger(self):
        """Initiate sliding when conditions are met."""
        if held_keys['control'] and not self.is_sliding and self.slide_timer <= 0 and self.is_sprinting:
            self.is_sliding = True
            self.slide_velocity = SLIDE_START_VELOCITY
            self.slide_direction = self.player.forward.normalized()
            self.slide_timer = SLIDE_COOLDOWN
            # Reset horizontal movement velocity
            self.movement_velocity.x = 0
            self.movement_velocity.z = 0
    
    def handle_sliding_physics(self):
        """Handle sliding physics and camera."""
        if self.is_sliding:
            hit_info = raycast(self.player.position, Vec3(0, -1, 0), distance=2, ignore=[self.player])
            if hit_info.hit:
                slope_normal = hit_info.normal
                downhill = Vec3(-slope_normal.x, 0, -slope_normal.z).normalized()
                self.slide_direction = lerp(self.slide_direction, downhill, time.dt * 2)
                self.slide_velocity += GRAVITY_FORCE * (1 - hit_info.normal.y) * time.dt

            slide_step = self.slide_direction * self.slide_velocity * time.dt
            hit = raycast(self.player.position, self.slide_direction, distance=slide_step.length() + 0.5, ignore=[self.player])
            if not hit.hit:
                self.player.position += slide_step
            else:
                self.is_sliding = False
                self.slide_velocity = 0

            self.player.camera_pivot.y = lerp(self.player.camera_pivot.y, SLIDE_CAMERA_Y, time.dt * 8)
            self.slide_velocity = max(self.slide_velocity - SLIDE_FRICTION * time.dt, 0)

            if held_keys['space']:
                self.is_sliding = False
                self.slide_velocity = 0
        else:
            self.player.camera_pivot.y = lerp(self.player.camera_pivot.y, NORMAL_CAMERA_Y, time.dt * 6)
    
    def handle_dash_input(self):
        """Handle dash input - applies force in look direction."""
        if held_keys['q'] and self.dash_timer <= 0:
            # Calculate separate horizontal and vertical components
            horizontal_force = DASH_FORCE * 1.5  # Boost horizontal to compensate for friction
            vertical_force = DASH_FORCE * 0.6    # Reduce vertical to balance with horizontal
            
            # Apply horizontal force (X and Z)
            dash_direction = camera.forward.normalized()
            horizontal_component = Vec3(dash_direction.x, 0, dash_direction.z).normalized()
            if horizontal_component.length() > 0:
                self.movement_velocity.x += horizontal_component.x * horizontal_force
                self.movement_velocity.z += horizontal_component.z * horizontal_force
            
            # Apply vertical force (Y) with constraints
            if self.player.grounded:
                # Ground dash: small upward boost only if looking up
                if dash_direction.y > 0:
                    self.movement_velocity.y += dash_direction.y * vertical_force * 0.5
            else:
                # Air dash: allow vertical movement but cap it
                vertical_boost = dash_direction.y * vertical_force * 0.7
                # Cap vertical velocity to prevent excessive flying
                new_y_velocity = self.movement_velocity.y + vertical_boost
                self.movement_velocity.y = max(-30, min(30, new_y_velocity))
            
            self.dash_timer = DASH_COOLDOWN
            print(f"Dash - H: {horizontal_force:.1f}, V: {vertical_force:.1f}, Dir: {dash_direction}")
    
    def update_jump_speed_timer(self):
        """Update jump speed boost timer."""
        if self.jump_speed_active:
            self.jump_speed_timer -= time.dt
            if self.jump_speed_timer <= 0:
                self.jump_speed_active = False
                print("Jump speed boost ended")
    
    def activate_jump_speed(self):
        """Activate jump speed boost when jumping."""
        if not JUMP_SPEED_PRESERVE and self.jump_speed_active:
            return  # Don't stack jump speed boosts
        
        self.jump_speed_active = True
        self.jump_speed_timer = JUMP_SPEED_DURATION
        
        # Determine jump direction
        if JUMP_SPEED_DIRECTIONAL:
            # Use current movement input direction
            input_dir = Vec3(
                held_keys['d'] - held_keys['a'],  # right-left
                0,
                held_keys['w'] - held_keys['s']   # forward-back
            )
            if input_dir.length() > 0:
                input_dir = input_dir.normalized()
                self.jump_direction = (camera.forward * input_dir.z + camera.right * input_dir.x)
                self.jump_direction.y = 0
                if self.jump_direction.length() > 0:
                    self.jump_direction = self.jump_direction.normalized()
                else:
                    self.jump_direction = camera.forward
                    self.jump_direction.y = 0
                    self.jump_direction = self.jump_direction.normalized()
            else:
                # No input, use camera forward direction
                self.jump_direction = camera.forward
                self.jump_direction.y = 0
                self.jump_direction = self.jump_direction.normalized()
        else:
            # Use current movement velocity direction
            horiz_vel = Vec3(self.movement_velocity.x, 0, self.movement_velocity.z)
            if horiz_vel.length() > 0:
                self.jump_direction = horiz_vel.normalized()
            else:
                self.jump_direction = camera.forward
                self.jump_direction.y = 0
                self.jump_direction = self.jump_direction.normalized()
        
        # Apply initial jump speed boost
        if JUMP_SPEED_PRESERVE:
            # Add to existing velocity
            boost_velocity = self.jump_direction * MAX_SPEED * (JUMP_SPEED_BOOST - 1.0)
            self.movement_velocity.x += boost_velocity.x
            self.movement_velocity.z += boost_velocity.z
        else:
            # Set velocity to boosted speed
            boost_velocity = self.jump_direction * MAX_SPEED * JUMP_SPEED_BOOST
            self.movement_velocity.x = boost_velocity.x
            self.movement_velocity.z = boost_velocity.z
        
        print(f"Jump speed activated! Boost: {JUMP_SPEED_BOOST}x for {JUMP_SPEED_DURATION}s")
    
    def update_jump_feel_timers(self):
        """Update jump buffer and coyote time timers."""
        # Update jump buffer timer
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= time.dt
        
        # Update coyote timer (grace period after leaving ground)
        if self.player.grounded:
            self.coyote_timer = COYOTE_TIME
            self.was_grounded = True
        else:
            if self.was_grounded:
                self.coyote_timer = COYOTE_TIME
                self.was_grounded = False
            else:
                self.coyote_timer = max(self.coyote_timer - time.dt, 0)
    
    def handle_jump_input(self):
        """Handle jump input with buffering and coyote time."""
        # Check for jump input
        if held_keys['space']:
            if not self.jump_held:
                # Just pressed jump
                self.jump_buffer_timer = JUMP_BUFFER_TIME
                self.jump_held = True
        else:
            self.jump_held = False
        
        # Try to execute buffered jump
        if self.jump_buffer_timer > 0:
            # Can jump if grounded or within coyote time
            if self.player.grounded or self.coyote_timer > 0:
                return True
        
        return False
    
    def handle_jump_cut(self):
        """Handle variable jump height by cutting jump short."""
        if JUMP_CUT_ENABLED and not held_keys['space'] and self.movement_velocity.y > 0:
            # Player released space while going up - cut jump short
            self.movement_velocity.y *= JUMP_CUT_MULTIPLIER
    
    def consume_jump(self):
        """Consume the jump input (called when jump is executed)."""
        self.jump_buffer_timer = 0
        self.coyote_timer = 0

# Global player instance (will be initialized in main.py)
player_controller = None