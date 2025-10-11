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
            color=color.dark_gray,
            z=1,
            texture_filtering='linear'
        )

        # Main menu title
        self.title = Text(
            "Main Menu",
            scale=2,
            origin=(0, 0),
            position=(0, 0.3),
            background=True
        )

        # Game mode selection buttons
        self.casual_button = Button(
            text='Casual Play',
            scale=(0.3, 0.1),
            position=(0, 0.1)
        )
        self.timed_button = Button(
            text='Timed Mode',
            scale=(0.3, 0.1),
            position=(0, -0.05)
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
        button.color = color.yellow

    def on_leave(self, button):
        """Button leave effect."""
        button.scale = (0.3, 0.1)
        button.color = color.green
    
    def hide_game_elements(self):
        """Hide all game elements."""
        try:
            from map_environment import map_environment
            if map_environment:
                map_environment.hide_game()
        except (ImportError, AttributeError):
            pass
        
        try:
            from player import player_controller
            if player_controller:
                player_controller.player.enabled = False
        except (ImportError, AttributeError):
            pass
        
        try:
            from weapons import weapon_controller
            if weapon_controller:
                weapon_controller.gun_model.enabled = False
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
            from map_environment import map_environment
            if map_environment:
                map_environment.show_game()
        except (ImportError, AttributeError):
            pass
        
        try:
            from player import player_controller
            if player_controller:
                player_controller.player.enabled = True
        except (ImportError, AttributeError):
            pass
        
        try:
            from weapons import weapon_controller
            if weapon_controller:
                weapon_controller.gun_model.enabled = True
        except (ImportError, AttributeError):
            pass
        
        try:
            from targets import target_manager
            if target_manager:
                target_manager.spawn_targets()
        except (ImportError, AttributeError):
            pass
        
        camera.fov = 90
        mouse.locked = True
    
    def start_timed_mode(self):
        """Start timed mode."""
        try:
            from game_state import game_state
            from targets import target_manager
            if game_state and target_manager:
                game_state.start_timed_mode(target_manager)
        except (ImportError, AttributeError):
            pass

# Global menu system (will be initialized in main.py)
menu_system = None