"""
3D First-Person Shooter Game
============================

A physics-based FPS game built with the Ursina engine featuring:
- Advanced movement mechanics (sliding, dashing, momentum-based physics, wall running)
- Target shooting with accuracy tracking
- Two game modes: Casual play and timed challenges
- 3D environment with custom maps and gun models
- Physics-based gun dropping/respawning system

Controls:
- WASD: Movement
- Mouse: Look around
- Space: Jump
- Shift: Sprint
- Ctrl: Slide (while sprinting)
- Q: Dash
- Left Click: Shoot
- R: Drop/respawn gun
- W + A/D: Wall running (hold forward + wall direction)
- Escape: Quit

Author: Matthew Richardson
Engine: Ursina (Python 3D game engine)
"""

from ursina import *

# Import all game modules
from config import *
from utils import *
from player import PlayerController
from weapons import WeaponController
from targets import TargetManager
from game_state import GameState
from menu import MenuSystem
from map_environment import MapEnvironment
from wall_running import *
from physics import *
import input_handler  # This sets up the global input function

# ===============================================
# === GAME INITIALIZATION ======================
# ===============================================

# Initialize Ursina engine
app = Ursina()

# Initialize all game systems in correct order
map_environment = MapEnvironment()
player_controller = PlayerController()
weapon_controller = WeaponController(player_controller)
target_manager = TargetManager()
game_state = GameState()

# Make systems globally accessible BEFORE creating menu
import player
import weapons
import targets
import game_state as gs
import menu
import map_environment as me

player.player_controller = player_controller
weapons.weapon_controller = weapon_controller
targets.target_manager = target_manager
gs.game_state = game_state
me.map_environment = map_environment

# Initialize menu system AFTER setting global references
menu_system = MenuSystem()
menu.menu_system = menu_system

# ===============================================
# === MAIN UPDATE LOOP =========================
# ===============================================

def update():
    """
    Main game update loop - called every frame by Ursina engine.
    Coordinates all game systems including physics, input, and rendering.
    """
    # Early exit if game is not active
    if not player_controller.player.enabled and not game_state.is_timed_mode:
        return
    
    # Safety check for critical objects
    if not player_controller.player or not hasattr(player_controller.player, 'position'):
        return

    # === CORE SYSTEM UPDATES ===
    player_controller.update_velocity_measurement()
    player_controller.update_timers()
    weapon_controller.update_gun_position()
    weapon_controller.update_timers()
    
    # === INPUT PROCESSING ===
    target_max_speed = player_controller.handle_sprint_input()
    player_controller.handle_slide_trigger()
    
    # === WALL RUNNING SYSTEM ===
    handle_wall_running(player_controller)
    update_wall_running_camera(player_controller)
    
    # === TARGET MANAGEMENT ===
    target_manager.respawn_targets()

    # Wall running completely overrides all other movement
    if player_controller.is_wall_running:
        # All physics handled in apply_wall_running_physics()
        # Skip all normal movement, sliding, jumping, dash, etc.
        player_controller.handle_dash_input()  # Still allow dashing while wall running
        game_state.update_timed_mode(target_manager)
        if held_keys['escape']:
            application.quit()
        return
    
    # Normal movement when not wall running
    if player_controller.is_sliding:
        player_controller.handle_sliding_physics()
    else:
        # --- Momentum-based ground movement (applies only when not sliding or wall running) ---
        # Skip normal movement when wall running, as wall running physics take over
        handle_momentum_movement(player_controller, target_max_speed)
        handle_jumping(player_controller)
        
        # Apply movement with collision detection
        if not player_controller.player.grounded:
            handle_airborne_movement(player_controller)
        else:
            handle_grounded_movement(player_controller)

    # === DASH INPUT ===
    player_controller.handle_dash_input()

    # === GAME MODE UPDATES ===
    game_state.update_timed_mode(target_manager)

    # === EXIT HANDLING ===
    if held_keys['escape']:
        application.quit()

# ===============================================
# === GAME EXECUTION ===========================
# ===============================================

# Start the main game loop
# This call blocks until the game window is closed
if __name__ == "__main__":
    app.run()