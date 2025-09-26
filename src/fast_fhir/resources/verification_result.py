"""FHIR R5 VerificationResult resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class VerificationResult(FHIRResourceBase):
    """FHIR R5 VerificationResult resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize VerificationResult resource."""
        super().__init__("VerificationResult", id, use_c_extensions)
        
        # VerificationResult-specific attributes
        self.target: List[Dict[str, Any]] = []
        self.target_location: List[str] = []
        self.need: Optional[Dict[str, Any]] = None
        self.status: Optional[str] = None  # attested | validated | in-process | req-revalid | val-fail | reval-fail
        self.status_date: Optional[str] = None
        self.validation_type: Optional[Dict[str, Any]] = None
        self.validation_process: List[Dict[str, Any]] = []
        self.frequency: Optional[Dict[str, Any]] = None
        self.last_performed: Optional[str] = None
        self.next_scheduled: Optional[str] = None
        self.failure_action: Optional[Dict[str, Any]] = None
        self.primary_source: List[Dict[str, Any]] = []
        self.attestation: Optional[Dict[str, Any]] = None
        self.validator: List[Dict[str, Any]] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert VerificationResult to dictionary representation."""
        result = super().to_dict()
        
        # Add VerificationResult-specific fields
        if self.target:
            result["target"] = self.target
        if self.target_location:
            result["targetLocation"] = self.target_location
        if self.need:
            result["need"] = self.need
        if self.status:
            result["status"] = self.status
        if self.status_date:
            result["statusDate"] = self.status_date
        if self.validation_type:
            result["validationType"] = self.validation_type
        if self.validation_process:
            result["validationProcess"] = self.validation_process
        if self.frequency:
            result["frequency"] = self.frequency
        if self.last_performed:
            result["lastPerformed"] = self.last_performed
        if self.next_scheduled:
            result["nextScheduled"] = self.next_scheduled
        if self.failure_action:
            result["failureAction"] = self.failure_action
        if self.primary_source:
            result["primarySource"] = self.primary_source
        if self.attestation:
            result["attestation"] = self.attestation
        if self.validator:
            result["validator"] = self.validator
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VerificationResult':
        """Create VerificationResult from dictionary representation."""
        instance = cls(data.get("id"))
        instance._populate_from_dict(data)
        
        # Set VerificationResult-specific fields
        instance.target = data.get("target", [])
        instance.target_location = data.get("targetLocation", [])
        instance.need = data.get("need")
        instance.status = data.get("status")
        instance.status_date = data.get("statusDate")
        instance.validation_type = data.get("validationType")
        instance.validation_process = data.get("validationProcess", [])
        instance.frequency = data.get("frequency")
        instance.last_performed = data.get("lastPerformed")
        instance.next_scheduled = data.get("nextScheduled")
        instance.failure_action = data.get("failureAction")
        instance.primary_source = data.get("primarySource", [])
        instance.attestation = data.get("attestation")
        instance.validator = data.get("validator", [])
        
        return instance
    
    def validate(self) -> List[str]:
        """Validate VerificationResult resource."""
        errors = super().validate()
        
        # VerificationResult-specific validation
        if not self.target:
            errors.append("VerificationResult.target is required")
        
        if not self.status:
            errors.append("VerificationResult.status is required")
        
        # Validate status values
        valid_statuses = ["attested", "validated", "in-process", "req-revalid", "val-fail", "reval-fail"]
        if self.status and self.status not in valid_statuses:
            errors.append(f"VerificationResult.status must be one of: {', '.join(valid_statuses)}")
        
        return errors
    
    def is_validated(self) -> bool:
        """Check if the verification result is validated."""
        return self.status == "validated"
    
    def is_attested(self) -> bool:
        """Check if the verification result is attested."""
        return self.status == "attested"
    
    def is_in_process(self) -> bool:
        """Check if the verification is in process."""
        return self.status == "in-process"
    
    def requires_revalidation(self) -> bool:
        """Check if revalidation is required."""
        return self.status == "req-revalid"
    
    def has_validation_failed(self) -> bool:
        """Check if validation has failed."""
        return self.status in ["val-fail", "reval-fail"]
    
    def get_targets(self) -> List[Dict[str, Any]]:
        """Get all verification targets."""
        return self.target.copy()
    
    def get_target_locations(self) -> List[str]:
        """Get all target locations."""
        return self.target_location.copy()
    
    def get_validation_type(self) -> Optional[Dict[str, Any]]:
        """Get the validation type."""
        return self.validation_type
    
    def get_validation_processes(self) -> List[Dict[str, Any]]:
        """Get all validation processes."""
        return self.validation_process.copy()
    
    def get_primary_sources(self) -> List[Dict[str, Any]]:
        """Get all primary sources."""
        return self.primary_source.copy()
    
    def get_validators(self) -> List[Dict[str, Any]]:
        """Get all validators."""
        return self.validator.copy()
    
    def get_attestation(self) -> Optional[Dict[str, Any]]:
        """Get the attestation information."""
        return self.attestation
    
    def get_last_performed(self) -> Optional[str]:
        """Get the last performed date."""
        return self.last_performed
    
    def get_next_scheduled(self) -> Optional[str]:
        """Get the next scheduled date."""
        return self.next_scheduled
    
    def set_status(self, status: str) -> None:
        """Set the verification status."""
        valid_statuses = ["attested", "validated", "in-process", "req-revalid", "val-fail", "reval-fail"]
        if status in valid_statuses:
            self.status = status
        else:
            raise ValueError(f"Invalid status: {status}")
    
    def add_target(self, target: Dict[str, Any]) -> None:
        """Add a verification target."""
        if target not in self.target:
            self.target.append(target)
    
    def add_target_location(self, location: str) -> None:
        """Add a target location."""
        if location not in self.target_location:
            self.target_location.append(location)
    
    def add_validation_process(self, process: Dict[str, Any]) -> None:
        """Add a validation process."""
        if process not in self.validation_process:
            self.validation_process.append(process)
    
    def add_primary_source(self, source: Dict[str, Any]) -> None:
        """Add a primary source."""
        self.primary_source.append(source)
    
    def add_validator(self, validator: Dict[str, Any]) -> None:
        """Add a validator."""
        self.validator.append(validator)
    
    def set_validation_type(self, validation_type: Dict[str, Any]) -> None:
        """Set the validation type."""
        self.validation_type = validation_type
    
    def set_attestation(self, attestation: Dict[str, Any]) -> None:
        """Set the attestation information."""
        self.attestation = attestation
    
    def set_frequency(self, frequency: Dict[str, Any]) -> None:
        """Set the validation frequency."""
        self.frequency = frequency
    
    def set_last_performed(self, date: str) -> None:
        """Set the last performed date."""
        self.last_performed = date
    
    def set_next_scheduled(self, date: str) -> None:
        """Set the next scheduled date."""
        self.next_scheduled = date
    
    def set_failure_action(self, action: Dict[str, Any]) -> None:
        """Set the failure action."""
        self.failure_action = action