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
    """Apply horizontal movement with enhanced collision detection to prevent clipping."""
    if horizontal_movement.length() <= 0:
        return
    
    # Break down large movements into smaller steps to prevent clipping
    max_step_size = MAX_MOVEMENT_STEP
    movement_distance = horizontal_movement.length()
    
    if movement_distance > max_step_size:
        # Break into multiple steps
        num_steps = int(math.ceil(movement_distance / max_step_size))
        step_movement = horizontal_movement / num_steps
        
        for _ in range(num_steps):
            apply_single_movement_step(player_controller, step_movement)
    else:
        # Single step movement
        apply_single_movement_step(player_controller, horizontal_movement)

def apply_single_movement_step(player_controller, movement):
    """Apply a single movement step with collision detection."""
    # Enhanced collision check with multiple rays
    collision_detected = False
    collision_normal = None
    
    # Check collision from multiple points around the player
    check_points = [
        Vec3(0, 0, 0),           # Center
        Vec3(0.3, 0, 0),         # Right
        Vec3(-0.3, 0, 0),        # Left  
        Vec3(0, 0, 0.3),         # Forward
        Vec3(0, 0, -0.3),        # Back
        Vec3(0, 0.5, 0),         # Upper center
    ]
    
    for offset in check_points:
        collision_check = check_collision(
            origin=player_controller.player.position + offset,
            direction=movement.normalized(),
            distance=movement.length() + 0.2,  # Extra safety margin
            ignore_list=[player_controller.player, player_controller.player_model]
        )
        
        if collision_check and collision_check.hit:
            collision_detected = True
            collision_normal = collision_check.normal
            break
    
    if not collision_detected:
        # Safe to move
        player_controller.player.position += movement
    else:
        # Collision detected - try sliding along surface
        slide_movement = apply_slide_movement(movement, collision_normal)
        
        if slide_movement.length() > 0.01:  # Only try sliding if meaningful movement
            # Check if slide movement is safe
            slide_collision = check_collision(
                origin=player_controller.player.position,
                direction=slide_movement.normalized(),
                distance=slide_movement.length() + 0.1,
                ignore_list=[player_controller.player, player_controller.player_model]
            )
            
            if not slide_collision or not slide_collision.hit:
                player_controller.player.position += slide_movement
            else:
                # Can't slide either - stop movement
                player_controller.movement_velocity.x = 0
                player_controller.movement_velocity.z = 0
        else:
            # No valid slide movement - stop
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

    # Cap horizontal speed (respect sprint target, but allow dash and jump speed boosts)
    horiz_speed = math.sqrt(player_controller.movement_velocity.x**2 + player_controller.movement_velocity.z**2)
    
    # Allow higher speeds temporarily after dashing or jumping
    speed_multiplier = 1.0
    if player_controller.dash_timer > (DASH_COOLDOWN - 0.5):
        speed_multiplier = max(speed_multiplier, 3.0)  # Dash boost
    if player_controller.jump_speed_active:
        speed_multiplier = max(speed_multiplier, JUMP_SPEED_BOOST)  # Jump speed boost
    
    effective_max_speed = target_max_speed * speed_multiplier
    
    if horiz_speed > effective_max_speed:
        scale = effective_max_speed / horiz_speed
        player_controller.movement_velocity.x *= scale
        player_controller.movement_velocity.z *= scale

def handle_jumping(player_controller):
    """Handle jumping physics with enhanced feel."""
    # Check for jump input with buffering and coyote time
    if player_controller.handle_jump_input():
        # gravity acceleration used for vertical integration
        gravity_accel = 9.8 * PLAYER_GRAVITY
        # required initial velocity to reach desired jump height: v = sqrt(2 * g * h)
        jump_vel = math.sqrt(2 * gravity_accel * PLAYER_JUMP_HEIGHT)
        player_controller.movement_velocity.y = jump_vel
        player_controller.is_airborne = True
        
        # Consume the jump input
        player_controller.consume_jump()
        
        # Activate jump speed boost
        player_controller.activate_jump_speed()
    
    # Handle variable jump height (jump cutting)
    player_controller.handle_jump_cut()

