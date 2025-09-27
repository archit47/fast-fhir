# Fast-FHIR Benchmarks

This directory contains comprehensive performance benchmarking tools for Fast-FHIR deserializers and parsers.

## 📁 Benchmark Files

| File | Purpose | Usage |
|------|---------|-------|
| `benchmark_parser.py` | Main benchmarking script | `python3 benchmarks/benchmark_parser.py` |
| `performance_tests.py` | Advanced performance analysis | `python3 benchmarks/performance_tests.py` |
| `__init__.py` | Module exports and API | Import functions for custom benchmarks |

## 🚀 Quick Start

### Run Basic Benchmarks
```bash
# From project root
PYTHONPATH=./src python3 benchmarks/benchmark_parser.py

# Or using Make
make benchmark
```

### Run Advanced Performance Tests
```bash
PYTHONPATH=./src python3 benchmarks/performance_tests.py
```

### Use in Python Code
```python
from fast_fhir.benchmarks import run_performance_test

# Test with file
result = run_performance_test("patient_data.json")
print(f"Parse time: {result.parse_time:.2f}ms")

# Test with generated data
result = run_performance_test()  # Uses default test data
print(f"Success rate: {result.success_rate:.1f}%")
```

## 📊 Benchmark Categories

### 1. **Parser Benchmarks** (`benchmark_parser.py`)

**Features:**
- Tests all three deserializer categories (Foundation, Entities, Care Provision)
- Compares Fast-FHIR performance against raw JSON parsing
- Measures parsing speed, memory usage, and success rates
- Supports custom resource counts and file inputs

**Sample Output:**
```
🧪 Benchmarking Patient Resources
----------------------------------------
  📊 Testing 1000 resources...
    Fast-FHIR: [actual time]ms ([actual rate]% success)
    Raw JSON:  [baseline time]ms ([baseline rate]% success)
    Speedup:   [calculated speedup]x
    Memory:    [measured memory]MB
```

### 2. **Performance Tests** (`performance_tests.py`)

**Features:**
- Detailed deserializer performance comparison
- Pydantic validation overhead analysis
- Memory usage profiling
- C extension vs Python-only benchmarks (future)
- Baseline performance comparisons

**Test Categories:**
- **Deserializer Benchmarks**: Compare all deserializer categories
- **C Extension Benchmarks**: Test C extension performance (placeholder)
- **Memory Analysis**: Detailed memory usage patterns
- **Baseline Comparison**: Compare against expected performance metrics

## 🎯 Benchmark Results

### Performance Characteristics

The benchmarks measure actual performance on your system. Results will vary based on:
- **Hardware**: CPU speed, memory, and system load
- **Python Version**: Different Python versions have varying performance
- **Pydantic Version**: Validation performance depends on Pydantic version
- **Data Complexity**: More complex FHIR resources take longer to parse

**Typical Performance Range:**
- **Small datasets (10-100 resources)**: Sub-millisecond to few milliseconds
- **Medium datasets (100-1000 resources)**: Few milliseconds to tens of milliseconds  
- **Large datasets (1000+ resources)**: Tens to hundreds of milliseconds

### Performance Characteristics

**Expected Characteristics:**
- ✅ **Linear Scaling**: Parse time should scale linearly with resource count
- ✅ **High Success Rate**: Should achieve near 100% parsing success for valid FHIR data
- ✅ **Memory Efficient**: Low memory overhead relative to data size
- ✅ **Consistent Performance**: Reliable performance across different resource types

**Future Optimization Opportunities:**
- 🔧 **C Extensions**: Potential for significant performance improvements
- 🔧 **Batch Processing**: Optimize for large dataset processing
- 🔧 **Memory Pooling**: Reduce allocation overhead for high-volume scenarios

## 🔧 Advanced Usage

### Custom Benchmark Configuration

```python
from benchmarks.benchmark_parser import FHIRBenchmark

# Create custom benchmark
benchmark = FHIRBenchmark()

# Test specific resource counts
results = benchmark.run_benchmark_suite([50, 500, 5000])

# Print detailed results
benchmark.print_summary(results)
```

### Memory Profiling

```python
from benchmarks.performance_tests import benchmark_memory_usage

# Analyze memory usage patterns
memory_results = benchmark_memory_usage([100, 1000, 5000])

# Results show memory per resource and peak usage
for count, metrics in memory_results.items():
    print(f"{count} resources: {metrics[0].memory_peak:.2f}MB peak")
```

