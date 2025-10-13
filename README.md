# 🎮 3D First-Person Parkour Shooter

A 3D first-person parkour shooter built with the Ursina engine, featuring advanced movement mechanics, target shooting, and a comprehensive configuration system with enterprise-level security.

## 🚀 Features

- **Advanced Movement Physics**: Momentum-based movement with sliding, dashing, and input-required wall running
- **Precision Shooting**: Vertical recoil system with state-based multipliers and accuracy tracking
- **Two Game Modes**: Casual play and 60-second timed challenges with scoring
- **3D Environment**: Custom maps with dynamic lighting, shadows, and physics-based interactions
- **Modular Architecture**: Clean separation into core, systems, and UI modules with safe cross-communication
- **Security-Hardened**: Enterprise-level input validation, sanitization, and injection prevention
- **Streamlined Configuration**: 58 essential settings with interactive tools and preset management
- **Robust Error Handling**: Comprehensive error handling with graceful fallbacks across all systems

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
├── 📁 src/                        # Source code modules
│   ├── 📁 core/                   # Core game components
│   │   ├── input_handler.py       # Centralized input processing with security validation
│   │   ├── player.py              # Player controller with advanced movement physics
│   │   ├── utils.py               # Core utility functions and collision detection
│   │   └── weapons.py             # Weapon mechanics, shooting, and recoil system
│   ├── 📁 systems/                # Game systems and mechanics
│   │   ├── map_environment.py     # 3D environment, lighting, and map management
│   │   ├── physics.py             # Advanced movement physics and momentum system
│   │   ├── targets.py             # Target spawning and management system
│   │   └── wall_running.py        # Wall running mechanics with input requirements
│   └── 📁 ui/                     # User interface and game state
│       ├── game_state.py          # Game modes, scoring, and time tracking
│       └── menu.py                # Menu system and navigation
├── 📁 config/                     # Configuration system
│   ├── config.py                  # Main configuration with 55+ essential settings
│   ├── presets/                   # Preset configurations with security validation
│   └── __init__.py                # Configuration module initialization
├── 📁 tools/                      # Development and configuration tools
│   ├── config_tools.py            # Interactive configuration interface
│   ├── config_validator.py        # Configuration validation with security checks
│   ├── settings_editor.py         # Real-time settings editor
│   └── security/                  # Security framework and validation
├── 📁 tests/                      # Comprehensive test suite
│   ├── security_tests.py          # Security validation tests (10/10 passing)
│   └── __init__.py                # Test module initialization
├── 📁 scripts/                    # Launch and utility scripts
│   ├── run_game.py                # Game launcher script
│   ├── run_config_tools.py        # Configuration tools launcher
│   └── run_tests.py               # Test suite runner
├── 📁 assets/                     # Game assets and resources
│   ├── gun3.obj                   # 3D gun model
│   ├── tutorial_map.obj           # Main game map
│   ├── texture_01.png             # Environment texture
│   ├── textures/                  # Texture assets
│   └── sounds/                    # Audio assets
├── 📁 docs/                       # Documentation
│   └── CONFIG_README.md           # Configuration system documentation
├── main.py                        # Main game entry point and initialization
├── requirements.txt               # Python dependencies
└── version.txt                    # Version tracking
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
- **🔊 Audio Settings** (3 settings) - Master volume, SFX volume, gunshot sound path
- **🏃 Player Settings** (9 settings) - Movement speed, gravity, jump height, camera settings
- **🏃‍♂️ Advanced Movement** (10 settings) - Sliding mechanics, dash system, wall running physics
- **🔫 Weapon Systems** (15 settings) - Recoil system, shooting mechanics, gun physics and positioning
- **🎮 Game Modes** (6 settings) - Casual/timed mode configuration, scoring, accuracy tracking
- **🖼️ User Interface** (8 settings) - Menu colors, fonts, UI element positioning
- **⚙️ Collision & Physics** (4 settings) - Collision detection, physics buffers, cooldowns
- **⚡ Debug & Development** (1 setting) - Debug mode toggle

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
The centralized input handler (`src/core/input_handler.py`) provides enterprise-level security:

- **Input Validation**: All key inputs validated for type, length (50 char limit), and format
- **Injection Prevention**: Input sanitization prevents code injection and malicious patterns
- **Safe Module Access**: Uses `getattr()` with null checking for cross-module communication
- **Comprehensive Error Handling**: Graceful fallback for missing modules or attributes
- **Game State Awareness**: Context-sensitive input handling (menu vs gameplay modes)
- **Cooldown Management**: Prevents input spam and abuse through timer validation

