"""
FHIR R5 Deserializers Package

This package provides comprehensive deserialization functionality for FHIR R5 resources,
including JSON to Python object conversion, Pydantic validation, and type-specific utilities.

Main Components:
- deserializers: Core deserialization functionality
- pydantic_models: General Pydantic model definitions
- pydantic_care_provision: Specialized Pydantic models for care provision resources

Usage:
    from fhir.deserializers import FHIRCareProvisionDeserializer
    from fhir.deserializers.pydantic_care_provision import CarePlan, CareTeam
"""

# Import main deserializer functionality
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
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False

# Import general Pydantic models
try:
    from .pydantic_models import (
        FHIRResource,
        FHIRElement,
        FHIRExtension
    )
except ImportError:
    pass

__all__ = [
    # Core deserializer
    'FHIRCareProvisionDeserializer',
    'FHIRDeserializationError',
    
    # Convenience functions
    'deserialize_care_provision_resource',
    'deserialize_care_plan',
    'deserialize_care_team', 
    'deserialize_goal',
    'deserialize_service_request',
    'deserialize_risk_assessment',
    'deserialize_vision_prescription',
    'deserialize_nutrition_order',
    
    # Pydantic availability flag
    'PYDANTIC_AVAILABLE'
]

# Add Pydantic models to __all__ if available
if PYDANTIC_AVAILABLE:
    __all__.extend([
        'CarePlan',
        'CareTeam',
        'Goal', 
        'ServiceRequest',
        'RiskAssessment',
        'VisionPrescription',
        'NutritionOrder',
        'FHIRResource',
        'FHIRElement',
        'FHIRExtension'
    ])