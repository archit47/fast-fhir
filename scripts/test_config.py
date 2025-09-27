#!/usr/bin/env python3
"""Test the pyproject.toml configuration."""

import subprocess
import sys

def test_config():
    """Test if the configuration is valid."""
    print("Testing pyproject.toml configuration...")
    
    try:
        # Test if setup.py can be parsed without errors
        result = subprocess.run([
            sys.executable, "setup.py", "--help-commands"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("SUCCESS: setup.py configuration is valid")
            return True
        else:
            print("ERROR: setup.py configuration failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"ERROR: Error testing configuration: {e}")
        return False

if __name__ == "__main__":
    success = test_config()
    sys.exit(0 if success else 1)