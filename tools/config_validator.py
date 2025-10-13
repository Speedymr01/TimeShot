#!/usr/bin/env python3
"""
Configuration Validator
=======================

Validates and provides information about game configuration settings.
SECURITY: Added safe imports and file validation.
"""

import os
import sys
from pathlib import Path

# Safely import config with validation
def safe_import_config():
    """Safely import config module with path validation."""
    try:
        current_dir = Path.cwd()
        config_dir = current_dir / 'config'
        config_path = config_dir / 'config.py'
        
        if not config_path.exists():
            raise ImportError("Config file not found")
        
        # Validate it's in project directory
        if not str(config_path.resolve()).startswith(str(current_dir)):
            raise ImportError("Invalid config file location")
        
        sys.path.insert(0, str(config_dir))
        import config
        return config
    except Exception as e:
        print(f"❌ Error importing config: {e}")
        sys.exit(1)

# Import config safely
config = safe_import_config()

def validate_config():
    """Validate configuration settings and report any issues."""
    issues = []
    warnings = []
    
    # Validate numeric ranges
    if not (0.0 <= config.MASTER_VOLUME <= 1.0):
        issues.append("MASTER_VOLUME must be between 0.0 and 1.0")
    
    if not (0.0 <= config.SFX_VOLUME <= 1.0):
        issues.append("SFX_VOLUME must be between 0.0 and 1.0")
    
    if config.FOV_DEFAULT < 60 or config.FOV_DEFAULT > 120:
        warnings.append("FOV_DEFAULT outside recommended range (60-120)")
    
    if config.RECOIL_VERTICAL < 0:
        issues.append("RECOIL_VERTICAL cannot be negative")
    
    if config.PLAYER_GRAVITY < 0:
        issues.append("PLAYER_GRAVITY cannot be negative")
    
    if config.MAX_SPEED <= 0:
        issues.append("MAX_SPEED must be positive")
    
    # Validate file paths exist (with security checks)
    def safe_check_file(file_path: str, file_type: str):
        """Safely check if file exists with path validation."""
        try:
            path = Path(file_path).resolve()
            current_dir = Path.cwd()
            
            # Prevent path traversal
            if not str(path).startswith(str(current_dir)):
                warnings.append(f"{file_type} file path outside project directory: {file_path}")
                return
            
            if not path.exists():
                warnings.append(f"{file_type} file not found: {file_path}")
        except Exception as e:
            warnings.append(f"Error checking {file_type} file {file_path}: {e}")
    
    # Check sound files
    if hasattr(config, 'GUNSHOT_SOUND'):
        safe_check_file(config.GUNSHOT_SOUND, "Sound")
    
    # Check model files  
    if hasattr(config, 'GUN_MODEL_PATH'):
        safe_check_file(config.GUN_MODEL_PATH, "Model")
    
    # Report results
    if issues:
        print("❌ Configuration Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    
    if warnings:
        print("⚠️  Configuration Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not issues and not warnings:
        print("✅ Configuration validation passed!")
    
    return len(issues) == 0

def print_config_summary():
    """Print a summary of key configuration settings."""
    print("🎮 Game Configuration Summary")
    print("=" * 40)
    
    # Safe attribute access with defaults
    def safe_get(attr_name, default="Unknown"):
        return getattr(config, attr_name, default)
    
    print(f"Display:")
    print(f"  Resolution: {safe_get('WINDOW_WIDTH', 1920)}x{safe_get('WINDOW_HEIGHT', 1080)}")
    print(f"  FOV: {safe_get('FOV_DEFAULT', 90)}°")
    print(f"  Fullscreen: {safe_get('WINDOW_FULLSCREEN', False)}")
    
    print(f"\nAudio:")
    master_vol = safe_get('MASTER_VOLUME', 1.0)
    sfx_vol = safe_get('SFX_VOLUME', 0.8)
    print(f"  Master Volume: {master_vol * 100:.0f}%")
    print(f"  SFX Volume: {sfx_vol * 100:.0f}%")
    
    print(f"\nPlayer:")
    print(f"  Max Speed: {safe_get('MAX_SPEED', 7)}")
    print(f"  Jump Height: {safe_get('PLAYER_JUMP_HEIGHT', 2)}")
    print(f"  Sprint Multiplier: {safe_get('SPRINT_MULTIPLIER', 1.8)}x")
    
    print(f"\nWeapons:")
    print(f"  Recoil Enabled: {safe_get('RECOIL_ENABLED', True)}")
    print(f"  Vertical Recoil: {safe_get('RECOIL_VERTICAL', 2.5)}")
    print(f"  Horizontal Recoil: {safe_get('RECOIL_HORIZONTAL', 1.0)}")
    
    print(f"\nGame Modes:")
    casual_enabled = safe_get('CASUAL_MODE_ENABLED', True)
    timed_enabled = safe_get('TIMED_MODE_ENABLED', True)
    print(f"  Casual Mode: {'Enabled' if casual_enabled else 'Disabled'}")
    print(f"  Timed Mode: {'Enabled' if timed_enabled else 'Disabled'}")
    print(f"  Timer Duration: {safe_get('TIMER_DURATION', 60)}s")
    
    print(f"\nAdvanced Movement:")
    slide_enabled = safe_get('SLIDE_ENABLED', True)
    dash_enabled = safe_get('DASH_ENABLED', True)
    wall_run_enabled = safe_get('WALL_RUN_ENABLED', True)
    print(f"  Sliding: {'Enabled' if slide_enabled else 'Disabled'}")
    print(f"  Dashing: {'Enabled' if dash_enabled else 'Disabled'}")
    print(f"  Wall Running: {'Enabled' if wall_run_enabled else 'Disabled'}")
    
    print(f"\nDebug:")
    debug_mode = safe_get('DEBUG_MODE', False)
    show_collision = safe_get('SHOW_COLLISION_BOXES', False)
    print(f"  Debug Mode: {'Enabled' if debug_mode else 'Disabled'}")
    print(f"  Show Collision Boxes: {'Yes' if show_collision else 'No'}")

def get_quality_preset_settings(preset):
    """Get recommended settings for different quality presets."""
    presets = {
        'low': {
            'SHADOW_QUALITY': 'low',
            'ANTI_ALIASING': False,
            'MOTION_BLUR': False,
            'PARTICLE_EFFECTS': False,
            'RENDER_DISTANCE': 500,
            'MAX_PARTICLES': 100
        },
        'medium': {
            'SHADOW_QUALITY': 'medium',
            'ANTI_ALIASING': True,
            'MOTION_BLUR': True,
            'PARTICLE_EFFECTS': True,
            'RENDER_DISTANCE': 750,
            'MAX_PARTICLES': 500
        },
        'high': {
            'SHADOW_QUALITY': 'high',
            'ANTI_ALIASING': True,
            'MOTION_BLUR': True,
            'PARTICLE_EFFECTS': True,
            'RENDER_DISTANCE': 1000,
            'MAX_PARTICLES': 1000
        },
        'ultra': {
            'SHADOW_QUALITY': 'high',
            'ANTI_ALIASING': True,
            'MOTION_BLUR': True,
            'PARTICLE_EFFECTS': True,
            'RENDER_DISTANCE': 1500,
            'MAX_PARTICLES': 2000
        }
    }
    
    return presets.get(preset, presets['medium'])

if __name__ == "__main__":
    print_config_summary()
    print()
    validate_config()