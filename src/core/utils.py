"""
Utility Functions
=================

Common utility functions used throughout the game.
"""

from ursina import *
from config import *
import math

# ===============================================
# === UTILITY FUNCTIONS ========================
# ===============================================

def check_collision(origin, direction, distance, ignore_list=None):
    """
    Perform collision detection with error handling and validation.
    
    Args:
        origin (Vec3): Starting point for collision check
        direction (Vec3): Direction vector to check collision
        distance (float): Maximum distance to check
        ignore_list (list): Entities to ignore during collision check
    
    Returns:
        Hit object or None if no collision or error occurred
    """
    if ignore_list is None:
        ignore_list = []
    
    # Validate inputs to prevent crashes
    if not origin or not direction or distance <= 0:
        return None
        
    try:
        return raycast(
            origin=origin + PLAYER_CENTER_OFFSET,  # Offset to player center
            direction=direction,
            distance=distance + COLLISION_BUFFER,   # Add buffer for safety
            ignore=ignore_list
        )
    except Exception:
        # Return safe default if raycast fails (asset loading issues, etc.)
        return None

def apply_slide_movement(movement, collision_normal):
    """
    Calculate sliding movement along a surface when hitting a wall.
    Uses vector projection to slide along the surface instead of stopping.
    
    Args:
        movement (Vec3): Original movement vector
        collision_normal (Vec3): Normal vector of the surface hit
    
    Returns:
        Vec3: Adjusted movement vector that slides along the surface
    """
    if not collision_normal:
        return Vec3(0, 0, 0)
    
    # Project movement onto surface: movement - (movement · normal) * normal
    slide_movement = movement - collision_normal * (movement.dot(collision_normal))
    return slide_movement

def safe_entity_create(model_path, texture_path=None, **kwargs):
    """
    Create an entity with error handling for missing assets.
    Falls back to a red cube if the specified model cannot be loaded.
    
    Args:
        model_path (str): Path to the 3D model file
        texture_path (str, optional): Path to texture file
        **kwargs: Additional Entity parameters
    
    Returns:
        Entity: Created entity or fallback cube if loading fails
    """
    try:
        entity = Entity(model=model_path, **kwargs)
        if texture_path:
            entity.texture = texture_path
        return entity
    except Exception as e:
        print(f"Warning: Could not load asset {model_path}: {e}")
        # Return a red cube as visual indicator of missing asset
        return Entity(model='cube', color=color.red, **kwargs)