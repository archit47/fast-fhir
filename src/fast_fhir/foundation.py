"""Python wrapper for FHIR R5 Foundation resources implemented in C."""

from typing import Any, Dict, List, Optional, Union
import json

try:
    import fhir_foundation_c
    HAS_C_FOUNDATION = True
except ImportError:
    HAS_C_FOUNDATION = False

from .datatypes import FHIRDataType, HAS_C_DATATYPES


class FHIRElement(FHIRDataType):
    """Base class for all FHIR elements."""
    
    def __init__(self, use_c_extensions: bool = True):
        """Initialize FHIR element."""
        super().__init__(use_c_extensions)
        self.id = None
        self.extension = []
    
    def validate(self) -> bool:
        """Validate the element."""
        return True


class FHIRResource(FHIRDataType):
    """Base class for all FHIR resources."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR resource."""
        super().__init__(use_c_extensions)
        self.id = id
        self.meta = None
        self.implicit_rules = None
        self.language = None
        self.text = None
        self.contained = []
        self.extension = []
        self.modifier_extension = []
    
    def validate(self) -> bool:
        """Validate the resource."""
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {}
        if self.id:
            result['id'] = self.id
        if self.meta:
            result['meta'] = self.meta
        if self.implicit_rules:
            result['implicitRules'] = self.implicit_rules
        if self.language:
            result['language'] = self.language
        if self.text:
            result['text'] = self.text
        if self.contained:
            result['contained'] = self.contained
        if self.extension:
            result['extension'] = self.extension
        if self.modifier_extension:
            result['modifierExtension'] = self.modifier_extension
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRResource':
        """Create from dictionary representation."""
        resource = cls(id=data.get('id'))
        resource.meta = data.get('meta')
        resource.implicit_rules = data.get('implicitRules')
        resource.language = data.get('language')
        resource.text = data.get('text')
        resource.contained = data.get('contained', [])
        resource.extension = data.get('extension', [])
        resource.modifier_extension = data.get('modifierExtension', [])
        return resource


