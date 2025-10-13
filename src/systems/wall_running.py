"""
Wall Running System
===================

Advanced wall running mechanics with input requirements and physics.
"""

from ursina import *
from config import *
from utils import *
import math

# ===============================================
# === WALL RUNNING SYSTEM ===================
# ===============================================

def check_wall_running_input(wall_run_side):
    """
    Check if player is holding the correct keys for wall running.
    Must hold W (forward) + A (left wall) or W + D (right wall).
    """
    forward_held = held_keys['w']
    left_held = held_keys['a']
    right_held = held_keys['d']
    
    if not forward_held:
        return False
    
    if wall_run_side == 1:  # Right wall
        return right_held
    elif wall_run_side == -1:  # Left wall
        return left_held
    
    return False

def detect_wall_for_running(player_controller):
    """
    Detect if player can start wall running on nearby walls.
    Must be holding W + A (left wall) or W + D (right wall).
    Returns wall normal and side (-1 left, 1 right, 0 none).
    """
    if not player_controller.player or player_controller.is_sliding:
        return None, 0
    
    # Must be holding forward key to start wall running
    if not held_keys['w']:
        return None, 0
    
    # Check horizontal speed requirement
    horizontal_speed = math.sqrt(player_controller.movement_velocity.x**2 + player_controller.movement_velocity.z**2)
    if horizontal_speed < WALL_RUN_MIN_SPEED:
        return None, 0
    
    # Check walls on left and right sides with multiple rays for better detection
    player_right = camera.right.normalized()
    
    # Check right wall with multiple height points
    right_hits = []
    for height_offset in [0.5, 1.0, 1.5]:
        right_hit = raycast(
            origin=player_controller.player.position + Vec3(0, height_offset, 0),
            direction=player_right,
            distance=2.0,
            ignore=[player_controller.player, player_controller.player_model]
        )
        if right_hit and right_hit.hit:
            right_hits.append(right_hit)
    
    # Check left wall with multiple height points
    left_hits = []
    for height_offset in [0.5, 1.0, 1.5]:
        left_hit = raycast(
            origin=player_controller.player.position + Vec3(0, height_offset, 0),
            direction=-player_right,
            distance=2.0,
            ignore=[player_controller.player, player_controller.player_model]
        )
        if left_hit and left_hit.hit:
            left_hits.append(left_hit)
    
    # Determine which wall to use
    movement_dir = Vec3(player_controller.movement_velocity.x, 0, player_controller.movement_velocity.z)
    if movement_dir.length() > 0:
        movement_dir = movement_dir.normalized()
    
    # Check right wall (must be holding W + D)
    if right_hits and held_keys['d']:
        right_hit = right_hits[0]
        if abs(right_hit.normal.y) < 0.5:
            dot_product = movement_dir.dot(player_right) if movement_dir.length() > 0 else 0
            if dot_product > 0.1:
                return right_hit.normal, 1
    
    # Check left wall (must be holding W + A)
    if left_hits and held_keys['a']:
        left_hit = left_hits[0]
        if abs(left_hit.normal.y) < 0.5:
            dot_product = movement_dir.dot(-player_right) if movement_dir.length() > 0 else 0
            if dot_product > 0.1:
                return left_hit.normal, -1
    
    return None, 0

def apply_wall_running_physics(player_controller):
    """
    Apply physics while wall running - requires holding correct input keys.
    """
    # Note: Key release handling is now done in handle_wall_running() 
    # to allow for kick effect before stopping
    
    # COMPLETELY override vertical movement - no gravity at all
    player_controller.movement_velocity.y = 0  # Reset any existing vertical velocity
    
    # Apply strong upward force to stick to wall
    player_controller.movement_velocity.y += 8.0 * time.dt
    
    # Cap vertical velocity
    player_controller.movement_velocity.y = max(-2, min(8, player_controller.movement_velocity.y))
    
    # Calculate movement along the wall with consistent horizontal speed
    forward_dir = camera.forward.normalized()
    
    # Get horizontal component of look direction (ignore Y)
    horizontal_forward = Vec3(forward_dir.x, 0, forward_dir.z)
    
    if horizontal_forward.length() > 0:
        horizontal_forward = horizontal_forward.normalized()
        
        # Project horizontal direction onto wall surface for full horizontal speed
        wall_horizontal = horizontal_forward - player_controller.wall_normal * horizontal_forward.dot(player_controller.wall_normal)
        
        if wall_horizontal.length() > 0:
            wall_horizontal = wall_horizontal.normalized()
            # Apply full speed horizontally
            horizontal_velocity = wall_horizontal * WALL_RUN_SPEED
        else:
            horizontal_velocity = Vec3(0, 0, 0)
    else:
        # If looking straight up/down, maintain current direction or use wall tangent
        # Use the wall's tangent direction (perpendicular to wall normal)
        wall_right = Vec3(-player_controller.wall_normal.z, 0, player_controller.wall_normal.x).normalized()
        horizontal_velocity = wall_right * WALL_RUN_SPEED * 0.5  # Reduced speed when no clear direction
    
    # Add miniscule vertical component based on look direction
    vertical_influence = forward_dir.y * WALL_RUN_SPEED * 0.1  # 10% of speed as vertical influence
    
    # DIRECTLY set horizontal velocity (no lerping - immediate response)
    player_controller.movement_velocity.x = horizontal_velocity.x
    player_controller.movement_velocity.z = horizontal_velocity.z
    
    # Add small vertical influence to the existing upward force
    player_controller.movement_velocity.y += vertical_influence * time.dt
    
    # Extremely strong inward force to stick to wall
    stick_force = player_controller.wall_normal * -20.0 * time.dt
    player_controller.movement_velocity.x += stick_force.x
    player_controller.movement_velocity.z += stick_force.z
    
    # Apply movement directly to player position
    player_controller.player.position += player_controller.movement_velocity * time.dt
    
    print(f"Wall running - Y vel: {player_controller.movement_velocity.y:.2f}, Speed: {math.sqrt(player_controller.movement_velocity.x**2 + player_controller.movement_velocity.z**2):.2f}, Keys: W+{'D' if player_controller.wall_run_side == 1 else 'A'}")

