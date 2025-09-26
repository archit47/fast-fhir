"""FHIR R5 Person Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, FHIRPersonResourceMixin


class Person(FHIRResourceBase, FHIRPersonResourceMixin):
    """FHIR R5 Person resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Person-specific fields."""
        # Initialize person fields from mixin
        self._init_person_fields()
        
        # Person-specific fields
        self.deceased_boolean = None
        self.deceased_date_time = None
        self.marital_status = None
        self.communication = []
        self.managing_organization = None
        self.link = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_person"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_person"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_person"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Person-specific fields to dictionary."""
        # Add person fields from mixin
        self._add_person_fields_to_dict(result)
        
        # Add Person-specific fields
        if self.deceased_boolean is not None:
            result["deceasedBoolean"] = self.deceased_boolean
        if self.deceased_date_time:
            result["deceasedDateTime"] = self.deceased_date_time
        if self.marital_status:
            result["maritalStatus"] = self.marital_status
        if self.communication:
            result["communication"] = self.communication
        if self.managing_organization:
            result["managingOrganization"] = self.managing_organization
        if self.link:
            result["link"] = self.link
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Person-specific fields from dictionary."""
        # Parse person fields from mixin
        self._parse_person_fields_from_dict(data)
        
        # Parse Person-specific fields
        self.deceased_boolean = data.get("deceasedBoolean")
        self.deceased_date_time = data.get("deceasedDateTime")
        self.marital_status = data.get("maritalStatus")
        self.communication = data.get("communication", [])
        self.managing_organization = data.get("managingOrganization")
        self.link = data.get("link", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Person-specific fields."""
        # Use person validation from mixin
        return self._validate_person_fields()
    
    def is_deceased(self) -> bool:
        """Check if person is deceased."""
        return (self.deceased_boolean is True or 
                self.deceased_date_time is not None)
    
    def get_linked_resources(self) -> list:
        """Get linked resources (Patient, Practitioner, etc.)."""
        return self.link
    
    def has_link_to_resource(self, resource_reference: str) -> bool:
        """Check if person has a link to a specific resource."""
        for link in self.link:
            if isinstance(link, dict) and link.get("target", {}).get("reference") == resource_reference:
                return True
        return False