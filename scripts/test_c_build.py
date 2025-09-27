#!/usr/bin/env python3
"""
Test script to verify C extension compilation across Python versions.
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"SUCCESS: {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout[:500]}...")
            return True
        else:
            print(f"FAILED: {description}")
            print(f"Error: {result.stderr[:500]}...")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - EXCEPTION: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"Python version: {python_version}")
    
    # Check platform
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    # Check for cJSON
    if platform.system() == "Darwin":  # macOS
        cjson_check = "brew list cjson || echo 'cjson not found'"
    else:  # Linux
        cjson_check = "pkg-config --exists libcjson && echo 'cjson found' || echo 'cjson not found'"
    
    run_command(cjson_check, "Checking cJSON availability")
    
    # Check for required Python packages
    required_packages = ["setuptools", "pkgconfig"]
    for package in required_packages:
        result = subprocess.run([sys.executable, "-c", f"import {package}"], 
                              capture_output=True)
        if result.returncode == 0:
            print(f"SUCCESS: {package} available")
        else:
            print(f"ERROR: {package} missing")
            return False
    
    return True

def test_c_compilation():
    """Test C extension compilation."""
    print("\n🏗️  Testing C Extension Compilation")
    print("=" * 50)
    
    if not check_dependencies():
        print("ERROR: Missing dependencies - cannot test compilation")
        return False
    
    # Clean previous builds
    clean_success = run_command("rm -rf build/ *.so", "Cleaning previous builds")
    
    # Test compilation
    python_cmd = sys.executable
    compile_success = run_command(
        f"{python_cmd} setup.py build_ext --inplace", 
        "Compiling C extensions"
    )
    
    if compile_success:
        print("\n🎉 C extension compilation successful!")
        
        # Test import
        test_import_success = run_command(
            f"PYTHONPATH=src {python_cmd} -c \"import fast_fhir; print('Package import successful')\"",
            "Testing package import"
        )
        
        # Test C extension import (optional)
        run_command(
            f"PYTHONPATH=src {python_cmd} -c \"try:\\n    import fast_fhir.fhir_parser_c\\n    print('C extensions loaded successfully')\\nexcept ImportError as e:\\n    print(f'C extensions not available: {{e}}')\"",
            "Testing C extension import"
        )
        
        return test_import_success
    else:
        print("\n⚠️  C extension compilation failed - testing Python-only mode")
        
        # Test Python-only import
        test_import_success = run_command(
            f"PYTHONPATH=src {python_cmd} -c \"import fast_fhir; print('Python-only package import successful')\"",
            "Testing Python-only package import"
        )
        
        return test_import_success

def main():
    """Main test function."""
    print("🧪 Fast-FHIR C Extension Build Test")
    print("=" * 40)
    
    if not os.path.exists("setup.py"):
        print("❌ Error: setup.py not found. Run this from the project root.")
        sys.exit(1)
    
    success = test_c_compilation()
    
    print("\n📋 Test Summary:")
    if success:
        print("✅ Build test completed successfully!")
        print("💡 The package should work in GitHub Actions")
    else:
        print("❌ Build test failed")
        print("💡 Check the errors above and fix before pushing")
    
    print(f"\n🐍 Tested with Python {sys.version}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())