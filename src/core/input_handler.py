"""
Input Handler
=============

Centralized input processing and key bindings.
"""

from ursina import *
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'config'))

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
    # Import with error handling using global references
    try:
        import src.core.player as player
        import src.core.weapons as weapons
        import src.ui.game_state as gs
        import src.systems.targets as targets
        
        player_controller = getattr(player, 'player_controller', None)
        weapon_controller = getattr(weapons, 'weapon_controller', None)
        game_state = getattr(gs, 'game_state', None)
        target_manager = getattr(targets, 'target_manager', None)
        
        if not all([player_controller, weapon_controller, game_state, target_manager]):
            return
            
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        return
    
    # Validate input key
    if not key or not isinstance(key, str):
        return
    
    # Sanitize input key (prevent injection)
    key = key.strip()
    if len(key) > 50:  # Reasonable key length limit
        return
    
    # Validate game objects exist
    if not all([player_controller, weapon_controller, game_state, target_manager]):
        return
    
    # Handle menu navigation when game is not active
    if not player_controller.player.enabled and not game_state.is_timed_mode:
        if key == 'enter':
            try:
                game_state.return_to_menu(player_controller)
            except AttributeError as e:
                print(f"Error returning to menu: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        return
    
    # Early exit if player is not enabled
    if not player_controller.player.enabled:
        return
    
    # Handle shooting input
    if key == 'left mouse down':
        if hasattr(weapon_controller, 'gun_equipped') and weapon_controller.gun_equipped:
            try:
                if hasattr(target_manager, 'target_spheres'):
                    weapon_controller.shoot(target_manager.target_spheres, game_state)
            except AttributeError as e:
                print(f"Error during shooting - missing attribute: {e}")
            except Exception as e:
                print(f"Error during shooting: {e}")
    
    # Handle grappling hook input
    if key == 'right mouse down':
        if hasattr(weapon_controller, 'gun_equipped') and weapon_controller.gun_equipped:
            try:
                weapon_controller.fire_grapple()
            except AttributeError as e:
                print(f"Error during grappling - missing attribute: {e}")
            except Exception as e:
                print(f"Error during grappling: {e}")
    
    # Handle grappling hook release
    if key == 'right mouse up':
        if hasattr(weapon_controller, 'grapple_active') and weapon_controller.grapple_active:
            try:
                weapon_controller.release_grapple()
            except AttributeError as e:
                print(f"Error releasing grapple - missing attribute: {e}")
            except Exception as e:
                print(f"Error releasing grapple: {e}")
    
    # Handle gun drop input with cooldown check
    if key == 'r':
        try:
            if (hasattr(weapon_controller, 'gun_drop_timer') and 
                weapon_controller.gun_drop_timer <= 0):
                weapon_controller.drop_and_respawn_gun()
                weapon_controller.gun_drop_timer = GUN_DROP_COOLDOWN
        except AttributeError as e:
            print(f"Error dropping gun - missing attribute: {e}")
        except Exception as e:
            print(f"Error dropping gun: {e}")
    
    # Graphics settings hotkeys (for debugging/testing)
    if key == 'f1':
        try:
            from src.core.graphics_utils import print_graphics_info
            print_graphics_info()
        except ImportError:
            print("Graphics utilities not available")
    
    if key == 'f2':
        try:
            from src.core.graphics_utils import optimize_for_performance
            optimize_for_performance()
        except ImportError:
            print("Graphics utilities not available")
    
    if key == 'f3':
        try:
            from src.core.graphics_utils import optimize_for_quality
            optimize_for_quality()
        except ImportError:
            print("Graphics utilities not available")
    
    if key == 'f4':
        try:
            from src.core.graphics_utils import optimize_for_ultra
            optimize_for_ultra()
        except ImportError:
            print("Graphics utilities not available")
    
    # Texture quality hotkeys
    if key == 'f5':
        try:
            from src.core.graphics_utils import set_texture_quality
            set_texture_quality('low')
        except ImportError:
            print("Graphics utilities not available")
    
    if key == 'f6':
        try:
            from src.core.graphics_utils import set_texture_quality
            set_texture_quality('medium')
        except ImportError:
            print("Graphics utilities not available")
    
    if key == 'f7':
        try:
            from src.core.graphics_utils import set_texture_quality
            set_texture_quality('high')
        except ImportError:
            print("Graphics utilities not available")
    
    if key == 'f8':
        try:
            from src.core.graphics_utils import set_texture_quality
            set_texture_quality('ultra')
        except ImportError:
            print("Graphics utilities not available")
    
