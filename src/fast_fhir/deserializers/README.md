# Fast-FHIR Deserializers Package

This package provides comprehensive deserialization functionality for FHIR R5 resources, converting JSON data into Python objects with optional Pydantic validation and high-performance processing.

## Package Structure

```
src/fhir/deserializers/
├── __init__.py                    # Package initialization and exports
├── deserializers.py               # Core deserialization functionality
├── pydantic_models.py             # General Pydantic model definitions
├── pydantic_care_provision.py     # Specialized Pydantic models for care provision
└── README.md                      # This file
```

## Core Components

### 1. FHIRCareProvisionDeserializer

The main deserializer class that handles conversion of JSON data to FHIR resource objects.

```python
from src.fhir.deserializers import FHIRCareProvisionDeserializer

deserializer = FHIRCareProvisionDeserializer(use_pydantic_validation=True)
care_plan = deserializer.deserialize_care_plan(json_data)
```

### 2. Convenience Functions

Type-specific functions for easy deserialization:

```python
from src.fhir.deserializers import (
    deserialize_care_plan,
    deserialize_care_team,
    deserialize_goal,
    deserialize_service_request,
    deserialize_risk_assessment,
    deserialize_vision_prescription,
    deserialize_nutrition_order
)

# Direct deserialization
care_plan = deserialize_care_plan(json_data)
care_team = deserialize_care_team(json_data)
```

### 3. Pydantic Models

Optional Pydantic models for enhanced validation:

```python
from src.fhir.deserializers.pydantic_care_provision import (
    CarePlan, CareTeam, Goal, ServiceRequest
)

# Check if Pydantic is available
from src.fhir.deserializers import PYDANTIC_AVAILABLE
```

## Supported Resource Types

The deserializers package currently supports the following FHIR R5 Care Provision resources:

- **CarePlan** - Care plans and treatment protocols
- **CareTeam** - Care team compositions and roles
- **Goal** - Patient goals and targets
- **ServiceRequest** - Service and procedure requests
- **RiskAssessment** - Risk assessments and predictions
- **VisionPrescription** - Vision prescriptions and lens specifications
- **NutritionOrder** - Nutrition orders and dietary instructions

## Usage Examples

### Basic Deserialization

```python
from src.fhir.deserializers import deserialize_care_plan

# From JSON string
json_string = '''
{
    "resourceType": "CarePlan",
    "id": "example-001",
    "status": "active",
    "intent": "plan",
    "title": "Diabetes Management Plan"
}
'''

care_plan = deserialize_care_plan(json_string)
print(f"Care Plan: {care_plan.title}")
print(f"Status: {care_plan.status}")
```

### Using the Deserializer Class

```python
from src.fhir.deserializers import FHIRCareProvisionDeserializer

deserializer = FHIRCareProvisionDeserializer(use_pydantic_validation=True)

# Deserialize multiple resources
resources = [
    deserializer.deserialize_care_plan(care_plan_json),
    deserializer.deserialize_care_team(care_team_json),
    deserializer.deserialize_goal(goal_json)
]
```

### Error Handling

```python
from src.fhir.deserializers import (
    deserialize_care_plan, 
    FHIRDeserializationError
)

try:
    care_plan = deserialize_care_plan(invalid_json)
except FHIRDeserializationError as e:
    print(f"Deserialization failed: {e}")
```

## Features

### ✅ JSON Support
- Parse from JSON strings or dictionaries
- Comprehensive error handling for malformed JSON
- Support for nested FHIR data structures

### ✅ Validation
- Optional Pydantic validation when available
- FHIR-compliant data type validation
- Resource-specific business rule validation

### ✅ Type Safety
- Type-specific convenience functions
- Runtime type checking
- Clear error messages for type mismatches

### ✅ Performance
- Efficient JSON parsing
- Minimal memory overhead
- Lazy loading of optional dependencies

## Dependencies

### Required
- Python 3.7+
- Standard library modules (json, typing, datetime)

### Optional
- **Pydantic** - For enhanced validation and type checking
  ```bash
  pip install pydantic
  ```

## Integration

The deserializers package integrates seamlessly with other FHIR system components:

- **Resources** (`src/fhir/resources/`) - Target resource classes
- **Datatypes** (`src/fhir/datatypes.py`) - FHIR data type definitions
- **Parser** (`src/fhir/parser.py`) - Main FHIR parsing functionality

## Testing

Run the deserializer tests:

```bash
PYTHONPATH=. python3 tests/test_deserializers.py
```

Run the comprehensive demo:

```bash
PYTHONPATH=. python3 examples/demo_deserializers.py
```

## Future Enhancements

- Support for additional FHIR resource categories
- Performance optimizations with C extensions
- Streaming deserialization for large datasets
- Custom validation rule support
- Schema-based validation