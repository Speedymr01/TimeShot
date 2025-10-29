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
    Apply physics while wall running - continues automatically once started.
    """
    # Wall running now continues until wall ends or player jumps
    
    # Completely disable Ursina's built-in physics during wall running
    disable_ursina_physics(player_controller)
    
    # COMPLETELY eliminate slipping - override ALL vertical movement
    # Disable Ursina's built-in gravity during wall running
    player_controller.player.velocity_y = 0
    player_controller.movement_velocity.y = 0
    
    # Force zero vertical velocity in the Ursina controller
    if hasattr(player_controller.player, 'velocity'):
        player_controller.player.velocity = Vec3(player_controller.player.velocity.x, 0, player_controller.player.velocity.z)
    
    # Optional: Allow slight vertical movement based on look direction
    forward_dir = camera.forward.normalized()
    vertical_control = 0
    if forward_dir.y > 0.1:  # Looking up
        vertical_control = forward_dir.y * WALL_RUN_SPEED * 0.3
    elif forward_dir.y < -0.1:  # Looking down
        vertical_control = forward_dir.y * WALL_RUN_SPEED * 0.3
    
    # Apply vertical control directly to position instead of velocity
    if abs(vertical_control) > 0.01:
        player_controller.player.position += Vec3(0, vertical_control * time.dt, 0)
    
    # Calculate movement along the wall with consistent horizontal speed
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
    
    # DIRECTLY set horizontal velocity (no lerping - immediate response)
    player_controller.movement_velocity.x = horizontal_velocity.x
    player_controller.movement_velocity.z = horizontal_velocity.z
    
    # Extremely strong inward force to stick to wall
    stick_force = player_controller.wall_normal * -20.0 * time.dt
    player_controller.movement_velocity.x += stick_force.x
    player_controller.movement_velocity.z += stick_force.z
    
    # Apply movement directly to player position, bypassing Ursina's physics
    movement_step = Vec3(
        player_controller.movement_velocity.x * time.dt,
        0,  # Force zero vertical movement
        player_controller.movement_velocity.z * time.dt
    )
    player_controller.player.position += movement_step
    
    # Ensure Ursina's controller doesn't interfere
    player_controller.player.velocity_y = 0
    if hasattr(player_controller.player, 'velocity'):
        player_controller.player.velocity = Vec3(0, 0, 0)
    
    print(f"Wall running - No slip mode - Y vel: {player_controller.movement_velocity.y:.2f}, Speed: {math.sqrt(player_controller.movement_velocity.x**2 + player_controller.movement_velocity.z**2):.2f}")

def disable_ursina_physics(player_controller):
    """Completely disable Ursina's built-in physics during wall running."""
    try:
        # Disable gravity
        player_controller.player.gravity = 0
        
        # Zero out all Ursina velocities
        player_controller.player.velocity_y = 0
        if hasattr(player_controller.player, 'velocity'):
            player_controller.player.velocity = Vec3(0, 0, 0)
        
        # Disable Ursina's movement processing
        if hasattr(player_controller.player, 'grounded'):
            player_controller.player.grounded = True  # Trick Ursina into thinking we're grounded
            
    except AttributeError:
        pass  # Some attributes might not exist in all Ursina versions

def restore_ursina_physics(player_controller):
    """Restore Ursina's built-in physics after wall running."""
    try:
        # Restore gravity
        player_controller.player.gravity = PLAYER_GRAVITY
        
        # Allow Ursina to process movement again
        if hasattr(player_controller.player, 'grounded'):
            # Let Ursina determine grounded state naturally
            pass
            
    except AttributeError:
        pass

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
            print(f"Started wall running on {'right' if detected_side == 1 else 'left'} wall - Press SPACE to jump off - Speed: {math.sqrt(player_controller.movement_velocity.x**2 + player_controller.movement_velocity.z**2):.1f}")
    
    else:
        # Continue wall running
        player_controller.wall_run_timer += time.dt
        
        # Check if we should stop wall running
        should_stop = False
        
        # ONLY stop wall running if:
        # 1. Wall ends (no longer near wall)
        # 2. Player presses space to jump
        
        # Check if wall still exists
        check_direction = camera.right if player_controller.wall_run_side == 1 else -camera.right
        wall_still_there = False
        
        # Check multiple points to detect wall end
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
        
        # Stop condition 1: Wall ends - apply momentum kick
        if not wall_still_there:
            # Calculate wall running direction for momentum kick
            forward_dir = camera.forward.normalized()
            horizontal_forward = Vec3(forward_dir.x, 0, forward_dir.z)
            
            if horizontal_forward.length() > 0:
                horizontal_forward = horizontal_forward.normalized()
                # Project direction along wall surface
                wall_direction = horizontal_forward - player_controller.wall_normal * horizontal_forward.dot(player_controller.wall_normal)
                
                if wall_direction.length() > 0:
                    wall_direction = wall_direction.normalized()
                    
                    # Apply momentum kick in wall running direction
                    kick_force = WALL_RUN_SPEED * WALL_END_MOMENTUM_KICK
                    player_controller.movement_velocity.x = wall_direction.x * kick_force
                    player_controller.movement_velocity.z = wall_direction.z * kick_force
                    
                    # Small upward component to help with transitions
                    player_controller.movement_velocity.y = WALL_RUN_JUMP_FORCE * 0.3
                    
                    print(f"Wall ended - momentum kick applied! Direction: {wall_direction}, Force: {kick_force:.1f}")
                else:
                    print("Wall running stopped - wall ended (no momentum)")
            else:
                print("Wall running stopped - wall ended (no direction)")
            
            should_stop = True
        
        # Stop condition 2: Player jumps (space key)
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
            
            # Restore normal physics when wall running ends
            restore_ursina_physics(player_controller)
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