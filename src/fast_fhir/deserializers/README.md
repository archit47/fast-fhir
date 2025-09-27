# Fast-FHIR Deserializers Package

This package provides comprehensive deserialization functionality for FHIR R5 resources, converting JSON data into Python objects with optional Pydantic validation and high-performance processing.

**Now supports both Foundation and Care Provision resources!**

## Package Structure

```
src/fast_fhir/deserializers/
├── __init__.py                      # Package initialization and exports
├── deserializers.py                 # Care provision deserialization functionality
├── foundation_deserializers.py     # Foundation resource deserialization
├── entities_deserializers.py       # Entities resource deserialization
├── pydantic_models.py               # General Pydantic model definitions
├── pydantic_care_provision.py       # Pydantic models for care provision resources
├── pydantic_foundation.py           # Pydantic models for foundation resources
├── pydantic_entities.py             # Pydantic models for entities resources
└── README.md                        # This file
```

## Core Components

### 1. Foundation Resource Deserializer

The main deserializer for core FHIR resources like Patient, Practitioner, etc.

```python
from fast_fhir.deserializers import FHIRFoundationDeserializer

deserializer = FHIRFoundationDeserializer(use_pydantic_validation=True)
patient = deserializer.deserialize_patient(json_data)
practitioner = deserializer.deserialize_practitioner(json_data)
```

### 2. Entities Resource Deserializer

Deserializer for entities and organizational resources.

```python
from fast_fhir.deserializers import FHIREntitiesDeserializer

deserializer = FHIREntitiesDeserializer(use_pydantic_validation=True)
organization = deserializer.deserialize_organization(json_data)
location = deserializer.deserialize_location(json_data)
```

### 3. Care Provision Deserializer

Specialized deserializer for care provision resources.

```python
from fast_fhir.deserializers import FHIRCareProvisionDeserializer

deserializer = FHIRCareProvisionDeserializer(use_pydantic_validation=True)
care_plan = deserializer.deserialize_care_plan(json_data)
```

### 4. Convenience Functions

Type-specific functions for easy deserialization:

```python
# Foundation resources
from fast_fhir.deserializers import (
    deserialize_patient,
    deserialize_practitioner,
    deserialize_practitioner_role,
    deserialize_encounter,
    deserialize_person,
    deserialize_related_person
)

# Entities resources
from fast_fhir.deserializers import (
    deserialize_organization,
    deserialize_location,
    deserialize_healthcare_service,
    deserialize_endpoint,
    deserialize_device,
    deserialize_group,
    deserialize_substance,
    deserialize_organization_affiliation
)

# Care provision resources
from fast_fhir.deserializers import (
    deserialize_care_plan,
    deserialize_care_team,
    deserialize_goal,
    deserialize_service_request,
    deserialize_risk_assessment,
    deserialize_vision_prescription,
    deserialize_nutrition_order
)

# Direct deserialization
patient = deserialize_patient(json_data)
organization = deserialize_organization(json_data)
care_plan = deserialize_care_plan(json_data)
```

### 5. Pydantic Models

Optional Pydantic models for enhanced validation:

```python
# Foundation resource models
from fast_fhir.deserializers.pydantic_foundation import (
    PatientModel, PractitionerModel, EncounterModel
)

# Entities resource models
from fast_fhir.deserializers.pydantic_entities import (
    OrganizationModel, LocationModel, DeviceModel
)

# Care provision resource models
from fast_fhir.deserializers.pydantic_care_provision import (
    CarePlan, CareTeam, Goal, ServiceRequest
)

# Check if Pydantic is available
from fast_fhir.deserializers import (
    PYDANTIC_AVAILABLE,
    PYDANTIC_FOUNDATION_AVAILABLE,
    PYDANTIC_ENTITIES_AVAILABLE,
    PYDANTIC_CARE_PROVISION_AVAILABLE
)
```

## Supported Resource Types

### Foundation Resources
Core FHIR resources for healthcare entities:

- **Patient** - Patient demographics and administrative information
- **Practitioner** - Healthcare provider information and credentials
- **PractitionerRole** - Practitioner roles, specialties, and availability
- **Encounter** - Healthcare encounters, visits, and episodes
- **Person** - Person demographics (broader scope than Patient)
- **RelatedPerson** - Persons related to patients (family, caregivers, etc.)

### Foundation Resources (continued)
- **Group** - Collections of entities (patients, practitioners, etc.)

### Entities Resources
Resources for healthcare organizations and infrastructure:

- **Organization** - Healthcare organizations, departments, and entities
- **OrganizationAffiliation** - Relationships between organizations
- **Location** - Physical locations and facilities
- **HealthcareService** - Services provided by organizations
- **Endpoint** - Technical endpoints for system integration
- **Device** - Medical devices and equipment
- **DeviceMetric** - Device measurements and metrics
- **Substance** - Chemical substances and materials
- **BiologicallyDerivedProduct** - Blood products, tissues, organs
- **NutritionProduct** - Nutritional products and supplements

### Care Provision Resources
Resources for care planning and coordination:

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