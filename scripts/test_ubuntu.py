#!/usr/bin/env python3
"""
Test script specifically for Ubuntu compatibility issues.
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description, critical=True):
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"Output: {result.stdout[:300]}...")
            return True
        else:
            status = "❌" if critical else "⚠️"
            print(f"{status} {description} - {'FAILED' if critical else 'WARNING'}")
            if result.stderr.strip():
                print(f"Error: {result.stderr[:300]}...")
            return not critical
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - EXCEPTION: {e}")
        return False

def check_ubuntu_system():
    """Check Ubuntu system information and dependencies."""
    print("🐧 Ubuntu System Check")
    print("=" * 30)
    
    if platform.system() != "Linux":
        print("⚠️ Not running on Linux - Ubuntu-specific tests may not apply")
        return True
    
    # Check Ubuntu version
    run_command("lsb_release -a", "Ubuntu version info", critical=False)
    
    # Check architecture
    run_command("uname -a", "System architecture", critical=False)
    
    # Check GCC
    if not run_command("gcc --version", "GCC compiler"):
        print("💡 Install with: sudo apt-get install build-essential")
        return False
    
    # Check pkg-config
    if not run_command("pkg-config --version", "pkg-config"):
        print("💡 Install with: sudo apt-get install pkg-config")
        return False
    
    # Check Python development headers
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if not run_command(f"python{python_version}-config --includes", "Python dev headers", critical=False):
        print(f"💡 Install with: sudo apt-get install python{python_version}-dev")
    
    return True

def check_cjson_ubuntu():
    """Check cJSON library on Ubuntu."""
    print("\n📚 cJSON Library Check")
    print("=" * 25)
    
    # Check if libcjson-dev is installed
    cjson_found = run_command("pkg-config --exists libcjson", "cJSON pkg-config", critical=False)
    
    if cjson_found:
        run_command("pkg-config --modversion libcjson", "cJSON version", critical=False)
        run_command("pkg-config --cflags libcjson", "cJSON compile flags", critical=False)
        run_command("pkg-config --libs libcjson", "cJSON link flags", critical=False)
    else:
        print("💡 Install cJSON with: sudo apt-get install libcjson-dev")
        
        # Check if we can find cJSON manually
        manual_paths = [
            "/usr/include/cjson/cJSON.h",
            "/usr/local/include/cjson/cJSON.h",
            "/usr/include/cJSON.h"
        ]
        
        for path in manual_paths:
            if os.path.exists(path):
                print(f"✅ Found cJSON header at: {path}")
                cjson_found = True
                break
    
    return cjson_found

def test_ubuntu_build():
    """Test building on Ubuntu."""
    print("\n🏗️ Ubuntu Build Test")
    print("=" * 20)
    
    # Clean previous builds
    run_command("rm -rf build/ *.so", "Cleaning previous builds")
    
    # Test Python package installation
    python_cmd = sys.executable
    
    # Install required packages
    if not run_command(f"{python_cmd} -m pip install setuptools wheel pkgconfig", "Installing build dependencies"):
        return False
    
    # Test configuration
    if not run_command(f"{python_cmd} scripts/test_config.py", "Testing configuration"):
        return False
    
    # Try building C extensions
    build_success = run_command(f"{python_cmd} setup.py build_ext --inplace", "Building C extensions", critical=False)
    
    # Test package import
    import_success = run_command(
        f"PYTHONPATH=src {python_cmd} -c \"import fast_fhir; print('Package imported successfully')\"",
        "Testing package import"
    )
    
    if build_success:
        print("🎉 C extensions built successfully on Ubuntu!")
    else:
        print("⚠️ C extensions failed to build, but package works in Python-only mode")
    
    return import_success

def main():
    """Main test function."""
    print("🧪 Fast-FHIR Ubuntu Compatibility Test")
    print("=" * 40)
    
    if not os.path.exists("setup.py"):
        print("❌ Error: setup.py not found. Run this from the project root.")
        sys.exit(1)
    
    success = True
    
    # Run all checks
    success &= check_ubuntu_system()
    success &= check_cjson_ubuntu()
    success &= test_ubuntu_build()
    
    print("\n📋 Ubuntu Test Summary:")
    if success:
        print("✅ Ubuntu compatibility test passed!")
        print("💡 Package should work on Ubuntu in GitHub Actions")
    else:
        print("❌ Ubuntu compatibility issues found")
        print("💡 Check the errors above and install missing dependencies")
    
    print(f"\n🐍 Tested with Python {sys.version}")
    print(f"🐧 Platform: {platform.platform()}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())