class FHIRFoundationResource(FHIRDataType):
    """Base class for all FHIR Foundation resources."""
    
    def __init__(self, resource_type: str, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Foundation resource."""
        super().__init__(use_c_extensions)
        self.resource_type = resource_type
        self.id = id
        self.use_c_extensions = use_c_extensions and HAS_C_FOUNDATION
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        raise NotImplementedError
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRFoundationResource':
        """Create from dictionary representation."""
        raise NotImplementedError
    
    @classmethod
    def from_json(cls, json_string: str) -> 'FHIRFoundationResource':
        """Create from JSON string."""
        data = json.loads(json_string)
        return cls.from_dict(data)


class FHIRPatient(FHIRFoundationResource):
    """FHIR Patient resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Patient."""
        super().__init__("Patient", id, use_c_extensions)
        self.active = None
        self.name = []
        self.telecom = []
        self.gender = None
        self.birth_date = None
        self.deceased = None
        self.address = []
        self.marital_status = None
        self.multiple_birth = None
        self.photo = []
        self.contact = []
        self.communication = []
        self.general_practitioner = []
        self.managing_organization = None
        self.link = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                # Create basic patient and convert to dict
                return fhir_foundation_c.create_patient(self.id)
            except:
                pass
        
        # Python fallback
        result = {"resourceType": "Patient"}
        if self.id:
            result["id"] = self.id
        if self.active is not None:
            result["active"] = self.active
        if self.name:
            result["name"] = self.name
        if self.telecom:
            result["telecom"] = self.telecom
        if self.gender:
            result["gender"] = self.gender
        if self.birth_date:
            result["birthDate"] = self.birth_date
        if self.address:
            result["address"] = self.address
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRPatient':
        """Create from dictionary."""
        patient = cls(data.get("id"))
        patient.active = data.get("active")
        patient.name = data.get("name", [])
        patient.telecom = data.get("telecom", [])
        patient.gender = data.get("gender")
        patient.birth_date = data.get("birthDate")
        patient.address = data.get("address", [])
        return patient
    
    @classmethod
    def from_json(cls, json_string: str) -> 'FHIRPatient':
        """Create from JSON string using C extension if available."""
        if HAS_C_FOUNDATION:
            try:
                data = fhir_foundation_c.parse_patient(json_string)
                return cls.from_dict(data)
            except:
                pass
        
        # Fallback to Python JSON parsing
        data = json.loads(json_string)
        return cls.from_dict(data)
    
    def get_full_name(self) -> Optional[str]:
        """Get patient's full name."""
        if self.use_c_extensions:
            try:
                json_string = json.dumps(self.to_dict())
                return fhir_foundation_c.patient_get_full_name(json_string)
            except:
                pass
        
        # Python fallback
        if not self.name:
            return None
        
        first_name = self.name[0]
        if isinstance(first_name, dict):
            if 'text' in first_name:
                return first_name['text']
            
            # Construct name from parts
            parts = []
            if 'given' in first_name:
                parts.extend(first_name['given'])
            if 'family' in first_name:
                parts.append(first_name['family'])
            
            return ' '.join(parts) if parts else None
        
        return None
    
    def is_active(self) -> bool:
        """Check if patient is active."""
        if self.use_c_extensions:
            try:
                json_string = json.dumps(self.to_dict())
                return fhir_foundation_c.patient_is_active(json_string)
            except:
                pass
        
        # Python fallback
        return self.active if self.active is not None else True
    
    def validate(self) -> bool:
        """Validate patient resource."""
        if self.use_c_extensions:
            try:
                json_string = json.dumps(self.to_dict())
                return fhir_foundation_c.validate_patient(json_string)
            except:
                pass
        
        # Python fallback validation
        if self.gender and self.gender not in ["male", "female", "other", "unknown"]:
            return False
        
        return True


class FHIRPractitioner(FHIRFoundationResource):
    """FHIR Practitioner resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Practitioner."""
        super().__init__("Practitioner", id, use_c_extensions)
        self.identifier = []
        self.active = None
        self.name = []
        self.telecom = []
        self.gender = None
        self.birth_date = None
        self.photo = []
        self.qualification = []
        self.communication = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_foundation_c.create_practitioner(self.id)
            except:
                pass
        
        # Python fallback
        result = {"resourceType": "Practitioner"}
        if self.id:
            result["id"] = self.id
        if self.active is not None:
            result["active"] = self.active
        if self.name:
            result["name"] = self.name
        if self.telecom:
            result["telecom"] = self.telecom
        if self.gender:
            result["gender"] = self.gender
        if self.birth_date:
            result["birthDate"] = self.birth_date
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRPractitioner':
        """Create from dictionary."""
        practitioner = cls(data.get("id"))
        practitioner.active = data.get("active")
        practitioner.name = data.get("name", [])
        practitioner.telecom = data.get("telecom", [])
        practitioner.gender = data.get("gender")
        practitioner.birth_date = data.get("birthDate")
        return practitioner


class FHIROrganization(FHIRFoundationResource):
    """FHIR Organization resource."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize FHIR Organization."""
        super().__init__("Organization", id, use_c_extensions)
        self.identifier = []
        self.active = None
        self.type = []
        self.name = None
        self.alias = []
        self.description = None
        self.telecom = []
        self.address = []
        self.part_of = None
        self.contact = []
        self.endpoint = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        if self.use_c_extensions:
            try:
                return fhir_foundation_c.create_organization(self.id)
            except:
                pass
        
        # Python fallback
        result = {"resourceType": "Organization"}
        if self.id:
            result["id"] = self.id
        if self.active is not None:
            result["active"] = self.active
        if self.name:
            result["name"] = self.name
        if self.description:
            result["description"] = self.description
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIROrganization':
        """Create from dictionary."""
        organization = cls(data.get("id"))
        organization.active = data.get("active")
        organization.name = data.get("name")
        organization.description = data.get("description")
        return organization


# Utility functions
def is_foundation_resource(resource_type: str) -> bool:
    """Check if resource type is a Foundation resource."""
    if HAS_C_FOUNDATION:
        try:
            return fhir_foundation_c.is_foundation_resource(resource_type)
        except:
            pass
    
    # Python fallback
    foundation_types = {
        "Patient", "Practitioner", "PractitionerRole", "Organization",
        "Location", "HealthcareService", "Endpoint", "RelatedPerson",
        "Person", "Group"
    }
    return resource_type in foundation_types


def get_resource_type(json_string: str) -> Optional[str]:
    """Get resource type from JSON string."""
    if HAS_C_FOUNDATION:
        try:
            return fhir_foundation_c.get_resource_type(json_string)
        except:
            pass
    
    # Python fallback
    try:
        data = json.loads(json_string)
        return data.get("resourceType")
    except:
        return None


# Export all Foundation resources and utilities
__all__ = [
    'FHIRFoundationResource', 'FHIRPatient', 'FHIRPractitioner', 'FHIROrganization',
    'is_foundation_resource', 'get_resource_type', 'HAS_C_FOUNDATION'
]