# FHIR R5 Parser - Build Instructions

This document provides comprehensive instructions for building the FHIR R5 Parser with C extensions on different platforms.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Dependencies](#system-dependencies)
3. [Python Environment Setup](#python-environment-setup)
4. [Building C Extensions](#building-c-extensions)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)
7. [Development Setup](#development-setup)
8. [Platform-Specific Notes](#platform-specific-notes)

## Prerequisites

### Required Software

- **Python**: 3.8 or higher
- **C Compiler**: GCC, Clang, or MSVC
- **pkg-config**: For library detection
- **cJSON library**: For high-performance JSON parsing
- **Git**: For version control (optional)

### Supported Platforms

- macOS (Intel and Apple Silicon)
- Linux (Ubuntu, Debian, CentOS, RHEL, Fedora)
- Windows (with appropriate C compiler)

## System Dependencies

### Automated Installation (Recommended)

The project includes an automated dependency installer:

```bash
# Make the script executable
chmod +x scripts/install_deps.sh

# Run the installer
./scripts/install_deps.sh
```

This script will:
- Detect your operating system
- Install the appropriate package manager dependencies
- Set up cJSON library and pkg-config

### Manual Installation

#### macOS

Using Homebrew:
```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cjson pkg-config

# Verify installation
pkg-config --modversion libcjson
```

Using MacPorts:
```bash
sudo port install cjson pkgconfig
```

#### Ubuntu/Debian

```bash
# Update package list
sudo apt-get update

# Install dependencies
sudo apt-get install -y libcjson-dev pkg-config build-essential python3-dev

# Verify installation
pkg-config --modversion libcjson
```

#### CentOS/RHEL 7/8

```bash
# Enable EPEL repository
sudo yum install -y epel-release

# Install dependencies
sudo yum install -y cjson-devel pkgconfig gcc python3-devel

# For RHEL 8, use dnf instead of yum
sudo dnf install -y cjson-devel pkgconfig gcc python3-devel
```

#### Fedora

```bash
# Install dependencies
sudo dnf install -y cjson-devel pkgconfig gcc python3-devel

# Verify installation
pkg-config --modversion libcjson
```

#### Windows

Using vcpkg:
```cmd
# Install vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# Install cJSON
.\vcpkg install cjson

# Set environment variables
set VCPKG_ROOT=C:\path\to\vcpkg
```

## Python Environment Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Upgrade pip and setuptools

```bash
# Upgrade to latest versions
pip install --upgrade pip setuptools wheel
```

### 3. Install Python Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## Building C Extensions

### Method 1: Using setup.py (Recommended)

```bash
# Build C extensions in-place
python setup.py build_ext --inplace

# Verify build
python -c "import fhir_parser_c, fhir_datatypes_c; print('C extensions loaded successfully')"
```

### Method 2: Using pip install

```bash
# Install in development mode with C extensions
pip install -e .
```

### Method 3: Using Makefile

```bash
# Build everything
make build

# Or use the complete setup target
make setup
```

### Build Configuration

The build system automatically detects cJSON library paths using pkg-config. If you need to specify custom paths:

```bash
# Set custom include and library paths
export CFLAGS="-I/custom/include/path"
export LDFLAGS="-L/custom/lib/path"

# Then build
python setup.py build_ext --inplace
```

### Build Options

You can customize the build with environment variables:

```bash
# Enable debug symbols
export CFLAGS="-g -O0"

# Enable optimization (default)
export CFLAGS="-O3"

# Enable verbose compilation
python setup.py build_ext --inplace --verbose
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_fhir_parser.py
pytest tests/test_fast_parser.py
pytest tests/test_datatypes.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### Test Categories

1. **Basic Parser Tests**: `tests/test_fhir_parser.py`
2. **Fast Parser Tests**: `tests/test_fast_parser.py`
3. **Data Types Tests**: `tests/test_datatypes.py`
4. **Main Module Tests**: `tests/test_main.py`

### Performance Testing

```bash
# Run performance benchmarks
make benchmark

# Or manually
python -m pytest tests/test_fast_parser.py::TestFastFHIRParser::test_performance_info -v
```

## Troubleshooting

### Common Issues

#### 1. cJSON Library Not Found

**Error**: `fatal error: cjson/cJSON.h: No such file or directory`

**Solutions**:
```bash
# Verify cJSON installation
pkg-config --modversion libcjson

# If not found, reinstall cJSON
# macOS:
brew reinstall cjson

# Ubuntu/Debian:
sudo apt-get install --reinstall libcjson-dev

# Check pkg-config path
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"
```

#### 2. pkg-config Not Found

**Error**: `pkg-config not found`

**Solutions**:
```bash
# macOS:
brew install pkg-config

# Ubuntu/Debian:
sudo apt-get install pkg-config

# CentOS/RHEL:
sudo yum install pkgconfig
```

#### 3. Python.h Not Found

**Error**: `fatal error: Python.h: No such file or directory`

**Solutions**:
```bash
# Ubuntu/Debian:
sudo apt-get install python3-dev

# CentOS/RHEL:
sudo yum install python3-devel

# macOS (usually not needed with Homebrew Python):
xcode-select --install
```

#### 4. Compilation Errors on macOS

**Error**: `clang: error: unsupported option '-fopenmp'`

**Solutions**:
```bash
# Install proper compiler
brew install llvm

# Or use GCC
brew install gcc
export CC=gcc-11
```

#### 5. Windows Build Issues

**Error**: `Microsoft Visual C++ 14.0 is required`

**Solutions**:
- Install Visual Studio Build Tools
- Or install Visual Studio Community
- Set environment variables properly

### Debug Build

For debugging C extensions:

```bash
# Build with debug symbols
export CFLAGS="-g -O0 -DDEBUG"
python setup.py build_ext --inplace --debug

# Use gdb for debugging (Linux/macOS)
gdb python
(gdb) run -c "import fhir_datatypes_c; fhir_datatypes_c.create_string('test')"
```

### Fallback Mode

If C extensions fail to build, the library will automatically fall back to pure Python:

```python
from src.fhir.datatypes import HAS_C_DATATYPES
print(f"C extensions available: {HAS_C_DATATYPES}")
```

## Development Setup

### Complete Development Environment

```bash
# Clone repository
git clone <repository-url>
cd fhir-r5-parser

# Run complete setup
make setup

# Verify installation
python src/main.py
```

### Development Workflow

```bash
# Make changes to C code
vim src/fhir/ext/fhir_datatypes.c

# Rebuild extensions
make build

# Run tests
make test

# Clean build artifacts
make clean
```

### Code Quality Checks

```bash
# Run code formatting
black src/ tests/

# Run linting
flake8 src/ tests/

# Run all quality checks
make check
```

## Platform-Specific Notes

### macOS Apple Silicon (M1/M2)

```bash
# Ensure Homebrew is installed for ARM64
/opt/homebrew/bin/brew install cjson pkg-config

# Set proper paths
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:$PKG_CONFIG_PATH"
export CFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
```

### Ubuntu 20.04 LTS

```bash
# Install specific versions
sudo apt-get install libcjson1 libcjson-dev=1.7.14-1

# If you encounter version conflicts
sudo apt-get install --fix-broken
```

### CentOS 7 (Older Systems)

```bash
# Enable Software Collections for newer GCC
sudo yum install centos-release-scl
sudo yum install devtoolset-9-gcc devtoolset-9-gcc-c++

# Activate newer compiler
scl enable devtoolset-9 bash

# Then build normally
python setup.py build_ext --inplace
```

### Docker Build

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcjson-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and build
COPY . /app
WORKDIR /app
RUN pip install -r requirements-dev.txt
RUN python setup.py build_ext --inplace

# Test
RUN pytest
```

## Performance Verification

After successful build, verify performance improvements:

```python
from src.fhir.fast_parser import FastFHIRParser
from src.fhir.datatypes import HAS_C_DATATYPES

parser = FastFHIRParser()
info = parser.get_performance_info()

print(f"C extensions available: {info['c_extensions_available']}")
print(f"C extensions enabled: {info['c_extensions_enabled']}")
print(f"Available features: {info['features']}")
```

Expected output with successful C extension build:
```
C extensions available: True
C extensions enabled: True
Available features: ['fast_json_validation', 'fast_resource_type_extraction', 'fast_bundle_entry_counting', 'fast_field_extraction']
```

## Getting Help

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify your system meets all [Prerequisites](#prerequisites)
3. Try the automated installer: `./scripts/install_deps.sh`
4. Check that pkg-config can find cJSON: `pkg-config --modversion libcjson`
5. Build with verbose output: `python setup.py build_ext --inplace --verbose`

The library is designed to work with or without C extensions, so even if the build fails, you can still use the pure Python implementation.