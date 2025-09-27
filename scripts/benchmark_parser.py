#!/usr/bin/env python3
"""
Fast-FHIR Parser Benchmarking Script (Scripts Version)

This is a convenience wrapper that calls the main benchmark module.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from benchmarks.benchmark_parser import main

if __name__ == "__main__":
    main()