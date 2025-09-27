#!/usr/bin/env python3
"""
Simple Comparative Benchmark: Fast-FHIR vs fhir.resources

This script compares Fast-FHIR performance against fhir.resources without Pydantic validation
to avoid version compatibility issues.
"""

import time
import json
import sys
import os
import tracemalloc
import statistics
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Add src to path for Fast-FHIR imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import Fast-FHIR (without Pydantic validation to avoid version conflicts)
try:
    from fast_fhir.deserializers import (
        deserialize_patient,
        deserialize_organization,
        deserialize_care_plan
    )
    FAST_FHIR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Fast-FHIR not available: {e}")
    FAST_FHIR_AVAILABLE = False

# Import fhir.resources
try:
    from fhir.resources.patient import Patient as FhirResourcesPatient
    from fhir.resources.organization import Organization as FhirResourcesOrganization
    from fhir.resources.careplan import CarePlan as FhirResourcesCarePlan
    FHIR_RESOURCES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: fhir.resources not available: {e}")
    FHIR_RESOURCES_AVAILABLE = False

@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""
    library_name: str
    resource_type: str
    resource_count: int
    parse_time: float  # milliseconds
    memory_usage: float  # MB
    success_count: int
    error_count: int
    errors: List[str]
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.error_count
        return (self.success_count / total * 100) if total > 0 else 0.0
    
    @property
    def resources_per_second(self) -> float:
        return (self.resource_count / (self.parse_time / 1000)) if self.parse_time > 0 else 0.0

def generate_test_data(resource_type: str, count: int) -> List[Dict[str, Any]]:
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
                "birthDate": "1990-01-01"
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
                "subject": {
                    "reference": f"Patient/patient-{i}",
                    "display": f"Test Patient {i}"
                }
            }
            for i in range(count)
        ]
    
    else:
        raise ValueError(f"Unsupported resource type: {resource_type}")

