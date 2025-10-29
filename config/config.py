"""
Game Configuration Constants
============================

Essential game settings for the parkour shooter game.
Only includes settings that are actively used in the current version.
"""

from ursina import *

# ===============================================
# === DISPLAY & GRAPHICS SETTINGS ==============
# ===============================================

FOV_DEFAULT = 90                 # Default field of view in degrees
TEXTURE_FILTERING = 'linear'      # Texture filtering: 'nearest', 'linear'

# === Antialiasing Settings ===
ANTIALIASING_ENABLED = True       # Enable antialiasing (MSAA)
ANTIALIASING_SAMPLES = 16          # MSAA samples: 2, 4, 8, 16 (higher = better quality, lower performance)
VSYNC_ENABLED = True              # Enable vertical sync to prevent screen tearing

# === Texture Softening Settings ===
MIPMAPPING_ENABLED = True         # Enable mipmapping for better distant textures
ANISOTROPIC_FILTERING = 8         # Anisotropic filtering level: 0, 2, 4, 8, 16 (0 = disabled)
TEXTURE_SOFTENING = True          # Enable additional texture softening effects
TEXTURE_BLUR_AMOUNT = 0.5         # Texture blur/softening amount (0.0 = none, 1.0 = maximum)
TEXTURE_QUALITY = 'high'          # Texture quality: 'low', 'medium', 'high', 'ultra'

# === Skybox Settings ===
SKYBOX_ENABLED = True             # Enable skybox rendering
SKYBOX_TEXTURE = './assets/skybox_2.jpg'  # Skybox texture path (can be single image or cubemap)
SKYBOX_SCALE = 1000               # Skybox scale (large enough to encompass entire scene)
SKYBOX_COLOR = color.white        # Skybox tint color

# ===============================================
# === AUDIO SETTINGS ===========================
# ===============================================

MASTER_VOLUME = 1.0               # Master volume (0.0 to 1.0)
SFX_VOLUME = 0.8                  # Sound effects volume
GUNSHOT_SOUND = './assets/sounds/gunshot.mp3'

# ===============================================
# === PLAYER SETTINGS ==========================
# ===============================================

# === Basic Movement ===
PLAYER_GRAVITY = 0.5              # Gravity multiplier for player
PLAYER_JUMP_HEIGHT = 2            # Maximum jump height in units
PLAYER_SPEED = 5                  # Base movement speed (legacy)
SPRINT_MULTIPLIER = 1.8           # Speed multiplier when sprinting

# === Player Physics ===
PLAYER_HEIGHT = 1.8               # Player height in units
PLAYER_WIDTH = 0.8                # Player width for collisions
PLAYER_START_POS = (15, 11, 0)    # Starting position in world coordinates

# === Camera Settings ===
NORMAL_CAMERA_Y = 1.7             # Normal standing camera height (eye level)

# === Movement Mechanics ===
ACCELERATION = 20                 # How quickly player accelerates from input
FRICTION = 15                     # How quickly player decelerates without input
MAX_SPEED = 7                     # Maximum horizontal movement speed

# ===============================================
# === ADVANCED MOVEMENT MECHANICS ==============
# ===============================================

# === Sliding System ===
SLIDE_FRICTION = 6                # How quickly slide velocity decreases
SLIDE_START_VELOCITY = 40         # Initial velocity when starting slide
SLIDE_COOLDOWN = 2.0              # Seconds before can slide again
SLIDE_CAMERA_Y = 1.0              # Camera height when sliding (crouched)
GRAVITY_FORCE = 20.0              # Additional gravity force on slopes during slide

# === Dash System ===
DASH_COOLDOWN = 1.0               # Seconds between dash uses
DASH_FORCE = 50                   # Force applied to velocity during dash

