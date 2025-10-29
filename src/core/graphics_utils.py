"""
Graphics Utilities
==================

Graphics configuration and optimization utilities.
"""

from ursina import *
from config import *

# ===============================================
# === GRAPHICS UTILITIES =======================
# ===============================================

def set_antialiasing(samples=4, enabled=True):
    """
    Dynamically set antialiasing level.
    
    Args:
        samples (int): Number of MSAA samples (2, 4, 8, 16)
        enabled (bool): Enable/disable antialiasing
    """
    try:
        if enabled and samples > 0:
            from panda3d.core import MultisampleAntialiasAttrib, ConfigVariableInt, ConfigVariableBool
            
            # Set MSAA
            render.setAntialias(MultisampleAntialiasAttrib.MAuto, samples)
            
            # Configure multisampling
            ConfigVariableInt("multisamples", samples).setValue(samples)
            ConfigVariableBool("framebuffer-multisample", True).setValue(True)
            
            print(f"✅ Antialiasing set to {samples}x MSAA")
            return True
        else:
            # Disable antialiasing
            render.clearAntialias()
            print("✅ Antialiasing disabled")
            return True
            
    except Exception as e:
        print(f"⚠️ Could not set antialiasing: {e}")
        return False

def set_vsync(enabled=True):
    """
    Enable or disable vertical sync.
    
    Args:
        enabled (bool): Enable/disable VSync
    """
    try:
        from panda3d.core import ConfigVariableBool
        ConfigVariableBool("sync-video", enabled).setValue(enabled)
        print(f"✅ VSync {'enabled' if enabled else 'disabled'}")
        return True
    except Exception as e:
        print(f"⚠️ Could not set VSync: {e}")
        return False

def set_texture_quality(quality='high'):
    """
    Set texture quality level.
    
    Args:
        quality (str): Quality level - 'low', 'medium', 'high', 'ultra'
    """
    try:
        from panda3d.core import ConfigVariableInt, ConfigVariableBool
        
        quality_settings = {
            'low': {'memory': 64, 'compression': True, 'max_size': 512, 'aniso': 2},
            'medium': {'memory': 128, 'compression': True, 'max_size': 1024, 'aniso': 4},
            'high': {'memory': 256, 'compression': False, 'max_size': 2048, 'aniso': 8},
            'ultra': {'memory': 512, 'compression': False, 'max_size': 4096, 'aniso': 16}
        }
        
        if quality not in quality_settings:
            quality = 'high'
        
        settings = quality_settings[quality]
        
        # Apply settings
        ConfigVariableInt("texture-memory-limit", settings['memory'] * 1024 * 1024).setValue(settings['memory'] * 1024 * 1024)
        ConfigVariableBool("compressed-textures", settings['compression']).setValue(settings['compression'])
        ConfigVariableInt("max-texture-dimension", settings['max_size']).setValue(settings['max_size'])
        ConfigVariableInt("texture-anisotropic-degree", settings['aniso']).setValue(settings['aniso'])
        
        print(f"✅ Texture quality set to: {quality}")
        return True
        
    except Exception as e:
        print(f"⚠️ Could not set texture quality: {e}")
        return False

def set_texture_softening(enabled=True, blur_amount=0.3):
    """
    Enable/disable texture softening effects.
    
    Args:
        enabled (bool): Enable texture softening
        blur_amount (float): Amount of softening (0.0 to 1.0)
    """
    try:
        from panda3d.core import ConfigVariableBool, ConfigVariableDouble
        
        if enabled:
            ConfigVariableBool("smooth-textures", True).setValue(True)
            ConfigVariableBool("texture-minfilter", "linear_mipmap_linear").setValue("linear_mipmap_linear")
            ConfigVariableBool("texture-magfilter", "linear").setValue("linear")
            
            # Apply blur amount (this is a conceptual setting - actual implementation varies)
            blur_factor = max(0.0, min(1.0, blur_amount))
            print(f"✅ Texture softening enabled with {blur_factor:.1f} blur amount")
        else:
            ConfigVariableBool("smooth-textures", False).setValue(False)
            print("✅ Texture softening disabled")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Could not set texture softening: {e}")
        return False

