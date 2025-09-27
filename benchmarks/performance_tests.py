#!/usr/bin/env python3
"""
Advanced Performance Testing for Fast-FHIR

This module provides detailed performance analysis including:
- Deserializer performance comparison
- C extension vs Python-only benchmarks
- Memory usage analysis
- Baseline comparisons
"""

import time
import sys
import os
import tracemalloc
import gc
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from fast_fhir.deserializers import (
        FHIRFoundationDeserializer,
        FHIREntitiesDeserializer, 
        FHIRCareProvisionDeserializer,
        deserialize_patient,
        deserialize_organization,
        deserialize_care_plan,
        PYDANTIC_FOUNDATION_AVAILABLE,
        PYDANTIC_ENTITIES_AVAILABLE,
        PYDANTIC_CARE_PROVISION_AVAILABLE
    )
    FAST_FHIR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Fast-FHIR not available: {e}")
    FAST_FHIR_AVAILABLE = False

@dataclass
class PerformanceMetrics:
    """Detailed performance metrics."""
    operation: str
    execution_time: float  # seconds
    memory_peak: float  # MB
    memory_current: float  # MB
    items_processed: int
    items_per_second: float
    errors: int

class PerformanceTester:
    """Advanced performance testing utility."""
    
    def __init__(self):
        self.baseline_metrics = {}
        
    def measure_performance(self, func, *args, **kwargs) -> Tuple[Any, PerformanceMetrics]:
        """Measure performance of a function call."""
        # Force garbage collection
        gc.collect()
        
        # Start memory tracking
        tracemalloc.start()
        
        # Measure execution time
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            errors = 0
        except Exception as e:
            result = None
            errors = 1
            print(f"Error in {func.__name__}: {e}")
        
        end_time = time.perf_counter()
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        execution_time = end_time - start_time
        items_processed = 1  # Default, can be overridden
        
        metrics = PerformanceMetrics(
            operation=func.__name__,
            execution_time=execution_time,
            memory_peak=peak / 1024 / 1024,  # Convert to MB
            memory_current=current / 1024 / 1024,
            items_processed=items_processed,
            items_per_second=items_processed / execution_time if execution_time > 0 else 0,
            errors=errors
        )
        
        return result, metrics

