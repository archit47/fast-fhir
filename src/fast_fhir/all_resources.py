"""Complete FHIR R5 resource registry and factory."""

from typing import Dict, List, Optional, Type, Union, Any
import json
from enum import Enum

# Import all resource modules
from .foundation import (
    FHIRPatient, FHIRPractitioner, FHIROrganization, 
    HAS_C_FOUNDATION
)
from .terminology import (
    FHIRCodeSystem, FHIRValueSet, FHIRConceptMap, FHIRBinary, FHIRBundle
)

# Import new resource classes
from .resources.organization_affiliation import OrganizationAffiliation
from .resources.biologically_derived_product import BiologicallyDerivedProduct
from .resources.device_metric import DeviceMetric
from .resources.nutrition_product import NutritionProduct
from .resources.transport import Transport
from .resources.appointment_response import AppointmentResponse
from .resources.verification_result import VerificationResult
from .resources.encounter_history import EncounterHistory
from .resources.episode_of_care import EpisodeOfCare

# Care Provision Resources
from .resources.care_plan import CarePlan
from .resources.care_team import CareTeam
from .resources.goal import Goal
from .resources.service_request import ServiceRequest
from .resources.nutrition_order import NutritionOrder
from .resources.risk_assessment import RiskAssessment
from .resources.vision_prescription import VisionPrescription

try:
    import fhir_clinical_c
    import fhir_medication_c
    import fhir_workflow_c
    HAS_ALL_C_EXTENSIONS = True
except ImportError:
    HAS_ALL_C_EXTENSIONS = False


class FHIRResourceCategory(Enum):
    """FHIR resource categories."""
    FOUNDATION = "foundation"
    CLINICAL = "clinical"
    MEDICATION = "medication"
    WORKFLOW = "workflow"
    FINANCIAL = "financial"
    SPECIALIZED = "specialized"


