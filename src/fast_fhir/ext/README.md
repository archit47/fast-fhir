# FHIR C Modules Architecture

## Overview

The FHIR C extensions have been completely restructured following modern C development best practices, emphasizing modularity, maintainability, and code quality. This document describes the new architecture and its benefits.

## 🏗️ Architecture Principles

### 1. **Separation of Concerns**
- Each resource has its own header and implementation file
- Common utilities are separated into a shared library
- Test code is isolated from production code
- Build configuration is centralized

### 2. **Single Responsibility Principle**
- Each module handles exactly one FHIR resource type
- Common functionality is abstracted into utilities
- Clear interfaces between modules

### 3. **DRY (Don't Repeat Yourself)**
- Common patterns are implemented once in shared utilities
- Resource-specific code focuses only on unique aspects
- Consistent error handling and memory management

### 4. **Defensive Programming**
- Comprehensive input validation
- Proper error handling and reporting
- Memory safety with bounds checking
- Resource cleanup on all paths

## 📁 Directory Structure

```
src/fhir/ext/
├── common/                          # Shared utilities
│   ├── fhir_common.h               # Common utilities header
│   └── fhir_common.c               # Common utilities implementation
├── resources/                       # Individual resource modules
│   ├── fhir_organization_affiliation.h
│   ├── fhir_organization_affiliation.c
│   ├── fhir_biologically_derived_product.h
│   ├── fhir_biologically_derived_product.c
│   ├── fhir_device_metric.h
│   ├── fhir_device_metric.c
│   ├── fhir_nutrition_product.h
│   ├── fhir_nutrition_product.c
│   ├── fhir_transport.h
│   ├── fhir_transport.c
│   ├── fhir_verification_result.h
│   ├── fhir_verification_result.c
│   ├── fhir_encounter_history.h
│   ├── fhir_encounter_history.c
│   ├── fhir_episode_of_care.h
│   └── fhir_episode_of_care.c
├── tests/                          # Test framework and tests
│   ├── test_framework.h           # Lightweight test framework
│   ├── test_framework.c
│   ├── test_common.c              # Tests for common utilities
│   ├── test_organization_affiliation.c
│   └── test_device_metric.c
├── build/                          # Build artifacts (generated)
│   ├── obj/                       # Object files
│   └── lib/                       # Libraries
├── CMakeLists.txt                  # Modern CMake configuration
├── Makefile                        # Traditional Make configuration
├── .clang-format                   # Code formatting rules
├── .clang-tidy                     # Static analysis rules
├── fhir_new_resources.c           # Legacy monolithic file (deprecated)
└── fhir_new_resources_python.c    # Python bindings
```

## 🔧 Build System

### CMake (Recommended)

Modern CMake configuration with:
- Automatic dependency detection
- Cross-platform compatibility
- Integrated testing
- Static analysis integration
- Documentation generation
- Package creation

```bash
# Configure and build
mkdir build && cd build
cmake ..
make -j$(nproc)

# Run tests
make test

# Generate documentation
make docs

# Create package
make package
```

### Traditional Makefile

For environments without CMake:

```bash
# Build all
make all

# Build with debug symbols
make debug

# Run static analysis
make analyze

# Format code
make format

# Clean build
make clean
```

## 📚 Common Utilities Library

### Error Handling (`fhir_common.h`)

Centralized error management with:
- Structured error information
- Thread-safe error storage
- Detailed error messages with context
- Error code to string conversion

```c
// Set error with context
FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, 
                     "Invalid ID format", "id");

// Get last error
const FHIRError* error = fhir_get_last_error();
if (error) {
    printf("Error: %s in field %s\n", error->message, error->field);
}
```

### Memory Management

Safe memory operations with error handling:
- `fhir_malloc()` - Safe allocation with error reporting
- `fhir_strdup()` - Safe string duplication
- `fhir_calloc()` - Safe zero-initialized allocation
- `fhir_realloc()` - Safe reallocation

```c
char* str = fhir_strdup("test");
if (!str) {
    const FHIRError* error = fhir_get_last_error();
    // Handle error
}
```

### Array Management

Dynamic array utilities:
- `fhir_resize_array()` - Safe array resizing
- `fhir_array_add()` - Add element to array
- `fhir_array_remove()` - Remove element from array
- `fhir_free_pointer_array()` - Free array of pointers

```c
int* array = NULL;
size_t count = 0;

// Add elements
for (int i = 0; i < 10; i++) {
    fhir_array_add((void**)&array, &count, &i, sizeof(int));
}
```

