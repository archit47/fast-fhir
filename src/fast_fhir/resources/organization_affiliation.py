"""FHIR R5 OrganizationAffiliation resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class OrganizationAffiliation(FHIRResourceBase):
    """FHIR R5 OrganizationAffiliation resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize OrganizationAffiliation resource."""
        super().__init__("OrganizationAffiliation", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize OrganizationAffiliation-specific fields."""
        self.active: Optional[bool] = None
        self.period: Optional[Dict[str, Any]] = None
        self.organization: Optional[Dict[str, Any]] = None
        self.participating_organization: Optional[Dict[str, Any]] = None
        self.network: List[Dict[str, Any]] = []
        self.code: List[Dict[str, Any]] = []
        self.specialty: List[Dict[str, Any]] = []
        self.location: List[Dict[str, Any]] = []
        self.healthcare_service: List[Dict[str, Any]] = []
        self.telecom: List[Dict[str, Any]] = []
        self.endpoint: List[Dict[str, Any]] = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "organization_affiliation_create"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "organization_affiliation_parse"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "organization_affiliation_parse"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add OrganizationAffiliation-specific fields to the result dictionary."""
        if self.active is not None:
            result["active"] = self.active
        if self.period:
            result["period"] = self.period
        if self.organization:
            result["organization"] = self.organization
        if self.participating_organization:
            result["participatingOrganization"] = self.participating_organization
        if self.network:
            result["network"] = self.network
        if self.code:
            result["code"] = self.code
        if self.specialty:
            result["specialty"] = self.specialty
        if self.location:
            result["location"] = self.location
        if self.healthcare_service:
            result["healthcareService"] = self.healthcare_service
        if self.telecom:
            result["telecom"] = self.telecom
        if self.endpoint:
            result["endpoint"] = self.endpoint
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse OrganizationAffiliation-specific fields from data dictionary."""
        self.active = data.get("active")
        self.period = data.get("period")
        self.organization = data.get("organization")
        self.participating_organization = data.get("participatingOrganization")
        self.network = data.get("network", [])
        self.code = data.get("code", [])
        self.specialty = data.get("specialty", [])
        self.location = data.get("location", [])
        self.healthcare_service = data.get("healthcareService", [])
        self.telecom = data.get("telecom", [])
        self.endpoint = data.get("endpoint", [])
    
    def _validate_resource_specific(self) -> bool:
        """Perform OrganizationAffiliation-specific validation."""
        # OrganizationAffiliation-specific validation
        if not self.organization:
            return False
        
        if not self.participating_organization:
            return False
        
        return True
    
    
    def is_active(self) -> bool:
        """Check if the organization affiliation is active."""
        return self.active is True
    
    def get_primary_organization(self) -> Optional[Dict[str, Any]]:
        """Get the primary organization reference."""
        return self.organization
    
    def get_participating_organization(self) -> Optional[Dict[str, Any]]:
        """Get the participating organization reference."""
        return self.participating_organization
    
    def get_networks(self) -> List[Dict[str, Any]]:
        """Get all network affiliations."""
        return self.network.copy()
    
    def get_specialties(self) -> List[Dict[str, Any]]:
        """Get all specialties."""
        return self.specialty.copy()
    
    def get_locations(self) -> List[Dict[str, Any]]:
        """Get all location references."""
        return self.location.copy()
    
    def get_healthcare_services(self) -> List[Dict[str, Any]]:
        """Get all healthcare service references."""
        return self.healthcare_service.copy()
    
    def add_network(self, network: Dict[str, Any]) -> None:
        """Add a network affiliation."""
        if network not in self.network:
            self.network.append(network)
    
    def add_specialty(self, specialty: Dict[str, Any]) -> None:
        """Add a specialty."""
        if specialty not in self.specialty:
            self.specialty.append(specialty)
    
    def add_location(self, location: Dict[str, Any]) -> None:
        """Add a location reference."""
        if location not in self.location:
            self.location.append(location)
    
    def add_healthcare_service(self, service: Dict[str, Any]) -> None:
        """Add a healthcare service reference."""
        if service not in self.healthcare_service:
            self.healthcare_service.append(service)