"""FHIR R5 Substance Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Substance(FHIRResourceBase):
    """FHIR R5 Substance resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Substance-specific fields."""
        self.identifier = []
        self.instance = None  # Required: true if instance, false if kind
        self.status = None  # active | inactive | entered-in-error
        self.category = []
        self.code = None  # Required
        self.description = None
        self.expiry = None
        self.quantity = None
        self.ingredient = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_substance"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_substance"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_substance"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Substance-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.instance is not None:
            result["instance"] = self.instance
        if self.status:
            result["status"] = self.status
        if self.category:
            result["category"] = self.category
        if self.code:
            result["code"] = self.code
        if self.description:
            result["description"] = self.description
        if self.expiry:
            result["expiry"] = self.expiry
        if self.quantity:
            result["quantity"] = self.quantity
        if self.ingredient:
            result["ingredient"] = self.ingredient
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Substance-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.instance = data.get("instance")
        self.status = data.get("status")
        self.category = data.get("category", [])
        self.code = data.get("code")
        self.description = data.get("description")
        self.expiry = data.get("expiry")
        self.quantity = data.get("quantity")
        self.ingredient = data.get("ingredient", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Substance-specific fields."""
        # Instance is required
        if self.instance is None:
            return False
        
        # Code is required
        if not self.code:
            return False
        
        # Validate status if present
        if self.status:
            valid_statuses = ["active", "inactive", "entered-in-error"]
            if not validate_fhir_code(self.status, valid_statuses):
                return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if substance is active."""
        return self.status == "active" if self.status else True
    
    def is_instance(self) -> bool:
        """Check if this is a substance instance (vs kind)."""
        return self.instance is True
    
    def get_substance_code(self) -> Optional[str]:
        """Get substance code."""
        if isinstance(self.code, dict) and self.code.get("coding"):
            for coding in self.code["coding"]:
                if coding.get("code"):
                    return coding["code"]
        return None