def get_graphics_info():
    """
    Get current graphics configuration information.
    
    Returns:
        dict: Graphics settings information
    """
    info = {
        'antialiasing_enabled': ANTIALIASING_ENABLED,
        'antialiasing_samples': ANTIALIASING_SAMPLES,
        'vsync_enabled': VSYNC_ENABLED,
        'texture_filtering': TEXTURE_FILTERING,
        'texture_quality': TEXTURE_QUALITY,
        'mipmapping_enabled': MIPMAPPING_ENABLED,
        'anisotropic_filtering': ANISOTROPIC_FILTERING,
        'texture_softening': TEXTURE_SOFTENING,
        'texture_blur_amount': TEXTURE_BLUR_AMOUNT,
        'fov': FOV_DEFAULT
    }
    
    try:
        from panda3d.core import ConfigVariableInt, ConfigVariableBool
        info['actual_multisamples'] = ConfigVariableInt("multisamples").getValue()
        info['actual_vsync'] = ConfigVariableBool("sync-video").getValue()
        info['actual_anisotropic'] = ConfigVariableInt("texture-anisotropic-degree").getValue()
        info['actual_texture_memory'] = ConfigVariableInt("texture-memory-limit").getValue()
    except:
        info['actual_multisamples'] = 'Unknown'
        info['actual_vsync'] = 'Unknown'
        info['actual_anisotropic'] = 'Unknown'
        info['actual_texture_memory'] = 'Unknown'
    
    return info

def optimize_for_performance():
    """
    Apply performance-optimized graphics settings.
    """
    print("🚀 Applying performance optimizations...")
    set_antialiasing(samples=2, enabled=True)  # Lower MSAA
    set_vsync(enabled=False)  # Disable VSync for higher FPS
    set_texture_quality('medium')  # Balanced texture quality
    set_texture_softening(enabled=True, blur_amount=0.2)  # Light softening
    
def optimize_for_quality():
    """
    Apply quality-optimized graphics settings.
    """
    print("✨ Applying quality optimizations...")
    set_antialiasing(samples=8, enabled=True)  # Higher MSAA
    set_vsync(enabled=True)  # Enable VSync for smooth display
    set_texture_quality('ultra')  # Maximum texture quality
    set_texture_softening(enabled=True, blur_amount=0.5)  # Enhanced softening

def optimize_for_ultra():
    """
    Apply maximum quality settings (may impact performance).
    """
    print("💎 Applying ultra quality settings...")
    set_antialiasing(samples=16, enabled=True)  # Maximum MSAA
    set_vsync(enabled=True)  # Smooth display
    set_texture_quality('ultra')  # Ultra texture quality
    set_texture_softening(enabled=True, blur_amount=0.7)  # Maximum softening

def print_graphics_info():
    """Print current graphics configuration."""
    info = get_graphics_info()
    print("\n📊 Graphics Configuration:")
    print(f"   🎨 Antialiasing: {info['antialiasing_samples']}x MSAA ({'Enabled' if info['antialiasing_enabled'] else 'Disabled'})")
    print(f"   📺 VSync: {'Enabled' if info['vsync_enabled'] else 'Disabled'}")
    print(f"   🖼️  Texture Quality: {info['texture_quality'].title()}")
    print(f"   🔍 Texture Filtering: {info['texture_filtering'].title()}")
    print(f"   🌟 Anisotropic Filtering: {info['anisotropic_filtering']}x")
    print(f"   ✨ Texture Softening: {'Enabled' if info['texture_softening'] else 'Disabled'}")
    if info['texture_softening']:
        print(f"   💫 Softening Amount: {info['texture_blur_amount']:.1f}")
    print(f"   📐 Field of View: {info['fov']}°")
    print(f"   🗺️  Mipmapping: {'Enabled' if info['mipmapping_enabled'] else 'Disabled'}")
    
    # Show actual values if available
    if info['actual_multisamples'] != 'Unknown':
        print(f"\n🔧 Actual Settings:")
        print(f"   MSAA Samples: {info['actual_multisamples']}")
        print(f"   Anisotropic: {info['actual_anisotropic']}x")
        if info['actual_texture_memory'] != 'Unknown':
            memory_mb = info['actual_texture_memory'] // (1024 * 1024)
            print(f"   Texture Memory: {memory_mb}MB")