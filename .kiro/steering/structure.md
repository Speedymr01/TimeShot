# Project Structure

## Root Directory
- `ursinagame.py`: Main game file containing all game logic, physics, and rendering code

## Asset Organization
```
assets/
├── *.obj              # 3D model files (maps, guns, objects)
├── *.mtl              # Material definition files
├── *.png              # Texture files
├── *.blend            # Blender source files
└── textures/          # Organized texture assets
    ├── gun3_texture.png
    └── texture_scigun.png
```

## Development Assets
```
potential_objs/        # Asset candidates and source files
├── *.zip             # Downloaded asset packs
├── *.blend           # Work-in-progress models
└── *                 # Misc asset files
```

## Code Organization Patterns

### Modular Architecture
The game is split into focused modules:
- `config.py`: All game constants and settings
- `player.py`: Player controller and movement state
- `weapons.py`: Gun mechanics and shooting system
- `physics.py`: Advanced movement physics
- `wall_running.py`: Wall running system
- `targets.py`: Target management (static placement for courses)
- `game_state.py`: Time tracking and course completion
- `main.py`: Application entry point and main loop

### Settings Organization
All game constants are centralized in `config.py`:
- Movement physics parameters
- Parkour mechanics (sliding, wall running, dashing)
- Course and target configurations
- Asset paths and references

### Entity Management
- Entities created with descriptive names and organized by function
- Asset paths use relative references: `'./assets/filename.ext'`
- Colliders and shaders applied consistently across similar objects
- Static target placement for parkour courses

### Game State Management
- Time-based progression tracking
- Course completion validation (all targets hit)
- Best time recording and comparison
- Modular system communication

## Naming Conventions
- Snake_case for variables and functions
- UPPER_CASE for constants
- Descriptive entity names for debugging
- Asset files use lowercase with underscores
- Module names reflect their primary responsibility