"""FHIR R5 Patient Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, FHIRPersonResourceMixin, validate_fhir_code


class Patient(FHIRResourceBase, FHIRPersonResourceMixin):
    """FHIR R5 Patient resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Patient-specific fields."""
        # Initialize person fields from mixin
        self._init_person_fields()
        
        # Patient-specific fields
        self.deceased_boolean = None
        self.deceased_date_time = None
        self.marital_status = None
        self.multiple_birth_boolean = None
        self.multiple_birth_integer = None
        self.contact = []
        self.communication = []
        self.general_practitioner = []
        self.managing_organization = None
        self.link = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_patient"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_patient"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_patient"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Patient-specific fields to dictionary."""
        # Add person fields from mixin
        self._add_person_fields_to_dict(result)
        
        # Add Patient-specific fields
        if self.deceased_boolean is not None:
            result["deceasedBoolean"] = self.deceased_boolean
        if self.deceased_date_time:
            result["deceasedDateTime"] = self.deceased_date_time
        if self.marital_status:
            result["maritalStatus"] = self.marital_status
        if self.multiple_birth_boolean is not None:
            result["multipleBirthBoolean"] = self.multiple_birth_boolean
        if self.multiple_birth_integer is not None:
            result["multipleBirthInteger"] = self.multiple_birth_integer
        if self.contact:
            result["contact"] = self.contact
        if self.communication:
            result["communication"] = self.communication
        if self.general_practitioner:
            result["generalPractitioner"] = self.general_practitioner
        if self.managing_organization:
            result["managingOrganization"] = self.managing_organization
        if self.link:
            result["link"] = self.link
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Patient-specific fields from dictionary."""
        # Parse person fields from mixin
        self._parse_person_fields_from_dict(data)
        
        # Parse Patient-specific fields
        self.deceased_boolean = data.get("deceasedBoolean")
        self.deceased_date_time = data.get("deceasedDateTime")
        self.marital_status = data.get("maritalStatus")
        self.multiple_birth_boolean = data.get("multipleBirthBoolean")
        self.multiple_birth_integer = data.get("multipleBirthInteger")
        self.contact = data.get("contact", [])
        self.communication = data.get("communication", [])
        self.general_practitioner = data.get("generalPractitioner", [])
        self.managing_organization = data.get("managingOrganization")
        self.link = data.get("link", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Patient-specific fields."""
        # Use person validation from mixin
        if not self._validate_person_fields():
            return False
        
        # Patient-specific validation
        # No additional validation needed for Patient
        return True
    
    def is_deceased(self) -> bool:
        """Check if patient is deceased."""
        return (self.deceased_boolean is True or 
                self.deceased_date_time is not None)