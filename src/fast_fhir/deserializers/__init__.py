"""
FHIR R5 Deserializers Package

This package provides comprehensive deserialization functionality for FHIR R5 resources,
including JSON to Python object conversion, Pydantic validation, and type-specific utilities.

Main Components:
- deserializers: Core deserialization functionality for care provision resources
- foundation_deserializers: Deserialization for foundation resources (Patient, Practitioner, etc.)
- pydantic_models: General Pydantic model definitions
- pydantic_care_provision: Specialized Pydantic models for care provision resources
- pydantic_foundation: Specialized Pydantic models for foundation resources

Usage:
    # Care provision resources
    from fast_fhir.deserializers import FHIRCareProvisionDeserializer
    from fast_fhir.deserializers.pydantic_care_provision import CarePlan, CareTeam
    
    # Foundation resources
    from fast_fhir.deserializers import FHIRFoundationDeserializer
    from fast_fhir.deserializers import deserialize_patient, deserialize_practitioner
"""

# Import care provision deserializer functionality
from .deserializers import (
    FHIRCareProvisionDeserializer,
    FHIRDeserializationError,
    deserialize_care_provision_resource,
    deserialize_care_plan,
    deserialize_care_team,
    deserialize_goal,
    deserialize_service_request,
    deserialize_risk_assessment,
    deserialize_vision_prescription,
    deserialize_nutrition_order
)

# Import foundation deserializer functionality
from .foundation_deserializers import (
    FHIRFoundationDeserializer,
    FHIRFoundationDeserializationError,
    deserialize_patient,
    deserialize_practitioner,
    deserialize_practitioner_role,
    deserialize_encounter,
    deserialize_person,
    deserialize_related_person
)

# Import Pydantic models for care provision resources
try:
    from .pydantic_care_provision import (
        CarePlan,
        CareTeam,
        Goal,
        ServiceRequest,
        RiskAssessment,
        VisionPrescription,
        NutritionOrder
    )
    PYDANTIC_CARE_PROVISION_AVAILABLE = True
except ImportError:
    PYDANTIC_CARE_PROVISION_AVAILABLE = False

# Import Pydantic models for foundation resources
try:
    from .pydantic_foundation import (
        PatientModel,
        PractitionerModel,
        PractitionerRoleModel,
        EncounterModel,
        PersonModel,
        RelatedPersonModel,
        HumanName,
        ContactPoint,
        Address,
        Identifier,
        Reference,
        CodeableConcept,
        AdministrativeGender
    )
    PYDANTIC_FOUNDATION_AVAILABLE = True
except ImportError:
    PYDANTIC_FOUNDATION_AVAILABLE = False

# Import general Pydantic models
try:
    from .pydantic_models import (
        FHIRResource,
        FHIRElement,
        FHIRExtension
    )
    PYDANTIC_GENERAL_AVAILABLE = True
except ImportError:
    PYDANTIC_GENERAL_AVAILABLE = False

# Overall Pydantic availability
PYDANTIC_AVAILABLE = (PYDANTIC_CARE_PROVISION_AVAILABLE or 
                     PYDANTIC_FOUNDATION_AVAILABLE or 
                     PYDANTIC_GENERAL_AVAILABLE)

__all__ = [
    # Core deserializers
    'FHIRCareProvisionDeserializer',
    'FHIRFoundationDeserializer',
    'FHIRDeserializationError',
    'FHIRFoundationDeserializationError',
    
    # Care provision convenience functions
    'deserialize_care_provision_resource',
    'deserialize_care_plan',
    'deserialize_care_team', 
    'deserialize_goal',
    'deserialize_service_request',
    'deserialize_risk_assessment',
    'deserialize_vision_prescription',
    'deserialize_nutrition_order',
    
    # Foundation convenience functions
    'deserialize_patient',
    'deserialize_practitioner',
    'deserialize_practitioner_role',
    'deserialize_encounter',
    'deserialize_person',
    'deserialize_related_person',
    
    # Pydantic availability flags
    'PYDANTIC_AVAILABLE',
    'PYDANTIC_CARE_PROVISION_AVAILABLE',
    'PYDANTIC_FOUNDATION_AVAILABLE',
    'PYDANTIC_GENERAL_AVAILABLE'
]

# Add Care Provision Pydantic models to __all__ if available
if PYDANTIC_CARE_PROVISION_AVAILABLE:
    __all__.extend([
        'CarePlan',
        'CareTeam',
        'Goal', 
        'ServiceRequest',
        'RiskAssessment',
        'VisionPrescription',
        'NutritionOrder'
    ])

# Add Foundation Pydantic models to __all__ if available
if PYDANTIC_FOUNDATION_AVAILABLE:
    __all__.extend([
        'PatientModel',
        'PractitionerModel',
        'PractitionerRoleModel',
        'EncounterModel',
        'PersonModel',
        'RelatedPersonModel',
        'HumanName',
        'ContactPoint',
        'Address',
        'Identifier',
        'Reference',
        'CodeableConcept',
        'AdministrativeGender'
    ])

# Add General Pydantic models to __all__ if available
if PYDANTIC_GENERAL_AVAILABLE:
    __all__.extend([
        'FHIRResource',
        'FHIRElement',
        'FHIRExtension'
    ])