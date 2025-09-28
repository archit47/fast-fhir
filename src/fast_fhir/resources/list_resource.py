"""FHIR R5 List Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class ListResource(FHIRResourceBase):
    """FHIR R5 List resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize List resource."""
        super().__init__("List", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize List-specific fields."""
        self.identifier = []
        self.status = None  # Required: current | retired | entered-in-error
        self.mode = None  # Required: working | snapshot | changes
        self.title = None
        self.code = None
        self.subject = []
        self.encounter = None
        self.date = None
        self.source = None
        self.ordered_by = None
        self.note = []
        self.entry = []
        self.empty_reason = None
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_list"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_list"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_list"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add List-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
        if self.status:
            result["status"] = self.status
        if self.mode:
            result["mode"] = self.mode
        if self.title:
            result["title"] = self.title
        if self.code:
            result["code"] = self.code
        if self.subject:
            result["subject"] = self.subject
        if self.encounter:
            result["encounter"] = self.encounter
        if self.date:
            result["date"] = self.date
        if self.source:
            result["source"] = self.source
        if self.ordered_by:
            result["orderedBy"] = self.ordered_by
        if self.note:
            result["note"] = self.note
        if self.entry:
            result["entry"] = self.entry
        if self.empty_reason:
            result["emptyReason"] = self.empty_reason
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse List-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.status = data.get("status")
        self.mode = data.get("mode")
        self.title = data.get("title")
        self.code = data.get("code")
        self.subject = data.get("subject", [])
        self.encounter = data.get("encounter")
        self.date = data.get("date")
        self.source = data.get("source")
        self.ordered_by = data.get("orderedBy")
        self.note = data.get("note", [])
        self.entry = data.get("entry", [])
        self.empty_reason = data.get("emptyReason")
    
    def _validate_resource_specific(self) -> bool:
        """Validate List-specific fields."""
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = ["current", "retired", "entered-in-error"]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Mode is required
        if not self.mode:
            return False
        
        # Validate mode code
        valid_modes = ["working", "snapshot", "changes"]
        if not validate_fhir_code(self.mode, valid_modes):
            return False
        
        return True
    
    def is_current(self) -> bool:
        """Check if list is current."""
        return self.status == "current"
    
    def get_entry_count(self) -> int:
        """Get number of entries in the list."""
        return len(self.entry)
    
    def add_entry(self, item_reference: str, deleted: bool = False) -> None:
        """Add an entry to the list."""
        entry = {
            "item": {"reference": item_reference}
        }
        if deleted:
            entry["deleted"] = deleted
        
        self.entry.append(entry)
    
    def get_entries(self) -> list:
        """Get list entries."""
        return self.entry