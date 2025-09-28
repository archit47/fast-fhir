"""FHIR R5 EpisodeOfCare resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class EpisodeOfCare(FHIRResourceBase):
    """FHIR R5 EpisodeOfCare resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize EpisodeOfCare resource."""
        super().__init__("EpisodeOfCare", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize EpisodeOfCare-specific fields."""
        # EpisodeOfCare-specific attributes
        self.status: Optional[str] = None  # planned | waitlist | active | onhold | finished | cancelled | entered-in-error
        self.status_history: List[Dict[str, Any]] = []
        self.type: List[Dict[str, Any]] = []
        self.diagnosis: List[Dict[str, Any]] = []
        self.patient: Optional[Dict[str, Any]] = None
        self.managing_organization: Optional[Dict[str, Any]] = None
        self.period: Optional[Dict[str, Any]] = None
        self.referral_request: List[Dict[str, Any]] = []
        self.care_manager: Optional[Dict[str, Any]] = None
        self.team: List[Dict[str, Any]] = []
        self.account: List[Dict[str, Any]] = []
    def to_dict(self) -> Dict[str, Any]:
        """Convert EpisodeOfCare to dictionary representation."""
        result = super().to_dict()
        
        # Add EpisodeOfCare-specific fields
        if self.status:
            result["status"] = self.status
        if self.status_history:
            result["statusHistory"] = self.status_history
        if self.type:
            result["type"] = self.type
        if self.diagnosis:
            result["diagnosis"] = self.diagnosis
        if self.patient:
            result["patient"] = self.patient
        if self.managing_organization:
            result["managingOrganization"] = self.managing_organization
        if self.period:
            result["period"] = self.period
        if self.referral_request:
            result["referralRequest"] = self.referral_request
        if self.care_manager:
            result["careManager"] = self.care_manager
        if self.team:
            result["team"] = self.team
        if self.account:
            result["account"] = self.account
        
        return result
    
    
    
    def is_active(self) -> bool:
        """Check if the episode of care is active."""
        return self.status == "active"
    
    def is_finished(self) -> bool:
        """Check if the episode of care is finished."""
        return self.status == "finished"
    
    def is_planned(self) -> bool:
        """Check if the episode of care is planned."""
        return self.status == "planned"
    
    def is_on_hold(self) -> bool:
        """Check if the episode of care is on hold."""
        return self.status == "onhold"
    
    def is_cancelled(self) -> bool:
        """Check if the episode of care is cancelled."""
        return self.status == "cancelled"
    
    def is_on_waitlist(self) -> bool:
        """Check if the episode of care is on waitlist."""
        return self.status == "waitlist"
    
    def get_patient(self) -> Optional[Dict[str, Any]]:
        """Get the patient reference."""
        return self.patient
    
    def get_managing_organization(self) -> Optional[Dict[str, Any]]:
        """Get the managing organization reference."""
        return self.managing_organization
    
    def get_care_manager(self) -> Optional[Dict[str, Any]]:
        """Get the care manager reference."""
        return self.care_manager
    
    def get_period(self) -> Optional[Dict[str, Any]]:
        """Get the episode period."""
        return self.period
    
    def get_types(self) -> List[Dict[str, Any]]:
        """Get all episode types."""
        return self.type.copy()
    
    def get_diagnoses(self) -> List[Dict[str, Any]]:
        """Get all diagnoses."""
        return self.diagnosis.copy()
    
    def get_status_history(self) -> List[Dict[str, Any]]:
        """Get the status history."""
        return self.status_history.copy()
    
    def get_referral_requests(self) -> List[Dict[str, Any]]:
        """Get all referral requests."""
        return self.referral_request.copy()
    
    def get_care_teams(self) -> List[Dict[str, Any]]:
        """Get all care teams."""
        return self.team.copy()
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        """Get all accounts."""
        return self.account.copy()
    
    def set_status(self, status: str) -> None:
        """Set the episode of care status."""
        valid_statuses = ["planned", "waitlist", "active", "onhold", "finished", "cancelled", "entered-in-error"]
        if status in valid_statuses:
            # Add to status history if status is changing
            if self.status and self.status != status:
                self.add_status_history({
                    "status": self.status,
                    "period": {"end": "now"}  # Simplified - should use proper datetime
                })
            self.status = status
        else:
            raise ValueError(f"Invalid status: {status}")
    
    def set_patient(self, patient: Dict[str, Any]) -> None:
        """Set the patient reference."""
        self.patient = patient
    
    def set_managing_organization(self, organization: Dict[str, Any]) -> None:
        """Set the managing organization reference."""
        self.managing_organization = organization
    
    def set_care_manager(self, care_manager: Dict[str, Any]) -> None:
        """Set the care manager reference."""
        self.care_manager = care_manager
    
    def set_period(self, period: Dict[str, Any]) -> None:
        """Set the episode period."""
        self.period = period
    
    def add_type(self, episode_type: Dict[str, Any]) -> None:
        """Add an episode type."""
        if episode_type not in self.type:
            self.type.append(episode_type)
    
    def add_diagnosis(self, diagnosis: Dict[str, Any]) -> None:
        """Add a diagnosis."""
        self.diagnosis.append(diagnosis)
    
    def add_status_history(self, status_history: Dict[str, Any]) -> None:
        """Add status history entry."""
        self.status_history.append(status_history)
    
    def add_referral_request(self, referral: Dict[str, Any]) -> None:
        """Add a referral request."""
        if referral not in self.referral_request:
            self.referral_request.append(referral)
    
    def add_care_team(self, team: Dict[str, Any]) -> None:
        """Add a care team."""
        if team not in self.team:
            self.team.append(team)
    
    def add_account(self, account: Dict[str, Any]) -> None:
        """Add an account."""
        if account not in self.account:
            self.account.append(account)
    
    def get_primary_diagnosis(self) -> Optional[Dict[str, Any]]:
        """Get the primary diagnosis (rank 1)."""
        for diagnosis in self.diagnosis:
            if diagnosis.get("rank") == 1:
                return diagnosis
        return None
    
    def get_diagnoses_by_role(self, role_code: str) -> List[Dict[str, Any]]:
        """Get diagnoses by role code."""
        matching_diagnoses = []
        for diagnosis in self.diagnosis:
            if diagnosis.get("role", {}).get("coding"):
                for coding in diagnosis["role"]["coding"]:
                    if coding.get("code") == role_code:
                        matching_diagnoses.append(diagnosis)
                        break
        return matching_diagnoses
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "create_episode_of_care"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "parse_episode_of_care"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "parse_episode_of_care"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add EpisodeOfCare-specific fields to the result dictionary."""
        # TODO: Implement resource-specific field serialization
        pass
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse EpisodeOfCare-specific fields from data dictionary."""
        # TODO: Implement resource-specific field parsing
        pass
    
    def _validate_resource_specific(self) -> bool:
        """Perform EpisodeOfCare-specific validation."""
        # EpisodeOfCare requires status and patient
        return self.status is not None and self.patient is not None
