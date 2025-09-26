"""FHIR R5 Location Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Location(FHIRResourceBase):
    """FHIR R5 Location resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Location-specific fields."""
        self.identifier = []
        self.status = None  # active | suspended | inactive
        self.operational_status = None
        self.name = None
        self.alias = []
        self.description = None
        self.mode = None  # instance | kind
        self.type = []
        self.contact = []
        self.address = None
        self.physical_type = None
        self.position = None
        self.managing_organization = None
        self.part_of = None
        self.characteristic = []
        self.hours_of_operation = []
        self.virtual_service = []
        self.endpoint = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_location"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_location"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_location"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Location-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.status:
            result["status"] = self.status
        if self.operational_status:
            result["operationalStatus"] = self.operational_status
        if self.name:
            result["name"] = self.name
        if self.alias:
            result["alias"] = self.alias
        if self.description:
            result["description"] = self.description
        if self.mode:
            result["mode"] = self.mode
        if self.type:
            result["type"] = self.type
        if self.contact:
            result["contact"] = self.contact
        if self.address:
            result["address"] = self.address
        if self.physical_type:
            result["physicalType"] = self.physical_type
        if self.position:
            result["position"] = self.position
        if self.managing_organization:
            result["managingOrganization"] = self.managing_organization
        if self.part_of:
            result["partOf"] = self.part_of
        if self.characteristic:
            result["characteristic"] = self.characteristic
        if self.hours_of_operation:
            result["hoursOfOperation"] = self.hours_of_operation
        if self.virtual_service:
            result["virtualService"] = self.virtual_service
        if self.endpoint:
            result["endpoint"] = self.endpoint
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Location-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.status = data.get("status")
        self.operational_status = data.get("operationalStatus")
        self.name = data.get("name")
        self.alias = data.get("alias", [])
        self.description = data.get("description")
        self.mode = data.get("mode")
        self.type = data.get("type", [])
        self.contact = data.get("contact", [])
        self.address = data.get("address")
        self.physical_type = data.get("physicalType")
        self.position = data.get("position")
        self.managing_organization = data.get("managingOrganization")
        self.part_of = data.get("partOf")
        self.characteristic = data.get("characteristic", [])
        self.hours_of_operation = data.get("hoursOfOperation", [])
        self.virtual_service = data.get("virtualService", [])
        self.endpoint = data.get("endpoint", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Location-specific fields."""
        # Validate status if present
        if self.status:
            valid_statuses = ["active", "suspended", "inactive"]
            if not validate_fhir_code(self.status, valid_statuses):
                return False
        
        # Validate mode if present
        if self.mode:
            valid_modes = ["instance", "kind"]
            if not validate_fhir_code(self.mode, valid_modes):
                return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if location is active."""
        return self.status == "active" if self.status else True
    
    def get_coordinates(self) -> Optional[Dict[str, float]]:
        """Get location coordinates if available."""
        if self.position and isinstance(self.position, dict):
            return {
                "longitude": self.position.get("longitude"),
                "latitude": self.position.get("latitude"),
                "altitude": self.position.get("altitude")
            }
        return None
    
    def set_coordinates(self, longitude: float, latitude: float, altitude: Optional[float] = None) -> None:
        """Set location coordinates."""
        self.position = {
            "longitude": longitude,
            "latitude": latitude
        }
        if altitude is not None:
            self.position["altitude"] = altitude