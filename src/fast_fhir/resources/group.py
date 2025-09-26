"""FHIR R5 Group Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Group(FHIRResourceBase):
    """FHIR R5 Group resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Group-specific fields."""
        self.identifier = []
        self.active = None
        self.type = None  # Required: person | animal | practitioner | device | careteam | healthcareservice | location | organization | relatedperson | specimen
        self.actual = None  # Required: true if actual group, false if descriptive
        self.code = None
        self.name = None
        self.description = None
        self.quantity = None
        self.managing_entity = None
        self.characteristic = []
        self.member = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_group"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_group"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_group"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Group-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.active is not None:
            result["active"] = self.active
        if self.type:
            result["type"] = self.type
        if self.actual is not None:
            result["actual"] = self.actual
        if self.code:
            result["code"] = self.code
        if self.name:
            result["name"] = self.name
        if self.description:
            result["description"] = self.description
        if self.quantity is not None:
            result["quantity"] = self.quantity
        if self.managing_entity:
            result["managingEntity"] = self.managing_entity
        if self.characteristic:
            result["characteristic"] = self.characteristic
        if self.member:
            result["member"] = self.member
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Group-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.active = data.get("active")
        self.type = data.get("type")
        self.actual = data.get("actual")
        self.code = data.get("code")
        self.name = data.get("name")
        self.description = data.get("description")
        self.quantity = data.get("quantity")
        self.managing_entity = data.get("managingEntity")
        self.characteristic = data.get("characteristic", [])
        self.member = data.get("member", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate Group-specific fields."""
        # Type is required
        if not self.type:
            return False
        
        # Validate type code
        valid_types = [
            "person", "animal", "practitioner", "device", "careteam",
            "healthcareservice", "location", "organization", "relatedperson", "specimen"
        ]
        if not validate_fhir_code(self.type, valid_types):
            return False
        
        # Actual is required
        if self.actual is None:
            return False
        
        return True
    
    def is_active(self) -> bool:
        """Check if group is active."""
        return self.active if self.active is not None else True
    
    def is_actual_group(self) -> bool:
        """Check if this is an actual group (vs descriptive)."""
        return self.actual is True
    
    def get_member_count(self) -> int:
        """Get the number of members in the group."""
        if self.quantity is not None:
            return self.quantity
        return len(self.member)
    
    def get_members(self) -> list:
        """Get group members."""
        return self.member
    
    def add_member(self, entity_reference: str, period: Optional[dict] = None, inactive: bool = False) -> None:
        """Add a member to the group."""
        member = {
            "entity": {"reference": entity_reference},
            "inactive": inactive
        }
        if period:
            member["period"] = period
        
        self.member.append(member)
        
        # Update quantity if it's an actual group
        if self.actual:
            self.quantity = len(self.member)
    
    def remove_member(self, entity_reference: str) -> bool:
        """Remove a member from the group."""
        for i, member in enumerate(self.member):
            if (isinstance(member, dict) and 
                member.get("entity", {}).get("reference") == entity_reference):
                del self.member[i]
                
                # Update quantity if it's an actual group
                if self.actual:
                    self.quantity = len(self.member)
                return True
        return False
    
    def has_member(self, entity_reference: str) -> bool:
        """Check if entity is a member of the group."""
        for member in self.member:
            if (isinstance(member, dict) and 
                member.get("entity", {}).get("reference") == entity_reference):
                return True
        return False
    
    def get_characteristics(self) -> list:
        """Get group characteristics."""
        return self.characteristic