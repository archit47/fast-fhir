"""FHIR R5 Endpoint Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Endpoint(FHIRResourceBase):
    """FHIR R5 Endpoint resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Endpoint-specific fields."""
        self.identifier = []
        self.status = None  # Required: active | suspended | error | off | entered-in-error | test
        self.connection_type = []  # Required
        self.name = None
        self.description = None
        self.environment_type = []
        self.managing_organization = None
        self.contact = []
        self.period = None
        self.payload = []
        self.address = None  # Required
        self.header = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_endpoint"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_endpoint"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_endpoint"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Endpoint-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.status:
            result["status"] = self.status
        if self.connection_type:
            result["connectionType"] = self.connection_type
        if self.name:
            result["name"] = self.name
        if self.description:
            result["description"] = self.description
        if self.environment_type:
            result["environmentType"] = self.environment_type
        if self.managing_organization:
            result["managingOrganization"] = self.managing_organization
        if self.contact:
            result["contact"] = self.contact
        if self.period:
            result["period"] = self.period
        if self.payload:
            result["payload"] = self.payload
        if self.address:
            result["address"] = self.address
        if self.header:
            result["header"] = self.header
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Endpoint-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.status = data.get("status")
        self.connection_type = data.get("connectionType", [])
        self.name = data.get("name")
        self.description = data.get("description")
        self.environment_type = data.get("environmentType", [])
        self.managing_organization = data.get("managingOrganization")
        self.contact = data.get("contact", [])
        self.period = data.get("period")
        self.payload = data.get("payload", [])
        self.address = data.get("address")
        self.header = data.get("header", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Endpoint-specific fields."""
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = ["active", "suspended", "error", "off", "entered-in-error", "test"]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Connection type is required
        if not self.connection_type:
            return False
        
        # Address is required
        if not self.address:
            return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if endpoint is active."""
        return self.status == "active"
    
    def get_connection_types(self) -> list:
        """Get endpoint connection types."""
        return self.connection_type
    
    def get_payload_types(self) -> list:
        """Get supported payload types."""
        return [payload.get("type") for payload in self.payload if payload.get("type")]