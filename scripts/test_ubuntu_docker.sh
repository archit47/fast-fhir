#!/bin/bash

# Test Fast-FHIR on different Ubuntu versions using Docker

echo "🐳 Fast-FHIR Ubuntu Docker Test"
echo "================================"

# Ubuntu versions to test
UBUNTU_VERSIONS=("20.04" "22.04" "latest")
PYTHON_VERSIONS=("3.9" "3.10" "3.11" "3.12")

# Function to test on specific Ubuntu version
test_ubuntu_version() {
    local ubuntu_version=$1
    local python_version=$2
    
    echo ""
    echo "🧪 Testing Ubuntu $ubuntu_version with Python $python_version"
    echo "-----------------------------------------------------------"
    
    # Create Dockerfile for this test
    cat > Dockerfile.test << EOF
FROM ubuntu:$ubuntu_version

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    python$python_version \\
    python$python_version-dev \\
    python$python_version-pip \\
    libcjson-dev \\
    build-essential \\
    pkg-config \\
    git

# Set Python as default
RUN ln -sf /usr/bin/python$python_version /usr/bin/python
RUN ln -sf /usr/bin/pip$python_version /usr/bin/pip

# Copy project files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel pkgconfig

# Test the build
RUN python scripts/test_ubuntu.py

# Test package import
RUN PYTHONPATH=src python -c "import fast_fhir; print('✅ Package works on Ubuntu $ubuntu_version with Python $python_version')"
EOF

    # Build and run the test
    if docker build -f Dockerfile.test -t fast-fhir-test:ubuntu$ubuntu_version-py$python_version . > /dev/null 2>&1; then
        if docker run --rm fast-fhir-test:ubuntu$ubuntu_version-py$python_version > /dev/null 2>&1; then
            echo "✅ Ubuntu $ubuntu_version + Python $python_version: SUCCESS"
        else
            echo "❌ Ubuntu $ubuntu_version + Python $python_version: FAILED"
        fi
    else
        echo "💥 Ubuntu $ubuntu_version + Python $python_version: BUILD FAILED"
    fi
    
    # Clean up
    rm -f Dockerfile.test
    docker rmi fast-fhir-test:ubuntu$ubuntu_version-py$python_version > /dev/null 2>&1 || true
}

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker to run Ubuntu tests."
    echo "💡 Alternative: Use GitHub Actions or a Ubuntu VM/container"
    exit 1
fi

echo "🔍 Testing Fast-FHIR compatibility across Ubuntu versions..."
echo "This may take several minutes..."

# Test combinations
for ubuntu_version in "${UBUNTU_VERSIONS[@]}"; do
    for python_version in "${PYTHON_VERSIONS[@]}"; do
        # Skip Python 3.8 on newer Ubuntu (not available by default)
        if [[ "$ubuntu_version" == "22.04" || "$ubuntu_version" == "latest" ]] && [[ "$python_version" == "3.8" ]]; then
            echo "⏭️ Skipping Ubuntu $ubuntu_version + Python $python_version (not available)"
            continue
        fi
        
        test_ubuntu_version "$ubuntu_version" "$python_version"
    done
done

echo ""
echo "📋 Ubuntu Docker Test Summary:"
echo "✅ Tests completed - check results above"
echo "💡 For detailed logs, run individual tests manually"
echo ""
echo "🚀 To run a specific test:"
echo "   ./scripts/test_ubuntu_docker.sh 20.04 3.9"