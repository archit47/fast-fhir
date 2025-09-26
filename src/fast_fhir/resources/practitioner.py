"""FHIR R5 Practitioner Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, FHIRPersonResourceMixin


class Practitioner(FHIRResourceBase, FHIRPersonResourceMixin):
    """FHIR R5 Practitioner resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Practitioner-specific fields."""
        # Initialize person fields from mixin
        self._init_person_fields()
        
        # Practitioner-specific fields
        self.qualification = []
        self.communication = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_practitioner"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_practitioner"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_practitioner"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Practitioner-specific fields to dictionary."""
        # Add person fields from mixin
        self._add_person_fields_to_dict(result)
        
        # Add Practitioner-specific fields
        if self.qualification:
            result["qualification"] = self.qualification
        if self.communication:
            result["communication"] = self.communication
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Practitioner-specific fields from dictionary."""
        # Parse person fields from mixin
        self._parse_person_fields_from_dict(data)
        
        # Parse Practitioner-specific fields
        self.qualification = data.get("qualification", [])
        self.communication = data.get("communication", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Practitioner-specific fields."""
        # Use person validation from mixin
        return self._validate_person_fields()
    
    def get_qualifications(self) -> list:
        """Get practitioner's qualifications."""
        return self.qualification
    
    def has_qualification(self, qualification_code: str) -> bool:
        """Check if practitioner has a specific qualification."""
        for qual in self.qualification:
            if isinstance(qual, dict) and qual.get("code", {}).get("coding"):
                for coding in qual["code"]["coding"]:
                    if coding.get("code") == qualification_code:
                        return True
        return False