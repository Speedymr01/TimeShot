#!/usr/bin/env python3
"""
Configuration Tools Launcher
============================

Quick launcher for all configuration and settings tools.
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.RESET}"

def clear_screen():
    """Clear the terminal screen safely."""
    try:
        if os.name == 'nt':
            subprocess.run(['cls'], shell=True, check=False, timeout=5)
        else:
            subprocess.run(['clear'], check=False, timeout=5)
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fallback: print newlines
        print('\n' * 50)

def print_header():
    """Print the application header."""
    header = """
╔══════════════════════════════════════════════════════════════╗
║                🛠️  GAME CONFIGURATION TOOLS 🛠️                 ║
║                 Choose your configuration tool               ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(Colors.colorize(header, Colors.BRIGHT_CYAN))

def print_menu():
    """Print the main menu."""
    print(Colors.colorize("🔧 Available Tools:", Colors.BRIGHT_WHITE))
    print()
    
    tools = [
        ("Interactive Settings Editor", "settings_editor.py", "Edit all game settings with a user-friendly interface"),
        ("Configuration Validator", "config_validator.py", "Validate settings and show configuration summary"),
        ("Settings Examples & Presets", "settings_examples.py", "View and apply preset configurations"),
        ("Start Game", "main.py", "Launch the game with current settings"),
    ]
    
    for i, (name, script, description) in enumerate(tools, 1):
        # Check if file exists
        exists = os.path.exists(script)
        status_color = Colors.GREEN if exists else Colors.RED
        status_text = "✅" if exists else "❌"
        
        print(f"  {Colors.colorize(f'{i}.', Colors.BRIGHT_BLUE)} "
              f"{Colors.colorize(name, Colors.WHITE)} {status_text}")
        print(f"     {Colors.colorize(description, Colors.CYAN)}")
        if not exists:
            print(f"     {Colors.colorize(f'File not found: {script}', Colors.RED)}")
        print()
    
    print(Colors.colorize("🔧 Quick Actions:", Colors.BRIGHT_WHITE))
    print(f"  {Colors.colorize('c.', Colors.BRIGHT_BLUE)} Show current config summary")
    print(f"  {Colors.colorize('h.', Colors.BRIGHT_BLUE)} Show help and usage tips")
    print(f"  {Colors.colorize('q.', Colors.BRIGHT_BLUE)} Quit")
    print()

def run_tool(script_name: str):
    """Run a configuration tool with security validation."""
    # Validate script path
    try:
        script_path = Path(script_name).resolve()
        current_dir = Path.cwd()
        
        # Prevent path traversal
        if not str(script_path).startswith(str(current_dir)):
            print(Colors.colorize("❌ Error: Invalid script path!", Colors.RED))
            input("Press Enter to continue...")
            return
        
        # Check if file exists and is a Python file
        if not script_path.exists():
            print(Colors.colorize(f"❌ Error: {script_name} not found!", Colors.RED))
            input("Press Enter to continue...")
            return
        
        if script_path.suffix != '.py':
            print(Colors.colorize("❌ Error: Only Python scripts allowed!", Colors.RED))
            input("Press Enter to continue...")
            return
        
    except Exception as e:
        print(Colors.colorize(f"❌ Error validating script: {e}", Colors.RED))
        input("Press Enter to continue...")
        return
    
    try:
        print(Colors.colorize(f"🚀 Launching {script_name}...", Colors.CYAN))
        print()
        
        # Run the script with timeout and security constraints
        result = subprocess.run(
            [sys.executable, str(script_path)], 
            capture_output=False, 
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=current_dir  # Ensure it runs in current directory
        )
        
        if result.returncode != 0:
            print(Colors.colorize(f"⚠️  Tool exited with code {result.returncode}", Colors.YELLOW))
        
    except subprocess.TimeoutExpired:
        print(Colors.colorize("\n⏰ Tool timed out after 5 minutes.", Colors.YELLOW))
    except KeyboardInterrupt:
        print(Colors.colorize("\n🛑 Tool interrupted by user.", Colors.YELLOW))
    except Exception as e:
        print(Colors.colorize(f"❌ Error running tool: {e}", Colors.RED))
    
    print()
    input("Press Enter to return to menu...")

