"""FHIR R5 EncounterHistory resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class EncounterHistory(FHIRResourceBase):
    """FHIR R5 EncounterHistory resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize EncounterHistory resource."""
        super().__init__("EncounterHistory", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize EncounterHistory-specific fields."""
        # EncounterHistory-specific attributes
        self.status: Optional[str] = None  # planned | in-progress | on-hold | discharged | completed | cancelled | discontinued | entered-in-error | unknown
        self.class_: Optional[Dict[str, Any]] = None  # 'class' is a reserved keyword, so using 'class_'
        self.type: Optional[Dict[str, Any]] = None
        self.service_type: List[Dict[str, Any]] = []
        self.subject: Optional[Dict[str, Any]] = None
        self.encounter: Optional[Dict[str, Any]] = None
        self.actual_period: Optional[Dict[str, Any]] = None
        self.planned_start_date: Optional[Dict[str, Any]] = None
        self.planned_end_date: Optional[Dict[str, Any]] = None
        self.length: Optional[Dict[str, Any]] = None
        self.location: List[Dict[str, Any]] = []
    def to_dict(self) -> Dict[str, Any]:
        """Convert EncounterHistory to dictionary representation."""
        result = super().to_dict()
        
        # Add EncounterHistory-specific fields
        if self.status:
            result["status"] = self.status
        if self.class_:
            result["class"] = self.class_
        if self.type:
            result["type"] = self.type
        if self.service_type:
            result["serviceType"] = self.service_type
        if self.subject:
            result["subject"] = self.subject
        if self.encounter:
            result["encounter"] = self.encounter
        if self.actual_period:
            result["actualPeriod"] = self.actual_period
        if self.planned_start_date:
            result["plannedStartDate"] = self.planned_start_date
        if self.planned_end_date:
            result["plannedEndDate"] = self.planned_end_date
        if self.length:
            result["length"] = self.length
        if self.location:
            result["location"] = self.location
        
        return result
    
    
    
    def is_completed(self) -> bool:
        """Check if the encounter history is completed."""
        return self.status == "completed"
    
    def is_in_progress(self) -> bool:
        """Check if the encounter history is in progress."""
        return self.status == "in-progress"
    
    def is_planned(self) -> bool:
        """Check if the encounter history is planned."""
        return self.status == "planned"
    
    def is_cancelled(self) -> bool:
        """Check if the encounter history is cancelled."""
        return self.status == "cancelled"
    
    def is_on_hold(self) -> bool:
        """Check if the encounter history is on hold."""
        return self.status == "on-hold"
    
    def get_encounter_class(self) -> Optional[Dict[str, Any]]:
        """Get the encounter class."""
        return self.class_
    
    def get_encounter_type(self) -> Optional[Dict[str, Any]]:
        """Get the encounter type."""
        return self.type
    
    def get_service_types(self) -> List[Dict[str, Any]]:
        """Get all service types."""
        return self.service_type.copy()
    
    def get_subject(self) -> Optional[Dict[str, Any]]:
        """Get the subject reference."""
        return self.subject
    
    def get_encounter_reference(self) -> Optional[Dict[str, Any]]:
        """Get the encounter reference."""
        return self.encounter
    
    def get_actual_period(self) -> Optional[Dict[str, Any]]:
        """Get the actual period."""
        return self.actual_period
    
    def get_planned_start_date(self) -> Optional[Dict[str, Any]]:
        """Get the planned start date."""
        return self.planned_start_date
    
    def get_planned_end_date(self) -> Optional[Dict[str, Any]]:
        """Get the planned end date."""
        return self.planned_end_date
    
    def get_length(self) -> Optional[Dict[str, Any]]:
        """Get the encounter length."""
        return self.length
    
    def get_locations(self) -> List[Dict[str, Any]]:
        """Get all location information."""
        return self.location.copy()
    
    def set_status(self, status: str) -> None:
        """Set the encounter history status."""
        valid_statuses = ["planned", "in-progress", "on-hold", "discharged", "completed", 
                         "cancelled", "discontinued", "entered-in-error", "unknown"]
        if status in valid_statuses:
            self.status = status
        else:
            raise ValueError(f"Invalid status: {status}")
    
    def set_encounter_class(self, encounter_class: Dict[str, Any]) -> None:
        """Set the encounter class."""
        self.class_ = encounter_class
    
    def set_encounter_type(self, encounter_type: Dict[str, Any]) -> None:
        """Set the encounter type."""
        self.type = encounter_type
    
    def set_subject(self, subject: Dict[str, Any]) -> None:
        """Set the subject reference."""
        self.subject = subject
    
    def set_encounter_reference(self, encounter: Dict[str, Any]) -> None:
        """Set the encounter reference."""
        self.encounter = encounter
    
    def set_actual_period(self, period: Dict[str, Any]) -> None:
        """Set the actual period."""
        self.actual_period = period
    
    def set_planned_dates(self, start_date: Dict[str, Any], end_date: Dict[str, Any]) -> None:
        """Set the planned start and end dates."""
        self.planned_start_date = start_date
        self.planned_end_date = end_date
    
    def set_length(self, length: Dict[str, Any]) -> None:
        """Set the encounter length."""
        self.length = length
    
    def add_service_type(self, service_type: Dict[str, Any]) -> None:
        """Add a service type."""
        if service_type not in self.service_type:
            self.service_type.append(service_type)
    
    def add_location(self, location: Dict[str, Any]) -> None:
        """Add location information."""
        self.location.append(location)
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "create_encounter_history"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "parse_encounter_history"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "parse_encounter_history"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add EncounterHistory-specific fields to the result dictionary."""
        # TODO: Implement resource-specific field serialization
        pass
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse EncounterHistory-specific fields from data dictionary."""
        # TODO: Implement resource-specific field parsing
        pass
    
    def _validate_resource_specific(self) -> bool:
        """Perform EncounterHistory-specific validation."""
        # EncounterHistory requires status, class_, subject, and encounter
        return (self.status is not None and 
                self.class_ is not None and 
                self.subject is not None and 
                self.encounter is not None)
