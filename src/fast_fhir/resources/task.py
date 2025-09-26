"""FHIR R5 Task Resource."""

from typing import Dict, Any, Optional
from .base import FHIRResourceBase, validate_fhir_code


class Task(FHIRResourceBase):
    """FHIR R5 Task resource following DRY principles."""
    
    def _init_resource_fields(self) -> None:
        """Initialize Task-specific fields."""
        self.identifier = []
        self.instantiates_canonical = None
        self.instantiates_uri = None
        self.based_on = []
        self.group_identifier = None
        self.part_of = []
        self.status = None  # Required: draft | requested | received | accepted | rejected | ready | cancelled | in-progress | on-hold | failed | completed | entered-in-error
        self.status_reason = None
        self.business_status = None
        self.intent = None  # Required: unknown | proposal | plan | order | original-order | reflex-order | filler-order | instance-order | option
        self.priority = None  # routine | urgent | asap | stat
        self.do_not_perform = None
        self.code = None
        self.description = None
        self.focus = None
        self.for_reference = None
        self.encounter = None
        self.requested_performer = []
        self.performer_type = []
        self.owner = None
        self.requestor = None
        self.reason_code = []
        self.reason_reference = []
        self.insurance = []
        self.note = []
        self.relevant_history = []
        self.restriction = None
        self.input = []
        self.output = []
        self.execution_period = None
        self.authored_on = None
        self.last_modified = None
        self.location = None
    
    def _get_c_extension_create_function(self) -> Optional[str]:
        """Get C extension create function name."""
        return "create_task"
    
    def _get_c_extension_parse_function(self) -> Optional[str]:
        """Get C extension parse function name."""
        return "parse_task"
    
    @classmethod
    def _get_c_extension_parse_function_static(cls) -> Optional[str]:
        """Static version of parse function name."""
        return "parse_task"
    
    def _add_resource_specific_fields(self, result: Dict[str, Any]) -> None:
        """Add Task-specific fields to dictionary."""
        if self.identifier:
            result["identifier"] = self.identifier
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
        if self.business_status:
            result["businessStatus"] = self.business_status
        if self.intent:
            result["intent"] = self.intent
        if self.priority:
            result["priority"] = self.priority
        if self.do_not_perform is not None:
            result["doNotPerform"] = self.do_not_perform
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
        if self.requested_performer:
            result["requestedPerformer"] = self.requested_performer
        if self.performer_type:
            result["performerType"] = self.performer_type
        if self.owner:
            result["owner"] = self.owner
        if self.requestor:
            result["requestor"] = self.requestor
        if self.reason_code:
            result["reasonCode"] = self.reason_code
        if self.reason_reference:
            result["reasonReference"] = self.reason_reference
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
        if self.execution_period:
            result["executionPeriod"] = self.execution_period
        if self.authored_on:
            result["authoredOn"] = self.authored_on
        if self.last_modified:
            result["lastModified"] = self.last_modified
        if self.location:
            result["location"] = self.location
    
    def _parse_resource_specific_fields(self, data: Dict[str, Any]) -> None:
        """Parse Task-specific fields from dictionary."""
        self.identifier = data.get("identifier", [])
        self.instantiates_canonical = data.get("instantiatesCanonical")
        self.instantiates_uri = data.get("instantiatesUri")
        self.based_on = data.get("basedOn", [])
        self.group_identifier = data.get("groupIdentifier")
        self.part_of = data.get("partOf", [])
        self.status = data.get("status")
        self.status_reason = data.get("statusReason")
        self.business_status = data.get("businessStatus")
        self.intent = data.get("intent")
        self.priority = data.get("priority")
        self.do_not_perform = data.get("doNotPerform")
        self.code = data.get("code")
        self.description = data.get("description")
        self.focus = data.get("focus")
        self.for_reference = data.get("for")
        self.encounter = data.get("encounter")
        self.requested_performer = data.get("requestedPerformer", [])
        self.performer_type = data.get("performerType", [])
        self.owner = data.get("owner")
        self.requestor = data.get("requestor")
        self.reason_code = data.get("reasonCode", [])
        self.reason_reference = data.get("reasonReference", [])
        self.insurance = data.get("insurance", [])
        self.note = data.get("note", [])
        self.relevant_history = data.get("relevantHistory", [])
        self.restriction = data.get("restriction")
        self.input = data.get("input", [])
        self.output = data.get("output", [])
        self.execution_period = data.get("executionPeriod")
        self.authored_on = data.get("authoredOn")
        self.last_modified = data.get("lastModified")
        self.location = data.get("location")
    
    def _validate_resource_specific(self) -> bool:
        """Validate Task-specific fields."""
        # Status is required
        if not self.status:
            return False
        
        # Validate status code
        valid_statuses = [
            "draft", "requested", "received", "accepted", "rejected", "ready",
            "cancelled", "in-progress", "on-hold", "failed", "completed", "entered-in-error"
        ]
        if not validate_fhir_code(self.status, valid_statuses):
            return False
        
        # Intent is required
        if not self.intent:
            return False
        
        # Validate intent code
        valid_intents = [
            "unknown", "proposal", "plan", "order", "original-order",
            "reflex-order", "filler-order", "instance-order", "option"
        ]
        if not validate_fhir_code(self.intent, valid_intents):
            return False
        
        return True
    
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == "completed"
    
    def is_in_progress(self) -> bool:
        """Check if task is in progress."""
        return self.status == "in-progress"
    
    def is_ready(self) -> bool:
        """Check if task is ready."""
        return self.status == "ready"
    
    def add_input(self, type_code: str, value: Any) -> None:
        """Add input parameter to task."""
        input_param = {
            "type": {"coding": [{"code": type_code}]},
            "value": value
        }
        self.input.append(input_param)
    
    def add_output(self, type_code: str, value: Any) -> None:
        """Add output parameter to task."""
        output_param = {
            "type": {"coding": [{"code": type_code}]},
            "value": value
        }
        self.output.append(output_param)