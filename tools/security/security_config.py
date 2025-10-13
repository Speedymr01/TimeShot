#!/usr/bin/env python3
"""
Security Configuration
======================

Security settings and validation rules for the game configuration system.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

class SecurityConfig:
    """Security configuration and validation rules."""
    
    # File size limits
    MAX_CONFIG_FILE_SIZE = 1024 * 1024  # 1MB
    MAX_ASSET_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    
    # Input limits
    MAX_INPUT_LENGTH = 1000
    MAX_SETTING_NAME_LENGTH = 50
    
    # Allowed file extensions
    ALLOWED_SCRIPT_EXTENSIONS = {'.py'}
    ALLOWED_AUDIO_EXTENSIONS = {'.mp3', '.wav', '.ogg'}
    ALLOWED_MODEL_EXTENSIONS = {'.obj', '.fbx', '.blend'}
    ALLOWED_TEXTURE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}
    
    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        'import',
        'exec',
        'eval',
        '__import__',
        'subprocess',
        'os.system',
        'open(',
        'file(',
        'input(',
        'raw_input',
        'compile',
        'globals',
        'locals',
        'vars',
        'dir(',
        'getattr',
        'setattr',
        'delattr',
        'hasattr',
    ]
    
    # Allowed setting types
    ALLOWED_SETTING_TYPES = (bool, int, float, str)
    
    # Numeric value ranges
    NUMERIC_RANGES = {
        'volume': (0.0, 1.0),
        'fov': (30, 180),
        'speed': (0.1, 100.0),
        'recoil': (0.0, 50.0),
        'timer': (1, 3600),  # 1 second to 1 hour
        'sensitivity': (1, 200),
    }
    
    @staticmethod
    def validate_file_path(file_path: str, allowed_extensions: set = None) -> Tuple[bool, str]:
        """Validate file path for security."""
        try:
            path = Path(file_path).resolve()
            current_dir = Path.cwd()
            
            # Prevent path traversal
            if not str(path).startswith(str(current_dir)):
                return False, "Path outside project directory"
            
            # Check extension if specified
            if allowed_extensions and path.suffix.lower() not in allowed_extensions:
                return False, f"Invalid file extension. Allowed: {allowed_extensions}"
            
            # Check if path contains dangerous patterns
            path_str = str(path).lower()
            for pattern in SecurityConfig.DANGEROUS_PATTERNS:
                if pattern in path_str:
                    return False, f"Path contains dangerous pattern: {pattern}"
            
            return True, "Valid"
            
        except Exception as e:
            return False, f"Path validation error: {e}"
    
    @staticmethod
    def validate_setting_name(name: str) -> Tuple[bool, str]:
        """Validate setting name."""
        if not isinstance(name, str):
            return False, "Setting name must be string"
        
        if len(name) > SecurityConfig.MAX_SETTING_NAME_LENGTH:
            return False, f"Setting name too long (max {SecurityConfig.MAX_SETTING_NAME_LENGTH})"
        
        if not re.match(r'^[A-Z_][A-Z0-9_]*$', name):
            return False, "Setting name must be uppercase with underscores only"
        
        return True, "Valid"
    
    @staticmethod
    def validate_setting_value(value: Any, setting_name: str = "") -> Tuple[bool, str]:
        """Validate setting value."""
        # Check type
        if not isinstance(value, SecurityConfig.ALLOWED_SETTING_TYPES):
            return False, f"Invalid type. Allowed: {SecurityConfig.ALLOWED_SETTING_TYPES}"
        
        # String validation
        if isinstance(value, str):
            if len(value) > SecurityConfig.MAX_INPUT_LENGTH:
                return False, f"String too long (max {SecurityConfig.MAX_INPUT_LENGTH})"
            
            # Check for dangerous patterns
            value_lower = value.lower()
            for pattern in SecurityConfig.DANGEROUS_PATTERNS:
                if pattern in value_lower:
                    return False, f"String contains dangerous pattern: {pattern}"
        
        # Numeric validation
        if isinstance(value, (int, float)):
            if not (-1000000 <= value <= 1000000):
                return False, "Numeric value out of reasonable range"
            
            # Specific range validation
            setting_lower = setting_name.lower()
            for range_key, (min_val, max_val) in SecurityConfig.NUMERIC_RANGES.items():
                if range_key in setting_lower:
                    if not (min_val <= value <= max_val):
                        return False, f"Value must be between {min_val} and {max_val}"
        
        return True, "Valid"
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Sanitize user input."""
        if not isinstance(user_input, str):
            return ""
        
        # Limit length
        sanitized = user_input[:SecurityConfig.MAX_INPUT_LENGTH]
        
        # Remove null bytes and control characters
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')
        
        # Strip whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    @staticmethod
    def is_safe_for_eval(value_str: str) -> bool:
        """Check if string is safe for evaluation."""
        # Only allow simple literals
        safe_patterns = [
            r'^\d+$',  # Integer
            r'^\d+\.\d+$',  # Float
            r'^True$|^False$',  # Boolean
            r'^None$',  # None
            r'^["\'][^"\']*["\']$',  # Simple string
        ]
        
        return any(re.match(pattern, value_str.strip()) for pattern in safe_patterns)

# Security logging
class SecurityLogger:
    """Simple security event logger."""
    
    @staticmethod
    def log_security_event(event_type: str, details: str, severity: str = "INFO"):
        """Log security events."""
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] SECURITY-{severity}: {event_type} - {details}"
        
        # In a real application, this would go to a proper log file
        print(log_entry)
        
        # Could also write to file
        try:
            with open('security.log', 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception:
            pass  # Don't fail if logging fails

# Rate limiting
class RateLimiter:
    """Simple rate limiter for operations."""
    
    def __init__(self, max_operations: int = 100, time_window: int = 60):
        self.max_operations = max_operations
        self.time_window = time_window
        self.operations = []
    
    def is_allowed(self) -> bool:
        """Check if operation is allowed under rate limit."""
        import time
        current_time = time.time()
        
        # Remove old operations outside time window
        self.operations = [op_time for op_time in self.operations 
                          if current_time - op_time < self.time_window]
        
        # Check if under limit
        if len(self.operations) < self.max_operations:
            self.operations.append(current_time)
            return True
        
        return False

# Global instances
security_config = SecurityConfig()
security_logger = SecurityLogger()
rate_limiter = RateLimiter()