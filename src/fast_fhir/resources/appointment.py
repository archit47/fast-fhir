"""FHIR R5 Appointment Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Appointment(FHIRResourceBase):
    """FHIR R5 Appointment resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Appointment-specific fields."""
        self.identifier = []
        self.status = None  # Required: proposed | pending | booked | arrived | fulfilled | cancelled | noshow | entered-in-error | checked-in | waitlist
        self.cancellation_reason = None
        self.class_element = []
        self.service_category = []
        self.service_type = []
        self.specialty = []
        self.appointment_type = None
        self.reason = []
        self.priority = None
        self.description = None
        self.replaces = []
        self.virtual_service = []
        self.supporting_information = []
        self.previous_appointment = None
        self.originating_appointment = None
        self.start = None
        self.end = None
        self.minutes_duration = None
        self.requested_period = []
        self.slot = []
        self.account = []
        self.created = None
        self.cancellation_date = None
        self.note = []
        self.patient_instruction = []
        self.based_on = []
        self.subject = None
        self.participant = []  # Required
        self.recurrence_id = None
        self.occurrence_changed = None
        self.recurrence_template = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_appointment"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_appointment"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_appointment"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Appointment-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.status:
            result["status"] = self.status
        if self.cancellation_reason:
            result["cancellationReason"] = self.cancellation_reason
        if self.class_element:
            result["class"] = self.class_element
        if self.service_category:
            result["serviceCategory"] = self.service_category
        if self.service_type:
            result["serviceType"] = self.service_type
        if self.specialty:
            result["specialty"] = self.specialty
        if self.appointment_type:
            result["appointmentType"] = self.appointment_type
        if self.reason:
            result["reason"] = self.reason
        if self.priority:
            result["priority"] = self.priority
        if self.description:
            result["description"] = self.description
        if self.replaces:
            result["replaces"] = self.replaces
        if self.virtual_service:
            result["virtualService"] = self.virtual_service
        if self.supporting_information:
            result["supportingInformation"] = self.supporting_information
        if self.previous_appointment:
            result["previousAppointment"] = self.previous_appointment
        if self.originating_appointment:
            result["originatingAppointment"] = self.originating_appointment
        if self.start:
            result["start"] = self.start
        if self.end:
            result["end"] = self.end
        if self.minutes_duration:
            result["minutesDuration"] = self.minutes_duration
        if self.requested_period:
            result["requestedPeriod"] = self.requested_period
        if self.slot:
            result["slot"] = self.slot
        if self.account:
            result["account"] = self.account
        if self.created:
            result["created"] = self.created
        if self.cancellation_date:
            result["cancellationDate"] = self.cancellation_date
        if self.note:
            result["note"] = self.note
        if self.patient_instruction:
            result["patientInstruction"] = self.patient_instruction
        if self.based_on:
            result["basedOn"] = self.based_on
        if self.subject:
            result["subject"] = self.subject
        if self.participant:
            result["participant"] = self.participant
        if self.recurrence_id:
            result["recurrenceId"] = self.recurrence_id
        if self.occurrence_changed:
            result["occurrenceChanged"] = self.occurrence_changed
        if self.recurrence_template:
            result["recurrenceTemplate"] = self.recurrence_template
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Appointment-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.status = data.get("status")
        self.cancellation_reason = data.get("cancellationReason")
        self.class_element = data.get("class", [])
        self.service_category = data.get("serviceCategory", [])
        self.service_type = data.get("serviceType", [])
        self.specialty = data.get("specialty", [])
        self.appointment_type = data.get("appointmentType")
        self.reason = data.get("reason", [])
        self.priority = data.get("priority")
        self.description = data.get("description")
        self.replaces = data.get("replaces", [])
        self.virtual_service = data.get("virtualService", [])
        self.supporting_information = data.get("supportingInformation", [])
        self.previous_appointment = data.get("previousAppointment")
        self.originating_appointment = data.get("originatingAppointment")
        self.start = data.get("start")
        self.end = data.get("end")
        self.minutes_duration = data.get("minutesDuration")
        self.requested_period = data.get("requestedPeriod", [])
        self.slot = data.get("slot", [])
        self.account = data.get("account", [])
        self.created = data.get("created")
        self.cancellation_date = data.get("cancellationDate")
        self.note = data.get("note", [])
        self.patient_instruction = data.get("patientInstruction", [])
        self.based_on = data.get("basedOn", [])
        self.subject = data.get("subject")
        self.participant = data.get("participant", [])
        self.recurrence_id = data.get("recurrenceId")
        self.occurrence_changed = data.get("occurrenceChanged")
        self.recurrence_template = data.get("recurrenceTemplate", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Appointment-specific fields."""
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = [
            "proposed", "pending", "booked", "arrived", "fulfilled",
            "cancelled", "noshow", "entered-in-error", "checked-in", "waitlist"
        ]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Participant is required
        if not self.participant:
            return False
        
        return True
    
    def is_booked(self) -> bool:
        """Check if appointment is booked."""
        return self.status == "booked"
    
    def is_cancelled(self) -> bool:
        """Check if appointment is cancelled."""
        return self.status == "cancelled"
    
    def add_participant(self, actor_reference: str, participant_type: Optional[list] = None, 
                       required: str = "required", status: str = "accepted") -> None:
        """Add a participant to the appointment."""
        participant = {
            "actor": {"reference": actor_reference},
            "required": required,
            "status": status
        }
        if participant_type:
            participant["type"] = participant_type
        
        self.participant.append(participant)