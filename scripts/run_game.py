#!/usr/bin/env python3
"""
Game Launcher Script
===================

Launches the parkour shooter game with proper path setup.
"""

import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Change to project directory
os.chdir(project_root)

# Import and run the main game
try:
    import main
    print("🎮 Starting Parkour Shooter Game...")
except ImportError as e:
    print(f"❌ Error starting game: {e}")
    print("Please ensure all game files are present.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Game error: {e}")
    sys.exit(1)