### String Utilities

Safe string operations:
- `fhir_strcmp()` - NULL-safe string comparison
- `fhir_string_trim()` - Trim whitespace
- `fhir_string_to_lower()` - Convert to lowercase
- `fhir_string_is_empty()` - Check if string is empty/NULL

### JSON Utilities

Safe JSON operations:
- `fhir_json_get_string()` - Safe string extraction
- `fhir_json_get_bool()` - Safe boolean extraction
- `fhir_json_add_string()` - Safe string addition

### Validation Utilities

FHIR-specific validation:
- `fhir_validate_id()` - Validate FHIR ID format
- `fhir_validate_uri()` - Validate URI format
- `fhir_validate_date()` - Validate date format
- `fhir_validate_datetime()` - Validate datetime format

### Logging System

Configurable logging with levels:
- `FHIR_LOG_DEBUG()` - Debug messages
- `FHIR_LOG_INFO()` - Informational messages
- `FHIR_LOG_WARN()` - Warning messages
- `FHIR_LOG_ERROR()` - Error messages
- `FHIR_LOG_FATAL()` - Fatal error messages

## 🧩 Resource Module Structure

Each resource module follows a consistent pattern:

### Header File Structure

```c
/**
 * @file fhir_resource_name.h
 * @brief FHIR R5 ResourceName resource C interface
 * @version 1.0.0
 * @date 2024-01-01
 */

#ifndef FHIR_RESOURCE_NAME_H
#define FHIR_RESOURCE_NAME_H

#include "../fhir_datatypes.h"
#include "../fhir_foundation.h"
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// Resource structure definition
typedef struct FHIRResourceName {
    FHIRDomainResource domain_resource;
    // Resource-specific fields...
} FHIRResourceName;

// Core functions
FHIRResourceName* fhir_resource_name_create(const char* id);
void fhir_resource_name_free(FHIRResourceName* resource);
FHIRResourceName* fhir_resource_name_parse(cJSON* json);
cJSON* fhir_resource_name_to_json(const FHIRResourceName* resource);
bool fhir_resource_name_validate(const FHIRResourceName* resource);

// Helper functions
bool fhir_resource_name_is_active(const FHIRResourceName* resource);
// ... other helpers

#ifdef __cplusplus
}
#endif

#endif /* FHIR_RESOURCE_NAME_H */
```

### Implementation File Structure

```c
/**
 * @file fhir_resource_name.c
 * @brief FHIR R5 ResourceName resource C implementation
 */

#include "fhir_resource_name.h"
#include "../common/fhir_common.h"
#include <stdlib.h>
#include <string.h>

// Private helper functions
static bool init_base_resource(FHIRResourceName* resource, const char* id);
static void free_resource_arrays(FHIRResourceName* resource);

// Public API implementation
FHIRResourceName* fhir_resource_name_create(const char* id) {
    if (!fhir_validate_id(id)) {
        FHIR_SET_FIELD_ERROR(FHIR_ERROR_VALIDATION_FAILED, 
                             "Invalid ID format", "id");
        return NULL;
    }
    
    FHIRResourceName* resource = fhir_calloc(1, sizeof(FHIRResourceName));
    if (!resource) {
        return NULL;
    }
    
    if (!init_base_resource(resource, id)) {
        fhir_free(resource);
        return NULL;
    }
    
    return resource;
}

// ... rest of implementation
```

## 🧪 Testing Framework

### Lightweight Test Framework

Custom test framework designed for C code:
- Simple assertion macros
- Test statistics tracking
- Memory leak detection integration
- Cross-platform compatibility

```c
#include "test_framework.h"

bool test_resource_creation(void) {
    FHIRResourceName* resource = fhir_resource_name_create("test-123");
    ASSERT_NOT_NULL(resource);
    ASSERT_STR_EQ("ResourceName", resource->domain_resource.resource.resource_type);
    ASSERT_STR_EQ("test-123", resource->domain_resource.resource.id);
    
    fhir_resource_name_free(resource);
    return true;
}

int main(void) {
    TEST_INIT();
    RUN_TEST(test_resource_creation);
    TEST_FINALIZE();
    return 0;
}
```

### Test Categories

1. **Unit Tests** - Test individual functions
2. **Integration Tests** - Test module interactions
3. **Memory Tests** - Valgrind integration for leak detection
4. **Performance Tests** - Benchmark critical operations

