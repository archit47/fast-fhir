#!/usr/bin/env python3
"""
Script to help publish fast-fhir to PyPI.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {description} failed")
        print(f"Command: {cmd}")
        print(f"Error: {result.stderr}")
        return False
    
    print(f"✅ {description} completed successfully")
    if result.stdout.strip():
        print(result.stdout)
    return True

def main():
    """Main publishing workflow."""
    print("🚀 Fast-FHIR PyPI Publishing Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("pyproject.toml"):
        print("❌ Error: pyproject.toml not found. Run this from the project root.")
        sys.exit(1)
    
    # Clean previous builds
    if not run_command("rm -rf dist/ build/ *.egg-info/", "Cleaning previous builds"):
        sys.exit(1)
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        print("\n💡 Tip: Install build tools with: pip install build")
        sys.exit(1)
    
    # Check the package
    if not run_command("python -m twine check dist/*", "Checking package"):
        print("\n💡 Tip: Install twine with: pip install twine")
        sys.exit(1)
    
    # Ask for confirmation before uploading
    print("\n📦 Package built successfully!")
    print("Files in dist/:")
    subprocess.run("ls -la dist/", shell=True)
    
    choice = input("\n🤔 Upload to PyPI? (y/N): ").lower().strip()
    
    if choice == 'y':
        # Upload to PyPI
        if not run_command("python -m twine upload dist/*", "Uploading to PyPI"):
            print("\n💡 Tip: Make sure you have PyPI credentials configured")
            print("   - Create account at https://pypi.org/account/register/")
            print("   - Configure credentials with: twine configure")
            sys.exit(1)
        
        print("\n🎉 Package successfully published to PyPI!")
        print("📋 Next steps:")
        print("   - Test installation: pip install fast-fhir")
        print("   - Check PyPI page: https://pypi.org/project/fast-fhir/")
    else:
        print("\n📋 To upload later, run: python -m twine upload dist/*")
        print("💡 To test locally: pip install dist/fast_fhir-*.whl")

if __name__ == "__main__":
    main()