class FHIRResourceRegistry:
    """Registry for all FHIR R5 resource types."""
    
    # Complete FHIR R5 resource type mapping based on HL7 specification
    RESOURCE_TYPES = {
        # Foundation Resources (Base)
        "Patient": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIRPatient},
        "Practitioner": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIRPractitioner},
        "PractitionerRole": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "Organization": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIROrganization},
        "OrganizationAffiliation": {"category": FHIRResourceCategory.FOUNDATION, "class": OrganizationAffiliation},
        "Location": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "HealthcareService": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "Endpoint": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "RelatedPerson": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "Person": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "Group": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        
        # Foundation Resources (Terminology)
        "CodeSystem": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIRCodeSystem},
        "ValueSet": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIRValueSet},
        "ConceptMap": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIRConceptMap},
        "NamingSystem": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        
        # Foundation Resources (Infrastructure)
        "Binary": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIRBinary},
        "Bundle": {"category": FHIRResourceCategory.FOUNDATION, "class": FHIRBundle},
        "Composition": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "DocumentManifest": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "DocumentReference": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "MessageDefinition": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "MessageHeader": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "OperationDefinition": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "OperationOutcome": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "Parameters": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "Subscription": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "SubscriptionStatus": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        "SubscriptionTopic": {"category": FHIRResourceCategory.FOUNDATION, "class": None},
        
        # Clinical Resources (Summary)
        "AllergyIntolerance": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "Condition": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "Procedure": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "FamilyMemberHistory": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "ClinicalImpression": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "DetectedIssue": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        
        # Clinical Resources (Diagnostics)
        "Observation": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "Media": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "DiagnosticReport": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "Specimen": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "BodyStructure": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "ImagingStudy": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "ImagingSelection": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        "MolecularSequence": {"category": FHIRResourceCategory.CLINICAL, "class": None},
        
        # Clinical Resources (Care Provision)
        "CarePlan": {"category": FHIRResourceCategory.CLINICAL, "class": CarePlan},
        "CareTeam": {"category": FHIRResourceCategory.CLINICAL, "class": CareTeam},
        "Goal": {"category": FHIRResourceCategory.CLINICAL, "class": Goal},
        "ServiceRequest": {"category": FHIRResourceCategory.CLINICAL, "class": ServiceRequest},
        "NutritionOrder": {"category": FHIRResourceCategory.CLINICAL, "class": NutritionOrder},
        "RiskAssessment": {"category": FHIRResourceCategory.CLINICAL, "class": RiskAssessment},
        "VisionPrescription": {"category": FHIRResourceCategory.CLINICAL, "class": VisionPrescription},
        
        # Medication Resources
        "Medication": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "MedicationAdministration": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "MedicationDispense": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "MedicationRequest": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "MedicationStatement": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "MedicationKnowledge": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "Immunization": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "ImmunizationEvaluation": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        "ImmunizationRecommendation": {"category": FHIRResourceCategory.MEDICATION, "class": None},
        
        # Workflow Resources (Request & Response)
        "Appointment": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "AppointmentResponse": {"category": FHIRResourceCategory.WORKFLOW, "class": AppointmentResponse},
        "Schedule": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "Slot": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "Encounter": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "EncounterHistory": {"category": FHIRResourceCategory.WORKFLOW, "class": EncounterHistory},
        "EpisodeOfCare": {"category": FHIRResourceCategory.WORKFLOW, "class": EpisodeOfCare},
        "Flag": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "List": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "Library": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "Task": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "Transport": {"category": FHIRResourceCategory.WORKFLOW, "class": Transport},
        
        # Workflow Resources (Definition)
        "ActivityDefinition": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "PlanDefinition": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "Questionnaire": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        "QuestionnaireResponse": {"category": FHIRResourceCategory.WORKFLOW, "class": None},
        
        # Financial Resources (Support)
        "Coverage": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "CoverageEligibilityRequest": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "CoverageEligibilityResponse": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "EnrollmentRequest": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "EnrollmentResponse": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        
        # Financial Resources (Billing)
        "Account": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "ChargeItem": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "ChargeItemDefinition": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "Contract": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "Invoice": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        
        # Financial Resources (Payment)
        "PaymentNotice": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "PaymentReconciliation": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        
        # Financial Resources (General)
        "Claim": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "ClaimResponse": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        "ExplanationOfBenefit": {"category": FHIRResourceCategory.FINANCIAL, "class": None},
        
        # Specialized Resources (Public Health & Research)
        "ResearchStudy": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "ResearchSubject": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "AdverseEvent": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        
        # Specialized Resources (Definitional Artifacts)
        "Evidence": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "EvidenceReport": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "EvidenceVariable": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "Citation": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        
        # Specialized Resources (Quality Reporting & Testing)
        "Measure": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "MeasureReport": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "TestReport": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "TestScript": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        
        # Specialized Resources (Medication Definition)
        "Substance": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "SubstanceDefinition": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "SubstanceNucleicAcid": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "SubstancePolymer": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "SubstanceProtein": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "SubstanceReferenceInformation": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "SubstanceSourceMaterial": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "BiologicallyDerivedProduct": {"category": FHIRResourceCategory.SPECIALIZED, "class": BiologicallyDerivedProduct},
        "NutritionProduct": {"category": FHIRResourceCategory.SPECIALIZED, "class": NutritionProduct},
        
        # Specialized Resources (Devices)
        "Device": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "DeviceDefinition": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "DeviceMetric": {"category": FHIRResourceCategory.SPECIALIZED, "class": DeviceMetric},
        "DeviceRequest": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "DeviceUsage": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        
        # Specialized Resources (Conformance)
        "CapabilityStatement": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "StructureDefinition": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "StructureMap": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "ImplementationGuide": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "SearchParameter": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "CompartmentDefinition": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "ExampleScenario": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "GraphDefinition": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        
        # Specialized Resources (Terminology)
        "TerminologyCapabilities": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        
        # Specialized Resources (Security)
        "AuditEvent": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "Provenance": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "Consent": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
        "VerificationResult": {"category": FHIRResourceCategory.SPECIALIZED, "class": VerificationResult},
        
        # Specialized Resources (Documents)
        "CatalogEntry": {"category": FHIRResourceCategory.SPECIALIZED, "class": None},
    }
    
    @classmethod
    def get_resource_info(cls, resource_type: str) -> Optional[Dict[str, Any]]:
        """Get resource information by type name."""
        return cls.RESOURCE_TYPES.get(resource_type)
    
    @classmethod
    def get_resource_category(cls, resource_type: str) -> Optional[FHIRResourceCategory]:
        """Get resource category by type name."""
        info = cls.get_resource_info(resource_type)
        return info["category"] if info else None
    
    @classmethod
    def get_resource_class(cls, resource_type: str) -> Optional[Type]:
        """Get resource class by type name."""
        info = cls.get_resource_info(resource_type)
        return info["class"] if info else None
    
    @classmethod
    def is_valid_resource_type(cls, resource_type: str) -> bool:
        """Check if resource type is valid."""
        return resource_type in cls.RESOURCE_TYPES
    
    @classmethod
    def get_resources_by_category(cls, category: FHIRResourceCategory) -> List[str]:
        """Get all resource types in a category."""
        return [
            resource_type for resource_type, info in cls.RESOURCE_TYPES.items()
            if info["category"] == category
        ]
    
    @classmethod
    def get_implemented_resources(cls) -> List[str]:
        """Get list of resource types with Python implementations."""
        return [
            resource_type for resource_type, info in cls.RESOURCE_TYPES.items()
            if info["class"] is not None
        ]
    
    @classmethod
    def get_total_resource_count(cls) -> int:
        """Get total number of FHIR R5 resource types."""
        return len(cls.RESOURCE_TYPES)
    
    @classmethod
    def get_implementation_coverage(cls) -> float:
        """Get percentage of implemented resource types."""
        implemented = len(cls.get_implemented_resources())
        total = cls.get_total_resource_count()
        return (implemented / total) * 100.0