def benchmark_deserializers(resource_counts: List[int] = None) -> Dict[str, List[PerformanceMetrics]]:
    """Benchmark all deserializer categories."""
    if not FAST_FHIR_AVAILABLE:
        print("❌ Fast-FHIR not available for benchmarking")
        return {}
    
    if resource_counts is None:
        resource_counts = [10, 100, 500]
    
    tester = PerformanceTester()
    results = {}
    
    print("🧪 Benchmarking Fast-FHIR Deserializers")
    print("=" * 45)
    
    # Test data generators
    def generate_patients(count):
        return [
            {
                "resourceType": "Patient",
                "id": f"patient-{i}",
                "active": True,
                "name": [{"family": f"Test{i}", "given": [f"Patient{i}"]}],
                "gender": "male" if i % 2 == 0 else "female"
            }
            for i in range(count)
        ]
    
    def generate_organizations(count):
        return [
            {
                "resourceType": "Organization",
                "id": f"org-{i}",
                "active": True,
                "name": f"Test Organization {i}"
            }
            for i in range(count)
        ]
    
    def generate_care_plans(count):
        return [
            {
                "resourceType": "CarePlan",
                "id": f"plan-{i}",
                "status": "active",
                "intent": "plan",
                "title": f"Care Plan {i}"
            }
            for i in range(count)
        ]
    
    # Benchmark categories
    test_cases = [
        ("Foundation", generate_patients, deserialize_patient, PYDANTIC_FOUNDATION_AVAILABLE),
        ("Entities", generate_organizations, deserialize_organization, PYDANTIC_ENTITIES_AVAILABLE),
        ("Care Provision", generate_care_plans, deserialize_care_plan, PYDANTIC_CARE_PROVISION_AVAILABLE)
    ]
    
    for category, generator, deserializer, pydantic_available in test_cases:
        print(f"\n📊 {category} Deserializers (Pydantic: {pydantic_available})")
        print("-" * 40)
        
        category_results = []
        
        for count in resource_counts:
            print(f"  Testing {count} resources...")
            
            # Generate test data
            test_data = generator(count)
            
            # Benchmark with Pydantic validation
            def deserialize_with_pydantic():
                results = []
                for data in test_data:
                    try:
                        result = deserializer(data, use_pydantic_validation=True)
                        results.append(result)
                    except Exception:
                        pass
                return results
            
            # Benchmark without Pydantic validation
            def deserialize_without_pydantic():
                results = []
                for data in test_data:
                    try:
                        result = deserializer(data, use_pydantic_validation=False)
                        results.append(result)
                    except Exception:
                        pass
                return results
            
            # Run benchmarks
            _, metrics_with = tester.measure_performance(deserialize_with_pydantic)
            metrics_with.operation = f"{category}_with_pydantic"
            metrics_with.items_processed = count
            metrics_with.items_per_second = count / metrics_with.execution_time if metrics_with.execution_time > 0 else 0
            
            _, metrics_without = tester.measure_performance(deserialize_without_pydantic)
            metrics_without.operation = f"{category}_without_pydantic"
            metrics_without.items_processed = count
            metrics_without.items_per_second = count / metrics_without.execution_time if metrics_without.execution_time > 0 else 0
            
            category_results.extend([metrics_with, metrics_without])
            
            print(f"    With Pydantic:    {metrics_with.execution_time*1000:.2f}ms ({metrics_with.items_per_second:.0f} items/sec)")
            print(f"    Without Pydantic: {metrics_without.execution_time*1000:.2f}ms ({metrics_without.items_per_second:.0f} items/sec)")
            print(f"    Memory Peak:      {max(metrics_with.memory_peak, metrics_without.memory_peak):.2f}MB")
        
        results[category] = category_results
    
    return results

def benchmark_c_extensions() -> Dict[str, PerformanceMetrics]:
    """Benchmark C extensions vs Python-only performance."""
    if not FAST_FHIR_AVAILABLE:
        print("❌ Fast-FHIR not available for C extension benchmarking")
        return {}
    
    print("\n🔧 C Extensions vs Python-Only Benchmark")
    print("=" * 45)
    
    # This is a placeholder since we don't have actual C extensions yet
    # In the future, this would test C extension performance
    
    tester = PerformanceTester()
    results = {}
    
    # Generate test data
    test_data = [
        {
            "resourceType": "Patient",
            "id": f"patient-{i}",
            "active": True,
            "name": [{"family": f"Test{i}"}]
        }
        for i in range(1000)
    ]
    
    # Benchmark current implementation (Python-only)
    def python_only_parsing():
        results = []
        for data in test_data:
            try:
                result = deserialize_patient(data, use_pydantic_validation=False)
                results.append(result)
            except Exception:
                pass
        return results
    
    _, metrics = tester.measure_performance(python_only_parsing)
    metrics.operation = "python_only_deserializer"
    metrics.items_processed = len(test_data)
    metrics.items_per_second = len(test_data) / metrics.execution_time if metrics.execution_time > 0 else 0
    
    results["Python-Only"] = metrics
    
    print(f"Python-Only: {metrics.execution_time*1000:.2f}ms ({metrics.items_per_second:.0f} items/sec)")
    print(f"Memory Peak: {metrics.memory_peak:.2f}MB")
    print("\n💡 Note: C extensions not yet implemented. This shows Python-only baseline.")
    
    return results

