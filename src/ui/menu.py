"""
Menu System
===========

Main menu, UI, and navigation.
"""

from ursina import *
from config import *

# ===============================================
# === MENU SYSTEM ===============================
# ===============================================

class MenuSystem:
    def __init__(self):
        # Menu background
        self.menu_background = Entity(
            model='quad',
            scale=(1.5, 1),
            color=MENU_BACKGROUND_COLOR,
            z=1,
            texture_filtering=TEXTURE_FILTERING
        )

        # Main menu title
        self.title = Text(
            "Main Menu",
            scale=MENU_FONT_SIZE * 1.5,
            origin=(0, 0),
            position=(0, 0.3),
            background=True,
            color=MENU_TEXT_COLOR
        )

        # Game mode selection buttons
        self.casual_button = Button(
            text='Casual Play' if CASUAL_MODE_ENABLED else 'Casual (Disabled)',
            scale=(0.3, 0.1),
            position=(0, 0.1),
            color=MENU_BUTTON_COLOR,
            enabled=CASUAL_MODE_ENABLED
        )
        self.timed_button = Button(
            text='Timed Mode' if TIMED_MODE_ENABLED else 'Timed (Disabled)',
            scale=(0.3, 0.1),
            position=(0, -0.05),
            color=MENU_BUTTON_COLOR,
            enabled=TIMED_MODE_ENABLED
        )

        # Button hover effects
        self.casual_button.on_mouse_enter = lambda: self.on_hover(self.casual_button)
        self.casual_button.on_mouse_exit = lambda: self.on_leave(self.casual_button)
        self.timed_button.on_mouse_enter = lambda: self.on_hover(self.timed_button)
        self.timed_button.on_mouse_exit = lambda: self.on_leave(self.timed_button)

        # Button click handlers
        self.casual_button.on_click = self.start_casual_play
        self.timed_button.on_click = self.start_timed_mode

        # Initially hide game elements
        self.hide_game_elements()
    
    def on_hover(self, button):
        """Button hover effect."""
        button.scale = (0.32, 0.11)
        button.color = MENU_HOVER_COLOR

    def on_leave(self, button):
        """Button leave effect."""
        button.scale = (0.3, 0.1)
        button.color = MENU_BUTTON_COLOR
    
    def hide_game_elements(self):
        """Hide all game elements."""
        # Use global references instead of imports since they're already set up
        try:
            import src.systems.map_environment as me
            if hasattr(me, 'map_environment') and me.map_environment:
                me.map_environment.hide_game()
        except (ImportError, AttributeError):
            pass
        
        try:
            import src.core.player as player
            if hasattr(player, 'player_controller') and player.player_controller:
                player.player_controller.player.enabled = False
        except (ImportError, AttributeError):
            pass
        
        try:
            import src.core.weapons as weapons
            if hasattr(weapons, 'weapon_controller') and weapons.weapon_controller:
                weapons.weapon_controller.gun_model.enabled = False
                weapons.weapon_controller.gun_equipped = False
        except (ImportError, AttributeError):
            pass
    
    def show_menu(self):
        """Show the main menu."""
        self.menu_background.enabled = True
        self.title.enabled = True
        self.casual_button.enabled = True
        self.timed_button.enabled = True
        self.hide_game_elements()
    
    def hide_menu(self):
        """Hide the main menu."""
        self.menu_background.enabled = False
        self.title.enabled = False
        self.casual_button.enabled = False
        self.timed_button.enabled = False
    
    def start_casual_play(self):
        """Start casual play mode."""
        self.hide_menu()
        
        try:
            import src.systems.map_environment as me
            if hasattr(me, 'map_environment') and me.map_environment:
                me.map_environment.show_game()
        except (ImportError, AttributeError):
            pass
        
        try:
            import src.core.player as player
            if hasattr(player, 'player_controller') and player.player_controller:
                player.player_controller.player.enabled = True
        except (ImportError, AttributeError):
            pass
        
        try:
            import src.core.weapons as weapons
            if hasattr(weapons, 'weapon_controller') and weapons.weapon_controller:
                weapons.weapon_controller.gun_model.enabled = True
                weapons.weapon_controller.gun_equipped = True
        except (ImportError, AttributeError):
            pass
        
        try:
            import src.systems.targets as targets
            if hasattr(targets, 'target_manager') and targets.target_manager:
                targets.target_manager.spawn_targets()
        except (ImportError, AttributeError):
            pass
        
        camera.fov = FOV_DEFAULT
        mouse.locked = True
    
    def start_timed_mode(self):
        """Start timed mode."""
        try:
            import src.ui.game_state as gs
            import src.systems.targets as targets
            if (hasattr(gs, 'game_state') and gs.game_state and 
                hasattr(targets, 'target_manager') and targets.target_manager):
                gs.game_state.start_timed_mode(targets.target_manager)
        except (ImportError, AttributeError):
            pass

# Global menu system (will be initialized in main.py)
menu_system = None