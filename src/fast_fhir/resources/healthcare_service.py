"""FHIR R5 HealthcareService Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase


class HealthcareService(FHIRResourceBase):
    """FHIR R5 HealthcareService resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize HealthcareService-specific fields."""
        self.identifier = []
        self.active = None
        self.provided_by = None
        self.offered_in = []
        self.category = []
        self.type = []
        self.specialty = []
        self.location = []
        self.name = None
        self.comment = None
        self.extra_details = None
        self.photo = None
        self.contact = []
        self.coverage_area = []
        self.service_provision_code = []
        self.eligibility = []
        self.program = []
        self.characteristic = []
        self.communication = []
        self.referral_method = []
        self.appointment_required = None
        self.available_time = []
        self.not_available = []
        self.availability_exceptions = None
        self.endpoint = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_healthcare_service"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_healthcare_service"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_healthcare_service"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add HealthcareService-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.active is not None:
            result["active"] = self.active
        if self.provided_by:
            result["providedBy"] = self.provided_by
        if self.offered_in:
            result["offeredIn"] = self.offered_in
        if self.category:
            result["category"] = self.category
        if self.type:
            result["type"] = self.type
        if self.specialty:
            result["specialty"] = self.specialty
        if self.location:
            result["location"] = self.location
        if self.name:
            result["name"] = self.name
        if self.comment:
            result["comment"] = self.comment
        if self.extra_details:
            result["extraDetails"] = self.extra_details
        if self.photo:
            result["photo"] = self.photo
        if self.contact:
            result["contact"] = self.contact
        if self.coverage_area:
            result["coverageArea"] = self.coverage_area
        if self.service_provision_code:
            result["serviceProvisionCode"] = self.service_provision_code
        if self.eligibility:
            result["eligibility"] = self.eligibility
        if self.program:
            result["program"] = self.program
        if self.characteristic:
            result["characteristic"] = self.characteristic
        if self.communication:
            result["communication"] = self.communication
        if self.referral_method:
            result["referralMethod"] = self.referral_method
        if self.appointment_required is not None:
            result["appointmentRequired"] = self.appointment_required
        if self.available_time:
            result["availableTime"] = self.available_time
        if self.not_available:
            result["notAvailable"] = self.not_available
        if self.availability_exceptions:
            result["availabilityExceptions"] = self.availability_exceptions
        if self.endpoint:
            result["endpoint"] = self.endpoint
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse HealthcareService-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.active = data.get("active")
        self.provided_by = data.get("providedBy")
        self.offered_in = data.get("offeredIn", [])
        self.category = data.get("category", [])
        self.type = data.get("type", [])
        self.specialty = data.get("specialty", [])
        self.location = data.get("location", [])
        self.name = data.get("name")
        self.comment = data.get("comment")
        self.extra_details = data.get("extraDetails")
        self.photo = data.get("photo")
        self.contact = data.get("contact", [])
        self.coverage_area = data.get("coverageArea", [])
        self.service_provision_code = data.get("serviceProvisionCode", [])
        self.eligibility = data.get("eligibility", [])
        self.program = data.get("program", [])
        self.characteristic = data.get("characteristic", [])
        self.communication = data.get("communication", [])
        self.referral_method = data.get("referralMethod", [])
        self.appointment_required = data.get("appointmentRequired")
        self.available_time = data.get("availableTime", [])
        self.not_available = data.get("notAvailable", [])
        self.availability_exceptions = data.get("availabilityExceptions")
        self.endpoint = data.get("endpoint", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate HealthcareService-specific fields."""
        # Basic validation - no specific requirements
        return True
    
    def is_active(self) -> bool:
        """Check if healthcare service is active."""
        return self.active if self.active is not None else True
    
    def requires_appointment(self) -> bool:
        """Check if service requires appointment."""
        return self.appointment_required if self.appointment_required is not None else False
    
    def get_service_types(self) -> list:
        """Get service types."""
        return self.type
    
    def get_specialties(self) -> list:
        """Get service specialties."""
        return self.specialty