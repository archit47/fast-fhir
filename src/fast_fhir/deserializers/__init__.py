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
    deserialize_related_person,
    deserialize_group
)

# Import entities deserializer functionality
from .entities_deserializers import (
    FHIREntitiesDeserializer,
    FHIREntitiesDeserializationError,
    deserialize_organization,
    deserialize_location,
    deserialize_healthcare_service,
    deserialize_endpoint,
    deserialize_device,
    deserialize_substance,
    deserialize_organization_affiliation,
    deserialize_biologically_derived_product,
    deserialize_nutrition_product,
    deserialize_device_metric
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
        GroupModel,
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

# Import Pydantic models for entities resources
try:
    from .pydantic_entities import (
        OrganizationModel,
        LocationModel,
        HealthcareServiceModel,
        EndpointModel,
        DeviceModel,
        SubstanceModel,
        OrganizationAffiliationModel,
        OrganizationContact,
        LocationPosition,
        DeviceUdiCarrier,
        OrganizationType,
        LocationStatus,
        DeviceStatus
    )
    PYDANTIC_ENTITIES_AVAILABLE = True
except ImportError:
    PYDANTIC_ENTITIES_AVAILABLE = False

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
                     PYDANTIC_ENTITIES_AVAILABLE or
                     PYDANTIC_GENERAL_AVAILABLE)

__all__ = [
    # Core deserializers
    'FHIRCareProvisionDeserializer',
    'FHIRFoundationDeserializer',
    'FHIREntitiesDeserializer',
    'FHIRDeserializationError',
    'FHIRFoundationDeserializationError',
    'FHIREntitiesDeserializationError',
    
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
    'deserialize_group',
    
    # Entities convenience functions
    'deserialize_organization',
    'deserialize_location',
    'deserialize_healthcare_service',
    'deserialize_endpoint',
    'deserialize_device',
    'deserialize_substance',
    'deserialize_organization_affiliation',
    'deserialize_biologically_derived_product',
    'deserialize_nutrition_product',
    'deserialize_device_metric',
    
    # Pydantic availability flags
    'PYDANTIC_AVAILABLE',
    'PYDANTIC_CARE_PROVISION_AVAILABLE',
    'PYDANTIC_FOUNDATION_AVAILABLE',
    'PYDANTIC_ENTITIES_AVAILABLE',
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
        'GroupModel',
        'HumanName',
        'ContactPoint',
        'Address',
        'Identifier',
        'Reference',
        'CodeableConcept',
        'AdministrativeGender'
    ])

# Add Entities Pydantic models to __all__ if available
if PYDANTIC_ENTITIES_AVAILABLE:
    __all__.extend([
        'OrganizationModel',
        'LocationModel',
        'HealthcareServiceModel',
        'EndpointModel',
        'DeviceModel',
        'SubstanceModel',
        'OrganizationAffiliationModel',
        'OrganizationContact',
        'LocationPosition',
        'DeviceUdiCarrier',
        'OrganizationType',
        'LocationStatus',
        'DeviceStatus'
    ])

# Add General Pydantic models to __all__ if available
if PYDANTIC_GENERAL_AVAILABLE:
    __all__.extend([
        'FHIRResource',
        'FHIRElement',
        'FHIRExtension'
    ])