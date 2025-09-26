"""FHIR R5 Device Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Device(FHIRResourceBase):
    """FHIR R5 Device resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Device-specific fields."""
        self.identifier = []
        self.display_name = None
        self.definition = None
        self.udi_carrier = []
        self.status = None  # active | inactive | entered-in-error
        self.availability_status = []
        self.biological_source_event = None
        self.manufacturer = None
        self.manufacture_date = None
        self.expiration_date = None
        self.lot_number = None
        self.serial_number = None
        self.name = []
        self.model_number = None
        self.part_number = None
        self.category = []
        self.type = []
        self.version = []
        self.conforms_to = []
        self.property = []
        self.mode = None
        self.cycle = None
        self.duration = None
        self.owner = None
        self.contact = []
        self.location = None
        self.url = None
        self.endpoint = []
        self.gateway = []
        self.note = []
        self.safety = []
        self.parent = None
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_device"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_device"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_device"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Device-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.display_name:
            result["displayName"] = self.display_name
        if self.definition:
            result["definition"] = self.definition
        if self.udi_carrier:
            result["udiCarrier"] = self.udi_carrier
        if self.status:
            result["status"] = self.status
        if self.availability_status:
            result["availabilityStatus"] = self.availability_status
        if self.biological_source_event:
            result["biologicalSourceEvent"] = self.biological_source_event
        if self.manufacturer:
            result["manufacturer"] = self.manufacturer
        if self.manufacture_date:
            result["manufactureDate"] = self.manufacture_date
        if self.expiration_date:
            result["expirationDate"] = self.expiration_date
        if self.lot_number:
            result["lotNumber"] = self.lot_number
        if self.serial_number:
            result["serialNumber"] = self.serial_number
        if self.name:
            result["name"] = self.name
        if self.model_number:
            result["modelNumber"] = self.model_number
        if self.part_number:
            result["partNumber"] = self.part_number
        if self.category:
            result["category"] = self.category
        if self.type:
            result["type"] = self.type
        if self.version:
            result["version"] = self.version
        if self.conforms_to:
            result["conformsTo"] = self.conforms_to
        if self.property:
            result["property"] = self.property
        if self.mode:
            result["mode"] = self.mode
        if self.cycle:
            result["cycle"] = self.cycle
        if self.duration:
            result["duration"] = self.duration
        if self.owner:
            result["owner"] = self.owner
        if self.contact:
            result["contact"] = self.contact
        if self.location:
            result["location"] = self.location
        if self.url:
            result["url"] = self.url
        if self.endpoint:
            result["endpoint"] = self.endpoint
        if self.gateway:
            result["gateway"] = self.gateway
        if self.note:
            result["note"] = self.note
        if self.safety:
            result["safety"] = self.safety
        if self.parent:
            result["parent"] = self.parent
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Device-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.display_name = data.get("displayName")
        self.definition = data.get("definition")
        self.udi_carrier = data.get("udiCarrier", [])
        self.status = data.get("status")
        self.availability_status = data.get("availabilityStatus", [])
        self.biological_source_event = data.get("biologicalSourceEvent")
        self.manufacturer = data.get("manufacturer")
        self.manufacture_date = data.get("manufactureDate")
        self.expiration_date = data.get("expirationDate")
        self.lot_number = data.get("lotNumber")
        self.serial_number = data.get("serialNumber")
        self.name = data.get("name", [])
        self.model_number = data.get("modelNumber")
        self.part_number = data.get("partNumber")
        self.category = data.get("category", [])
        self.type = data.get("type", [])
        self.version = data.get("version", [])
        self.conforms_to = data.get("conformsTo", [])
        self.property = data.get("property", [])
        self.mode = data.get("mode")
        self.cycle = data.get("cycle")
        self.duration = data.get("duration")
        self.owner = data.get("owner")
        self.contact = data.get("contact", [])
        self.location = data.get("location")
        self.url = data.get("url")
        self.endpoint = data.get("endpoint", [])
        self.gateway = data.get("gateway", [])
        self.note = data.get("note", [])
        self.safety = data.get("safety", [])
        self.parent = data.get("parent")
    
    def _validate_resource_specific(self) -> bool:
        """Validate Device-specific fields."""
        # Validate status if present
        if self.status:
            valid_statuses = ["active", "inactive", "entered-in-error"]
            if not validate_fhir_code(self.status, valid_statuses):
                return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if device is active."""
        return self.status == "active" if self.status else True
    
    def get_device_name(self) -> Optional[str]:
        """Get primary device name."""
        if self.display_name:
            return self.display_name
        
        if self.name:
            for name_entry in self.name:
                if isinstance(name_entry, dict) and name_entry.get("value"):
                    return name_entry["value"]
        
        return None
    
    def get_udi_device_identifier(self) -> Optional[str]:
        """Get UDI device identifier."""
        for udi in self.udi_carrier:
            if isinstance(udi, dict) and udi.get("deviceIdentifier"):
                return udi["deviceIdentifier"]
        return None