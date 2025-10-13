#!/usr/bin/env python3
"""
Test Runner Script
=================

Runs all tests with proper path setup.
"""

import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'tests'))
sys.path.insert(0, str(project_root / 'tools' / 'security'))

# Change to project directory
os.chdir(project_root)

# Import and run tests
try:
    from tests.security_tests import run_security_tests
    print("🧪 Running Test Suite...")
    success = run_security_tests()
    sys.exit(0 if success else 1)
except ImportError as e:
    print(f"❌ Error importing tests: {e}")
    print("Please ensure all test files are present.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test error: {e}")
    sys.exit(1)