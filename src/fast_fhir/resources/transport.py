"""FHIR R5 Transport resource implementation following DRY principles."""

from typing import Optional, List, Dict, Any
from .base import FHIRResourceBase


class Transport(FHIRResourceBase):
    """FHIR R5 Transport resource following DRY principles."""
    
    def __init__(self, id: Optional[str] = None, use_c_extensions: bool = True):
        """Initialize Transport resource."""
        super().__init__("Transport", id, use_c_extensions)
        
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
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transport':
        """Create Transport from dictionary representation."""
        instance = cls(data.get("id"))
        instance._populate_from_dict(data)
        
        # Set Transport-specific fields
        instance.instantiates_canonical = data.get("instantiatesCanonical")
        instance.instantiates_uri = data.get("instantiatesUri")
        instance.based_on = data.get("basedOn", [])
        instance.group_identifier = data.get("groupIdentifier")
        instance.part_of = data.get("partOf", [])
        instance.status = data.get("status")
        instance.status_reason = data.get("statusReason")
        instance.intent = data.get("intent")
        instance.priority = data.get("priority")
        instance.code = data.get("code")
        instance.description = data.get("description")
        instance.focus = data.get("focus")
        instance.for_reference = data.get("for")
        instance.encounter = data.get("encounter")
        instance.completion_time = data.get("completionTime")
        instance.authored_on = data.get("authoredOn")
        instance.last_modified = data.get("lastModified")
        instance.requester = data.get("requester")
        instance.performer_type = data.get("performerType")
        instance.owner = data.get("owner")
        instance.location = data.get("location")
        instance.insurance = data.get("insurance", [])
        instance.note = data.get("note", [])
        instance.relevant_history = data.get("relevantHistory", [])
        instance.restriction = data.get("restriction")
        instance.input = data.get("input", [])
        instance.output = data.get("output", [])
        instance.requested_location = data.get("requestedLocation")
        instance.current_location = data.get("currentLocation")
        instance.reason_code = data.get("reasonCode")
        instance.reason_reference = data.get("reasonReference")
        instance.history = data.get("history")
        
        return instance
    
    def validate(self) -> List[str]:
        """Validate Transport resource."""
        errors = super().validate()
        
        # Transport-specific validation
        if not self.status:
            errors.append("Transport.status is required")
        
        if not self.intent:
            errors.append("Transport.intent is required")
        
        # Validate status values
        valid_statuses = ["draft", "requested", "received", "accepted", "rejected", 
                         "in-progress", "completed", "cancelled", "entered-in-error"]
        if self.status and self.status not in valid_statuses:
            errors.append(f"Transport.status must be one of: {', '.join(valid_statuses)}")
        
        # Validate intent values
        valid_intents = ["unknown", "proposal", "plan", "order", "original-order", 
                        "reflex-order", "filler-order", "instance-order", "option"]
        if self.intent and self.intent not in valid_intents:
            errors.append(f"Transport.intent must be one of: {', '.join(valid_intents)}")
        
        # Validate priority values
        valid_priorities = ["routine", "urgent", "asap", "stat"]
        if self.priority and self.priority not in valid_priorities:
            errors.append(f"Transport.priority must be one of: {', '.join(valid_priorities)}")
        
        return errors
    
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