def show_config_summary():
    """Show a quick configuration summary."""
    try:
        # Safely import config from config directory
        current_dir = Path.cwd()
        config_dir = current_dir / 'config'
        config_path = config_dir / 'config.py'
        
        if not config_path.exists():
            print(Colors.colorize("❌ Config file not found!", Colors.RED))
            return
        
        # Validate it's in project directory (prevent path traversal)
        if not str(config_path.resolve()).startswith(str(current_dir)):
            print(Colors.colorize("❌ Invalid config file location!", Colors.RED))
            return
        
        sys.path.insert(0, str(config_dir))
        import config
        
        print(Colors.colorize("📊 Quick Configuration Summary", Colors.BRIGHT_WHITE))
        print("=" * 50)
        
        # Key settings
        key_settings = [
            ("Display Resolution", f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"),
            ("Field of View", f"{config.FOV_DEFAULT}°"),
            ("Master Volume", f"{config.MASTER_VOLUME * 100:.0f}%"),
            ("Max Player Speed", str(config.MAX_SPEED)),
            ("Recoil Enabled", "Yes" if config.RECOIL_ENABLED else "No"),
            ("Vertical Recoil", str(config.RECOIL_VERTICAL)),
            ("Sliding Enabled", "Yes" if config.SLIDE_ENABLED else "No"),
            ("Wall Running Enabled", "Yes" if config.WALL_RUN_ENABLED else "No"),
            ("Debug Mode", "Yes" if config.DEBUG_MODE else "No"),
        ]
        
        for setting, value in key_settings:
            print(f"{Colors.colorize(setting + ':', Colors.CYAN):25s} {Colors.colorize(value, Colors.WHITE)}")
        
        print()
        print(Colors.colorize("💡 Use the Interactive Settings Editor to modify these values!", Colors.YELLOW))
        
    except ImportError as e:
        print(Colors.colorize(f"❌ Error loading config: {e}", Colors.RED))
    except Exception as e:
        print(Colors.colorize(f"❌ Error: {e}", Colors.RED))
    
    print()
    input("Press Enter to continue...")

def show_help():
    """Show help and usage information."""
    help_text = f"""
{Colors.colorize('🎮 Game Configuration Help', Colors.BRIGHT_WHITE)}
{'=' * 50}

{Colors.colorize('📝 Configuration Files:', Colors.CYAN)}
  • config.py           - Main configuration file with all settings
  • settings_editor.py  - Interactive editor for real-time changes
  • config_validator.py - Validates settings and shows summary
  • settings_examples.py - Preset configurations for different gameplay

{Colors.colorize('🔧 How to Use:', Colors.CYAN)}
  1. Use Interactive Settings Editor for easy configuration
  2. Validate your settings before playing
  3. Apply presets for quick setup
  4. Launch the game to test your changes

{Colors.colorize('⚡ Quick Tips:', Colors.CYAN)}
  • All settings take effect after restarting the game
  • Use presets to quickly try different gameplay styles
  • Validate settings to catch configuration errors
  • Backup your config.py before making major changes

{Colors.colorize('🎯 Popular Settings to Adjust:', Colors.CYAN)}
  • RECOIL_VERTICAL/HORIZONTAL - Gun recoil strength
  • MAX_SPEED - Player movement speed
  • FOV_DEFAULT - Field of view (60-120 recommended)
  • MASTER_VOLUME/SFX_VOLUME - Audio levels
  • SLIDE_ENABLED/DASH_ENABLED - Enable/disable movement mechanics

{Colors.colorize('🚨 Troubleshooting:', Colors.CYAN)}
  • If game crashes: Run validator to check for invalid settings
  • If performance issues: Try lower quality preset
  • If controls feel wrong: Adjust mouse sensitivity and FOV
  • If audio issues: Check volume settings and file paths
    """
    
    print(help_text)
    input("Press Enter to continue...")

def main():
    """Main application loop."""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        try:
            choice = input(Colors.colorize("Select option: ", Colors.BRIGHT_GREEN)).strip().lower()
            
            if choice == 'q':
                print(Colors.colorize("👋 Goodbye!", Colors.BRIGHT_CYAN))
                break
            elif choice == '1':
                run_tool('settings_editor.py')
            elif choice == '2':
                run_tool('config_validator.py')
            elif choice == '3':
                run_tool('settings_examples.py')
            elif choice == '4':
                run_tool('main.py')
            elif choice == 'c':
                clear_screen()
                show_config_summary()
            elif choice == 'h':
                clear_screen()
                show_help()
            else:
                print(Colors.colorize("❌ Invalid option. Please try again.", Colors.RED))
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print(Colors.colorize("\n👋 Goodbye!", Colors.BRIGHT_CYAN))
            break
        except Exception as e:
            print(Colors.colorize(f"❌ Error: {e}", Colors.RED))
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()