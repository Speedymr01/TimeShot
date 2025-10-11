# Technology Stack

## Framework & Engine
- **Ursina Engine**: Python-based 3D game engine for rapid prototyping
- **Python 3**: Core programming language

## Key Dependencies
- `ursina`: Main game engine
- `ursina.prefabs.first_person_controller`: Built-in FPS controller
- `ursina.shaders.lit_with_shadows_shader`: Lighting and shadow system
- Standard Python libraries: `math`, `random`

## Asset Pipeline
- **3D Models**: `.obj` format for meshes
- **Textures**: `.png` format for materials and UI
- **Materials**: `.mtl` files for model materials
- **Blender**: `.blend` files for 3D asset creation

## Common Commands
Since this is a single-file Python game, common operations include:

```bash
# Run the game
python ursinagame.py

# Install dependencies (if needed)
pip install ursina
```

## Architecture Notes
- Modular architecture with focused responsibilities
- Entity-component system via Ursina
- Event-driven input handling
- Advanced physics integration (momentum, wall running, parkour mechanics)
- Asset loading from relative paths in `./assets/`
- Cross-module communication via global instances
- Time-based progression system for parkour courses