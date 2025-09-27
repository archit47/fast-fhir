#!/usr/bin/env python3
"""
FHIR Resources Library Benchmark

This script benchmarks the fhir.resources library and provides baseline JSON parsing
for comparison with Fast-FHIR results.
"""

import time
import json
import tracemalloc
import statistics
from dataclasses import dataclass
from typing import Dict, List, Any

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
                ],
                "address": [
                    {
                        "use": "work",
                        "line": [f"{i} Business Ave"],
                        "city": "Business City",
                        "state": "BC",
                        "postalCode": f"{i+10000:05d}",
                        "country": "US"
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
                },
                "activity": [
                    {
                        "detail": {
                            "status": "in-progress",
                            "description": f"Activity {i} for care plan"
                        }
                    }
                ]
            }
            for i in range(count)
        ]
    
    else:
        raise ValueError(f"Unsupported resource type: {resource_type}")

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

def benchmark_json_baseline(resources: List[Dict[str, Any]], resource_type: str) -> BenchmarkResult:
    """Benchmark raw JSON parsing as baseline."""
    errors = []
    success_count = 0
    
    # Start memory tracking
    tracemalloc.start()
    
    # Benchmark JSON parsing
    start_time = time.perf_counter()
    
    for resource_data in resources:
        try:
            # Convert to JSON string and back to simulate real parsing
            json_str = json.dumps(resource_data)
            parsed = json.loads(json_str)
            if parsed and parsed.get('resourceType') == resource_type:
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
        library_name="JSON Baseline",
        resource_type=resource_type,
        resource_count=len(resources),
        parse_time=parse_time,
        memory_usage=memory_usage,
        success_count=success_count,
        error_count=error_count,
        errors=errors[:5]
    )

def run_benchmark_suite(resource_counts: List[int] = None) -> Dict[str, List[BenchmarkResult]]:
    """Run benchmark suite."""
    if resource_counts is None:
        resource_counts = [10, 100, 500]
    
    resource_types = ["Patient", "Organization", "CarePlan"]
    results = {}
    
    print("🚀 FHIR Resources Library Benchmark")
    print("=" * 50)
    print(f"📦 fhir.resources Available: {FHIR_RESOURCES_AVAILABLE}")
    print("📝 Note: Includes JSON baseline for comparison")
    print()
    
    for resource_type in resource_types:
        print(f"🧪 Benchmarking {resource_type} Resources")
        print("-" * 50)
        
        type_results = []
        
        for count in resource_counts:
            print(f"  📊 Testing {count} resources...")
            
            # Generate test data
            test_resources = generate_test_data(resource_type, count)
            
            # Benchmark JSON baseline
            json_result = benchmark_json_baseline(test_resources, resource_type)
            type_results.append(json_result)
            
            # Benchmark fhir.resources
            fhir_resources_result = benchmark_fhir_resources(test_resources, resource_type)
            type_results.append(fhir_resources_result)
            
            # Calculate overhead
            if json_result.parse_time > 0 and fhir_resources_result.parse_time > 0:
                overhead = fhir_resources_result.parse_time / json_result.parse_time
            else:
                overhead = 0
            
            print(f"    JSON Baseline:  {json_result.parse_time:.2f}ms ({json_result.success_rate:.1f}% success, {json_result.memory_usage:.2f}MB)")
            print(f"    fhir.resources: {fhir_resources_result.parse_time:.2f}ms ({fhir_resources_result.success_rate:.1f}% success, {fhir_resources_result.memory_usage:.2f}MB)")
            
            if overhead > 0:
                print(f"    📊 Validation overhead: {overhead:.2f}x")
            
            if fhir_resources_result.errors:
                print(f"    ⚠️  fhir.resources errors: {len(fhir_resources_result.errors)}")
            
            print()
        
        results[resource_type] = type_results
    
    return results

