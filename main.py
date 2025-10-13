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
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

# Import all game modules with error handling
try:
    from config import *
    from core.utils import *
except ImportError as e:
    print(f"❌ Error importing core modules: {e}")
    print("Please ensure all required files are present.")
    sys.exit(1)

try:
    from core.player import PlayerController
    from core.weapons import WeaponController
    from systems.targets import TargetManager
    from ui.game_state import GameState
    from ui.menu import MenuSystem
    from systems.map_environment import MapEnvironment
    from systems.wall_running import *
    from systems.physics import *
    from core.input_handler import input  # Import the input function so Ursina can use it
except ImportError as e:
    print(f"❌ Error importing game modules: {e}")
    print("Please ensure all game files are present and properly configured.")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    sys.exit(1)
    sys.exit(1)

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
import src.core.player as player
import src.core.weapons as weapons
import src.systems.targets as targets
import src.ui.game_state as gs
import src.ui.menu as menu
import src.systems.map_environment as me

player.player_controller = player_controller
weapons.weapon_controller = weapon_controller
targets.target_manager = target_manager
gs.game_state = game_state
me.map_environment = map_environment

# Disable game elements initially (before menu creation)
player_controller.player.enabled = False
weapon_controller.gun_model.enabled = False
weapon_controller.gun_equipped = False
map_environment.hide_game()

# Initialize menu system AFTER setting global references and hiding game
menu_system = MenuSystem()
menu.menu_system = menu_system

# Show the menu by default when game starts
menu_system.show_menu()

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