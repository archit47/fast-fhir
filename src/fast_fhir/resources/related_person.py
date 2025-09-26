"""FHIR R5 RelatedPerson Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, FHIRPersonResourceMixin


class RelatedPerson(FHIRResourceBase, FHIRPersonResourceMixin):
    """FHIR R5 RelatedPerson resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize RelatedPerson-specific fields."""
        # Initialize person fields from mixin
        self._init_person_fields()
        
        # RelatedPerson-specific fields
        self.patient = None  # Required reference to Patient
        self.relationship = []
        self.period = None
        self.communication = []
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_related_person"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_related_person"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_related_person"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add RelatedPerson-specific fields to dictionary."""
        # Add person fields from mixin
        self._add_person_fields_to_dict(result)
        
        # Add RelatedPerson-specific fields
        if self.patient:
            result["patient"] = self.patient
        if self.relationship:
            result["relationship"] = self.relationship
        if self.period:
            result["period"] = self.period
        if self.communication:
            result["communication"] = self.communication
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse RelatedPerson-specific fields from dictionary."""
        # Parse person fields from mixin
        self._parse_person_fields_from_dict(data)
        
        # Parse RelatedPerson-specific fields
        self.patient = data.get("patient")
        self.relationship = data.get("relationship", [])
        self.period = data.get("period")
        self.communication = data.get("communication", [])
    
    def _validate_resource_specific(self) -> bool:
        """Validate RelatedPerson-specific fields."""
        # Use person validation from mixin
        if not self._validate_person_fields():
            return False
        
        # RelatedPerson must have a patient reference
        if not self.patient:
            return False
        
        return True
    
    def get_relationships(self) -> list:
        """Get relationship types to the patient."""
        return self.relationship
    
    def has_relationship(self, relationship_code: str) -> bool:
        """Check if related person has a specific relationship to the patient."""
        for rel in self.relationship:
            if isinstance(rel, dict) and rel.get("coding"):
                for coding in rel["coding"]:
                    if coding.get("code") == relationship_code:
                        return True
        return False
    
    def get_patient_reference(self) -> Optional[str]:
        """Get the patient reference."""
        if isinstance(self.patient, dict):
            return self.patient.get("reference")
        return self.patient