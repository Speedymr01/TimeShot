"""
Physics System
==============

Movement physics, collision handling, and momentum system.
"""

from ursina import *
from config import *
from utils import *
import math

# ===============================================
# === PHYSICS SYSTEM ===========================
# ===============================================

def apply_horizontal_movement_with_collision(player_controller, horizontal_movement):
    """Apply horizontal movement with collision detection."""
    if horizontal_movement.length() > 0:
        collision_check = check_collision(
            origin=player_controller.player.position,
            direction=horizontal_movement.normalized(),
            distance=horizontal_movement.length(),
            ignore_list=[player_controller.player, player_controller.player_model]
        )
        
        if not collision_check or not collision_check.hit:
            player_controller.player.position += horizontal_movement
        else:
            # Try sliding along surface
            slide_movement = apply_slide_movement(horizontal_movement, collision_check.normal)
            slide_check = check_collision(
                origin=player_controller.player.position,
                direction=slide_movement.normalized() if slide_movement.length() > 0 else Vec3(0,0,0),
                distance=slide_movement.length(),
                ignore_list=[player_controller.player, player_controller.player_model]
            )
            if not slide_check or not slide_check.hit and slide_movement.length() > 0:
                player_controller.player.position += slide_movement
            else:
                player_controller.movement_velocity.x = 0
                player_controller.movement_velocity.z = 0

def handle_momentum_movement(player_controller, target_max_speed):
    """Handle momentum-based ground movement."""
    # Input direction from WASD / arrow keys
    input_dir = Vec3(
        held_keys['d'] - held_keys['a'],  # right-left
        0,
        held_keys['w'] - held_keys['s']   # forward-back
    )
    if input_dir.length() > 0:
        input_dir = input_dir.normalized()

    # Build world-space move direction ignoring vertical component
    if input_dir.length() > 0:
        move_dir_world = (camera.forward * input_dir.z + camera.right * input_dir.x)
        move_dir_world.y = 0
        if move_dir_world.length() > 0:
            move_dir_world = move_dir_world.normalized()
    else:
        move_dir_world = Vec3(0, 0, 0)

    # Apply acceleration when input provided
    if move_dir_world.length() > 0:
        player_controller.movement_velocity += move_dir_world * ACCELERATION * time.dt
    else:
        # Apply friction to horizontal velocity
        horiz = Vec3(player_controller.movement_velocity.x, 0, player_controller.movement_velocity.z)
        if horiz.length() > 0:
            friction_force = horiz.normalized() * FRICTION * time.dt
            if friction_force.length() >= horiz.length():
                player_controller.movement_velocity.x = 0
                player_controller.movement_velocity.z = 0
            else:
                player_controller.movement_velocity.x -= friction_force.x
                player_controller.movement_velocity.z -= friction_force.z

    # Cap horizontal speed (respect sprint target, but allow dash boost)
    horiz_speed = math.sqrt(player_controller.movement_velocity.x**2 + player_controller.movement_velocity.z**2)
    
    # Allow higher speeds temporarily after dashing
    dash_speed_multiplier = 3.0 if player_controller.dash_timer > (DASH_COOLDOWN - 0.5) else 1.0
    effective_max_speed = target_max_speed * dash_speed_multiplier
    
    if horiz_speed > effective_max_speed:
        scale = effective_max_speed / horiz_speed
        player_controller.movement_velocity.x *= scale
        player_controller.movement_velocity.z *= scale

def handle_jumping(player_controller):
    """Handle jumping physics."""
    # gravity acceleration used for vertical integration
    gravity_accel = 9.8 * PLAYER_GRAVITY
    if player_controller.player.grounded and held_keys['space']:
        # required initial velocity to reach desired jump height: v = sqrt(2 * g * h)
        jump_vel = math.sqrt(2 * gravity_accel * PLAYER_JUMP_HEIGHT)
        player_controller.movement_velocity.y = jump_vel
        player_controller.is_airborne = True

def handle_airborne_movement(player_controller):
    """Handle movement when player is airborne."""
    gravity_accel = 9.8 * PLAYER_GRAVITY
    player_controller.movement_velocity.y -= gravity_accel * time.dt
    
    # Apply air resistance to vertical movement for balance
    if abs(player_controller.movement_velocity.y) > 0:
        air_resistance = player_controller.movement_velocity.y * 0.5 * time.dt  # 50% air resistance
        player_controller.movement_velocity.y -= air_resistance
    
    # Apply movement with collision checking for airborne movement
    full_movement = player_controller.movement_velocity * time.dt
    
    # Check horizontal movement first
    horizontal_movement = Vec3(full_movement.x, 0, full_movement.z)
    if horizontal_movement.length() > 0:
        collision_check = check_collision(
            origin=player_controller.player.position,
            direction=horizontal_movement.normalized(),
            distance=horizontal_movement.length(),
            ignore_list=[player_controller.player, player_controller.player_model]
        )
        
        if not collision_check or not collision_check.hit:
            player_controller.player.position += horizontal_movement
        else:
            # Hit wall while airborne - slide along it
            slide_movement = apply_slide_movement(horizontal_movement, collision_check.normal)
            slide_check = check_collision(
                origin=player_controller.player.position,
                direction=slide_movement.normalized() if slide_movement.length() > 0 else Vec3(0,0,0),
                distance=slide_movement.length(),
                ignore_list=[player_controller.player, player_controller.player_model]
            )
            if not slide_check or not slide_check.hit and slide_movement.length() > 0:
                player_controller.player.position += slide_movement
            else:
                player_controller.movement_velocity.x = 0
                player_controller.movement_velocity.z = 0
    
    # Apply vertical movement separately (for gravity/jumping)
    vertical_movement = Vec3(0, full_movement.y, 0)
    if vertical_movement.y != 0:
        # Check for ceiling collision when moving up
        if vertical_movement.y > 0:
            ceiling_check = raycast(
                origin=player_controller.player.position + HEAD_HEIGHT_OFFSET,
                direction=Vec3(0, 1, 0),
                distance=abs(vertical_movement.y) + 0.1,
                ignore=[player_controller.player, player_controller.player_model]
            )
            if ceiling_check and ceiling_check.hit:
                player_controller.movement_velocity.y = 0
            else:
                player_controller.player.position += vertical_movement
        else:
            # Moving down (gravity), apply normally
            player_controller.player.position += vertical_movement

def handle_grounded_movement(player_controller):
    """Handle movement when player is on ground."""
    horizontal_movement = Vec3(player_controller.movement_velocity.x, 0, player_controller.movement_velocity.z)
    step_size = horizontal_movement * time.dt
    
    apply_horizontal_movement_with_collision(player_controller, step_size)
    
    player_controller.movement_velocity.y = 0
    player_controller.is_airborne = False