def benchmark_fast_fhir(resources: List[Dict[str, Any]], resource_type: str) -> BenchmarkResult:
    """Benchmark Fast-FHIR deserializers."""
    if not FAST_FHIR_AVAILABLE:
        return BenchmarkResult(
            library_name="Fast-FHIR",
            resource_type=resource_type,
            resource_count=len(resources),
            parse_time=0.0,
            memory_usage=0.0,
            success_count=0,
            error_count=len(resources),
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
        raise ValueError(f"No Fast-FHIR deserializer for {resource_type}")
    
    errors = []
    success_count = 0
    
    # Start memory tracking
    tracemalloc.start()
    
    # Benchmark parsing
    start_time = time.perf_counter()
    
    for resource_data in resources:
        try:
            # Use without Pydantic validation to avoid version conflicts
            result = deserializer(resource_data, use_pydantic_validation=False)
            if result:
                success_count += 1
        except Exception as e:
            errors.append(str(e))
    
    end_time = time.perf_counter()
    
    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    parse_time = (end_time - start_time) * 1000  # Convert to milliseconds
    memory_usage = peak / 1024 / 1024  # Convert to MB
    error_count = len(resources) - success_count
    
    return BenchmarkResult(
        library_name="Fast-FHIR",
        resource_type=resource_type,
        resource_count=len(resources),
        parse_time=parse_time,
        memory_usage=memory_usage,
        success_count=success_count,
        error_count=error_count,
        errors=errors[:5]  # Keep only first 5 errors
    )

def benchmark_fhir_resources(resources: List[Dict[str, Any]], resource_type: str) -> BenchmarkResult:
    """Benchmark fhir.resources library."""
    if not FHIR_RESOURCES_AVAILABLE:
        return BenchmarkResult(
            library_name="fhir.resources",
            resource_type=resource_type,
            resource_count=len(resources),
            parse_time=0.0,
            memory_usage=0.0,
            success_count=0,
            error_count=len(resources),
            errors=["fhir.resources not available"]
        )
    
    # Select appropriate class
    if resource_type == "Patient":
        ResourceClass = FhirResourcesPatient
    elif resource_type == "Organization":
        ResourceClass = FhirResourcesOrganization
    elif resource_type == "CarePlan":
        ResourceClass = FhirResourcesCarePlan
    else:
        raise ValueError(f"No fhir.resources class for {resource_type}")
    
    errors = []
    success_count = 0
    
    # Start memory tracking
    tracemalloc.start()
    
    # Benchmark parsing
    start_time = time.perf_counter()
    
    for resource_data in resources:
        try:
            # Use the modern parse method for Pydantic v2
            result = ResourceClass.model_validate(resource_data)
            if result:
                success_count += 1
        except Exception as e:
            errors.append(str(e))
    
    end_time = time.perf_counter()
    
    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    parse_time = (end_time - start_time) * 1000  # Convert to milliseconds
    memory_usage = peak / 1024 / 1024  # Convert to MB
    error_count = len(resources) - success_count
    
    return BenchmarkResult(
        library_name="fhir.resources",
        resource_type=resource_type,
        resource_count=len(resources),
        parse_time=parse_time,
        memory_usage=memory_usage,
        success_count=success_count,
        error_count=error_count,
        errors=errors[:5]
    )

def run_comparative_benchmark(resource_counts: List[int] = None) -> Dict[str, List[BenchmarkResult]]:
    """Run comparative benchmark suite."""
    if resource_counts is None:
        resource_counts = [10, 100, 500]
    
    resource_types = ["Patient", "Organization", "CarePlan"]
    results = {}
    
    print("🚀 Fast-FHIR vs fhir.resources Comparative Benchmark")
    print("=" * 60)
    print(f"📦 Fast-FHIR Available: {FAST_FHIR_AVAILABLE}")
    print(f"📦 fhir.resources Available: {FHIR_RESOURCES_AVAILABLE}")
    print()
    
    for resource_type in resource_types:
        print(f"🧪 Benchmarking {resource_type} Resources")
        print("-" * 50)
        
        type_results = []
        
        for count in resource_counts:
            print(f"  📊 Testing {count} resources...")
            
            # Generate test data
            test_resources = generate_test_data(resource_type, count)
            
            # Benchmark Fast-FHIR
            fast_fhir_result = benchmark_fast_fhir(test_resources, resource_type)
            type_results.append(fast_fhir_result)
            
            # Benchmark fhir.resources
            fhir_resources_result = benchmark_fhir_resources(test_resources, resource_type)
            type_results.append(fhir_resources_result)
            
            # Calculate speedup
            if fhir_resources_result.parse_time > 0 and fast_fhir_result.parse_time > 0:
                speedup = fhir_resources_result.parse_time / fast_fhir_result.parse_time
            else:
                speedup = 0
            
            print(f"    Fast-FHIR:      {fast_fhir_result.parse_time:.2f}ms ({fast_fhir_result.success_rate:.1f}% success, {fast_fhir_result.memory_usage:.2f}MB)")
            print(f"    fhir.resources: {fhir_resources_result.parse_time:.2f}ms ({fhir_resources_result.success_rate:.1f}% success, {fhir_resources_result.memory_usage:.2f}MB)")
            
            if speedup > 0:
                if speedup > 1:
                    print(f"    🚀 Fast-FHIR is {speedup:.2f}x faster")
                else:
                    print(f"    🐌 fhir.resources is {1/speedup:.2f}x faster")
            
            if fast_fhir_result.errors:
                print(f"    ⚠️  Fast-FHIR errors: {len(fast_fhir_result.errors)}")
            if fhir_resources_result.errors:
                print(f"    ⚠️  fhir.resources errors: {len(fhir_resources_result.errors)}")
            
            print()
        
        results[resource_type] = type_results
    
    return results

def print_summary_table(results: Dict[str, List[BenchmarkResult]]):
    """Print comparative summary table."""
    print("📊 Comparative Performance Summary")
    print("=" * 80)
    
    for resource_type, type_results in results.items():
        print(f"\n{resource_type} Resources:")
        print("┌─────────────────┬───────┬──────────┬─────────┬──────────┬─────────┬──────────┐")
        print("│ Library         │ Count │ Time(ms) │ Memory  │ Success  │ Rate/s  │ Speedup  │")
        print("├─────────────────┼───────┼──────────┼─────────┼──────────┼─────────┼──────────┤")
        
        # Group results by count
        by_count = {}
        for result in type_results:
            if result.resource_count not in by_count:
                by_count[result.resource_count] = {}
            by_count[result.resource_count][result.library_name] = result
        
        for count in sorted(by_count.keys()):
            count_results = by_count[count]
            
            # Calculate speedup
            speedup_str = ""
            if "Fast-FHIR" in count_results and "fhir.resources" in count_results:
                fast_result = count_results["Fast-FHIR"]
                fhir_result = count_results["fhir.resources"]
                
                if fhir_result.parse_time > 0 and fast_result.parse_time > 0:
                    speedup = fhir_result.parse_time / fast_result.parse_time
                    speedup_str = f"{speedup:.2f}x"
            
            for lib_name in ["Fast-FHIR", "fhir.resources"]:
                if lib_name in count_results:
                    result = count_results[lib_name]
                    speedup_display = speedup_str if lib_name == "Fast-FHIR" else ""
                    print(f"│ {lib_name:<15} │ {result.resource_count:5d} │ {result.parse_time:8.2f} │ {result.memory_usage:7.2f} │ {result.success_rate:7.1f}% │ {result.resources_per_second:7.0f} │ {speedup_display:8} │")
            
            if count != max(by_count.keys()):
                print("├─────────────────┼───────┼──────────┼─────────┼──────────┼─────────┼──────────┤")
        
        print("└─────────────────┴───────┴──────────┴─────────┴──────────┴─────────┴──────────┘")

def print_analysis(results: Dict[str, List[BenchmarkResult]]):
    """Print performance analysis."""
    print("\n🔍 Performance Analysis")
    print("=" * 30)
    
    all_fast_fhir = [r for type_results in results.values() for r in type_results if r.library_name == "Fast-FHIR" and r.parse_time > 0]
    all_fhir_resources = [r for type_results in results.values() for r in type_results if r.library_name == "fhir.resources" and r.parse_time > 0]
    
    if all_fast_fhir and all_fhir_resources:
        # Average performance
        avg_fast_fhir_time = statistics.mean([r.parse_time for r in all_fast_fhir])
        avg_fhir_resources_time = statistics.mean([r.parse_time for r in all_fhir_resources])
        
        avg_fast_fhir_memory = statistics.mean([r.memory_usage for r in all_fast_fhir])
        avg_fhir_resources_memory = statistics.mean([r.memory_usage for r in all_fhir_resources])
        
        print(f"📈 Average Parse Time:")
        print(f"   Fast-FHIR:      {avg_fast_fhir_time:.2f}ms")
        print(f"   fhir.resources: {avg_fhir_resources_time:.2f}ms")
        
        if avg_fast_fhir_time > 0:
            overall_speedup = avg_fhir_resources_time / avg_fast_fhir_time
            print(f"   Overall Speedup: {overall_speedup:.2f}x")
        
        print(f"\n💾 Average Memory Usage:")
        print(f"   Fast-FHIR:      {avg_fast_fhir_memory:.2f}MB")
        print(f"   fhir.resources: {avg_fhir_resources_memory:.2f}MB")
        
        if avg_fast_fhir_memory > 0:
            memory_efficiency = avg_fhir_resources_memory / avg_fast_fhir_memory
            print(f"   Memory Ratio: {memory_efficiency:.2f}x")
        
        # Success rates
        fast_fhir_success = statistics.mean([r.success_rate for r in all_fast_fhir])
        fhir_resources_success = statistics.mean([r.success_rate for r in all_fhir_resources])
        
        print(f"\n✅ Success Rates:")
        print(f"   Fast-FHIR:      {fast_fhir_success:.1f}%")
        print(f"   fhir.resources: {fhir_resources_success:.1f}%")

def main():
    """Main comparative benchmark execution."""
    # Check availability
    if not FAST_FHIR_AVAILABLE and not FHIR_RESOURCES_AVAILABLE:
        print("❌ Neither Fast-FHIR nor fhir.resources is available")
        return
    
    if not FAST_FHIR_AVAILABLE:
        print("⚠️  Fast-FHIR not available - only testing fhir.resources")
    
    if not FHIR_RESOURCES_AVAILABLE:
        print("⚠️  fhir.resources not available - only testing Fast-FHIR")
    
    # Run comparative benchmark
    results = run_comparative_benchmark([10, 100, 500])
    
    # Print results
    print_summary_table(results)
    print_analysis(results)
    
    print("\n🎯 Key Findings:")
    print("- Performance comparison between Fast-FHIR and fhir.resources")
    print("- Fast-FHIR tested without Pydantic validation for compatibility")
    print("- fhir.resources uses Pydantic v2 validation by default")
    print("- Results show actual performance on your system")
    
    print("\n💡 Notes:")
    print("- Fast-FHIR can use Pydantic validation when versions are compatible")
    print("- Performance varies based on system resources and data complexity")
    print("- Both libraries provide reliable FHIR resource parsing")

if __name__ == "__main__":
    main()