# 🎮 3D First-Person Parkour Shooter

A 3D first-person parkour shooter built with the Ursina engine, featuring advanced movement mechanics, target shooting, and a comprehensive configuration system with enterprise-level security.

## 🚀 Features

- **Advanced Movement**: Sliding, dashing, wall running, momentum-based physics
- **Target Shooting**: Precision shooting with recoil and accuracy tracking
- **Two Game Modes**: Casual play and timed challenges
- **3D Environment**: Custom maps with dynamic lighting and physics
- **Streamlined Configuration**: 55 essential settings (reduced from 100+) with interactive tools
- **Modular Architecture**: Clean separation into core, systems, and UI modules
- **Security-Hardened**: Enterprise-level security for all configuration tools

## 🎯 Quick Start

### Option 1: Direct Launch
```bash
python main.py
```

### Option 2: Using Launch Scripts
```bash
# Launch the game
python scripts/run_game.py

# Configuration tools
python scripts/run_config_tools.py

# Run tests
python scripts/run_tests.py
```

## 🏗️ Project Structure

```
3D-Parkour-Shooter/                # Project root
├── 📁 src/                        # Source code
│   ├── 📁 core/                   # Core components (player, weapons, input, utils)
│   │   ├── input_handler.py       # Centralized input processing
│   │   ├── player.py              # Player controller and movement
│   │   ├── utils.py               # Core utility functions
│   │   └── weapons.py             # Weapon mechanics and shooting
│   ├── 📁 systems/                # Game systems (physics, targets, environment)
│   │   ├── map_environment.py     # 3D environment and map management
│   │   ├── physics.py             # Advanced movement physics
│   │   ├── targets.py             # Target management system
│   │   └── wall_running.py        # Wall running mechanics
│   └── 📁 ui/                     # User interface (menus, game state)
│       ├── game_state.py          # Game state and time tracking
│       └── menu.py                # Menu system
├── 📁 config/                     # Configuration files and presets
├── 📁 tools/                      # Development and configuration tools
├── 📁 tests/                      # Test suite (security, functionality)
├── 📁 docs/                       # Documentation
├── 📁 scripts/                    # Launch scripts
├── 📁 assets/                     # Game assets (models, sounds, textures)
└── main.py                        # Main game entry point
```

## 🎮 Controls

| Action | Key | Description |
|--------|-----|-------------|
| **Movement** | WASD | Basic movement |
| **Look** | Mouse | Camera control |
| **Jump** | Space | Jump/parkour |
| **Sprint** | Shift | Faster movement |
| **Slide** | Ctrl | Slide while sprinting |
| **Dash** | Q | Dash in look direction |
| **Shoot** | Left Click | Fire weapon |
| **Drop Gun** | R | Drop and respawn weapon |
| **Wall Run** | W + A/D | Run on walls |
| **Quit** | Escape | Exit game |

## ⚙️ Configuration System

### 🔧 Interactive Configuration Tools

```bash
# Launch unified configuration interface
python scripts/run_config_tools.py
```

**Available Tools:**
1. **Interactive Settings Editor** - Real-time configuration with validation
2. **Configuration Validator** - Verify settings and show summaries  
3. **Settings Examples & Presets** - Apply preset configurations
4. **Game Launcher** - Start game with current settings

### 📁 Configuration Structure

The configuration system uses a modular directory structure with enhanced security:
- **`config/config.py`** - Main configuration file with essential game settings
- **`config/presets/`** - Preset configurations with security validation
- **`tools/config_validator.py`** - Validates configuration files with comprehensive security checks
- **`tools/security/`** - Security framework with validation, logging, and rate limiting
- **`tools/settings_editor_secure.py`** - Security-hardened interactive settings editor

### 📊 Configuration Categories (Essential Settings)

- **🖥️ Display & Graphics** (2 settings) - FOV, texture filtering
- **🔊 Audio Settings** (3 settings) - Volume controls, sound paths
- **🏃 Player Settings** (9 settings) - Movement, camera, physics
- **🏃‍♂️ Advanced Movement** (10 settings) - Sliding, dashing, wall running
- **🔫 Weapon Systems** (15 settings) - Recoil (vertical-only), shooting, gun physics
- **🎮 Game Modes** (6 settings) - Casual/timed configuration, accuracy tracking
- **🖼️ User Interface** (8 settings) - Menu styling, UI positioning
- **⚡ Debug & Development** (2 settings) - Debug mode, collision detection

### 🎯 Popular Configuration Presets

All presets include automatic security validation and safe application:

- **Realistic Mode** - High vertical recoil (4.0x), immersive settings, slower recovery
- **Arcade Mode** - Fast-paced movement, low vertical recoil (1.0x), enhanced mechanics
- **Precision Challenge** - Accuracy-focused, controlled movement, vertical-only recoil
- **Parkour Mode** - Movement-focused, enhanced sliding/wall-running mechanics
- **Beginner Friendly** - Easy settings, reduced recoil, simplified mechanics
- **Competitive Mode** - Balanced settings, consistent vertical recoil patterns, performance tracking

