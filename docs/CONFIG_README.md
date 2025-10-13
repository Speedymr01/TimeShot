# 🎮 Game Configuration System

A streamlined, interactive configuration system for the parkour shooter game with essential settings for optimal gameplay.

## 🚀 Quick Start

### Option 1: Interactive Settings Editor (Recommended)
```bash
python settings_editor.py
```
- **Colored CLI interface** with easy navigation
- **Real-time editing** of all game settings
- **Built-in validation** and error checking
- **Preset configurations** for different gameplay styles
- **Auto-save** functionality with backup

### Option 1b: Secure Settings Editor (For Enhanced Security)
```bash
python settings_editor_secure.py
```
- **Security-hardened** configuration editing
- **Input validation** to prevent code injection
- **Safe parsing** using AST literal evaluation
- **Path traversal protection** and file size limits
- **Atomic file operations** with automatic backups

### Option 2: Configuration Tools Launcher
```bash
python config_tools.py
```
- **Unified interface** for all configuration tools
- **Quick access** to editor, validator, and presets
- **Help system** with usage tips
- **Configuration summary** display

### Option 3: Direct File Editing
Edit `config.py` directly with any text editor, then validate:
```bash
python config_validator.py
```

## 📂 Configuration Categories

### 🖥️ Display & Graphics (2 settings)
- Field of view (FOV_DEFAULT)
- Texture filtering quality

### 🔊 Audio Settings (3 settings)
- Master volume and SFX volume controls
- Gunshot sound file path

### 🏃 Player Settings (9 settings)
- Movement physics and controls
- Camera settings and player dimensions
- Gravity, jump height, and speed settings

### 🏃‍♂️ Advanced Movement (10 settings)
- **Sliding System**: Speed, friction, cooldowns, camera positioning
- **Dash System**: Force and cooldowns
- **Wall Running**: Speed, detection, jump force, camera tilt

### 🔫 Weapon Systems (15 settings)
- **Gun Models**: Paths, scaling, positioning
- **Shooting Mechanics**: Bullet range and shooting toggle
- **Recoil System**: Vertical/horizontal kick, recovery speed
- **Gun Physics**: Gravity, respawn timing

### 🎮 Game Modes (6 settings)
- Casual and timed mode configuration
- Timer duration and scoring system
- Accuracy tracking toggle

### 🖼️ User Interface (8 settings)
- Menu styling and colors
- UI positioning for timer, score, accuracy

### ⚡ Debug & Development (2 settings)
- Debug mode toggle
- Collision detection offset

## 🎯 Popular Settings to Adjust

### Movement Feel
```python
MAX_SPEED = 12              # Faster movement
SPRINT_MULTIPLIER = 2.5     # Faster sprinting
DASH_FORCE = 80            # Stronger dash
SLIDE_START_VELOCITY = 60   # Faster slides
```

### Shooting Experience
```python
RECOIL_VERTICAL = 4.0       # Higher recoil
RECOIL_HORIZONTAL = 2.0     # More sway
RECOIL_RECOVERY_SPEED = 4.0 # Slower recovery
MOUSE_SENSITIVITY = 30      # Lower sensitivity
```

### Visual Experience
```python
FOV_DEFAULT = 100           # Wider field of view
FOV_SPRINT = 110           # Even wider when sprinting
WINDOW_FULLSCREEN = True    # Fullscreen mode
ANTI_ALIASING = True       # Smoother graphics
```

### Audio Experience
```python
MASTER_VOLUME = 0.8        # 80% volume
SFX_VOLUME = 1.0          # Full sound effects
SPATIAL_AUDIO = True       # 3D positional audio
```

## 🎮 Preset Configurations

### 1. Realistic Shooting Mode
- High recoil and slower movement
- Immersive audio settings
- Precision-focused gameplay

### 2. Arcade Mode
- Fast-paced, low recoil
- High speed movement
- Wide FOV for speed sensation