def handle_wall_running(player_controller):
    """Handle wall running detection and state management."""
    if not player_controller.is_wall_running:
        # Try to start wall running
        detected_normal, detected_side = detect_wall_for_running(player_controller)
        
        if detected_normal and detected_side != 0 and not player_controller.player.grounded:
            player_controller.is_wall_running = True
            player_controller.wall_normal = detected_normal
            player_controller.wall_run_side = detected_side
            player_controller.wall_run_timer = 0.0
            print(f"Started wall running on {'right' if detected_side == 1 else 'left'} wall - Hold W+{'D' if detected_side == 1 else 'A'} to continue - Speed: {math.sqrt(player_controller.movement_velocity.x**2 + player_controller.movement_velocity.z**2):.1f}")
    
    else:
        # Continue wall running
        player_controller.wall_run_timer += time.dt
        
        # Check if we should stop wall running
        should_stop = False
        
        # Stop if timer exceeded
        if player_controller.wall_run_timer > WALL_RUN_MAX_TIME:
            should_stop = True
        
        # Stop if we hit the ground
        if player_controller.player.grounded:
            should_stop = True
        
        # Stop if player releases required keys - apply kick effect
        if not check_wall_running_input(player_controller.wall_run_side):
            # Apply wall kick when releasing keys (same as space jump)
            jump_direction = player_controller.wall_normal.normalized()
            
            # Strong horizontal kick away from wall
            kick_force = WALL_RUN_JUMP_FORCE * 1.5
            player_controller.movement_velocity.x = jump_direction.x * kick_force
            player_controller.movement_velocity.z = jump_direction.z * kick_force
            
            # Strong upward component
            player_controller.movement_velocity.y = WALL_RUN_JUMP_FORCE * 1.2
            
            should_stop = True
            print(f"Wall kick from key release! Kicked away from {'right' if player_controller.wall_run_side == 1 else 'left'} wall with force {kick_force:.1f}")
        
        # Stop if we're no longer near the wall (more forgiving check)
        check_direction = camera.right if player_controller.wall_run_side == 1 else -camera.right
        wall_still_there = False
        
        # Check multiple points to be more forgiving
        for height_offset in [0.5, 1.0, 1.5]:
            for distance in [2.5, 3.0]:
                wall_check = raycast(
                    origin=player_controller.player.position + Vec3(0, height_offset, 0),
                    direction=check_direction,
                    distance=distance,
                    ignore=[player_controller.player, player_controller.player_model]
                )
                if wall_check and wall_check.hit:
                    # Update wall normal for better tracking
                    player_controller.wall_normal = wall_check.normal
                    wall_still_there = True
                    break
            if wall_still_there:
                break
        
        if not wall_still_there:
            should_stop = True
        
        # Stop if player jumps (space key)
        if held_keys['space']:
            # Wall jump - kick player away from wall with strong force
            jump_direction = player_controller.wall_normal.normalized()
            
            # Strong horizontal kick away from wall
            kick_force = WALL_RUN_JUMP_FORCE * 1.5
            player_controller.movement_velocity.x = jump_direction.x * kick_force
            player_controller.movement_velocity.z = jump_direction.z * kick_force
            
            # Strong upward component
            player_controller.movement_velocity.y = WALL_RUN_JUMP_FORCE * 1.2
            
            should_stop = True
            print(f"Wall jump! Kicked away from {'right' if player_controller.wall_run_side == 1 else 'left'} wall with force {kick_force:.1f}")
        
        if should_stop:
            player_controller.is_wall_running = False
            player_controller.wall_run_timer = 0.0
            player_controller.wall_run_side = 0
            print("Stopped wall running")
        else:
            # Apply wall running physics
            apply_wall_running_physics(player_controller)

def update_wall_running_camera(player_controller):
    """Apply camera effects during wall running."""
    if player_controller.is_wall_running:
        # Tilt camera based on wall side
        target_tilt = WALL_RUN_CAMERA_TILT * player_controller.wall_run_side
        try:
            if hasattr(camera, 'rotation_z'):
                camera.rotation_z = lerp(camera.rotation_z, target_tilt, time.dt * 5)
        except:
            pass
    else:
        # Return camera to normal
        try:
            if hasattr(camera, 'rotation_z'):
                camera.rotation_z = lerp(camera.rotation_z, 0, time.dt * 8)
        except:
            pass