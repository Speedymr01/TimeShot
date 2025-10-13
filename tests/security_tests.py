#!/usr/bin/env python3
"""
Security Test Suite
===================

Comprehensive security tests for the game configuration system.
"""

import unittest
import tempfile
import os
from pathlib import Path
from security_config import SecurityConfig, SecurityLogger, RateLimiter

class TestSecurityConfig(unittest.TestCase):
    """Test security configuration validation."""
    
    def setUp(self):
        self.security = SecurityConfig()
    
    def test_validate_file_path_safe(self):
        """Test safe file path validation."""
        # Create a temporary file in current directory
        current_dir = Path.cwd()
        test_file = current_dir / 'test_config.py'
        
        # Create the test file
        test_file.write_text('# Test config file')
        
        try:
            is_valid, message = self.security.validate_file_path(str(test_file), {'.py'})
            self.assertTrue(is_valid, f"Safe path should be valid: {message}")
        finally:
            if test_file.exists():
                test_file.unlink()
    
    def test_validate_file_path_traversal(self):
        """Test path traversal prevention."""
        dangerous_paths = [
            '../../../etc/passwd',
            '..\\..\\windows\\system32\\config\\sam',
            '/etc/shadow',
            'C:\\Windows\\System32\\config\\SAM'
        ]
        
        for path in dangerous_paths:
            is_valid, message = self.security.validate_file_path(path)
            self.assertFalse(is_valid, f"Dangerous path should be invalid: {path}")
    
    def test_validate_setting_name_valid(self):
        """Test valid setting names."""
        valid_names = [
            'MAX_SPEED',
            'PLAYER_JUMP_HEIGHT',
            'FOV_DEFAULT',
            'RECOIL_ENABLED'
        ]
        
        for name in valid_names:
            is_valid, message = self.security.validate_setting_name(name)
            self.assertTrue(is_valid, f"Valid name should pass: {name} - {message}")
    
    def test_validate_setting_name_invalid(self):
        """Test invalid setting names."""
        invalid_names = [
            'lowercase',
            '123_INVALID',
            'INVALID-NAME',
            'INVALID NAME',
            '__import__',
            'A' * 100  # Too long
        ]
        
        for name in invalid_names:
            is_valid, message = self.security.validate_setting_name(name)
            self.assertFalse(is_valid, f"Invalid name should fail: {name}")
    
    def test_validate_setting_value_safe(self):
        """Test safe setting values."""
        safe_values = [
            (True, "ENABLED"),
            (False, "DISABLED"),
            (42, "MAX_SPEED"),
            (3.14, "RECOIL_VERTICAL"),
            ("safe_string", "TEXTURE_PATH"),
            (0.5, "MASTER_VOLUME")
        ]
        
        for value, setting in safe_values:
            is_valid, message = self.security.validate_setting_value(value, setting)
            self.assertTrue(is_valid, f"Safe value should pass: {value} - {message}")
    
    def test_validate_setting_value_dangerous(self):
        """Test dangerous setting values."""
        dangerous_values = [
            ("__import__('os').system('rm -rf /')", "MALICIOUS"),
            ("exec('print(1)')", "MALICIOUS"),
            ("eval('1+1')", "MALICIOUS"),
            ("import subprocess", "MALICIOUS"),
            ("A" * 2000, "TOO_LONG"),  # Too long string
            (float('inf'), "INFINITE"),
            (-999999999, "TOO_NEGATIVE")
        ]
        
        for value, setting in dangerous_values:
            is_valid, message = self.security.validate_setting_value(value, setting)
            self.assertFalse(is_valid, f"Dangerous value should fail: {value}")
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        test_cases = [
            ("normal input", "normal input"),
            ("  whitespace  ", "whitespace"),
            ("with\x00null\x01bytes", "withnullbytes"),
            ("A" * 2000, "A" * 1000),  # Truncated
        ]
        
        for input_val, expected in test_cases:
            result = self.security.sanitize_input(input_val)
            self.assertEqual(result, expected, f"Sanitization failed for: {input_val}")
    
    def test_is_safe_for_eval(self):
        """Test eval safety check."""
        safe_strings = [
            "42",
            "3.14",
            "True",
            "False",
            "None",
            "'simple string'",
            '"another string"'
        ]
        
        dangerous_strings = [
            "__import__('os')",
            "exec('code')",
            "eval('1+1')",
            "open('/etc/passwd')",
            "subprocess.run(['ls'])"
        ]
        
        for safe_str in safe_strings:
            self.assertTrue(self.security.is_safe_for_eval(safe_str), 
                          f"Safe string should pass: {safe_str}")
        
        for dangerous_str in dangerous_strings:
            self.assertFalse(self.security.is_safe_for_eval(dangerous_str), 
                           f"Dangerous string should fail: {dangerous_str}")

class TestRateLimiter(unittest.TestCase):
    """Test rate limiting functionality."""
    
    def test_rate_limiting(self):
        """Test basic rate limiting."""
        limiter = RateLimiter(max_operations=3, time_window=60)
        
        # First 3 operations should be allowed
        for i in range(3):
            self.assertTrue(limiter.is_allowed(), f"Operation {i+1} should be allowed")
        
        # 4th operation should be blocked
        self.assertFalse(limiter.is_allowed(), "4th operation should be blocked")

class TestSecurityIntegration(unittest.TestCase):
    """Integration tests for security features."""
    
    def test_config_file_validation(self):
        """Test complete config file validation."""
        # Create a test config with both safe and dangerous content
        test_config = '''
# Safe settings
MAX_SPEED = 10
RECOIL_ENABLED = True
MASTER_VOLUME = 0.8

# Dangerous settings (should be filtered out)
MALICIOUS = __import__('os').system('echo pwned')
EVAL_DANGER = eval('1+1')
'''
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(test_config)
            tmp_path = tmp.name
        
        try:
            # Test that our security system would catch these
            security = SecurityConfig()
            
            # Test malicious setting name
            is_valid, _ = security.validate_setting_name('MALICIOUS')
            self.assertTrue(is_valid, "Setting name itself is valid format")
            
            # Test malicious setting value
            is_valid, _ = security.validate_setting_value("__import__('os').system('echo pwned')")
            self.assertFalse(is_valid, "Malicious value should be rejected")
            
        finally:
            os.unlink(tmp_path)

def run_security_tests():
    """Run all security tests."""
    print("🔒 Running Security Test Suite...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimiter))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All security tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} error(s) occurred")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_security_tests()
    exit(0 if success else 1)