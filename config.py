"""
Game Configuration Constants
============================

All game settings and constants organized by category.
"""

from ursina import *

# ===============================================
# === GAME CONFIGURATION =======================
# ===============================================

# === Environment Settings ===
MAP_SIZE = 100                    # Size of the game world
GROUND_TEXTURE = 'grass'          # Default ground texture
SKY_TYPE = 'default'              # Sky environment type

# === Player Movement Physics ===
PLAYER_GRAVITY = 0.5              # Gravity multiplier for player
PLAYER_JUMP_HEIGHT = 2            # Maximum jump height in units
PLAYER_SPEED = 5                  # Base movement speed (legacy, now uses momentum system)
SPRINT_MULTIPLIER = 1.8           # Speed multiplier when sprinting
PLAYER_START_POS = (15, 11, 0)    # Starting position in world coordinates

# === Advanced Movement Mechanics ===
# Sliding System
SLIDE_FRICTION = 6                # How quickly slide velocity decreases
SLIDE_START_VELOCITY = 40         # Initial velocity when starting slide
SLIDE_COOLDOWN = 2.0              # Seconds before can slide again
SLIDE_CAMERA_Y = 1.0              # Camera height when sliding (crouched)
NORMAL_CAMERA_Y = 1.7             # Normal standing camera height (eye level)
GRAVITY_FORCE = 20.0              # Additional gravity force on slopes during slide

# Dash System
DASH_DISTANCE = 15                # Legacy dash distance (unused)
DASH_COOLDOWN = 1.0               # Seconds between dash uses
DASH_FORCE = 50                   # Force applied to velocity during dash

# === Momentum-Based Movement System ===
ACCELERATION = 20                 # How quickly player accelerates from input
FRICTION = 15                     # How quickly player decelerates without input
MAX_SPEED = 7                     # Maximum horizontal movement speed

# === Gun Physics ===
GUN_GRAVITY = 12                  # Gravity applied to dropped guns
GUN_POP_FORCE = 2                 # Upward force when gun is dropped
GUN_DROP_COOLDOWN = 2.0           # Seconds between gun drops

# === Collision Detection ===
COLLISION_BUFFER = 0.5            # Extra distance added to collision checks
PLAYER_CENTER_OFFSET = Vec3(0, 1, 0)    # Offset for collision ray origin
HEAD_HEIGHT_OFFSET = Vec3(0, 1.8, 0)    # Offset for ceiling collision checks
GUN_OFFSET = Vec3(0.3, -0.2, 1.5)       # Gun position relative to camera

# === Game Mode Settings ===
OBSTACLE_COUNT = 20               # Number of obstacles to spawn
OBSTACLE_COLOR = color.orange     # Color for obstacle entities
OBSTACLE_TEXTURE = 'brick'        # Texture for obstacles
TIMER_DURATION = 60               # Duration of timed mode in seconds

# === Wall Running Settings ===
WALL_RUN_SPEED = 18               # Speed when wall running
WALL_RUN_GRAVITY = 0.05           # Very reduced gravity during wall run (almost no gravity)
WALL_RUN_MIN_SPEED = 6            # Minimum speed required to start wall running
WALL_RUN_MAX_TIME = 8.0           # Maximum time you can wall run (seconds)
WALL_RUN_JUMP_FORCE = 20          # Force applied when jumping off wall
WALL_RUN_CAMERA_TILT = 15         # Camera tilt angle during wall run (degrees)