def print_summary_table(results: Dict[str, List[BenchmarkResult]]):
    """Print summary table."""
    print("📊 Performance Summary")
    print("=" * 80)
    
    for resource_type, type_results in results.items():
        print(f"\n{resource_type} Resources:")
        print("┌─────────────────┬───────┬──────────┬─────────┬──────────┬─────────┬──────────┐")
        print("│ Method          │ Count │ Time(ms) │ Memory  │ Success  │ Rate/s  │ Overhead │")
        print("├─────────────────┼───────┼──────────┼─────────┼──────────┼─────────┼──────────┤")
        
        # Group results by count
        by_count = {}
        for result in type_results:
            if result.resource_count not in by_count:
                by_count[result.resource_count] = {}
            by_count[result.resource_count][result.library_name] = result
        
        for count in sorted(by_count.keys()):
            count_results = by_count[count]
            
            # Calculate overhead
            overhead_str = ""
            if "JSON Baseline" in count_results and "fhir.resources" in count_results:
                json_result = count_results["JSON Baseline"]
                fhir_result = count_results["fhir.resources"]
                
                if json_result.parse_time > 0 and fhir_result.parse_time > 0:
                    overhead = fhir_result.parse_time / json_result.parse_time
                    overhead_str = f"{overhead:.2f}x"
            
            for lib_name in ["JSON Baseline", "fhir.resources"]:
                if lib_name in count_results:
                    result = count_results[lib_name]
                    overhead_display = overhead_str if lib_name == "fhir.resources" else ""
                    print(f"│ {lib_name:<15} │ {result.resource_count:5d} │ {result.parse_time:8.2f} │ {result.memory_usage:7.2f} │ {result.success_rate:7.1f}% │ {result.resources_per_second:7.0f} │ {overhead_display:8} │")
            
            if count != max(by_count.keys()):
                print("├─────────────────┼───────┼──────────┼─────────┼──────────┼─────────┼──────────┤")
        
        print("└─────────────────┴───────┴──────────┴─────────┴──────────┴─────────┴──────────┘")

def print_analysis(results: Dict[str, List[BenchmarkResult]]):
    """Print performance analysis."""
    print("\n🔍 Performance Analysis")
    print("=" * 30)
    
    all_json = [r for type_results in results.values() for r in type_results if r.library_name == "JSON Baseline" and r.parse_time > 0]
    all_fhir_resources = [r for type_results in results.values() for r in type_results if r.library_name == "fhir.resources" and r.parse_time > 0]
    
    if all_json and all_fhir_resources:
        # Average performance
        avg_json_time = statistics.mean([r.parse_time for r in all_json])
        avg_fhir_resources_time = statistics.mean([r.parse_time for r in all_fhir_resources])
        
        avg_json_memory = statistics.mean([r.memory_usage for r in all_json])
        avg_fhir_resources_memory = statistics.mean([r.memory_usage for r in all_fhir_resources])
        
        print(f"📈 Average Parse Time:")
        print(f"   JSON Baseline:  {avg_json_time:.2f}ms")
        print(f"   fhir.resources: {avg_fhir_resources_time:.2f}ms")
        
        if avg_json_time > 0:
            overall_overhead = avg_fhir_resources_time / avg_json_time
            print(f"   Validation Overhead: {overall_overhead:.2f}x")
        
        print(f"\n💾 Average Memory Usage:")
        print(f"   JSON Baseline:  {avg_json_memory:.2f}MB")
        print(f"   fhir.resources: {avg_fhir_resources_memory:.2f}MB")
        
        if avg_json_memory > 0:
            memory_overhead = avg_fhir_resources_memory / avg_json_memory
            print(f"   Memory Overhead: {memory_overhead:.2f}x")
        
        # Success rates
        json_success = statistics.mean([r.success_rate for r in all_json])
        fhir_resources_success = statistics.mean([r.success_rate for r in all_fhir_resources])
        
        print(f"\n✅ Success Rates:")
        print(f"   JSON Baseline:  {json_success:.1f}%")
        print(f"   fhir.resources: {fhir_resources_success:.1f}%")

def main():
    """Main benchmark execution."""
    if not FHIR_RESOURCES_AVAILABLE:
        print("❌ fhir.resources not available")
        return
    
    # Run benchmark suite
    results = run_benchmark_suite([10, 100, 500])
    
    # Print results
    print_summary_table(results)
    print_analysis(results)
    
    print("\n🎯 Key Findings:")
    print("- fhir.resources provides comprehensive FHIR validation using Pydantic v2")
    print("- Validation overhead shows the cost of full FHIR compliance checking")
    print("- JSON baseline represents minimal parsing without validation")
    print("- Results provide reference for comparing other FHIR libraries")
    
    print("\n💡 For Fast-FHIR Comparison:")
    print("- Run: PYTHONPATH=./src python3 benchmarks/benchmark_parser.py")
    print("- Compare Fast-FHIR results with these fhir.resources benchmarks")
    print("- Consider validation requirements vs performance needs")

if __name__ == "__main__":
    main()