### 3. Precision Challenge
- Accuracy-focused settings
- Smaller targets, longer time
- Controlled movement

### 4. Parkour Mode
- Movement-only gameplay
- Enhanced parkour mechanics
- No shooting distractions

### 5. Beginner Friendly
- Easy settings for new players
- Low recoil, larger targets
- Simplified mechanics

### 6. Competitive Mode
- Balanced settings for competition
- Consistent recoil patterns
- Standard timing and scoring

## 🔧 Configuration Tools

### Interactive Settings Editor (`settings_editor.py`)
- **Colored CLI interface** with intuitive navigation
- **Category-based organization** of settings
- **Real-time validation** and error checking
- **Preset application** with one-click setup
- **Auto-save functionality** with change tracking

### Secure Settings Editor (`settings_editor_secure.py`)
- **Security-hardened configuration editing** with comprehensive input validation
- **Safe parsing system** using AST literal evaluation to prevent code injection
- **Path traversal protection** ensuring files stay within project directory
- **Input sanitization** with length limits and content filtering
- **Atomic file operations** with automatic backup creation
- **Type safety enforcement** with strict validation of setting values

### Configuration Validator (`config_validator.py`)
- **Comprehensive validation** of all settings
- **Configuration summary** display
- **Error detection** and warnings
- **File path verification**

### Settings Examples (`settings_examples.py`)
- **6 preset configurations** for different gameplay styles
- **Easy preset application**
- **Configuration comparison** tools

### Configuration Launcher (`config_tools.py`)
- **Unified interface** for all tools
- **Quick access** to any configuration utility
- **Help system** and usage tips
- **Configuration summary** at a glance

## 🚨 Troubleshooting

### Game Won't Start
1. Run `python config_validator.py` to check for errors
2. Look for invalid values (negative numbers, out-of-range values)
3. Check file paths for missing assets

### Performance Issues
1. Try the "Low Quality" preset
2. Reduce `RENDER_DISTANCE` and `MAX_PARTICLES`
3. Disable `ANTI_ALIASING` and `MOTION_BLUR`

### Controls Feel Wrong
1. Adjust `MOUSE_SENSITIVITY` (25-50 recommended)
2. Modify `FOV_DEFAULT` (80-100 for most players)
3. Check `RECOIL_VERTICAL` and `RECOIL_HORIZONTAL`

### Audio Issues
1. Verify `MASTER_VOLUME` and `SFX_VOLUME` are between 0.0-1.0
2. Check sound file paths exist
3. Ensure `SPATIAL_AUDIO` is compatible with your system

## 💡 Tips for Best Experience

1. **Start with presets** - Use preset configurations as starting points
2. **Make small changes** - Adjust one setting at a time to see effects
3. **Validate frequently** - Run validator after making changes
4. **Backup your config** - Save working configurations before experimenting
5. **Test in-game** - Always test changes by playing the game
6. **Use the interactive editor** - Much easier than manual file editing

## 📁 File Structure

```
├── config.py                  # Main configuration file (essential settings)
├── settings_editor.py         # Interactive CLI editor with colors
├── settings_editor_secure.py  # Security-hardened configuration editor
├── config_validator.py        # Settings validation and summary
├── settings_examples.py       # Preset configurations
├── config_tools.py           # Unified launcher for all tools
└── CONFIG_README.md           # This documentation
```

## 🎯 Advanced Usage

### Creating Custom Presets
1. Configure settings using the interactive editor
2. Save your configuration
3. Copy the relevant settings to create a new preset
4. Add your preset to `settings_examples.py`

### Batch Configuration Changes
1. Edit multiple settings in the interactive editor
2. Use the validation tool to check for conflicts
3. Apply and test changes incrementally

### Performance Optimization
1. Use the performance category settings
2. Adjust quality presets based on your hardware
3. Monitor frame rate and adjust accordingly

---

**🎮 Happy Gaming! Customize your perfect parkour shooter experience!**