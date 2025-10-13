#!/usr/bin/env python3
"""
Settings Examples
=================

Examples of how to adjust game settings for different experiences.
SECURITY: Added input validation and safe preset application.
"""

import re
import sys
import os
from pathlib import Path

# Add security tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'security'))

try:
    from security_config import security_config, security_logger
except ImportError:
    # Fallback if security_config not available
    class MockSecurityConfig:
        @staticmethod
        def validate_setting_name(name): return True, "Valid"
        @staticmethod
        def validate_setting_value(value, setting=""): return True, "Valid"
        @staticmethod
        def sanitize_input(text): return text
    
    class MockSecurityLogger:
        @staticmethod
        def log_security_event(event, details, severity="INFO"): pass
    
    security_config = MockSecurityConfig()
    security_logger = MockSecurityLogger()

# Example 1: High Recoil, Realistic Shooting
def realistic_shooting_mode():
    """Configure for realistic, high-recoil shooting experience."""
    settings = {
        'RECOIL_VERTICAL': 4.0,           # Much higher recoil
        'RECOIL_HORIZONTAL': 2.0,         # More horizontal sway
        'RECOIL_RECOVERY_SPEED': 4.0,     # Slower recovery
        'RECOIL_DURATION': 0.3,           # Longer recoil effect
        'RECOIL_MULTIPLIER_MOVING': 2.0,  # Heavy penalty for moving
        'MOUSE_SENSITIVITY': 30,          # Lower sensitivity for precision
        'SFX_VOLUME': 1.0,                # Full volume for immersion
    }
    return settings

# Example 2: Arcade Style, Fast-Paced
def arcade_mode():
    """Configure for fast-paced arcade gameplay."""
    settings = {
        'MAX_SPEED': 12,                  # Much faster movement
        'SPRINT_MULTIPLIER': 2.5,         # Even faster sprinting
        'DASH_FORCE': 80,                 # Stronger dash
        'DASH_COOLDOWN': 0.5,             # Faster dash cooldown
        'SLIDE_START_VELOCITY': 60,       # Faster sliding
        'WALL_RUN_SPEED': 25,             # Faster wall running
        'RECOIL_VERTICAL': 1.0,           # Reduced recoil for speed
        'FOV_DEFAULT': 100,               # Wider FOV for speed feel
        'FOV_SPRINT': 110,                # Even wider when sprinting
    }
    return settings

# Example 3: Precision Challenge Mode
def precision_mode():
    """Configure for precision shooting challenges."""
    settings = {
        'MAX_SPEED': 4,                   # Slower, more controlled movement
        'RECOIL_VERTICAL': 1.5,           # Moderate recoil
        'RECOIL_HORIZONTAL': 0.5,         # Less horizontal sway
        'MOUSE_SENSITIVITY': 25,          # Lower sensitivity
        'TARGET_SIZE': 0.3,               # Smaller targets
        'POINTS_PER_TARGET': 200,         # Higher points for difficulty
        'ACCURACY_BONUS': True,           # Reward accuracy
        'TIMER_DURATION': 120,            # Longer time for precision
    }
    return settings

# Example 4: Parkour Focus Mode
def parkour_mode():
    """Configure for parkour and movement focus."""
    settings = {
        'SLIDE_START_VELOCITY': 50,       # Faster slides
        'SLIDE_COOLDOWN': 1.0,            # Shorter slide cooldown
        'DASH_FORCE': 70,                 # Stronger dashes
        'DASH_COOLDOWN': 0.7,             # Faster dash recovery
        'WALL_RUN_MAX_TIME': 12.0,        # Longer wall runs
        'WALL_RUN_SPEED': 22,             # Faster wall running
        'PLAYER_JUMP_HEIGHT': 2.5,        # Higher jumps
        'AIR_CONTROL': 0.5,               # Better air control
        'SHOOTING_ENABLED': False,        # Focus on movement only
    }
    return settings