**Security Features:**
- Input validation and sanitization for all preset names
- Setting value validation against security rules
- Automatic logging of preset applications
- Graceful fallback when security modules unavailable

## 🎮 Input System

### 🔒 Secure Input Handler
The centralized input handler (`src/core/input_handler.py`) provides:

- **Input Validation**: All key inputs are validated and sanitized before processing
- **Length Limiting**: Input keys are limited to reasonable lengths (50 characters) to prevent abuse
- **Injection Prevention**: Input sanitization prevents code injection attacks
- **Safe Module Access**: Uses `getattr()` with null checking for cross-module communication
- **Comprehensive Error Handling**: Graceful fallback for missing modules or attributes
- **Game State Awareness**: Context-sensitive input handling based on current game state

### 🎯 Input Processing Flow
1. **Validation**: Input key is validated for type and length
2. **Sanitization**: Key is stripped and checked for dangerous patterns
3. **Module Safety**: All required game modules are safely imported and validated
4. **Context Checking**: Input is processed based on current game state (menu vs gameplay)
5. **Action Execution**: Validated actions are executed with comprehensive error handling

## 🛡️ Security Features

The project includes enterprise-level security with comprehensive validation:

- ✅ **No Code Injection** - Safe configuration parsing with eval protection and dangerous pattern detection
- ✅ **Path Validation** - Prevents directory traversal attacks with strict path resolution
- ✅ **Input Sanitization** - All inputs validated, sanitized, and length-limited with comprehensive key validation in centralized input handler
- ✅ **Rate Limiting** - Prevents abuse and DoS attacks with configurable thresholds
- ✅ **Security Logging** - Comprehensive security event tracking with timestamps
- ✅ **Secure File Access** - Configuration files validated within project boundaries
- ✅ **Fallback Protection** - Graceful degradation when security modules unavailable
- ✅ **Type Validation** - Strict type checking for all configuration values
- ✅ **Range Validation** - Numeric values validated against reasonable ranges
- ✅ **Pattern Blocking** - Dangerous code patterns automatically detected and blocked
- ✅ **Robust Error Handling** - Safe module imports with proper exception handling
- ✅ **Comprehensive Tests** - 10/10 security tests passing with integration coverage

## 🧪 Testing

```bash
# Run complete security test suite
python scripts/run_tests.py

# Or run directly
python tests/security_tests.py
```

## 🛠️ Installation & Requirements

### Prerequisites
- **Python 3.8+**
- **Ursina Engine**: `pip install ursina`

### Installation
1. Clone/download this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the game: `python main.py`

## 🎯 Game Modes

### 🎮 Casual Play
- Unlimited time for practice
- Respawning targets
- Perfect for learning movement mechanics

### ⏱️ Timed Mode  
- 60-second challenges
- Score tracking and accuracy statistics
- Competitive leaderboard system

## 🏃‍♂️ Advanced Movement Mechanics

### 🛷 Sliding
- **Trigger**: Hold Ctrl while sprinting
- **Physics**: Maintains momentum, gains speed on slopes
- **Chaining**: Combine with jumps and dashes

### 💨 Dashing
- **Trigger**: Press Q
- **Direction**: Dash in camera look direction
- **Versatility**: Works in air and on ground

### 🧗 Wall Running
- **Trigger**: Hold W + A/D against walls
- **Physics**: Defies gravity on vertical surfaces
- **Momentum**: Jump off walls to maintain speed

## 📚 Documentation

- **[Configuration Guide](docs/CONFIG_README.md)** - Complete configuration documentation
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Detailed structure guide
- **[Security Report](docs/SECURITY_AUDIT_REPORT.md)** - Security audit and fixes

## 🔧 Development

### Recent Architecture Improvements
- **✅ Streamlined Configuration**: Reduced configuration complexity from 100+ settings to 55 essential settings, removing unused performance optimization, advanced debug options, and legacy settings
- **✅ Modular Architecture**: Complete separation into `core/`, `systems/`, and `ui/` modules with proper dependency management
- **✅ Enhanced Game Systems**: Added `map_environment.py` for 3D environment management and `utils.py` for core utilities
- **✅ Standardized Import Paths**: All modules use consistent, full import paths for better code organization
- **✅ Enhanced Module Structure**: Cross-module communication follows established patterns with proper namespace resolution
- **✅ Improved Maintainability**: Cleaner import structure makes the codebase easier to navigate and extend
- **✅ Enhanced Game Initialization**: Proper startup sequence with game elements disabled during menu display for cleaner user experience
- **✅ Robust Error Handling**: All cross-module imports include comprehensive error handling with graceful fallbacks
- **✅ Consistent Attribute Checking**: Safe module access patterns using `hasattr()` and `getattr()` checks prevent runtime errors
- **✅ Enhanced Input Handler Security**: Centralized input processing with comprehensive validation, sanitization, and error prevention
- **✅ Global Reference System**: Improved cross-module communication using global references with proper null checking