## 🔍 Code Quality Tools

### Static Analysis

- **Clang-Tidy**: Comprehensive static analysis
- **Cppcheck**: Additional static analysis
- **Compiler Warnings**: Strict warning levels enabled

### Code Formatting

- **Clang-Format**: Consistent code formatting
- **Custom Rules**: Medical software coding standards

### Documentation

- **Doxygen**: API documentation generation
- **Inline Comments**: Comprehensive code documentation

## 🚀 Performance Optimizations

### Memory Management

- **Pool Allocation**: For frequently allocated objects
- **Reference Counting**: For shared objects
- **Copy-on-Write**: For large data structures

### Parsing Optimization

- **Streaming Parser**: For large JSON documents
- **Validation Caching**: Cache validation results
- **Lazy Loading**: Load data only when needed

### Compilation Optimization

- **Link-Time Optimization**: Enabled in release builds
- **Profile-Guided Optimization**: Available for critical paths
- **Architecture-Specific**: Optimized for target platforms

## 📦 Packaging and Distribution

### Library Packaging

- **Static Libraries**: For embedding in applications
- **Shared Libraries**: For system-wide installation
- **Header-Only**: For template-heavy code

### Platform Support

- **Linux**: Native support with package managers
- **macOS**: Homebrew integration
- **Windows**: MSYS2/MinGW support
- **Cross-Compilation**: ARM, RISC-V support

### Python Integration

- **Extension Modules**: Native Python extensions
- **Wheel Packages**: Easy pip installation
- **Conda Packages**: Scientific Python ecosystem

## 🔧 Development Workflow

### Local Development

```bash
# Clone and setup
git clone <repository>
cd fhir-c-extensions

# Build and test
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make -j$(nproc)
make test

# Format and analyze
make format
make analyze
```

### Continuous Integration

- **GitHub Actions**: Automated testing
- **Multiple Platforms**: Linux, macOS, Windows
- **Multiple Compilers**: GCC, Clang, MSVC
- **Coverage Reports**: Code coverage tracking

### Release Process

1. **Version Bump**: Update version numbers
2. **Changelog**: Update CHANGELOG.md
3. **Testing**: Full test suite on all platforms
4. **Documentation**: Update API documentation
5. **Packaging**: Create distribution packages
6. **Tagging**: Git tag for release
7. **Distribution**: Upload to package repositories

## 🎯 Benefits of New Architecture

### For Developers

- **Easier Maintenance**: Clear module boundaries
- **Faster Compilation**: Incremental builds
- **Better Testing**: Isolated unit tests
- **Code Reuse**: Common utilities library

### For Users

- **Better Performance**: Optimized implementations
- **Smaller Footprint**: Link only needed modules
- **Better Reliability**: Comprehensive testing
- **Easier Integration**: Clear APIs

### For the Project

- **Scalability**: Easy to add new resources
- **Quality**: Consistent coding standards
- **Documentation**: Comprehensive API docs
- **Community**: Easier for contributors

## 🔮 Future Enhancements

### Short Term

- Complete all resource implementations
- Add more comprehensive tests
- Improve documentation
- Performance benchmarking

### Medium Term

- Add more FHIR R5 resources
- Implement FHIR search parameters
- Add validation against FHIR schemas
- Create language bindings (Rust, Go, etc.)

### Long Term

- Real-time FHIR subscriptions
- FHIR server implementation
- Cloud-native optimizations
- Machine learning integration

## 📖 Getting Started

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get install build-essential cmake libcjson-dev python3-dev

# macOS
brew install cmake cjson python3

# CentOS/RHEL
sudo yum install gcc cmake cjson-devel python3-devel
```

### Quick Start

```bash
# Build
mkdir build && cd build
cmake ..
make -j$(nproc)

# Test
make test

# Install
sudo make install
```

### Example Usage

```c
#include <fhir/resources/fhir_organization_affiliation.h>

int main() {
    // Create resource
    FHIROrganizationAffiliation* affiliation = 
        fhir_organization_affiliation_create("test-123");
    
    if (!affiliation) {
        const FHIRError* error = fhir_get_last_error();
        printf("Error: %s\n", error->message);
        return 1;
    }
    
    // Use resource...
    
    // Clean up
    fhir_organization_affiliation_free(affiliation);
    return 0;
}
```

This new modular architecture provides a solid foundation for building high-quality, maintainable FHIR implementations in C while following industry best practices for medical software development.