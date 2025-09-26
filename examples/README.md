# FHIR R5 Examples and Demonstrations

This directory contains example scripts and demonstration files for the FHIR R5 implementation.

## Files

### Demo Scripts

- **`demo_comprehensive.py`** - Complete FHIR R5 system demonstration showing all major features and capabilities
- **`demo_care_provision.py`** - Demonstrates the Care Provision resources (CarePlan, CareTeam, Goal, ServiceRequest, NutritionOrder, RiskAssessment, VisionPrescription)
- **`demo_deserializers.py`** - Demonstrates the Pydantic-based JSON deserializers for Care Provision resources

### Test Implementation

- **`test_implementation.py`** - Implementation testing and validation script

## Running the Examples

To run any of the demo scripts, navigate to the project root and use:

```bash
# From the project root directory
PYTHONPATH=. python3 examples/demo_comprehensive.py
PYTHONPATH=. python3 examples/demo_care_provision.py
PYTHONPATH=. python3 examples/demo_deserializers.py
PYTHONPATH=. python3 examples/test_implementation.py
```

## What These Examples Demonstrate

### Comprehensive System Demo
- Complete FHIR R5 system overview
- All major resource categories and types
- Parser and factory demonstrations
- Data type validation and creation
- Resource relationships and workflows
- Performance and capability information

### Care Provision Resources Demo
- Creation and manipulation of all 7 Care Provision resources
- Status management and validation
- Business logic methods (is_active, is_urgent, etc.)
- Resource relationships and references
- Real-world healthcare scenarios

### Deserializers Demo
- JSON-to-object conversion with validation
- Pydantic model integration
- Error handling and validation
- Complex nested data structures
- Type-safe deserialization

### Test Implementation
- Comprehensive testing of resource functionality
- Validation testing
- Integration testing
- Performance testing

## Note

These files are excluded from version control via `.gitignore` as they are primarily for development, testing, and demonstration purposes.