# Makefile for FHIR R5 Parser with C extensions

.PHONY: help install deps build test clean dev-install

help:
	@echo "Available targets:"
	@echo "  deps        - Install system dependencies (cJSON, pkg-config)"
	@echo "  install     - Install Python dependencies"
	@echo "  build       - Build C extensions"
	@echo "  dev-install - Install in development mode with C extensions"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean build artifacts"
	@echo "  benchmark   - Run performance benchmarks"

deps:
	@echo "Installing system dependencies..."
	./scripts/install_deps.sh

install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

build:
	@echo "Building C extensions..."
	python3 setup.py build_ext --inplace

dev-install: install build
	@echo "Installing in development mode..."
	pip install -e .

test:
	@echo "Running tests..."
	PYTHONPATH=./src python3 -m pytest tests/ -v

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/fhir/__pycache__/
	rm -rf src/fhir/resources/__pycache__/
	rm -rf tests/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.so" -delete

benchmark:
	@echo "Running performance benchmarks..."
	PYTHONPATH=./src python3 benchmarks/benchmark_parser.py
	@echo ""
	@echo "For advanced performance tests, run: PYTHONPATH=./src python3 benchmarks/performance_tests.py"

# Development shortcuts
setup: deps install build
	@echo "Development environment ready!"

check:
	@echo "Running code quality checks..."
	black --check src/ tests/
	flake8 src/ tests/