def handle_airborne_movement(player_controller):
    """Handle movement when player is airborne."""
    gravity_accel = 9.8 * PLAYER_GRAVITY
    
    # Check if player is grappling and apply reduced gravity
    try:
        import src.core.weapons as weapons
        if (hasattr(weapons, 'weapon_controller') and 
            weapons.weapon_controller and 
            hasattr(weapons.weapon_controller, 'grapple_active') and 
            weapons.weapon_controller.grapple_active):
            # Apply reduced gravity when grappling
            gravity_accel *= GRAPPLE_GRAVITY_REDUCTION
    except (ImportError, AttributeError):
        pass  # Use normal gravity if grapple system not available
    
    player_controller.movement_velocity.y -= gravity_accel * time.dt
    
    # Enhanced air control for smoother feel
    input_dir = Vec3(
        held_keys['d'] - held_keys['a'],  # right-left
        0,
        held_keys['w'] - held_keys['s']   # forward-back
    )
    if input_dir.length() > 0:
        input_dir = input_dir.normalized()
        
        # Build world-space move direction
        move_dir_world = (camera.forward * input_dir.z + camera.right * input_dir.x)
        move_dir_world.y = 0
        if move_dir_world.length() > 0:
            move_dir_world = move_dir_world.normalized()
            
            # Apply air control (reduced acceleration in air)
            air_accel = AIR_ACCELERATION * AIR_CONTROL_MULTIPLIER * time.dt
            player_controller.movement_velocity += move_dir_world * air_accel
    
    # Apply air resistance (lighter than ground friction)
    horiz = Vec3(player_controller.movement_velocity.x, 0, player_controller.movement_velocity.z)
    if horiz.length() > 0:
        air_friction_force = horiz.normalized() * AIR_FRICTION * time.dt
        if air_friction_force.length() < horiz.length():
            player_controller.movement_velocity.x -= air_friction_force.x
            player_controller.movement_velocity.z -= air_friction_force.z
    
    # Apply movement with collision checking for airborne movement
    full_movement = player_controller.movement_velocity * time.dt
    
    # Check horizontal movement first with enhanced collision detection
    horizontal_movement = Vec3(full_movement.x, 0, full_movement.z)
    if horizontal_movement.length() > 0:
        apply_horizontal_movement_with_collision(player_controller, horizontal_movement)
    
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
    # Check if player is stuck in geometry and correct position
    correct_player_position(player_controller)
    
    horizontal_movement = Vec3(player_controller.movement_velocity.x, 0, player_controller.movement_velocity.z)
    step_size = horizontal_movement * time.dt
    
    apply_horizontal_movement_with_collision(player_controller, step_size)
    
    player_controller.movement_velocity.y = 0
    player_controller.is_airborne = False

def correct_player_position(player_controller):
    """Correct player position if they're stuck inside geometry."""
    # Check if player is inside a wall
    center_check = raycast(
        origin=player_controller.player.position,
        direction=Vec3(0, 0, 1),  # Check forward
        distance=0.1,
        ignore=[player_controller.player, player_controller.player_model]
    )
    
    if center_check and center_check.hit and center_check.distance < 0.05:
        # Player might be inside geometry - try to push them out
        push_directions = [
            Vec3(1, 0, 0),   # Right
            Vec3(-1, 0, 0),  # Left
            Vec3(0, 0, 1),   # Forward
            Vec3(0, 0, -1),  # Back
            Vec3(0, 1, 0),   # Up
        ]
        
        for direction in push_directions:
            # Try pushing in this direction
            push_distance = 1.0
            push_check = raycast(
                origin=player_controller.player.position,
                direction=direction,
                distance=push_distance,
                ignore=[player_controller.player, player_controller.player_model]
            )
            
            if not push_check or not push_check.hit or push_check.distance > 0.5:
                # Found a safe direction - push player out
                player_controller.player.position += direction * 0.5
                print("Position corrected - pushed player out of geometry")
                break