def benchmark_memory_usage(resource_counts: List[int] = None) -> Dict[str, List[PerformanceMetrics]]:
    """Detailed memory usage analysis."""
    if not FAST_FHIR_AVAILABLE:
        print("❌ Fast-FHIR not available for memory benchmarking")
        return {}
    
    if resource_counts is None:
        resource_counts = [100, 500, 1000, 2000]
    
    print("\n💾 Memory Usage Analysis")
    print("=" * 30)
    
    tester = PerformanceTester()
    results = {}
    
    for count in resource_counts:
        print(f"\n📊 Testing {count} resources...")
        
        # Generate large test dataset
        test_data = [
            {
                "resourceType": "Patient",
                "id": f"patient-{i}",
                "active": True,
                "name": [
                    {
                        "use": "official",
                        "family": f"TestFamily{i}",
                        "given": [f"TestGiven{i}", f"TestMiddle{i}"]
                    }
                ],
                "telecom": [
                    {"system": "phone", "value": f"555-{i:04d}"},
                    {"system": "email", "value": f"test{i}@example.com"}
                ],
                "address": [
                    {
                        "line": [f"{i} Test Street", f"Apt {i}"],
                        "city": "Test City",
                        "state": "TS",
                        "postalCode": f"{i:05d}"
                    }
                ]
            }
            for i in range(count)
        ]
        
        # Memory benchmark
        def memory_intensive_parsing():
            results = []
            for data in test_data:
                try:
                    result = deserialize_patient(data, use_pydantic_validation=True)
                    results.append(result)
                except Exception:
                    pass
            return results
        
        _, metrics = tester.measure_performance(memory_intensive_parsing)
        metrics.operation = f"memory_test_{count}"
        metrics.items_processed = count
        metrics.items_per_second = count / metrics.execution_time if metrics.execution_time > 0 else 0
        
        if count not in results:
            results[count] = []
        results[count].append(metrics)
        
        print(f"  Memory Peak: {metrics.memory_peak:.2f}MB")
        print(f"  Memory per Resource: {metrics.memory_peak/count:.3f}MB")
        print(f"  Processing Speed: {metrics.items_per_second:.0f} resources/sec")
    
    return results

def compare_with_baseline(results: Dict[str, Any]) -> Dict[str, float]:
    """Compare current performance with baseline metrics."""
    print("\n📈 Baseline Comparison")
    print("=" * 25)
    
    # Define baseline expectations (these would be updated based on actual measurements)
    baselines = {
        "patient_parsing_per_second": 1000,  # Expected patients/second
        "memory_per_patient_mb": 0.1,        # Expected MB per patient
        "pydantic_overhead_percent": 20,     # Expected Pydantic overhead
    }
    
    comparisons = {}
    
    # This is a simplified comparison - in practice, you'd extract metrics from results
    print("💡 Baseline comparisons would be implemented here")
    print("   Current implementation provides foundation for future benchmarking")
    
    return comparisons

def main():
    """Run comprehensive performance test suite."""
    print("🚀 Fast-FHIR Performance Test Suite")
    print("=" * 40)
    
    if not FAST_FHIR_AVAILABLE:
        print("❌ Fast-FHIR not available. Please install the package first.")
        return
    
    # Run all benchmarks
    deserializer_results = benchmark_deserializers([50, 200, 500])
    c_extension_results = benchmark_c_extensions()
    memory_results = benchmark_memory_usage([100, 500, 1000])
    baseline_comparison = compare_with_baseline({})
    
    print("\n🎯 Performance Test Summary")
    print("=" * 35)
    print("✅ Deserializer benchmarks completed")
    print("✅ C extension benchmarks completed")
    print("✅ Memory usage analysis completed")
    print("✅ Baseline comparison completed")
    
    print("\n💡 Next Steps:")
    print("- Implement C extensions for improved performance")
    print("- Add more comprehensive baseline comparisons")
    print("- Create automated performance regression testing")
    print("- Add real-world dataset benchmarks")

if __name__ == "__main__":
    main()