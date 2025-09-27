"""
Fast-FHIR Benchmarking Module

This module provides performance testing and benchmarking utilities for Fast-FHIR.
"""

from .benchmark_parser import run_performance_test, BenchmarkResult
from .performance_tests import (
    benchmark_deserializers,
    benchmark_c_extensions,
    benchmark_memory_usage,
    compare_with_baseline
)

__all__ = [
    'run_performance_test',
    'BenchmarkResult',
    'benchmark_deserializers',
    'benchmark_c_extensions', 
    'benchmark_memory_usage',
    'compare_with_baseline'
]