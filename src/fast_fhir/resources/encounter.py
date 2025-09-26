"""FHIR R5 Encounter Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Encounter(FHIRResourceBase):
    """FHIR R5 Encounter resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Encounter-specific fields."""
        self.identifier = []
        self.status = None  # Required: planned | in-progress | on-hold | discharged | completed | cancelled | discontinued | entered-in-error | unknown
        self.class_element = None  # Required: Classification of patient encounter
        self.priority = None
        self.type = []
        self.service_type = []
        self.subject = None
        self.subject_status = None
        self.episode_of_care = []
        self.based_on = []
        self.care_team = []
        self.part_of = None
        self.service_provider = None
        self.participant = []
        self.appointment = []
        self.virtual_service = []
        self.actual_period = None
        self.planned_start_date = None
        self.planned_end_date = None
        self.length = None
        self.reason = []
        self.diagnosis = []
        self.account = []
        self.diet_preference = []
        self.special_arrangement = []
        self.special_courtesy = []
        self.admission = None
        self.location = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_encounter"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_encounter"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_encounter"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Encounter-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.status:
            result["status"] = self.status
        if self.class_element:
            result["class"] = self.class_element
        if self.priority:
            result["priority"] = self.priority
        if self.type:
            result["type"] = self.type
        if self.service_type:
            result["serviceType"] = self.service_type
        if self.subject:
            result["subject"] = self.subject
        if self.subject_status:
            result["subjectStatus"] = self.subject_status
        if self.episode_of_care:
            result["episodeOfCare"] = self.episode_of_care
        if self.based_on:
            result["basedOn"] = self.based_on
        if self.care_team:
            result["careTeam"] = self.care_team
        if self.part_of:
            result["partOf"] = self.part_of
        if self.service_provider:
            result["serviceProvider"] = self.service_provider
        if self.participant:
            result["participant"] = self.participant
        if self.appointment:
            result["appointment"] = self.appointment
        if self.virtual_service:
            result["virtualService"] = self.virtual_service
        if self.actual_period:
            result["actualPeriod"] = self.actual_period
        if self.planned_start_date:
            result["plannedStartDate"] = self.planned_start_date
        if self.planned_end_date:
            result["plannedEndDate"] = self.planned_end_date
        if self.length:
            result["length"] = self.length
        if self.reason:
            result["reason"] = self.reason
        if self.diagnosis:
            result["diagnosis"] = self.diagnosis
        if self.account:
            result["account"] = self.account
        if self.diet_preference:
            result["dietPreference"] = self.diet_preference
        if self.special_arrangement:
            result["specialArrangement"] = self.special_arrangement
        if self.special_courtesy:
            result["specialCourtesy"] = self.special_courtesy
        if self.admission:
            result["admission"] = self.admission
        if self.location:
            result["location"] = self.location
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Encounter-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.status = data.get("status")
        self.class_element = data.get("class")
        self.priority = data.get("priority")
        self.type = data.get("type", [])
        self.service_type = data.get("serviceType", [])
        self.subject = data.get("subject")
        self.subject_status = data.get("subjectStatus")
        self.episode_of_care = data.get("episodeOfCare", [])
        self.based_on = data.get("basedOn", [])
        self.care_team = data.get("careTeam", [])
        self.part_of = data.get("partOf")
        self.service_provider = data.get("serviceProvider")
        self.participant = data.get("participant", [])
        self.appointment = data.get("appointment", [])
        self.virtual_service = data.get("virtualService", [])
        self.actual_period = data.get("actualPeriod")
        self.planned_start_date = data.get("plannedStartDate")
        self.planned_end_date = data.get("plannedEndDate")
        self.length = data.get("length")
        self.reason = data.get("reason", [])
        self.diagnosis = data.get("diagnosis", [])
        self.account = data.get("account", [])
        self.diet_preference = data.get("dietPreference", [])
        self.special_arrangement = data.get("specialArrangement", [])
        self.special_courtesy = data.get("specialCourtesy", [])
        self.admission = data.get("admission")
        self.location = data.get("location", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Encounter-specific fields."""
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = [
            "planned", "in-progress", "on-hold", "discharged", "completed",
            "cancelled", "discontinued", "entered-in-error", "unknown"
        ]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Class is required
        if not self.class_element:
            return False
        
        return True
    
    def is_completed(self) -> bool:
        """Check if encounter is completed."""
        return self.status == "completed"
    
    def is_in_progress(self) -> bool:
        """Check if encounter is in progress."""
        return self.status == "in-progress"
    
    def get_encounter_class(self) -> Optional[str]:
        """Get encounter class code."""
        if isinstance(self.class_element, dict):
            return self.class_element.get("code")
        return self.class_element
    
    def get_participants(self) -> list:
        """Get encounter participants."""
        return self.participant
    
    def add_participant(self, actor_reference: str, participant_type: Optional[list] = None, period: Optional[dict] = None) -> None:
        """Add a participant to the encounter."""
        participant = {
            "actor": {"reference": actor_reference}
        }
        if participant_type:
            participant["type"] = participant_type
        if period:
            participant["period"] = period
        
        self.participant.append(participant)
    
    def get_diagnoses(self) -> list:
        """Get encounter diagnoses."""
        return self.diagnosis
    
    def add_diagnosis(self, condition_reference: str, use_code: Optional[str] = None, rank: Optional[int] = None) -> None:
        """Add a diagnosis to the encounter."""
        diagnosis = {
            "condition": [{"reference": condition_reference}]
        }
        if use_code:
            diagnosis["use"] = [{"coding": [{"code": use_code}]}]
        if rank:
            diagnosis["rank"] = rank
        
        self.diagnosis.append(diagnosis)
    
    def get_locations(self) -> list:
        """Get encounter locations."""
        return self.location
    
    def add_location(self, location_reference: str, status: str = "active", period: Optional[dict] = None) -> None:
        """Add a location to the encounter."""
        location = {
            "location": {"reference": location_reference},
            "status": status
        }
        if period:
            location["period"] = period
        
        self.location.append(location)