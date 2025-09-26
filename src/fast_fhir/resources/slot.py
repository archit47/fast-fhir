"""FHIR R5 Slot Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Slot(FHIRResourceBase):
    """FHIR R5 Slot resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Slot-specific fields."""
        self.identifier = []
        self.service_category = []
        self.service_type = []
        self.specialty = []
        self.appointment_type = []
        self.schedule = None  # Required
        self.status = None  # Required: busy | free | busy-unavailable | busy-tentative | entered-in-error
        self.start = None  # Required
        self.end = None  # Required
        self.overbooked = None
        self.comment = None
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_slot"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_slot"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_slot"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Slot-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.service_category:
            result["serviceCategory"] = self.service_category
        if self.service_type:
            result["serviceType"] = self.service_type
        if self.specialty:
            result["specialty"] = self.specialty
        if self.appointment_type:
            result["appointmentType"] = self.appointment_type
        if self.schedule:
            result["schedule"] = self.schedule
        if self.status:
            result["status"] = self.status
        if self.start:
            result["start"] = self.start
        if self.end:
            result["end"] = self.end
        if self.overbooked is not None:
            result["overbooked"] = self.overbooked
        if self.comment:
            result["comment"] = self.comment
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Slot-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.service_category = data.get("serviceCategory", [])
        self.service_type = data.get("serviceType", [])
        self.specialty = data.get("specialty", [])
        self.appointment_type = data.get("appointmentType", [])
        self.schedule = data.get("schedule")
        self.status = data.get("status")
        self.start = data.get("start")
        self.end = data.get("end")
        self.overbooked = data.get("overbooked")
        self.comment = data.get("comment")
    
    def _validate_resource_specific(self) -> bool:
        """Validate Slot-specific fields."""
        # Schedule is required
        if not self.schedule:
            return False
        
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = ["busy", "free", "busy-unavailable", "busy-tentative", "entered-in-error"]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Start is required
        if not self.start:
            return False
        
        # End is required
        if not self.end:
            return False
        
        return True
    
    def is_free(self) -> bool:
        """Check if slot is free."""
        return self.status == "free"
    
    def is_busy(self) -> bool:
        """Check if slot is busy."""
        return self.status == "busy"
    
    def is_overbooked(self) -> bool:
        """Check if slot is overbooked."""
        return self.overbooked is True