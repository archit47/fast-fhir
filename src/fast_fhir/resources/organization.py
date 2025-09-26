"""FHIR R5 Organization Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, FHIROrganizationResourceMixin


class Organization(FHIRResourceBase, FHIROrganizationResourceMixin):
    """FHIR R5 Organization resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Organization-specific fields."""
        # Initialize organization fields from mixin
        self._init_organization_fields()
        
        # Organization-specific fields
        self.type = []
        self.part_of = None
        self.endpoint = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_organization"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_organization"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_organization"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Organization-specific fields to dictionary."""
        # Add organization fields from mixin
        self._add_organization_fields_to_dict(result)
        
        # Add Organization-specific fields
        if self.type:
            result["type"] = self.type
        if self.part_of:
            result["partOf"] = self.part_of
        if self.endpoint:
            result["endpoint"] = self.endpoint
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Organization-specific fields from dictionary."""
        # Parse organization fields from mixin
        self._parse_organization_fields_from_dict(data)
        
        # Parse Organization-specific fields
        self.type = data.get("type", [])
        self.part_of = data.get("partOf")
        self.endpoint = data.get("endpoint", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Organization-specific fields."""
        # Organization must have a name
        if not self.name:
            return False
        
        return True
    
    def get_organization_types(self) -> list:
        """Get organization types."""
        return self.type
    
    def has_type(self, type_code: str) -> bool:
        """Check if organization has a specific type."""
        for org_type in self.type:
            if isinstance(org_type, dict) and org_type.get("coding"):
                for coding in org_type["coding"]:
                    if coding.get("code") == type_code:
                        return True
        return False
    
    def is_part_of_organization(self) -> bool:
        """Check if this organization is part of another organization."""
        return self.part_of is not None