### 🎯 Input Processing Flow
1. **Validation**: Input key validated for type, length, and safety
2. **Sanitization**: Key stripped and checked for dangerous patterns
3. **Module Safety**: Game modules safely imported with error handling
4. **Context Checking**: Input processed based on current game state
5. **Action Execution**: Validated actions executed with comprehensive error handling
6. **Cooldown Enforcement**: Timer-based restrictions prevent input abuse

### 🎮 Supported Input Actions
- **Shooting**: Left mouse click with recoil and accuracy tracking
- **Gun Management**: 'R' key for drop/respawn with cooldown protection
- **Menu Navigation**: Enter key for menu transitions with state validation

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

### 🛷 Sliding System
- **Trigger**: Hold Ctrl while sprinting (requires forward momentum)
- **Physics**: Maintains momentum with slope-based acceleration
- **Mechanics**: Friction-based deceleration with gravity influence on slopes
- **Camera**: Dynamic camera lowering with smooth transitions
- **Chaining**: Combine with jumps and dashes for complex movement

### 💨 Dash System
- **Trigger**: Press Q (1-second cooldown)
- **Direction**: Dash in camera look direction with separate horizontal/vertical components
- **Physics**: Horizontal force boosted 1.5x, vertical force reduced for balance
- **Versatility**: Works in air and on ground with different vertical constraints
- **Speed Boost**: Temporary speed multiplier after dashing for momentum chaining

### 🧗 Wall Running System
- **Input Requirements**: Must hold W (forward) + A (left wall) or W + D (right wall)
- **Physics**: Complete gravity override with upward force and wall adhesion
- **Speed Requirements**: Minimum horizontal speed threshold to initiate
- **Camera Effects**: Dynamic camera tilting based on wall side
- **Wall Kicks**: Strong kick-off force when releasing keys or pressing space
- **Time Limit**: Maximum wall run duration with automatic termination

### ⚡ Momentum Physics
- **Acceleration**: Input-based acceleration with friction when no input
- **Collision**: Surface sliding along walls instead of hard stops
- **Air Control**: Reduced air resistance with maintained horizontal momentum
- **Speed Capping**: Dynamic speed limits with dash boost allowances
- **Ground Detection**: Proper grounded/airborne state management

## 📚 Documentation

- **[Configuration Guide](docs/CONFIG_README.md)** - Complete configuration documentation
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Detailed structure guide
- **[Security Report](docs/SECURITY_AUDIT_REPORT.md)** - Security audit and fixes

## 🔫 Weapon System

### 🎯 Shooting Mechanics
- **Recoil System**: Vertical-only recoil patterns with state-based multipliers
- **Recovery**: Smooth recoil recovery with configurable speed and duration
- **State Modifiers**: Different recoil multipliers for standing, crouching, and moving
- **Audio**: Validated gunshot sound with volume control and error handling
- **Accuracy Tracking**: Shot counting and hit percentage calculation

### 🔄 Gun Physics
- **Drop System**: Physics-based gun dropping with gravity and momentum
- **Respawn**: Timed gun respawning with cooldown protection
- **Positioning**: Dynamic gun positioning relative to camera movement
- **Collision**: Gun model collision detection and world interaction

### 🎮 Weapon Controls
- **Shooting**: Left mouse click with recoil feedback
- **Drop/Respawn**: R key with cooldown timer (1-second default)
- **Visual Feedback**: Gun model rotation matching camera pitch
- **Error Handling**: Comprehensive error handling for missing assets

## 🔧 Development

### Recent Architecture Improvements
- **✅ Modular Architecture**: Complete separation into focused modules (`core/`, `systems/`, `ui/`) with proper dependency management
- **✅ Streamlined Configuration**: Reduced from 100+ to 58 essential settings, removing unused legacy options
- **✅ Enhanced Security**: Enterprise-level input validation, sanitization, and injection prevention throughout
- **✅ Advanced Physics**: Momentum-based movement system with collision detection and surface sliding
- **✅ Wall Running System**: Input-required wall running with physics integration and camera effects
- **✅ Weapon System**: Complete recoil system with vertical-only patterns and recovery mechanics
- **✅ Environment Management**: Dedicated 3D environment system with lighting and map management
- **✅ Robust Error Handling**: Comprehensive error handling with graceful fallbacks across all modules
- **✅ Safe Module Communication**: Global reference system with `getattr()` null checking patterns
- **✅ Enhanced Game Initialization**: Proper startup sequence preventing visual artifacts during menu display
- **✅ Centralized Input Processing**: Security-hardened input handler with validation and cooldown management
- **✅ Target Management**: Improved target spawning with bounds checking and error prevention