### Performance Comparison

```python
from benchmarks.performance_tests import benchmark_deserializers

# Compare deserializer performance
results = benchmark_deserializers([100, 500, 1000])

# Analyze Pydantic validation overhead
for category, metrics_list in results.items():
    with_pydantic = [m for m in metrics_list if 'with_pydantic' in m.operation]
    without_pydantic = [m for m in metrics_list if 'without_pydantic' in m.operation]
    
    # Calculate overhead
    for with_p, without_p in zip(with_pydantic, without_pydantic):
        overhead = ((with_p.execution_time - without_p.execution_time) / without_p.execution_time) * 100
        print(f"{category}: {overhead:.1f}% Pydantic overhead")
```

## 📈 Interpreting Results

### Performance Metrics

**Parse Time**: Time to deserialize resources (lower is better)
- Varies based on system performance and data complexity
- Should scale linearly with resource count
- Compare against baseline JSON parsing for relative performance

**Memory Usage**: Peak memory consumption (lower is better)  
- Should be proportional to data size
- Monitor for memory leaks in long-running processes
- Compare memory per resource across different dataset sizes

**Success Rate**: Percentage of successful parsing (higher is better)
- **100%**: Perfect parsing (expected for valid FHIR data)
- **95-99%**: Good (some edge cases)
- **< 95%**: Investigate parsing issues

**Speedup**: Performance vs baseline (higher is better)
- **> 2x**: Significant improvement
- **1.5-2x**: Good improvement
- **1-1.5x**: Modest improvement
- **< 1x**: Performance regression (investigate)

### Benchmark Interpretation

**Linear Scaling**: Parse time should scale linearly with resource count
```
# Performance should be proportional to dataset size
# Actual times depend on your system
```

**Memory Efficiency**: Memory usage should be proportional to data size
```
Memory per resource = Peak Memory / Resource Count
# Should remain relatively constant across dataset sizes
```

**Validation Overhead**: Pydantic validation adds processing time
```
# Overhead varies based on resource complexity
# Compare with/without validation to measure impact
```

## 🔍 Troubleshooting

### Common Issues

#### Slow Performance
```bash
# Check if running in debug mode
python3 -O benchmarks/benchmark_parser.py

# Verify Pydantic is installed
python3 -c "import pydantic; print(pydantic.VERSION)"

# Check system resources
top -p $(pgrep python3)
```

#### Memory Issues
```bash
# Run with memory profiling
python3 -m tracemalloc benchmarks/performance_tests.py

# Check for memory leaks
python3 -c "
import gc
from benchmarks.performance_tests import benchmark_memory_usage
gc.set_debug(gc.DEBUG_LEAK)
benchmark_memory_usage([100])
"
```

#### Import Errors
```bash
# Verify PYTHONPATH
echo $PYTHONPATH

# Check Fast-FHIR installation
PYTHONPATH=./src python3 -c "import fast_fhir; print('OK')"

# Install missing dependencies
pip install -r requirements.txt
```

### Performance Debugging

#### Enable Verbose Output
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from benchmarks.benchmark_parser import main
main()
```

#### Profile Specific Functions
```python
import cProfile
import pstats

from benchmarks.performance_tests import benchmark_deserializers

# Profile deserializer performance
cProfile.run('benchmark_deserializers([1000])', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative').print_stats(10)
```

## 🚀 Future Enhancements

### Planned Features
- **C Extension Benchmarks**: Test native C extension performance
- **Real-World Data**: Benchmark with actual healthcare datasets
- **Regression Testing**: Automated performance regression detection
- **Comparison Framework**: Compare against other FHIR libraries
- **Visualization**: Generate performance charts and graphs

### Integration Opportunities
- **CI/CD Integration**: Automated performance testing in GitHub Actions
- **Performance Monitoring**: Track performance metrics over time
- **Alerting**: Notify on performance regressions
- **Optimization Guidance**: Automated performance recommendations

## 📞 Support

For benchmark-related issues:

1. **Verify Setup**: Ensure Fast-FHIR is properly installed
2. **Check Dependencies**: Verify all required packages are available
3. **Review Output**: Look for error messages or warnings
4. **Compare Baselines**: Check if performance matches expected ranges
5. **Report Issues**: Create GitHub issues for performance problems

The benchmarking suite provides comprehensive performance analysis to ensure Fast-FHIR meets production performance requirements.