"""
Game State Management
=====================

Game modes, UI, and state management.
"""

from ursina import *
from config import *

# ===============================================
# === GAME STATE MANAGEMENT ====================
# ===============================================

class GameState:
    def __init__(self):
        # Timed mode state
        self.is_timed_mode = False
        self.time_remaining = TIMER_DURATION
        self.score = 0
        self.shots_fired = 0
        self.hits = 0
        self.results_screen = None
        
        # UI Elements
        self.timer_text = Text(
            text="Time: 0",
            position=window.top_left + Vec2(0.05, -0.05),
            origin=(0, 0),
            scale=1.2,
            background=True,
            enabled=False
        )
        self.score_text = Text(
            text="Score: 0",
            position=window.top + Vec2(0, -0.05),
            origin=(0, 0),
            scale=1.2,
            background=True,
            enabled=False
        )
        self.accuracy_text = Text(
            text="Accuracy: 0%",
            position=window.top_right + Vec2(-0.25, -0.05),
            origin=(0, 0),
            scale=1.2,
            background=True,
            enabled=False
        )
    
    def start_timed_mode(self, target_manager):
        """Start timed mode with UI and targets."""
        # Hide menu
        try:
            from menu import menu_system
            if menu_system:
                menu_system.hide_menu()
        except (ImportError, AttributeError):
            pass
        
        # Show game elements
        try:
            from map_environment import map_environment
            if map_environment:
                map_environment.show_game()
        except (ImportError, AttributeError):
            pass
        
        # Show HUD
        self.timer_text.enabled = True
        self.score_text.enabled = True
        self.accuracy_text.enabled = True

        # Setup state
        target_manager.spawn_targets()
        camera.fov = 90
        mouse.locked = True
        self.is_timed_mode = True
        self.time_remaining = TIMER_DURATION
        self.score = 0
        self.shots_fired = 0
        self.hits = 0
        self.score_text.text = f"Score: {self.score}"
        self.accuracy_text.text = "Accuracy: 0%"

        if self.results_screen:
            destroy(self.results_screen)
    
    def end_timed_mode(self, target_manager):
        """End timed mode and show results."""
        self.is_timed_mode = False

        # Hide HUD + game elements
        self.timer_text.enabled = False
        self.score_text.enabled = False
        self.accuracy_text.enabled = False
        
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
        
        if target_manager:
            target_manager.clear_targets()

        # Unlock mouse
        mouse.locked = False

        # Calculate accuracy
        accuracy = (self.hits / self.shots_fired * 100) if self.shots_fired > 0 else 0

        # Results screen
        self.results_screen = Text(
            f"⏱ Time's up!\nScore: {self.score}\nAccuracy: {accuracy:.1f}%\n\nPress ENTER to return to Menu",
            origin=(0, 0),
            scale=2,
            background=True,
            color=color.yellow
        )
    
    def update_timed_mode(self, target_manager):
        """Update timed mode countdown and UI."""
        if self.is_timed_mode:
            self.time_remaining -= time.dt
            self.timer_text.text = f"Time: {int(self.time_remaining)}"
            if self.time_remaining <= 0:
                self.end_timed_mode(target_manager)
    
    def return_to_menu(self, player_controller):
        """Return to main menu."""
        if self.results_screen:
            destroy(self.results_screen)
            self.results_screen = None

        # Show menu again
        try:
            from menu import menu_system
            if menu_system:
                menu_system.show_menu()
        except (ImportError, AttributeError):
            pass
        
        # Reset player
        if player_controller:
            player_controller.player.position = PLAYER_START_POS
            player_controller.player.rotation = Vec3(0, 0, 0)

# Global game state (will be initialized in main.py)
game_state = None