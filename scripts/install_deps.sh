#!/bin/bash

# Install dependencies for FHIR parser C extensions

echo "Installing FHIR Parser C extension dependencies..."

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS"
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first:"
        echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    # Install cJSON library
    echo "Installing cJSON via Homebrew..."
    brew install cjson
    
    # Install pkg-config if not present
    if ! command -v pkg-config &> /dev/null; then
        echo "Installing pkg-config..."
        brew install pkg-config
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux"
    
    # Detect package manager
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        echo "Installing cJSON via apt..."
        sudo apt-get update
        sudo apt-get install -y libcjson-dev pkg-config
        
    elif command -v yum &> /dev/null; then
        # RHEL/CentOS
        echo "Installing cJSON via yum..."
        sudo yum install -y cjson-devel pkgconfig
        
    elif command -v dnf &> /dev/null; then
        # Fedora
        echo "Installing cJSON via dnf..."
        sudo dnf install -y cjson-devel pkgconfig
        
    else
        echo "Unsupported Linux distribution. Please install libcjson-dev and pkg-config manually."
        exit 1
    fi
    
else
    echo "Unsupported operating system: $OSTYPE"
    echo "Please install cJSON library and pkg-config manually."
    exit 1
fi

echo "Dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Create virtual environment: python -m venv venv"
echo "2. Activate it: source venv/bin/activate"
echo "3. Install Python dependencies: pip install -r requirements-dev.txt"
echo "4. Build C extensions: python setup.py build_ext --inplace"
echo "5. Run tests: pytest"