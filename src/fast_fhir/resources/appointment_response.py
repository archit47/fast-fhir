"""FHIR R5 AppointmentResponse resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class AppointmentResponse(FHIRResourceBase):
    """FHIR R5 AppointmentResponse resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize AppointmentResponse resource."""
        super().__init__("AppointmentResponse", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize AppointmentResponse-specific fields."""
        # AppointmentResponse-specific attributes
        self.appointment: Optional[Dict[str, Any]] = None
        self.start: Optional[str] = None
        self.end: Optional[str] = None
        self.participant_type: List[Dict[str, Any]] = []
        self.actor: Optional[Dict[str, Any]] = None
        self.participant_status: Optional[str] = None  # accepted | declined | tentative | needs-action
        self.comment: Optional[str] = None
        self.recurring: Optional[bool] = None
        self.occurrence_date: Optional[str] = None
        self.occurrence_count: Optional[int] = None
    def to_dict(self) -> Dict[str, Any]:
        """Convert AppointmentResponse to dictionary representation."""
        result = super().to_dict()
        
        # Add AppointmentResponse-specific fields
        if self.appointment:
            result["appointment"] = self.appointment
        if self.start:
            result["start"] = self.start
        if self.end:
            result["end"] = self.end
        if self.participant_type:
            result["participantType"] = self.participant_type
        if self.actor:
            result["actor"] = self.actor
        if self.participant_status:
            result["participantStatus"] = self.participant_status
        if self.comment:
            result["comment"] = self.comment
        if self.recurring is not None:
            result["recurring"] = self.recurring
        if self.occurrence_date:
            result["occurrenceDate"] = self.occurrence_date
        if self.occurrence_count is not None:
            result["occurrenceCount"] = self.occurrence_count
        
        return result
    
    
    
    def is_accepted(self) -> bool:
        """Check if the appointment response is accepted."""
        return self.participant_status == "accepted"
    
    def is_declined(self) -> bool:
        """Check if the appointment response is declined."""
        return self.participant_status == "declined"
    
    def is_tentative(self) -> bool:
        """Check if the appointment response is tentative."""
        return self.participant_status == "tentative"
    
    def needs_action(self) -> bool:
        """Check if the appointment response needs action."""
        return self.participant_status == "needs-action"
    
    def is_recurring(self) -> bool:
        """Check if this is a recurring appointment response."""
        return self.recurring is True
    
    def get_appointment_reference(self) -> Optional[Dict[str, Any]]:
        """Get the appointment reference."""
        return self.appointment
    
    def get_actor(self) -> Optional[Dict[str, Any]]:
        """Get the actor (participant) reference."""
        return self.actor
    
    def get_participant_types(self) -> List[Dict[str, Any]]:
        """Get all participant types."""
        return self.participant_type.copy()
    
    def get_start_time(self) -> Optional[str]:
        """Get the start time."""
        return self.start
    
    def get_end_time(self) -> Optional[str]:
        """Get the end time."""
        return self.end
    
    def get_comment(self) -> Optional[str]:
        """Get the comment."""
        return self.comment
    
    def set_participant_status(self, status: str) -> None:
        """Set the participant status."""
        valid_statuses = ["accepted", "declined", "tentative", "needs-action"]
        if status in valid_statuses:
            self.participant_status = status
        else:
            raise ValueError(f"Invalid participant status: {status}")
    
    def set_appointment(self, appointment: Dict[str, Any]) -> None:
        """Set the appointment reference."""
        self.appointment = appointment
    
    def set_actor(self, actor: Dict[str, Any]) -> None:
        """Set the actor (participant) reference."""
        self.actor = actor
    
    def set_time_period(self, start: str, end: str) -> None:
        """Set the start and end times."""
        self.start = start
        self.end = end
    
    def set_comment(self, comment: str) -> None:
        """Set the comment."""
        self.comment = comment
    
    def add_participant_type(self, participant_type: Dict[str, Any]) -> None:
        """Add a participant type."""
        if participant_type not in self.participant_type:
            self.participant_type.append(participant_type)
    
    def set_recurring(self, recurring: bool) -> None:
        """Set whether this is a recurring appointment response."""
        self.recurring = recurring
    
    def set_occurrence_date(self, date: str) -> None:
        """Set the occurrence date for recurring appointments."""
        self.occurrence_date = date
    
    def set_occurrence_count(self, count: int) -> None:
        """Set the occurrence count for recurring appointments."""
        self.occurrence_count = count
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "create_appointment_response"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "parse_appointment_response"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "parse_appointment_response"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add AppointmentResponse-specific fields to the result dictionary."""
        # TODO: Implement resource-specific field serialization
        pass
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse AppointmentResponse-specific fields from data dictionary."""
        # TODO: Implement resource-specific field parsing
        pass
    
    def _validate_resource_specific(self) -> bool:
        """Perform AppointmentResponse-specific validation."""
        # AppointmentResponse requires appointment and participant_status
        return self.appointment is not None and self.participant_status is not None
