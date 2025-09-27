#!/usr/bin/env python3
"""
Fast-FHIR Parser Benchmarking Script

This script benchmarks Fast-FHIR parser performance against other FHIR libraries
and provides detailed performance metrics.
"""

import time
import json
import sys
import os
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import statistics
import tracemalloc

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from fast_fhir.deserializers import (
        deserialize_patient,
        deserialize_organization,
        deserialize_care_plan,
        PYDANTIC_AVAILABLE
    )
    FAST_FHIR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Fast-FHIR not available: {e}")
    FAST_FHIR_AVAILABLE = False

@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""
    library_name: str
    parse_time: float  # milliseconds
    memory_usage: float  # MB
    success_rate: float  # percentage
    resources_parsed: int
    errors: List[str]

class FHIRBenchmark:
    """FHIR parser benchmarking utility."""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        
    def generate_test_data(self, resource_type: str, count: int) -> List[Dict[str, Any]]:
        """Generate test FHIR resources for benchmarking."""
        
        if resource_type == "Patient":
            return [
                {
                    "resourceType": "Patient",
                    "id": f"patient-{i}",
                    "active": True,
                    "name": [
                        {
                            "use": "official",
                            "family": f"TestFamily{i}",
                            "given": [f"TestGiven{i}"]
                        }
                    ],
                    "gender": "male" if i % 2 == 0 else "female",
                    "birthDate": "1990-01-01",
                    "telecom": [
                        {
                            "system": "phone",
                            "value": f"555-000-{i:04d}",
                            "use": "home"
                        }
                    ],
                    "address": [
                        {
                            "use": "home",
                            "line": [f"{i} Test Street"],
                            "city": "Test City",
                            "state": "TS",
                            "postalCode": f"{i:05d}",
                            "country": "US"
                        }
                    ]
                }
                for i in range(count)
            ]
        
        elif resource_type == "Organization":
            return [
                {
                    "resourceType": "Organization",
                    "id": f"org-{i}",
                    "active": True,
                    "name": f"Test Organization {i}",
                    "type": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                                    "code": "prov",
                                    "display": "Healthcare Provider"
                                }
                            ]
                        }
                    ],
                    "telecom": [
                        {
                            "system": "phone",
                            "value": f"555-100-{i:04d}",
                            "use": "work"
                        }
                    ]
                }
                for i in range(count)
            ]
        
        elif resource_type == "CarePlan":
            return [
                {
                    "resourceType": "CarePlan",
                    "id": f"careplan-{i}",
                    "status": "active",
                    "intent": "plan",
                    "title": f"Test Care Plan {i}",
                    "description": f"Test care plan description {i}",
                    "subject": {
                        "reference": f"Patient/patient-{i}",
                        "display": f"Test Patient {i}"
                    },
                    "period": {
                        "start": "2024-01-01",
                        "end": "2024-12-31"
                    }
                }
                for i in range(count)
            ]
        
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")
    
    def benchmark_fast_fhir(self, resources: List[Dict[str, Any]], resource_type: str) -> BenchmarkResult:
        """Benchmark Fast-FHIR deserializers."""
        if not FAST_FHIR_AVAILABLE:
            return BenchmarkResult(
                library_name="Fast-FHIR",
                parse_time=0.0,
                memory_usage=0.0,
                success_rate=0.0,
                resources_parsed=0,
                errors=["Fast-FHIR not available"]
            )
        
        # Select appropriate deserializer
        if resource_type == "Patient":
            deserializer = deserialize_patient
        elif resource_type == "Organization":
            deserializer = deserialize_organization
        elif resource_type == "CarePlan":
            deserializer = deserialize_care_plan
        else:
            raise ValueError(f"No deserializer for {resource_type}")
        
        errors = []
        parsed_count = 0
        
        # Start memory tracking
        tracemalloc.start()
        
        # Benchmark parsing
        start_time = time.perf_counter()
        
        for resource_data in resources:
            try:
                result = deserializer(resource_data)
                if result:
                    parsed_count += 1
            except Exception as e:
                errors.append(str(e))
        
        end_time = time.perf_counter()
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        parse_time = (end_time - start_time) * 1000  # Convert to milliseconds
        memory_usage = peak / 1024 / 1024  # Convert to MB
        success_rate = (parsed_count / len(resources)) * 100
        
        return BenchmarkResult(
            library_name="Fast-FHIR",
            parse_time=parse_time,
            memory_usage=memory_usage,
            success_rate=success_rate,
            resources_parsed=parsed_count,
            errors=errors[:5]  # Keep only first 5 errors
        )
    
    def benchmark_json_parsing(self, resources: List[Dict[str, Any]]) -> BenchmarkResult:
        """Benchmark raw JSON parsing as baseline."""
        errors = []
        parsed_count = 0
        
        # Start memory tracking
        tracemalloc.start()
        
        # Benchmark JSON parsing
        start_time = time.perf_counter()
        
        for resource_data in resources:
            try:
                # Convert to JSON string and back to simulate real parsing
                json_str = json.dumps(resource_data)
                parsed = json.loads(json_str)
                if parsed:
                    parsed_count += 1
            except Exception as e:
                errors.append(str(e))
        
        end_time = time.perf_counter()
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        parse_time = (end_time - start_time) * 1000  # Convert to milliseconds
        memory_usage = peak / 1024 / 1024  # Convert to MB
        success_rate = (parsed_count / len(resources)) * 100
        
        return BenchmarkResult(
            library_name="Raw JSON",
            parse_time=parse_time,
            memory_usage=memory_usage,
            success_rate=success_rate,
            resources_parsed=parsed_count,
            errors=errors[:5]
        )
    
    def run_benchmark_suite(self, resource_counts: List[int] = None) -> Dict[str, List[BenchmarkResult]]:
        """Run comprehensive benchmark suite."""
        if resource_counts is None:
            resource_counts = [10, 100, 1000]
        
        resource_types = ["Patient", "Organization", "CarePlan"]
        results = {}
        
        print("🚀 Fast-FHIR Benchmark Suite")
        print("=" * 50)
        print(f"📦 Pydantic Available: {PYDANTIC_AVAILABLE}")
        print(f"📦 Fast-FHIR Available: {FAST_FHIR_AVAILABLE}")
        print()
        
        for resource_type in resource_types:
            print(f"🧪 Benchmarking {resource_type} Resources")
            print("-" * 40)
            
            type_results = []
            
            for count in resource_counts:
                print(f"  📊 Testing {count} resources...")
                
                # Generate test data
                test_resources = self.generate_test_data(resource_type, count)
                
                # Benchmark Fast-FHIR
                fast_fhir_result = self.benchmark_fast_fhir(test_resources, resource_type)
                type_results.append(fast_fhir_result)
                
                # Benchmark raw JSON (baseline)
                json_result = self.benchmark_json_parsing(test_resources)
                
                # Calculate speedup
                if json_result.parse_time > 0:
                    speedup = json_result.parse_time / fast_fhir_result.parse_time if fast_fhir_result.parse_time > 0 else 0
                else:
                    speedup = 0
                
                print(f"    Fast-FHIR: {fast_fhir_result.parse_time:.2f}ms ({fast_fhir_result.success_rate:.1f}% success)")
                print(f"    Raw JSON:  {json_result.parse_time:.2f}ms ({json_result.success_rate:.1f}% success)")
                print(f"    Speedup:   {speedup:.2f}x")
                print(f"    Memory:    {fast_fhir_result.memory_usage:.2f}MB")
                
                if fast_fhir_result.errors:
                    print(f"    Errors:    {len(fast_fhir_result.errors)} (showing first 3)")
                    for error in fast_fhir_result.errors[:3]:
                        print(f"      - {error}")
                
                print()
            
            results[resource_type] = type_results
        
        return results
    
    def print_summary(self, results: Dict[str, List[BenchmarkResult]]):
        """Print benchmark summary."""
        print("📊 Benchmark Summary")
        print("=" * 50)
        
        for resource_type, type_results in results.items():
            print(f"\n{resource_type} Resources:")
            print("| Count | Parse Time | Memory | Success Rate |")
            print("|-------|------------|--------|--------------|")
            
            for result in type_results:
                count = result.resources_parsed
                print(f"| {count:5d} | {result.parse_time:8.2f}ms | {result.memory_usage:6.2f}MB | {result.success_rate:10.1f}% |")
        
        # Overall statistics
        all_results = [result for type_results in results.values() for result in type_results]
        if all_results:
            avg_parse_time = statistics.mean([r.parse_time for r in all_results])
            avg_memory = statistics.mean([r.memory_usage for r in all_results])
            avg_success = statistics.mean([r.success_rate for r in all_results])
            
            print(f"\n📈 Overall Averages:")
            print(f"   Parse Time: {avg_parse_time:.2f}ms")
            print(f"   Memory Usage: {avg_memory:.2f}MB")
            print(f"   Success Rate: {avg_success:.1f}%")

