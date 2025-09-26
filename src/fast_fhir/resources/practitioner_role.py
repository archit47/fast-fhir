"""FHIR R5 PractitionerRole Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class PractitionerRole(FHIRResourceBase):
    """FHIR R5 PractitionerRole resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize PractitionerRole-specific fields."""
        self.identifier = []
        self.active = None
        self.period = None
        self.practitioner = None
        self.organization = None
        self.code = []
        self.specialty = []
        self.location = []
        self.healthcare_service = []
        self.contact = []
        self.characteristic = []
        self.communication = []
        self.availability_exceptions = None
        self.endpoint = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_practitioner_role"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_practitioner_role"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_practitioner_role"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add PractitionerRole-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.active is not None:
            result["active"] = self.active
        if self.period:
            result["period"] = self.period
        if self.practitioner:
            result["practitioner"] = self.practitioner
        if self.organization:
            result["organization"] = self.organization
        if self.code:
            result["code"] = self.code
        if self.specialty:
            result["specialty"] = self.specialty
        if self.location:
            result["location"] = self.location
        if self.healthcare_service:
            result["healthcareService"] = self.healthcare_service
        if self.contact:
            result["contact"] = self.contact
        if self.characteristic:
            result["characteristic"] = self.characteristic
        if self.communication:
            result["communication"] = self.communication
        if self.availability_exceptions:
            result["availabilityExceptions"] = self.availability_exceptions
        if self.endpoint:
            result["endpoint"] = self.endpoint
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse PractitionerRole-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.active = data.get("active")
        self.period = data.get("period")
        self.practitioner = data.get("practitioner")
        self.organization = data.get("organization")
        self.code = data.get("code", [])
        self.specialty = data.get("specialty", [])
        self.location = data.get("location", [])
        self.healthcare_service = data.get("healthcareService", [])
        self.contact = data.get("contact", [])
        self.characteristic = data.get("characteristic", [])
        self.communication = data.get("communication", [])
        self.availability_exceptions = data.get("availabilityExceptions")
        self.endpoint = data.get("endpoint", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate PractitionerRole-specific fields."""
        # Basic validation - at least one of practitioner or organization should be present
        if not self.practitioner and not self.organization:
            return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if practitioner role is active."""
        return self.active if self.active is not None else True
    
    def get_role_codes(self) -> list:
        """Get role codes for this practitioner role."""
        return self.code
    
    def has_role(self, role_code: str) -> bool:
        """Check if practitioner role has a specific role code."""
        for code in self.code:
            if isinstance(code, dict) and code.get("coding"):
                for coding in code["coding"]:
                    if coding.get("code") == role_code:
                        return True
        return False
    
    def get_specialties(self) -> list:
        """Get specialties for this practitioner role."""
        return self.specialty