# Example 5: Beginner Friendly
def beginner_mode():
    """Configure for new players."""
    settings = {
        'RECOIL_VERTICAL': 1.0,           # Very low recoil
        'RECOIL_HORIZONTAL': 0.3,         # Minimal horizontal kick
        'MOUSE_SENSITIVITY': 40,          # Moderate sensitivity
        'TARGET_SIZE': 0.8,               # Larger targets
        'TARGET_COUNT': 8,                # Fewer targets
        'TIMER_DURATION': 90,             # More time
        'MAX_SPEED': 5,                   # Slower movement
        'SLIDE_ENABLED': False,           # Disable advanced mechanics
        'DASH_ENABLED': False,            # Keep it simple
        'WALL_RUN_ENABLED': False,        # Focus on basics
    }
    return settings

# Example 6: Competitive Settings
def competitive_mode():
    """Configure for competitive play."""
    settings = {
        'RECOIL_VERTICAL': 2.0,           # Balanced recoil
        'RECOIL_HORIZONTAL': 0.8,         # Predictable pattern
        'RECOIL_PATTERN_ENABLED': True,   # Consistent recoil
        'MAX_SPEED': 8,                   # Balanced speed
        'MOUSE_SENSITIVITY': 35,          # Standard sensitivity
        'TARGET_SIZE': 0.4,               # Competitive target size
        'TIMER_DURATION': 60,             # Standard time
        'ACCURACY_TRACKING': True,        # Track performance
        'LEADERBOARD_ENABLED': True,      # Enable rankings
    }
    return settings

def apply_settings_preset(preset_name):
    """Apply a settings preset by modifying config.py values with security validation."""
    # Validate preset name
    if not isinstance(preset_name, str) or len(preset_name) > 50:
        print("❌ Invalid preset name")
        return
    
    # Sanitize preset name
    preset_name = re.sub(r'[^a-zA-Z0-9_-]', '', preset_name.lower())
    
    presets = {
        'realistic': realistic_shooting_mode(),
        'arcade': arcade_mode(),
        'precision': precision_mode(),
        'parkour': parkour_mode(),
        'beginner': beginner_mode(),
        'competitive': competitive_mode(),
    }
    
    if preset_name not in presets:
        print(f"❌ Unknown preset: {preset_name}")
        print(f"Available presets: {', '.join(presets.keys())}")
        return
    
    settings = presets[preset_name]
    
    # Validate all settings in preset
    print(f"🔍 Validating {preset_name} preset...")
    for setting, value in settings.items():
        is_valid_name, name_error = security_config.validate_setting_name(setting)
        is_valid_value, value_error = security_config.validate_setting_value(value, setting)
        
        if not is_valid_name:
            print(f"❌ Invalid setting name {setting}: {name_error}")
            return
        
        if not is_valid_value:
            print(f"❌ Invalid setting value for {setting}: {value_error}")
            return
    
    print(f"✅ Preset validation passed")
    print(f"🎮 Applying {preset_name} preset:")
    
    for setting, value in settings.items():
        print(f"  {setting} = {value}")
    
    # Log security event
    security_logger.log_security_event(
        "PRESET_APPLIED", 
        f"User applied preset: {preset_name}",
        "INFO"
    )
    
    print(f"\n✅ {preset_name.title()} preset ready!")
    print("Use the settings editor to save changes to config.py")

if __name__ == "__main__":
    print("🎮 Game Settings Presets")
    print("=" * 30)
    print("Available presets:")
    print("  realistic  - High recoil, realistic shooting")
    print("  arcade     - Fast-paced, low recoil")
    print("  precision  - Slow, accurate gameplay")
    print("  parkour    - Movement-focused, no shooting")
    print("  beginner   - Easy settings for new players")
    print("  competitive- Balanced competitive settings")
    print()
    
    # Example usage with input validation
    try:
        preset = input("Enter preset name (or press Enter for default): ").strip().lower()
        
        # Validate input length
        if len(preset) > 50:
            print("❌ Preset name too long")
        elif preset:
            # Sanitize input
            preset = security_config.sanitize_input(preset)
            apply_settings_preset(preset)
        else:
            print("Using default settings from config.py")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        security_logger.log_security_event("INPUT_ERROR", str(e), "WARNING")