def run_performance_test(file_path: str = None) -> BenchmarkResult:
    """
    Run performance test on a specific file or generate test data.
    This function matches the API referenced in README.md
    """
    benchmark = FHIRBenchmark()
    
    if file_path:
        # If file path provided, try to load and parse it
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Determine resource type
            if isinstance(data, dict):
                resources = [data]
                resource_type = data.get('resourceType', 'Patient')
            elif isinstance(data, list):
                resources = data
                resource_type = resources[0].get('resourceType', 'Patient') if resources else 'Patient'
            else:
                raise ValueError("Invalid JSON structure")
            
            return benchmark.benchmark_fast_fhir(resources, resource_type)
            
        except Exception as e:
            return BenchmarkResult(
                library_name="Fast-FHIR",
                parse_time=0.0,
                memory_usage=0.0,
                success_rate=0.0,
                resources_parsed=0,
                errors=[f"Failed to load {file_path}: {e}"]
            )
    else:
        # Generate test data and run benchmark
        test_resources = benchmark.generate_test_data("Patient", 100)
        return benchmark.benchmark_fast_fhir(test_resources, "Patient")

def main():
    """Main benchmark execution."""
    benchmark = FHIRBenchmark()
    
    # Run benchmark suite
    results = benchmark.run_benchmark_suite([10, 100, 1000])
    
    # Print summary
    benchmark.print_summary(results)
    
    print("\n🎯 Recommendations:")
    print("- For best performance, ensure C extensions are compiled")
    print("- Use Pydantic validation for production environments")
    print("- Monitor memory usage for large datasets")
    print("- Consider batch processing for very large files")

if __name__ == "__main__":
    main()