### 🏗️ Architecture Overview

The game uses a modular architecture with clear separation of concerns:

**Core Modules** (`src/core/`):
- `player.py`: Player controller with advanced movement physics and state management
- `weapons.py`: Weapon system with recoil, shooting mechanics, and gun physics
- `input_handler.py`: Centralized, security-validated input processing
- `utils.py`: Shared utility functions for collision detection and entity management

**System Modules** (`src/systems/`):
- `physics.py`: Momentum-based movement physics with collision handling
- `wall_running.py`: Wall running mechanics with input requirements and camera effects
- `targets.py`: Target spawning and management with bounds checking
- `map_environment.py`: 3D environment, lighting, and map management

**UI Modules** (`src/ui/`):
- `game_state.py`: Game modes, scoring, timing, and state transitions
- `menu.py`: Menu system with navigation and game mode selection

**Global Communication**: Modules communicate through global references with safe `getattr()` patterns and comprehensive error handling.

### Adding New Features
1. **Module Placement**: Create files in appropriate `src/` subdirectory based on functionality
2. **Import Patterns**: Use standardized imports (e.g., `import src.core.player as player`)
3. **Global References**: Set up global instances in `main.py` for cross-module access
4. **Configuration**: Add settings to `config/config.py` with proper categorization
5. **Error Handling**: Implement comprehensive error handling with graceful fallbacks
6. **Security**: Validate all inputs and use safe module access patterns
7. **Testing**: Run security test suite to ensure no vulnerabilities introduced

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
- ✅ **Modular Architecture Complete** - Full restructure into `core/`, `systems/`, and `ui/` modules with proper separation of concerns
- ✅ **Configuration Optimization** - Streamlined to 58 essential settings, removing unused legacy options and performance settings
- ✅ **Advanced Physics Integration** - Momentum-based movement with collision detection, surface sliding, and airborne mechanics
- ✅ **Wall Running System** - Input-required wall running with physics integration, camera tilting, and wall kick mechanics
- ✅ **Enhanced Weapon System** - Complete recoil system with vertical patterns, recovery mechanics, and state-based multipliers
- ✅ **Security Hardening** - Enterprise-level input validation, sanitization, and injection prevention across all systems
- ✅ **Environment Management** - Dedicated 3D environment system with lighting, shadows, and map management
- ✅ **Robust Error Handling** - Comprehensive error handling with graceful fallbacks and safe module access patterns
- ✅ **Centralized Input Processing** - Security-validated input handler with cooldown management and state awareness
- ✅ **Global Reference System** - Safe cross-module communication using `getattr()` with null checking and error prevention

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
- **Dependencies**: Verify Python 3.8+ and install Ursina: `pip install ursina`
- **File Structure**: Ensure all `src/` modules are present in correct directories
- **Assets**: Check that `assets/` folder contains required models and textures
- **Import Errors**: Verify all module imports in `main.py` are successful

### Module Import Issues
- **Missing Modules**: Check that all files in `src/core/`, `src/systems/`, and `src/ui/` exist
- **Path Issues**: Ensure Python path includes project root directory
- **Circular Imports**: Module structure prevents circular imports with global references
- **Error Messages**: Check console for specific import error details

### Performance Issues
- **Graphics Settings**: Use configuration tools to adjust FOV and texture filtering
- **Asset Loading**: Verify 3D models and textures load without errors
- **Physics**: Reduce collision detection frequency if experiencing lag
- **Memory**: Monitor memory usage during extended play sessions

### Configuration Issues
- **Validator**: Run `python tools/config_validator.py` for comprehensive validation
- **Security**: Check for security validation errors in configuration files
- **Presets**: Use validated presets in `config/presets/` to reset settings
- **Missing Constants**: Ensure all required constants are defined in `config/config.py`
- **Type Errors**: Verify configuration values match expected types (int, float, Vec3)

### Input/Control Issues
- **Input Handler**: Check `src/core/input_handler.py` for input processing errors
- **Key Validation**: Ensure input keys are properly validated and sanitized
- **Cooldowns**: Verify cooldown timers are functioning for actions like gun drop
- **State Management**: Check that game state properly enables/disables input processing

## 📊 Performance Specifications

- **Target FPS**: 60 FPS
- **Memory Usage**: ~200MB RAM
- **Storage**: ~150MB (including assets)
- **Graphics**: Supports integrated graphics
- **Platforms**: Windows, Linux, macOS
- **Version**: pre-25m10-3 (Pre-release Development Build)

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