#!/usr/bin/env python3
"""
Interactive Settings Editor
===========================

CLI-based interactive editor for game configuration with colored output.
Allows real-time editing of all game settings with validation and preview.
SECURITY: Fixed eval() vulnerability and added comprehensive input validation.
"""

import os
import sys
import re
import ast
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple, Union

# Color codes for terminal output
class Colors:
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Reset
    RESET = '\033[0m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """Apply color to text."""
        return f"{color}{text}{Colors.RESET}"

class SettingsEditor:
    # Security constants
    MAX_FILE_SIZE = 1024 * 1024  # 1MB limit
    MAX_INPUT_LENGTH = 1000
    ALLOWED_SETTING_TYPES = (bool, int, float, str)
    
    def __init__(self):
        self.config_file = self._validate_config_path('config.py')
        self.settings = {}
        self.categories = {}
        self.current_category = None
        self.modified = False
        
        # Load current settings
        self.load_settings()
        self.organize_categories()
    
    def _validate_config_path(self, path: str) -> str:
        """Validate and sanitize the config file path to prevent path traversal."""
        try:
            current_dir = Path.cwd()
            
            # Handle both 'config.py' and 'config/config.py' paths
            if path == 'config.py':
                config_path = current_dir / 'config' / 'config.py'
            else:
                config_path = Path(path).resolve()
            
            # Prevent path traversal attacks
            if not str(config_path).startswith(str(current_dir)):
                raise ValueError("Config file must be in project directory")
            
            # Ensure it's a Python file
            if config_path.suffix != '.py':
                raise ValueError("Config file must be a Python file")
            
            return str(config_path)
        except Exception as e:
            print(Colors.colorize(f"❌ Invalid config path: {e}", Colors.RED))
            sys.exit(1)
    
    def _safe_literal_eval(self, value_str: str) -> Any:
        """Safely evaluate literal values without code execution."""
        value_str = value_str.strip()
        
        # Handle special Ursina types as strings
        if any(prefix in value_str for prefix in ['color.', 'Vec3(', 'window.']):
            return value_str
        
        # Handle boolean literals
        if value_str in ('True', 'true'):
            return True
        elif value_str in ('False', 'false'):
            return False
        elif value_str == 'None':
            return None
        
        # Try to safely evaluate as literal
        try:
            return ast.literal_eval(value_str)
        except (ValueError, SyntaxError):
            # If it fails, treat as string (remove quotes if present)
            return value_str.strip("'\"")
    
    def _is_valid_setting_name(self, name: str) -> bool:
        """Validate setting name to prevent injection."""
        return bool(re.match(r'^[A-Z_][A-Z0-9_]*$', name)) and len(name) <= 50
    
    def _is_valid_setting_value(self, value: Any) -> bool:
        """Validate setting value type and content."""
        if not isinstance(value, self.ALLOWED_SETTING_TYPES):
            return False
        
        if isinstance(value, str):
            if len(value) > self.MAX_INPUT_LENGTH:
                return False
            # Check for suspicious content
            dangerous_patterns = ['import', 'exec', 'eval', '__', 'subprocess', 'os.system']
            if any(pattern in value.lower() for pattern in dangerous_patterns):
                return False
        
        if isinstance(value, (int, float)):
            if not (-1000000 <= value <= 1000000):
                return False
        
        return True

    def load_settings(self):
        """Load settings from config.py file with security validation."""
        try:
            config_path = Path(self.config_file)
            
            # Check file size to prevent DoS
            if config_path.stat().st_size > self.MAX_FILE_SIZE:
                raise ValueError(f"Config file too large (max {self.MAX_FILE_SIZE} bytes)")
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse settings using regex with validation
            pattern = r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)(?:\s*#.*)?$'
            
            for line_num, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                match = re.match(pattern, line)
                if match:
                    key, value = match.groups()
                    
                    # Validate setting name
                    if not self._is_valid_setting_name(key):
                        print(f"Warning: Skipping invalid setting name: {key}")
                        continue
                    
                    # Safely parse value
                    try:
                        parsed_value = self._safe_literal_eval(value)
                        
                        # Validate value
                        if self._is_valid_setting_value(parsed_value):
                            self.settings[key] = parsed_value
                        else:
                            print(f"Warning: Skipping invalid value for {key}: {value}")
                            
                    except Exception as e:
                        print(f"Warning: Could not parse {key} on line {line_num}: {e}")
        
        except FileNotFoundError:
            print(Colors.colorize("❌ Config file not found!", Colors.RED))
            sys.exit(1)
        except PermissionError:
            print(Colors.colorize("❌ Permission denied reading config file!", Colors.RED))
            sys.exit(1)
        except Exception as e:
            print(Colors.colorize(f"❌ Error loading config: {e}", Colors.RED))
            sys.exit(1)
    
    def organize_categories(self):
        """Organize settings into categories based on prefixes and comments."""
        self.categories = {
            'Display & Graphics': [],
            'Audio Settings': [],
            'Environment': [],
            'Player Settings': [],
            'Movement Mechanics': [],
            'Weapon Systems': [],
            'Target System': [],
            'Game Modes': [],
            'User Interface': [],
            'Performance & Debug': []
        }
        
        # Categorize settings based on prefixes
        for key in self.settings:
            if any(prefix in key for prefix in ['WINDOW_', 'FOV_', 'SHADOW_', 'RENDER_', 'ANTI_']):
                self.categories['Display & Graphics'].append(key)
            elif any(prefix in key for prefix in ['MASTER_', 'SFX_', 'MUSIC_', 'AUDIO_', 'SOUND']):
                self.categories['Audio Settings'].append(key)
            elif any(prefix in key for prefix in ['MAP_', 'GROUND_', 'SKY_', 'SUN_', 'FOG_', 'WIND_']):
                self.categories['Environment'].append(key)
            elif any(prefix in key for prefix in ['PLAYER_', 'MOUSE_', 'CAMERA_', 'JUMP_', 'CROUCH_']):
                self.categories['Player Settings'].append(key)
            elif any(prefix in key for prefix in ['SLIDE_', 'DASH_', 'WALL_RUN_', 'ACCELERATION', 'FRICTION', 'MAX_SPEED']):
                self.categories['Movement Mechanics'].append(key)
            elif any(prefix in key for prefix in ['GUN_', 'RECOIL_', 'SHOOTING_', 'BULLET_', 'MUZZLE_']):
                self.categories['Weapon Systems'].append(key)
            elif any(prefix in key for prefix in ['TARGET_']):
                self.categories['Target System'].append(key)
            elif any(prefix in key for prefix in ['CASUAL_', 'TIMED_', 'TIMER_', 'SCORE_', 'POINTS_']):
                self.categories['Game Modes'].append(key)
            elif any(prefix in key for prefix in ['SHOW_', 'MENU_', 'CROSSHAIR_', 'HUD_']):
                self.categories['User Interface'].append(key)
            elif any(prefix in key for prefix in ['DEBUG_', 'QUALITY_', 'MAX_', 'ENABLE_']):
                self.categories['Performance & Debug'].append(key)
            else:
                # Default category for uncategorized settings
                if 'Display & Graphics' not in [cat for cat, settings in self.categories.items() if key in settings]:
                    self.categories['Display & Graphics'].append(key)
    
    def clear_screen(self):
        """Clear the terminal screen safely."""
        try:
            if os.name == 'nt':
                subprocess.run(['cls'], shell=True, check=False, timeout=5)
            else:
                subprocess.run(['clear'], check=False, timeout=5)
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            # Fallback: print newlines
            print('\n' * 50)
    
    def print_header(self):
        """Print the application header."""
        header = """
╔══════════════════════════════════════════════════════════════╗
║                    🎮 GAME SETTINGS EDITOR 🎮                ║
║                     Interactive Configuration                ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(Colors.colorize(header, Colors.BRIGHT_CYAN))
        
        if self.modified:
            print(Colors.colorize("⚠️  Unsaved changes detected!", Colors.YELLOW))
        print()
    
    def print_main_menu(self):
        """Print the main category selection menu."""
        print(Colors.colorize("📂 Configuration Categories:", Colors.BRIGHT_WHITE))
        print()
        
        for i, (category, settings) in enumerate(self.categories.items(), 1):
            count = len(settings)
            if count > 0:
                color = Colors.GREEN if count > 0 else Colors.DIM
                print(f"  {Colors.colorize(f'{i:2d}.', Colors.BRIGHT_BLUE)} "
                      f"{Colors.colorize(category, color)} "
                      f"{Colors.colorize(f'({count} settings)', Colors.DIM)}")
        
        print()
        print(Colors.colorize("🔧 Actions:", Colors.BRIGHT_WHITE))
        print(f"  {Colors.colorize('s.', Colors.BRIGHT_BLUE)} Save changes to config.py")
        print(f"  {Colors.colorize('r.', Colors.BRIGHT_BLUE)} Reload from config.py")
        print(f"  {Colors.colorize('v.', Colors.BRIGHT_BLUE)} Validate current settings")
        print(f"  {Colors.colorize('p.', Colors.BRIGHT_BLUE)} Apply preset configuration")
        print(f"  {Colors.colorize('q.', Colors.BRIGHT_BLUE)} Quit editor")
        print()
    
    def print_category_menu(self, category: str):
        """Print settings for a specific category."""
        settings_list = self.categories[category]
        
        print(Colors.colorize(f"📋 {category} Settings:", Colors.BRIGHT_WHITE))
        print()
        
        if not settings_list:
            print(Colors.colorize("  No settings in this category.", Colors.DIM))
            return
        
        for i, setting in enumerate(settings_list, 1):
            if setting in self.settings:
                value = self.settings[setting]
                value_str = str(value)
                
                # Color code based on value type
                if isinstance(value, bool):
                    value_color = Colors.GREEN if value else Colors.RED
                elif isinstance(value, (int, float)):
                    value_color = Colors.CYAN
                elif isinstance(value, str):
                    value_color = Colors.YELLOW
                else:
                    value_color = Colors.WHITE
                
                # Truncate long values
                if len(value_str) > 40:
                    value_str = value_str[:37] + "..."
                
                print(f"  {Colors.colorize(f'{i:2d}.', Colors.BRIGHT_BLUE)} "
                      f"{Colors.colorize(setting, Colors.WHITE):30s} = "
                      f"{Colors.colorize(value_str, value_color)}")
        
        print()
        print(Colors.colorize("🔧 Actions:", Colors.BRIGHT_WHITE))
        print(f"  {Colors.colorize('b.', Colors.BRIGHT_BLUE)} Back to main menu")
        print(f"  {Colors.colorize('1-{len(settings_list)}.', Colors.BRIGHT_BLUE)} Edit setting")
        print()
    
    def edit_setting(self, setting_name: str):
        """Edit a specific setting."""
        current_value = self.settings.get(setting_name, "")
        
        print(Colors.colorize(f"✏️  Editing: {setting_name}", Colors.BRIGHT_WHITE))
        print(f"Current value: {Colors.colorize(str(current_value), Colors.CYAN)}")
        print()
        
        # Provide hints based on setting type
        if isinstance(current_value, bool):
            print(Colors.colorize("💡 Hint: Enter 'true' or 'false'", Colors.DIM))
        elif isinstance(current_value, (int, float)):
            print(Colors.colorize("💡 Hint: Enter a number", Colors.DIM))
        elif isinstance(current_value, str):
            print(Colors.colorize("💡 Hint: Enter text (quotes optional)", Colors.DIM))
        
        print(Colors.colorize("Press Enter to keep current value, or type new value:", Colors.DIM))
        
        try:
            new_value = input(f"{Colors.colorize('New value:', Colors.BRIGHT_GREEN)} ").strip()
            
            # Validate input length
            if len(new_value) > self.MAX_INPUT_LENGTH:
                print(Colors.colorize(f"❌ Input too long (max {self.MAX_INPUT_LENGTH} characters)", Colors.RED))
                return
            
            if not new_value:
                print(Colors.colorize("✅ Value unchanged.", Colors.GREEN))
                return
            
            # Parse the new value based on current type
            try:
                if isinstance(current_value, bool):
                    if new_value.lower() in ['true', 't', '1', 'yes', 'y', 'on']:
                        parsed_value = True
                    elif new_value.lower() in ['false', 'f', '0', 'no', 'n', 'off']:
                        parsed_value = False
                    else:
                        raise ValueError("Invalid boolean value")
                elif isinstance(current_value, int):
                    parsed_value = int(new_value)
                elif isinstance(current_value, float):
                    parsed_value = float(new_value)
                else:
                    # String value - sanitize
                    parsed_value = new_value.strip("'\"")
                
                # Validate the new value
                is_valid, error_msg = self.validate_setting(setting_name, parsed_value)
                if is_valid:
                    self.settings[setting_name] = parsed_value
                    self.modified = True
                    print(Colors.colorize(f"✅ {setting_name} updated to: {parsed_value}", Colors.GREEN))
                else:
                    print(Colors.colorize(f"❌ Invalid value: {error_msg}", Colors.RED))
            
            except ValueError as e:
                print(Colors.colorize(f"❌ Invalid input format: {e}", Colors.RED))
        
        except ValueError as e:
            print(Colors.colorize(f"❌ Invalid input: {e}", Colors.RED))
        except KeyboardInterrupt:
            print(Colors.colorize("\n❌ Edit cancelled.", Colors.YELLOW))
        
        input(Colors.colorize("\nPress Enter to continue...", Colors.DIM))
    
    def validate_setting(self, setting_name: str, value: Any) -> tuple[bool, str]:
        """Validate a setting value with detailed error messages."""
        if not self._is_valid_setting_value(value):
            return False, "Invalid value type or content"
        
        # Specific validation rules
        if 'VOLUME' in setting_name and isinstance(value, (int, float)):
            if not (0.0 <= value <= 1.0):
                return False, "Volume must be between 0.0 and 1.0"
        
        elif 'FOV' in setting_name and isinstance(value, (int, float)):
            if not (30 <= value <= 180):
                return False, "FOV must be between 30 and 180 degrees"
        
        elif setting_name in ['MAX_SPEED', 'PLAYER_JUMP_HEIGHT'] and isinstance(value, (int, float)):
            if value <= 0:
                return False, "Value must be positive"
        
        elif 'RECOIL' in setting_name and isinstance(value, (int, float)):
            if value < 0:
                return False, "Recoil cannot be negative"
        
        elif setting_name.endswith('_ENABLED') and not isinstance(value, bool):
            return False, "Enable/disable settings must be boolean"
        
        return True, "Valid"
    
    def save_settings(self):
        """Save current settings back to config.py with backup and atomic operations."""
        try:
            config_path = Path(self.config_file)
            
            # Create backup
            backup_path = config_path.with_suffix('.py.backup')
            if config_path.exists():
                shutil.copy2(config_path, backup_path)
                print(Colors.colorize(f"📁 Backup created: {backup_path.name}", Colors.CYAN))
            
            # Read the original file to preserve structure and comments
            with open(self.config_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Update lines with new values
            updated_lines = []
            for line in lines:
                # Check if this line contains a setting we've modified
                match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.+?)(\s*#.*)?$', line.strip())
                if match:
                    key = match.group(1)
                    comment = match.group(3) or ''
                    
                    if key in self.settings:
                        value = self.settings[key]
                        # Format the value safely
                        if isinstance(value, str) and not value.startswith(('color.', 'Vec3(', 'window.')):
                            formatted_value = repr(value)  # Use repr for safe string formatting
                        else:
                            formatted_value = str(value)
                        
                        updated_lines.append(f"{key} = {formatted_value}{comment}\n")
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            # Atomic write operation
            temp_path = config_path.with_suffix('.py.tmp')
            try:
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.writelines(updated_lines)
                
                # Atomic move
                temp_path.replace(config_path)
                
                self.modified = False
                print(Colors.colorize("✅ Settings saved successfully!", Colors.GREEN))
                
            except Exception as e:
                # Cleanup temp file on error
                if temp_path.exists():
                    temp_path.unlink()
                raise e
            
        except PermissionError:
            print(Colors.colorize("❌ Permission denied writing config file!", Colors.RED))
        except Exception as e:
            print(Colors.colorize(f"❌ Error saving settings: {e}", Colors.RED))
        
        input(Colors.colorize("Press Enter to continue...", Colors.DIM))
    
    def apply_preset(self):
        """Apply a preset configuration."""
        presets = {
            '1': ('Realistic Shooting', {
                'RECOIL_VERTICAL': 4.0,
                'RECOIL_HORIZONTAL': 2.0,
                'RECOIL_RECOVERY_SPEED': 4.0,
                'MOUSE_SENSITIVITY': 30,
                'SFX_VOLUME': 1.0
            }),
            '2': ('Arcade Mode', {
                'MAX_SPEED': 12,
                'SPRINT_MULTIPLIER': 2.5,
                'DASH_FORCE': 80,
                'RECOIL_VERTICAL': 1.0,
                'FOV_DEFAULT': 100
            }),
            '3': ('Precision Challenge', {
                'MAX_SPEED': 4,
                'RECOIL_VERTICAL': 1.5,
                'MOUSE_SENSITIVITY': 25,
                'TARGET_SIZE': 0.3,
                'TIMER_DURATION': 120
            }),
            '4': ('Beginner Friendly', {
                'RECOIL_VERTICAL': 1.0,
                'RECOIL_HORIZONTAL': 0.3,
                'TARGET_SIZE': 0.8,
                'TIMER_DURATION': 90,
                'MAX_SPEED': 5
            })
        }
        
        print(Colors.colorize("🎮 Available Presets:", Colors.BRIGHT_WHITE))
        print()
        
        for key, (name, _) in presets.items():
            print(f"  {Colors.colorize(f'{key}.', Colors.BRIGHT_BLUE)} {Colors.colorize(name, Colors.GREEN)}")
        
        print(f"  {Colors.colorize('b.', Colors.BRIGHT_BLUE)} Back to main menu")
        print()
        
        choice = input(Colors.colorize("Select preset: ", Colors.BRIGHT_GREEN)).strip()
        
        if choice == 'b':
            return
        
        if choice in presets:
            name, settings = presets[choice]
            print(Colors.colorize(f"\n📥 Applying {name} preset...", Colors.CYAN))
            
            for setting, value in settings.items():
                if setting in self.settings:
                    self.settings[setting] = value
                    print(f"  {Colors.colorize(setting, Colors.WHITE)} = {Colors.colorize(str(value), Colors.CYAN)}")
            
            self.modified = True
            print(Colors.colorize(f"\n✅ {name} preset applied!", Colors.GREEN))
        else:
            print(Colors.colorize("❌ Invalid preset selection.", Colors.RED))
        
        input(Colors.colorize("Press Enter to continue...", Colors.DIM))
    
    def validate_all_settings(self):
        """Validate all current settings."""
        print(Colors.colorize("🔍 Validating all settings...", Colors.CYAN))
        print()
        
        issues = []
        warnings = []
        
        # Check critical settings
        for setting, value in self.settings.items():
            if 'VOLUME' in setting and isinstance(value, (int, float)):
                if not (0.0 <= value <= 1.0):
                    issues.append(f"{setting}: Volume must be between 0.0 and 1.0")
            elif setting == 'FOV_DEFAULT' and isinstance(value, (int, float)):
                if not (60 <= value <= 120):
                    warnings.append(f"{setting}: FOV outside recommended range (60-120)")
            elif 'RECOIL' in setting and isinstance(value, (int, float)):
                if value < 0:
                    issues.append(f"{setting}: Cannot be negative")
        
        # Display results
        if issues:
            print(Colors.colorize("❌ Issues Found:", Colors.RED))
            for issue in issues:
                print(f"  • {issue}")
            print()
        
        if warnings:
            print(Colors.colorize("⚠️  Warnings:", Colors.YELLOW))
            for warning in warnings:
                print(f"  • {warning}")
            print()
        
        if not issues and not warnings:
            print(Colors.colorize("✅ All settings are valid!", Colors.GREEN))
        
        input(Colors.colorize("Press Enter to continue...", Colors.DIM))
    
    def run(self):
        """Run the interactive settings editor."""
        while True:
            self.clear_screen()
            self.print_header()
            
            if self.current_category is None:
                self.print_main_menu()
                
                try:
                    choice = input(Colors.colorize("Select option: ", Colors.BRIGHT_GREEN)).strip().lower()
                    
                    if choice == 'q':
                        if self.modified:
                            save_choice = input(Colors.colorize("Save changes before quitting? (y/n): ", Colors.YELLOW)).strip().lower()
                            if save_choice == 'y':
                                self.save_settings()
                        print(Colors.colorize("👋 Goodbye!", Colors.BRIGHT_CYAN))
                        break
                    elif choice == 's':
                        self.save_settings()
                    elif choice == 'r':
                        self.load_settings()
                        self.modified = False
                        print(Colors.colorize("✅ Settings reloaded from file.", Colors.GREEN))
                        input(Colors.colorize("Press Enter to continue...", Colors.DIM))
                    elif choice == 'v':
                        self.validate_all_settings()
                    elif choice == 'p':
                        self.apply_preset()
                    elif choice.isdigit():
                        category_index = int(choice) - 1
                        categories = list(self.categories.keys())
                        if 0 <= category_index < len(categories):
                            self.current_category = categories[category_index]
                
                except (ValueError, KeyboardInterrupt):
                    continue
            
            else:
                # In category view
                self.print_category_menu(self.current_category)
                
                try:
                    choice = input(Colors.colorize("Select option: ", Colors.BRIGHT_GREEN)).strip().lower()
                    
                    if choice == 'b':
                        self.current_category = None
                    elif choice.isdigit():
                        setting_index = int(choice) - 1
                        settings_list = self.categories[self.current_category]
                        if 0 <= setting_index < len(settings_list):
                            setting_name = settings_list[setting_index]
                            self.edit_setting(setting_name)
                
                except (ValueError, KeyboardInterrupt):
                    continue

if __name__ == "__main__":
    try:
        editor = SettingsEditor()
        editor.run()
    except KeyboardInterrupt:
        print(Colors.colorize("\n\n👋 Editor closed by user.", Colors.BRIGHT_CYAN))
    except Exception as e:
        print(Colors.colorize(f"\n❌ Error: {e}", Colors.RED))
        sys.exit(1)