### Adding New Features
1. Create files in appropriate `src/` subdirectory:
   - `core/` - Player mechanics, weapons, input handling, utilities
   - `systems/` - Physics, targets, environment, advanced mechanics
   - `ui/` - Menus, game state, user interface elements
2. Use proper module imports (e.g., `import src.core.player as player`)
3. Update imports in `main.py` and relevant modules
4. Add configuration options to `config/config.py` (keep essential settings only)
5. Follow proper initialization sequence (disable game elements before menu creation)
6. Use global reference patterns with `getattr()` for safe cross-module access
7. Test with security suite

**Import Best Practices:**
- Always use full module paths for cross-module imports (e.g., `import src.core.module as module`)
- Use `getattr()` with default `None` for safe attribute access across modules
- Implement comprehensive error handling for all cross-module communications
- Follow the established `src/core/`, `src/systems/`, `src/ui/` structure
- Validate all inputs and sanitize user data before processing
- Use null checking patterns: `if not all([obj1, obj2, obj3]): return`

### Module Import Guidelines
- **Core modules**: `import src.core.module_name as module`
- **System modules**: `import src.systems.module_name as module`
- **UI modules**: `import src.ui.module_name as module`
- **Config**: `from config import SETTING_NAME`
- **Safe Access**: `obj = getattr(module, 'instance_name', None)`
- **Validation**: `if not all([obj1, obj2]): return`

**Recent Updates:**
- ✅ **Configuration Streamlining Complete** - Reduced from 100+ to 55 essential settings, removing unused performance optimization, advanced debug options, and legacy settings from config.py
- ✅ **Modular Architecture Enhancement** - Complete restructure into focused modules: `core/` (player, weapons, input, utils), `systems/` (physics, targets, environment), `ui/` (menus, game state)
- ✅ **Import Path Standardization Complete** - All cross-module imports now use proper module paths (e.g., `import src.ui.menu as menu`)
- ✅ **Enhanced Module Structure** - Consistent import patterns across all game systems for better maintainability
- ✅ **Environment System Addition** - New `map_environment.py` module for comprehensive 3D environment and map management
- ✅ **Core Utilities Integration** - Added `utils.py` for shared utility functions across the game systems
- ✅ **Improved Startup Sequence** - Game elements are now properly disabled during initialization to prevent visual artifacts and ensure clean menu presentation
- ✅ **Robust Cross-Module Communication** - All modules now use standardized import patterns with proper error handling and attribute checking
- ✅ **Enhanced Input Handler** - Centralized input processing with comprehensive security validation, sanitization, and graceful error handling
- ✅ **Global Reference Architecture** - Improved module communication using `getattr()` with null checking for safer cross-module access

### Custom Configuration
1. Use security-hardened settings editor: `python tools/settings_editor_secure.py`
2. Validate changes with security checks: `python tools/config_validator.py`
3. Apply validated presets: `python config/presets/settings_examples.py`

**Security Enhancements:**
- All configuration tools now include comprehensive input validation
- Automatic path traversal attack prevention
- Dangerous code pattern detection and blocking
- Rate limiting to prevent configuration abuse
- Security event logging with timestamps
- Graceful fallback when security modules are unavailable
- Type and range validation for all setting values

## 🐛 Troubleshooting

### Game Won't Start
- Verify Python 3.8+ installed
- Install Ursina: `pip install ursina`
- Check all files present in correct directories

### Performance Issues
- Use configuration tools to lower graphics settings
- Try "Low Quality" preset in settings examples
- Reduce `RENDER_DISTANCE` and `MAX_PARTICLES`

### Configuration Issues
- Run security-enhanced validator: `python tools/config_validator.py`
- Validator automatically locates config files with path validation
- Check `security.log` for detailed security event logs
- Reset to defaults using validated presets in `config/presets/`
- Use fallback mode if security modules are unavailable
- All configuration changes are logged for audit trails

## 📊 Performance Specifications

- **Target FPS**: 60 FPS
- **Memory Usage**: ~200MB RAM
- **Storage**: ~150MB (including assets)
- **Graphics**: Supports integrated graphics
- **Platforms**: Windows, Linux, macOS
- **Version**: pre-25m10-1 (Streamlined Configuration Release)

## 🤝 Contributing

1. Fork the repository
2. Follow the established project structure
3. Run security tests before submitting
4. Update documentation for new features
5. Submit pull request with detailed description

## 📄 License

Open source project. Feel free to modify and distribute according to license terms.

## 🙏 Credits

- **Engine**: [Ursina](https://www.ursinaengine.org/) - Python 3D game engine
- **Developer**: Matthew Richardson
- **Security Framework**: Custom enterprise-level security implementation
- **Assets**: Open-source 3D models, textures, and audio files

---

**🎮 Ready to master the ultimate parkour shooter experience!**

*For detailed configuration options, see [Configuration Guide](docs/CONFIG_README.md)*