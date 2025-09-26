"""FHIR R5 Schedule Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase


class Schedule(FHIRResourceBase):
    """FHIR R5 Schedule resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Schedule-specific fields."""
        self.identifier = []
        self.active = None
        self.service_category = []
        self.service_type = []
        self.specialty = []
        self.name = None
        self.actor = []  # Required
        self.planning_horizon = None
        self.comment = None
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_schedule"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_schedule"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_schedule"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Schedule-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.active is not None:
            result["active"] = self.active
        if self.service_category:
            result["serviceCategory"] = self.service_category
        if self.service_type:
            result["serviceType"] = self.service_type
        if self.specialty:
            result["specialty"] = self.specialty
        if self.name:
            result["name"] = self.name
        if self.actor:
            result["actor"] = self.actor
        if self.planning_horizon:
            result["planningHorizon"] = self.planning_horizon
        if self.comment:
            result["comment"] = self.comment
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Schedule-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.active = data.get("active")
        self.service_category = data.get("serviceCategory", [])
        self.service_type = data.get("serviceType", [])
        self.specialty = data.get("specialty", [])
        self.name = data.get("name")
        self.actor = data.get("actor", [])
        self.planning_horizon = data.get("planningHorizon")
        self.comment = data.get("comment")
    
    def _validate_resource_specific(self) -> bool:
        """Validate Schedule-specific fields."""
        # Actor is required
        if not self.actor:
            return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if schedule is active."""
        return self.active if self.active is not None else True
    
    def get_actors(self) -> list:
        """Get schedule actors."""
        return self.actor
    
    def add_actor(self, actor_reference: str) -> None:
        """Add an actor to the schedule."""
        self.actor.append({"reference": actor_reference})