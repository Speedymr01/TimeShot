#!/usr/bin/env python3
"""
Configuration Tools Launcher
============================

Launches the configuration tools with proper path setup.
"""

import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'tools'))

# Change to project directory
os.chdir(project_root)

# Import and run config tools
try:
    from tools.config_tools import main
    print("🔧 Starting Configuration Tools...")
    main()
except ImportError as e:
    print(f"❌ Error starting config tools: {e}")
    print("Please ensure all tool files are present.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Config tools error: {e}")
    sys.exit(1)