"""FHIR R5 Transport resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class Transport(FHIRResourceBase):
    """FHIR R5 Transport resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize Transport resource."""
        super().__init__("Transport", id, use_c_extensions)
    
    def _init_resource_fields(self) -> None:
        """Initialize Transport-specific fields."""
        # Transport-specific attributes
        self.instantiates_canonical: Optional[str] = None
        self.instantiates_uri: Optional[str] = None
        self.based_on: List[Dict[str, Any]] = []
        self.group_identifier: Optional[Dict[str, Any]] = None
        self.part_of: List[Dict[str, Any]] = []
        self.status: Optional[str] = None  # draft | requested | received | accepted | rejected | in-progress | completed | cancelled | entered-in-error
        self.status_reason: Optional[Dict[str, Any]] = None
        self.intent: Optional[str] = None  # unknown | proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option
        self.priority: Optional[str] = None  # routine | urgent | asap | stat
        self.code: Optional[Dict[str, Any]] = None
        self.description: Optional[str] = None
        self.focus: Optional[Dict[str, Any]] = None
        self.for_reference: Optional[Dict[str, Any]] = None
        self.encounter: Optional[Dict[str, Any]] = None
        self.completion_time: Optional[Dict[str, Any]] = None
        self.authored_on: Optional[str] = None
        self.last_modified: Optional[str] = None
        self.requester: Optional[Dict[str, Any]] = None
        self.performer_type: Optional[Dict[str, Any]] = None
        self.owner: Optional[Dict[str, Any]] = None
        self.location: Optional[Dict[str, Any]] = None
        self.insurance: List[Dict[str, Any]] = []
        self.note: List[Dict[str, Any]] = []
        self.relevant_history: List[Dict[str, Any]] = []
        self.restriction: Optional[Dict[str, Any]] = None
        self.input: List[Dict[str, Any]] = []
        self.output: List[Dict[str, Any]] = []
        self.requested_location: Optional[Dict[str, Any]] = None
        self.current_location: Optional[Dict[str, Any]] = None
        self.reason_code: Optional[Dict[str, Any]] = None
        self.reason_reference: Optional[Dict[str, Any]] = None
        self.history: Optional[Dict[str, Any]] = None
    def to_dict(self) -> Dict[str, Any]:
        """Convert Transport to dictionary representation."""
        result = super().to_dict()
        
        # Add Transport-specific fields
        if self.instantiates_canonical:
            result["instantiatesCanonical"] = self.instantiates_canonical
        if self.instantiates_uri:
            result["instantiatesUri"] = self.instantiates_uri
        if self.based_on:
            result["basedOn"] = self.based_on
        if self.group_identifier:
            result["groupIdentifier"] = self.group_identifier
        if self.part_of:
            result["partOf"] = self.part_of
        if self.status:
            result["status"] = self.status
        if self.status_reason:
            result["statusReason"] = self.status_reason
        if self.intent:
            result["intent"] = self.intent
        if self.priority:
            result["priority"] = self.priority
        if self.code:
            result["code"] = self.code
        if self.description:
            result["description"] = self.description
        if self.focus:
            result["focus"] = self.focus
        if self.for_reference:
            result["for"] = self.for_reference
        if self.encounter:
            result["encounter"] = self.encounter
        if self.completion_time:
            result["completionTime"] = self.completion_time
        if self.authored_on:
            result["authoredOn"] = self.authored_on
        if self.last_modified:
            result["lastModified"] = self.last_modified
        if self.requester:
            result["requester"] = self.requester
        if self.performer_type:
            result["performerType"] = self.performer_type
        if self.owner:
            result["owner"] = self.owner
        if self.location:
            result["location"] = self.location
        if self.insurance:
            result["insurance"] = self.insurance
        if self.note:
            result["note"] = self.note
        if self.relevant_history:
            result["relevantHistory"] = self.relevant_history
        if self.restriction:
            result["restriction"] = self.restriction
        if self.input:
            result["input"] = self.input
        if self.output:
            result["output"] = self.output
        if self.requested_location:
            result["requestedLocation"] = self.requested_location
        if self.current_location:
            result["currentLocation"] = self.current_location
        if self.reason_code:
            result["reasonCode"] = self.reason_code
        if self.reason_reference:
            result["reasonReference"] = self.reason_reference
        if self.history:
            result["history"] = self.history
        
        return result
    
    
    
    def is_completed(self) -> bool:
        """Check if the transport is completed."""
        return self.status == "completed"
    
    def is_in_progress(self) -> bool:
        """Check if the transport is in progress."""
        return self.status == "in-progress"
    
    def is_cancelled(self) -> bool:
        """Check if the transport is cancelled."""
        return self.status == "cancelled"
    
    def is_high_priority(self) -> bool:
        """Check if the transport has high priority (urgent, asap, or stat)."""
        return self.priority in ["urgent", "asap", "stat"]
    
    def get_requested_location(self) -> Optional[Dict[str, Any]]:
        """Get the requested location."""
        return self.requested_location
    
    def get_current_location(self) -> Optional[Dict[str, Any]]:
        """Get the current location."""
        return self.current_location
    
    def set_status(self, status: str) -> None:
        """Set the transport status."""
        valid_statuses = ["draft", "requested", "received", "accepted", "rejected", 
                         "in-progress", "completed", "cancelled", "entered-in-error"]
        if status in valid_statuses:
            self.status = status
        else:
            raise ValueError(f"Invalid status: {status}")
    
    def set_priority(self, priority: str) -> None:
        """Set the transport priority."""
        valid_priorities = ["routine", "urgent", "asap", "stat"]
        if priority in valid_priorities:
            self.priority = priority
        else:
            raise ValueError(f"Invalid priority: {priority}")
    
    def add_input(self, input_item: Dict[str, Any]) -> None:
        """Add an input parameter."""
        self.input.append(input_item)
    
    def add_output(self, output_item: Dict[str, Any]) -> None:
        """Add an output parameter."""
        self.output.append(output_item)
    
    def add_note(self, note: Dict[str, Any]) -> None:
        """Add a note."""
        self.note.append(note)
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get the C extension create function name."""
        return "create_transport"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get the C extension parse function name."""
        return "parse_transport"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of _get_c_extension_parse_function."""
        return "parse_transport"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Transport-specific fields to the result dictionary."""
        # TODO: Implement resource-specific field serialization
        pass
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Transport-specific fields from data dictionary."""
        # TODO: Implement resource-specific field parsing
        pass
    
    def _validate_resource_specific(self) -> bool:
        """Perform Transport-specific validation."""
        # Transport requires status and intent
        return self.status is not None and self.intent is not None
