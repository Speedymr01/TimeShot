"""
Target System
=============

Target spawning, management, and respawning mechanics.
"""

from ursina import *
from config import *
from random import uniform

# ===============================================
# === TARGET SYSTEM =============================
# ===============================================

class TargetManager:
    def __init__(self):
        self.target_spheres = []
    
    def spawn_targets(self, count=10):
        """
        Spawn target entities with bounds checking and error handling.
        
        Args:
            count (int): Number of targets to spawn
        """
        # Validate input parameters
        if not isinstance(count, int) or count <= 0 or count > 50:  # Prevent excessive spawning
            return
        
        for _ in range(count):
            try:
                # Generate random positions within safe bounds
                y = uniform(11, 20)
                z = uniform(-10, 10)
                
                sphere = Entity(
                    model='sphere',
                    color=color.red,
                    scale=1,
                    position=(62, y, z),
                    collider='box',
                    name='target'
                )
                self.target_spheres.append(sphere)
                
            except Exception as e:
                print(f"Error spawning target: {e}")
                continue

    def respawn_targets(self):
        """
        Maintain target count with safety checks.
        """
        try:
            # Clean up any None or destroyed targets
            self.target_spheres[:] = [target for target in self.target_spheres if target and hasattr(target, 'enabled')]
            
            # Respawn if below minimum count
            current_count = len(self.target_spheres)
            if current_count < 10:
                spawn_count = min(10 - current_count, 10)  # Cap spawn count
                self.spawn_targets(count=spawn_count)
                
        except Exception as e:
            print(f"Error in respawn_targets: {e}")
    
    def clear_targets(self):
        """Clear all targets (used when ending game modes)."""
        for target in self.target_spheres:
            if target:
                destroy(target)
        self.target_spheres.clear()

# Global target manager (will be initialized in main.py)
target_manager = None