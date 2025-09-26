"""Base classes for FHIR resources following DRY principles."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
import json

try:
    import fhir_foundation_c
    HAS_C_FOUNDATION = True
except ImportError:
    HAS_C_FOUNDATION = False


class FHIRResourceBase(ABC):
    """Abstract base class for all FHIR resources implementing DRY principles."""
    
    def __init__(self, resource_type: str, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize base FHIR resource."""
        self.resource_type = resource_type
        self.id = id
        self.use_c_extensions = use_c_extensions and HAS_C_FOUNDATION
        
        # Common DomainResource fields
        self.meta = None
        self.implicit_rules = None
        self.language = None
        self.text = None
        self.contained = []
        self.extension = []
        self.modifier_extension = []
        
        # Initialize resource-specific fields
        self._init_resource_fields()
    
    @abstractmethod
    def _init_resource_fields(self) -> None:
        """Initialize resource-specific fields. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name. Return None if not available."""
        pass
    
    @abstractmethod
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name. Return None if not available."""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert resource to dictionary representation."""
        if self.use_c_extensions:
            c_function = self._get_c_extension_create_function()
            if c_function and hasattr(fhir_foundation_c, c_function):
                try:
                    return getattr(fhir_foundation_c, c_function)(self.id)
                except:
                    pass
        
        # Python fallback
        return self._to_dict_python()
    
    def _to_dict_python(self) -> Dict[str, Any]:
        """Python implementation of to_dict."""
        result = {"resourceType": self.resource_type}
        
        # Add common fields
        if self.id:
            result["id"] = self.id
        if self.meta:
            result["meta"] = self.meta
        if self.implicit_rules:
            result["implicitRules"] = self.implicit_rules
        if self.language:
            result["language"] = self.language
        if self.text:
            result["text"] = self.text
        if self.contained:
            result["contained"] = self.contained
        if self.extension:
            result["extension"] = self.extension
        if self.modifier_extension:
            result["modifierExtension"] = self.modifier_extension
        
        # Add resource-specific fields
        self._add_resource_specific_fields(result)
        
        return result
    
    @abstractmethod
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add resource-specific fields to the result dictionary."""
        pass
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FHIRResourceBase':
        """Create resource from dictionary data."""
        resource = cls(data.get("id"))
        resource._parse_common_fields(data)
        resource._parse_resource_specific_fields(data)
        return resource
    
    def _parse_common_fields(self, data: Dict[str, Any]) -> None:
        """Parse common DomainResource fields."""
        self.meta = data.get("meta")
        self.implicit_rules = data.get("implicitRules")
        self.language = data.get("language")
        self.text = data.get("text")
        self.contained = data.get("contained", [])
        self.extension = data.get("extension", [])
        self.modifier_extension = data.get("modifierExtension", [])
    
    @abstractmethod
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse resource-specific fields from data dictionary."""
        pass
    
    @classmethod
    def from_json(cls, json_string: str) -> 'FHIRResourceBase':
        """Create resource from JSON string."""
        # Try C extension first if available
        if HAS_C_FOUNDATION:
            c_function = cls._get_c_extension_parse_function_static()
            if c_function and hasattr(fhir_foundation_c, c_function):
                try:
                    data = getattr(fhir_foundation_c, c_function)(json_string)
                    return cls.from_dict(data)
                except:
                    pass
        
        # Python fallback
        data = json.loads(json_string)
        return cls.from_dict(data)
    
    @classmethod
    @abstractmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function for class methods."""
        pass
    
    def validate(self) -> bool:
        """Validate the resource."""
        # Basic validation
        if not self.resource_type:
            return False
        
        # Resource-specific validation
        return self._validate_resource_specific()
    
    @abstractmethod
    def _validate_resource_specific(self) -> bool:
        """Perform resource-specific validation."""
        pass
    
    def __str__(self) -> str:
        """String representation of the resource."""
        return f"{self.resource_type}(id={self.id})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the resource."""
        return f"{self.__class__.__name__}(resource_type='{self.resource_type}', id='{self.id}')"


