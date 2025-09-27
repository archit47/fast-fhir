#!/usr/bin/env python3
"""
Test script to verify license configuration works with Python 3.12+
"""

import subprocess
import sys
import tempfile
import os

def test_license_config():
    """Test if the license configuration works without errors."""
    print("Testing License Configuration Compatibility")
    print("=" * 45)
    
    print(f"Python version: {sys.version}")
    
    # Test setup.py parsing
    print("\n🔄 Testing setup.py configuration...")
    try:
        result = subprocess.run([
            sys.executable, "setup.py", "--help-commands"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("SUCCESS: setup.py configuration valid")
            
            # Check for license-related errors in stderr
            if "license" in result.stderr.lower() and "error" in result.stderr.lower():
                print("WARNING: License warnings found:")
                print(result.stderr[:500])
                return False
            else:
                print("SUCCESS: No license configuration errors")
                return True
        else:
            print("ERROR: setup.py configuration failed:")
            print(result.stderr[:500])
            return False
            
    except Exception as e:
        print(f"ERROR: Error testing setup.py: {e}")
        return False

def test_build_metadata():
    """Test if we can extract build metadata without errors."""
    print("\n🔄 Testing build metadata extraction...")
    
    try:
        # Try to get package metadata
        result = subprocess.run([
            sys.executable, "-c", 
            "import setuptools; from setuptools import setup; "
            "import sys; sys.argv = ['setup.py', '--name']; "
            "exec(open('setup.py').read())"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("SUCCESS: Build metadata extraction successful")
            return True
        else:
            print("ERROR: Build metadata extraction failed:")
            print(result.stderr[:300])
            return False
            
    except Exception as e:
        print(f"ERROR: Error testing metadata: {e}")
        return False

def main():
    """Main test function."""
    if not os.path.exists("setup.py"):
        print("ERROR: setup.py not found. Run this from the project root.")
        sys.exit(1)
    
    success = True
    success &= test_license_config()
    success &= test_build_metadata()
    
    print("\nLicense Configuration Test Summary:")
    if success:
        print("SUCCESS: License configuration is compatible!")
        print("Should work with Python 3.12+ in GitHub Actions")
    else:
        print("ERROR: License configuration issues found")
        print("Check the errors above and update configuration")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())