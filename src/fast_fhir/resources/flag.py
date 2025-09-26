"""FHIR R5 Flag Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Flag(FHIRResourceBase):
    """FHIR R5 Flag resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Flag-specific fields."""
        self.identifier = []
        self.status = None  # Required: active | inactive | entered-in-error
        self.category = []
        self.code = None  # Required
        self.subject = None  # Required
        self.period = None
        self.encounter = None
        self.author = None
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_flag"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_flag"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_flag"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Flag-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.status:
            result["status"] = self.status
        if self.category:
            result["category"] = self.category
        if self.code:
            result["code"] = self.code
        if self.subject:
            result["subject"] = self.subject
        if self.period:
            result["period"] = self.period
        if self.encounter:
            result["encounter"] = self.encounter
        if self.author:
            result["author"] = self.author
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Flag-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.status = data.get("status")
        self.category = data.get("category", [])
        self.code = data.get("code")
        self.subject = data.get("subject")
        self.period = data.get("period")
        self.encounter = data.get("encounter")
        self.author = data.get("author")
    
    def _validate_resource_specific(self) -> bool:
        """Validate Flag-specific fields."""
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = ["active", "inactive", "entered-in-error"]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Code is required
        if not self.code:
            return False
        
        # Subject is required
        if not self.subject:
            return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if flag is active."""
        return self.status == "active"