class FHIRPersonResourceMixin:
    """Mixin for resources that represent people (Patient, Practitioner, RelatedPerson, Person)."""
    
    def _init_person_fields(self) -> None:
        """Initialize common person fields."""
        self.identifier = []
        self.active = None
        self.name = []
        self.telecom = []
        self.gender = None
        self.birth_date = None
        self.address = []
        self.photo = []
    
    def _add_person_fields_to_dict(self, result: Dict[str, Any]) -> None:
        """Add common person fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
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
        if self.photo:
            result["photo"] = self.photo
    
    def _parse_person_fields_from_dict(self, data: Dict[str, Any]) -> None:
        """Parse common person fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.active = data.get("active")
        self.name = data.get("name", [])
        self.telecom = data.get("telecom", [])
        self.gender = data.get("gender")
        self.birth_date = data.get("birthDate")
        self.address = data.get("address", [])
        self.photo = data.get("photo", [])
    
    def get_full_name(self) -> Optional[str]:
        """Get person's full name from first HumanName entry."""
        if not self.name:
            return None
        
        first_name = self.name[0]
        if isinstance(first_name, dict):
            if 'text' in first_name:
                return first_name['text']
            
            # Construct name from parts
            parts = []
            if 'given' in first_name:
                if isinstance(first_name['given'], list):
                    parts.extend(first_name['given'])
                else:
                    parts.append(first_name['given'])
            if 'family' in first_name:
                parts.append(first_name['family'])
            
            return ' '.join(parts) if parts else None
        
        return None
    
    def is_active(self) -> bool:
        """Check if person is active."""
        return self.active if self.active is not None else True
    
    def _validate_person_fields(self) -> bool:
        """Validate common person fields."""
        # Validate gender if present
        if self.gender and self.gender not in ["male", "female", "other", "unknown"]:
            return False
        
        # Validate birth date format if present (basic check)
        if self.birth_date and not isinstance(self.birth_date, str):
            return False
        
        return True


class FHIROrganizationResourceMixin:
    """Mixin for organization-related resources."""
    
    def _init_organization_fields(self) -> None:
        """Initialize common organization fields."""
        self.identifier = []
        self.active = None
        self.name = None
        self.alias = []
        self.description = None
        self.telecom = []
        self.address = []
        self.contact = []
    
    def _add_organization_fields_to_dict(self, result: Dict[str, Any]) -> None:
        """Add common organization fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.active is not None:
            result["active"] = self.active
        if self.name:
            result["name"] = self.name
        if self.alias:
            result["alias"] = self.alias
        if self.description:
            result["description"] = self.description
        if self.telecom:
            result["telecom"] = self.telecom
        if self.address:
            result["address"] = self.address
        if self.contact:
            result["contact"] = self.contact
    
    def _parse_organization_fields_from_dict(self, data: Dict[str, Any]) -> None:
        """Parse common organization fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.active = data.get("active")
        self.name = data.get("name")
        self.alias = data.get("alias", [])
        self.description = data.get("description")
        self.telecom = data.get("telecom", [])
        self.address = data.get("address", [])
        self.contact = data.get("contact", [])
    
    def get_display_name(self) -> Optional[str]:
        """Get organization display name."""
        return self.name
    
    def is_active(self) -> bool:
        """Check if organization is active."""
        return self.active if self.active is not None else True


# Utility functions following DRY principles
def validate_fhir_code(code: str, valid_codes: List[str]) -> bool:
    """Validate a FHIR code against a list of valid codes."""
    return code in valid_codes if code else True


def validate_fhir_date(date_string: str) -> bool:
    """Validate FHIR date format (YYYY, YYYY-MM, or YYYY-MM-DD)."""
    if not date_string:
        return True
    
    import re
    pattern = r'^\d{4}(-\d{2}(-\d{2})?)?$'
    return bool(re.match(pattern, date_string))


def safe_get_nested(data: Dict[str, Any], *keys) -> Any:
    """Safely get nested dictionary values."""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current