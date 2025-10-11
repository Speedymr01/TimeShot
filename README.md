# TimeShot - 3D Parkour Shooter

A physics-based first-person parkour shooter built with the Ursina engine, featuring advanced movement mechanics and time trial gameplay.

## 🎮 Game Overview

TimeShot combines fluid parkour movement with precision shooting in a 3D environment. Race through courses while hitting all targets to achieve the best completion times.

### Core Features
- **Advanced Movement System**: Sliding, wall running, dashing, and momentum-based physics
- **Time Trial Gameplay**: Race for the best times while maintaining accuracy
- **Parkour Mechanics**: Chain movements for optimal speed and flow
- **Target Shooting**: Precision shooting required to complete courses
- **Physics-Based Gun System**: Realistic weapon handling and mechanics

## 🕹️ Controls

| Key | Action |
|-----|--------|
| **WASD** | Movement |
| **Mouse** | Look around |
| **Space** | Jump |
| **Shift** | Sprint |
| **Ctrl** | Slide (while sprinting) |
| **Q** | Dash |
| **Left Click** | Shoot |
| **R** | Drop/respawn gun |
| **W + A** | Wall run (left wall) |
| **W + D** | Wall run (right wall) |
| **P** | Restart current mode |
| **Escape** | Quit game |

## 🏃‍♂️ Movement Mechanics

### Wall Running
- **Activation**: Hold W + A (left wall) or W + D (right wall)
- **Speed**: Consistent 18 units/sec horizontally regardless of look direction
- **Exit**: Release keys or press Space for wall kick
- **Duration**: Maximum 8 seconds per wall run
- **Physics**: Reduced gravity with strong wall adhesion

### Sliding
- **Activation**: Hold Ctrl while sprinting
- **Physics**: Momentum-based with slope acceleration
- **Speed**: Initial velocity of 40 units/sec with friction decay
- **Camera**: Lowered perspective during slide

### Dashing
- **Activation**: Press Q (1-second cooldown)
- **Effect**: Applies force in look direction
- **Speed Boost**: Temporary 3x speed multiplier for 0.5 seconds
- **3D Movement**: Works in all directions including vertical

## 🎯 Game Modes

### Casual Play
- Free exploration and target practice
- No time pressure
- Targets respawn automatically
- Focus on movement and shooting mechanics

### Timed Mode
- 60-second time limit
- Score tracking and accuracy measurement
- All targets must be hit to complete
- Leaderboard potential for best times

## 🏗️ Technical Architecture

### Modular Design
The game is built with a clean, modular architecture:

```
├── main.py              # Application entry point
├── config.py            # Game constants and settings
├── player.py            # Player controller and movement
├── weapons.py           # Gun mechanics and shooting
├── wall_running.py      # Advanced wall running system
├── physics.py           # Movement physics and collision
├── targets.py           # Target management
├── game_state.py        # Game modes and UI
├── menu.py              # Main menu system
├── map_environment.py   # 3D environment and lighting
├── input_handler.py     # Centralized input processing
└── utils.py             # Common utility functions
```

### Key Technologies
- **Engine**: Ursina (Python 3D game engine)
- **Physics**: Custom momentum-based movement system
- **Graphics**: OpenGL via Ursina with shader support
- **Assets**: 3D models (.obj), textures (.png), materials (.mtl)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Ursina engine

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install ursina
   ```
3. Run the game:
   ```bash
   python main.py
   ```

### Asset Requirements
Ensure the following assets are in the `assets/` directory:
- `tutorial_map.obj` - Main game map
- `texture_01.png` - Map texture
- `gun3.obj` - Gun model
- `textures/gun3_texture.png` - Gun texture

## 🎨 Game Vision

TimeShot is designed as a **parkour time trial shooter** where players:
- Race through carefully designed courses
- Must hit all targets along the route to finish
- Optimize movement chains for the fastest completion times
- Balance speed with shooting accuracy
- Master advanced movement techniques for competitive times

The game emphasizes **flow state** through fluid movement mechanics and **precision** through required target accuracy.

## 🔧 Development

### Code Style
- **Modular Architecture**: Each system in its own file
- **Clear Separation**: UI, physics, input, and game logic separated
- **Consistent Naming**: Snake_case for functions, UPPER_CASE for constants
- **Comprehensive Comments**: All major functions documented

### Physics System
- **Momentum-Based Movement**: Realistic acceleration and friction
- **Advanced Collision**: Raycast-based with surface sliding
- **Wall Running Physics**: Custom gravity and adhesion system
- **Dash Mechanics**: Force-based with speed multipliers

### Performance Considerations
- **Efficient Collision Detection**: Optimized raycast usage
- **Modular Updates**: Systems update only when needed
- **Asset Management**: Safe loading with fallback handling

## 📝 Recent Updates

- ✅ Modular architecture implementation
- ✅ Advanced wall running with key-based controls
- ✅ Consistent horizontal speed during wall running
- ✅ Wall kick on key release
- ✅ Restart functionality (P key)
- ✅ Improved collision detection and physics
- ✅ Enhanced movement chaining capabilities

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome!

## 📄 License

This project is for educational and personal use.

---

**Built with ❤️ using Python and Ursina**