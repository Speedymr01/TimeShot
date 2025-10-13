"""
Input Handler
=============

Centralized input processing and key bindings.
"""

from ursina import *
from config import *

# ===============================================
# === INPUT HANDLER =============================
# ===============================================

def input(key):
    """
    Handle user input with validation and error prevention.
    
    Args:
        key (str): The input key pressed by the user
    """
    from player import player_controller
    from weapons import weapon_controller
    from game_state import game_state
    from targets import target_manager
    
    # Validate input key
    if not key or not isinstance(key, str):
        return
    
    # Handle menu navigation when game is not active
    if not player_controller.player.enabled and not game_state.is_timed_mode:
        if key == 'enter':
            try:
                game_state.return_to_menu(player_controller)
            except Exception as e:
                print(f"Error returning to menu: {e}")
        return
    
    # Early exit if player is not enabled
    if not player_controller.player.enabled:
        return
    
    # Handle shooting input
    if key == 'left mouse down':
        if weapon_controller.gun_equipped:
            try:
                weapon_controller.shoot(target_manager.target_spheres, game_state)
            except Exception as e:
                print(f"Error during shooting: {e}")
    
    # Handle gun drop input with cooldown check
    if key == 'r' and weapon_controller.gun_drop_timer <= 0:
        try:
            weapon_controller.drop_and_respawn_gun()
            weapon_controller.gun_drop_timer = GUN_DROP_COOLDOWN
        except Exception as e:
            print(f"Error dropping gun: {e}")
    