class FHIRResourceFactory:
    """Factory for creating FHIR resources."""
    
    def __init__(self, use_c_extensions: bool = True):
        """Initialize resource factory."""
        self.use_c_extensions = use_c_extensions and HAS_ALL_C_EXTENSIONS
        self.registry = FHIRResourceRegistry()
    
    def create_resource(self, resource_type: str, id: Optional[str] = None, **kwargs) -> Optional[Any]:
        """Create a FHIR resource by type."""
        resource_class = self.registry.get_resource_class(resource_type)
        if resource_class:
            return resource_class(id, use_c_extensions=self.use_c_extensions, **kwargs)
        return None
    
    def parse_resource(self, data: Union[str, Dict[str, Any]]) -> Optional[Any]:
        """Parse FHIR resource from JSON data."""
        if isinstance(data, str):
            data = json.loads(data)
        
        resource_type = data.get("resourceType")
        if not resource_type:
            raise ValueError("Missing resourceType in FHIR data")
        
        resource_class = self.registry.get_resource_class(resource_type)
        if resource_class:
            return resource_class.from_dict(data)
        
        # Return generic dict for unimplemented resources
        return data
    
    def get_performance_info(self) -> Dict[str, Any]:
        """Get performance information about the factory."""
        return {
            "c_extensions_available": HAS_ALL_C_EXTENSIONS,
            "c_extensions_enabled": self.use_c_extensions,
            "total_resource_types": self.registry.get_total_resource_count(),
            "implemented_resource_types": len(self.registry.get_implemented_resources()),
            "implementation_coverage": f"{self.registry.get_implementation_coverage():.1f}%",
            "categories": {
                category.value: len(self.registry.get_resources_by_category(category))
                for category in FHIRResourceCategory
            }
        }


# Utility functions
def get_all_fhir_resource_types() -> List[str]:
    """Get list of all FHIR R5 resource types."""
    return list(FHIRResourceRegistry.RESOURCE_TYPES.keys())


def get_fhir_resource_categories() -> Dict[str, List[str]]:
    """Get FHIR resource types organized by category."""
    result = {}
    for category in FHIRResourceCategory:
        result[category.value] = FHIRResourceRegistry.get_resources_by_category(category)
    return result


def is_fhir_resource_implemented(resource_type: str) -> bool:
    """Check if a FHIR resource type has a Python implementation."""
    return FHIRResourceRegistry.get_resource_class(resource_type) is not None


def get_fhir_implementation_status() -> Dict[str, Any]:
    """Get comprehensive implementation status."""
    registry = FHIRResourceRegistry()
    
    return {
        "total_resources": registry.get_total_resource_count(),
        "implemented_resources": len(registry.get_implemented_resources()),
        "coverage_percentage": registry.get_implementation_coverage(),
        "c_extensions_available": HAS_ALL_C_EXTENSIONS,
        "by_category": {
            category.value: {
                "total": len(registry.get_resources_by_category(category)),
                "implemented": len([
                    rt for rt in registry.get_resources_by_category(category)
                    if registry.get_resource_class(rt) is not None
                ])
            }
            for category in FHIRResourceCategory
        },
        "implemented_list": registry.get_implemented_resources(),
        "not_implemented_list": [
            rt for rt in registry.RESOURCE_TYPES.keys()
            if registry.get_resource_class(rt) is None
        ]
    }


# Export all public functions and classes
__all__ = [
    'FHIRResourceCategory', 'FHIRResourceRegistry', 'FHIRResourceFactory',
    'get_all_fhir_resource_types', 'get_fhir_resource_categories',
    'is_fhir_resource_implemented', 'get_fhir_implementation_status',
    'HAS_ALL_C_EXTENSIONS'
]