# === Wall Running System ===
WALL_RUN_SPEED = 18               # Speed when wall running
WALL_RUN_MIN_SPEED = 6            # Minimum speed required to start wall running
WALL_RUN_MAX_TIME = 8.0           # Maximum time you can wall run (seconds)
WALL_RUN_JUMP_FORCE = 20          # Force applied when jumping off wall
WALL_RUN_CAMERA_TILT = 15         # Camera tilt angle during wall run (degrees)

# ===============================================
# === WEAPON SYSTEMS ===========================
# ===============================================

# === Gun Model & Positioning ===
GUN_MODEL_PATH = './assets/gun3.obj'           # Path to gun 3D model
GUN_TEXTURE_PATH = './assets/textures/gun3_texture.png'  # Gun texture
GUN_SCALE = 0.1                   # Scale of gun model
GUN_OFFSET = Vec3(0.3, -0.2, 1.5) # Gun position relative to camera

# === Shooting Mechanics ===
SHOOTING_ENABLED = True           # Enable shooting
BULLET_RANGE = 9999               # Maximum bullet range

# === Gun Physics ===
GUN_GRAVITY = 12                  # Gravity applied to dropped guns
GUN_POP_FORCE = 2                 # Upward force when gun is dropped
GUN_RESPAWN_TIME = 1.0            # Time to respawn new gun after drop

# === Recoil System ===
RECOIL_ENABLED = True             # Enable recoil effects
RECOIL_VERTICAL = 0.3             # Upward camera kick on shot
RECOIL_HORIZONTAL = 0           # Random horizontal camera kick
RECOIL_RECOVERY_SPEED = 8.0       # How fast recoil recovers
RECOIL_DURATION = 0.15            # How long recoil effect lasts
RECOIL_PATTERN_ENABLED = False    # Use predictable recoil pattern
RECOIL_MULTIPLIER_STANDING = 1.0  # Recoil multiplier when standing
RECOIL_MULTIPLIER_CROUCHING = 0.7 # Recoil multiplier when crouching
RECOIL_MULTIPLIER_MOVING = 1.3    # Recoil multiplier when moving

# ===============================================
# === COLLISION & PHYSICS =======================
# ===============================================

HEAD_HEIGHT_OFFSET = Vec3(0, 1.8, 0)    # Offset for ceiling collision checks

# ===============================================
# === GAME MODES & SCORING =====================
# ===============================================

# === Game Modes ===
CASUAL_MODE_ENABLED = True        # Enable casual play mode
TIMED_MODE_ENABLED = True         # Enable timed challenge mode
TIMER_DURATION = 60               # Duration of timed mode in seconds
SCORE_MULTIPLIER = 1.0            # Score multiplier for timed mode
ACCURACY_TRACKING = False         # Track shooting accuracy

# === Scoring System ===
POINTS_PER_TARGET = 100           # Base points per target hit

# ===============================================
# === USER INTERFACE ===========================
# ===============================================

# === Menu Settings ===
MENU_BACKGROUND_COLOR = color.dark_gray  # Menu background color
MENU_TEXT_COLOR = color.white     # Menu text color
MENU_BUTTON_COLOR = color.green   # Menu button color
MENU_HOVER_COLOR = color.yellow   # Button hover color
MENU_FONT_SIZE = 1.2              # Menu font size

# === UI Positioning ===
TIMER_POSITION = (-0.8, 0.4)     # Timer display position
SCORE_POSITION = (0, 0.4)        # Score display position
ACCURACY_POSITION = (0.6, 0.4)   # Accuracy display position

# ===============================================
# === COLLISION & PHYSICS =======================
# ===============================================

HEAD_HEIGHT_OFFSET = Vec3(0, 1.8, 0)    # Offset for ceiling collision checks
PLAYER_CENTER_OFFSET = Vec3(0, 0.9, 0)  # Offset to player center for collision detection
COLLISION_BUFFER = 0.1                  # Safety buffer for collision detection
GUN_DROP_COOLDOWN = 1.0                 # Cooldown between gun drops

# ===============================================
# === DEBUG & DEVELOPMENT ======================
# ===============================================

DEBUG_MODE = False                # Enable debug mode