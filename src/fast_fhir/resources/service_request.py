"""
FHIR R5 ServiceRequest Resource
A record of a request for service such as diagnostic investigations, treatments, or operations to be performed.
"""

from typing import List, Optional, Union, Dict, Any
from enum import Enum
from ..foundation import FHIRResource, FHIRElement
from ..datatypes import (
    FHIRIdentifier, FHIRReference, FHIRCodeableConcept, FHIRString, 
    FHIRBoolean, FHIRQuantity, FHIRRange, FHIRRatio, FHIRPeriod,
    FHIRDateTime, FHIRTiming, FHIRAnnotation
)


class ServiceRequestStatus(Enum):
    """ServiceRequest status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    REVOKED = "revoked"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class ServiceRequestIntent(Enum):
    """ServiceRequest intent enumeration"""
    PROPOSAL = "proposal"
    PLAN = "plan"
    DIRECTIVE = "directive"
    ORDER = "order"
    ORIGINAL_ORDER = "original-order"
    REFLEX_ORDER = "reflex-order"
    FILLER_ORDER = "filler-order"
    INSTANCE_ORDER = "instance-order"
    OPTION = "option"


class ServiceRequestPriority(Enum):
    """ServiceRequest priority enumeration"""
    ROUTINE = "routine"
    URGENT = "urgent"
    ASAP = "asap"
    STAT = "stat"


class ServiceRequestOrderDetail(FHIRElement):
    """ServiceRequest order detail information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parameter_code: Optional[FHIRCodeableConcept] = None
        
        # Value (choice type)
        self.value_quantity: Optional[FHIRQuantity] = None
        self.value_ratio: Optional[FHIRRatio] = None
        self.value_range: Optional[FHIRRange] = None
        self.value_boolean: Optional[FHIRBoolean] = None
        self.value_codeable_concept: Optional[FHIRCodeableConcept] = None
        self.value_string: Optional[FHIRString] = None
        self.value_period: Optional[FHIRPeriod] = None


class ServiceRequest(FHIRResource):
    """
    FHIR R5 ServiceRequest resource
    
    A record of a request for service such as diagnostic investigations, treatments,
    or operations to be performed.
    """
    
    resource_type = "ServiceRequest"
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # ServiceRequest-specific fields
        self.identifier: List[FHIRIdentifier] = []
        self.instantiates_canonical: List[FHIRReference] = []
        self.instantiates_uri: List[FHIRReference] = []
        self.based_on: List[FHIRReference] = []
        self.replaces: List[FHIRReference] = []
        self.requisition: Optional[FHIRIdentifier] = None
        self.status: ServiceRequestStatus = ServiceRequestStatus.DRAFT
        self.intent: ServiceRequestIntent = ServiceRequestIntent.PROPOSAL
        self.category: List[FHIRCodeableConcept] = []
        self.priority: ServiceRequestPriority = ServiceRequestPriority.ROUTINE
        self.do_not_perform: Optional[FHIRBoolean] = None
        self.code: Optional[FHIRCodeableConcept] = None
        self.order_detail: List[ServiceRequestOrderDetail] = []
        
        # Quantity (choice type)
        self.quantity_quantity: Optional[FHIRQuantity] = None
        self.quantity_ratio: Optional[FHIRRatio] = None
        self.quantity_range: Optional[FHIRRange] = None
        
        self.subject: Optional[FHIRReference] = None
        self.focus: Optional[FHIRCodeableConcept] = None
        self.for_reference: Optional[FHIRReference] = None
        self.encounter: Optional[FHIRReference] = None
        
        # Occurrence (choice type)
        self.occurrence_date_time: Optional[FHIRDateTime] = None
        self.occurrence_period: Optional[FHIRPeriod] = None
        self.occurrence_timing: Optional[FHIRTiming] = None
        
        # As needed (choice type)
        self.as_needed_boolean: Optional[FHIRBoolean] = None
        self.as_needed_codeable_concept: Optional[FHIRCodeableConcept] = None
        
        self.authored_on: Optional[FHIRDateTime] = None
        self.requester: Optional[FHIRReference] = None
        self.performer_type: Optional[FHIRCodeableConcept] = None
        self.performer: List[FHIRReference] = []
        self.location_code: List[FHIRReference] = []
        self.location_reference: List[FHIRReference] = []
        self.reason_code: List[FHIRCodeableConcept] = []
        self.reason_reference: List[FHIRReference] = []
        self.insurance: List[FHIRReference] = []
        self.supporting_info: List[FHIRReference] = []
        self.specimen: List[FHIRReference] = []
        self.body_site: List[FHIRCodeableConcept] = []
        self.body_structure: Optional[FHIRCodeableConcept] = None
        self.note: List[FHIRAnnotation] = []
        self.patient_instruction: Optional[FHIRString] = None
        self.relevant_history: List[FHIRReference] = []
    
    def is_active(self) -> bool:
        """Check if ServiceRequest is active"""
        return self.status == ServiceRequestStatus.ACTIVE
    
    def is_urgent(self) -> bool:
        """Check if ServiceRequest is urgent"""
        return self.priority in [ServiceRequestPriority.URGENT, ServiceRequestPriority.ASAP, ServiceRequestPriority.STAT]
    
    def get_display_name(self) -> str:
        """Get display name for ServiceRequest"""
        if self.code and self.code.text:
            return self.code.text.value
        return "ServiceRequest"
    
    def validate(self) -> bool:
        """Validate ServiceRequest resource"""
        if not super().validate():
            return False
        
        # Subject is required
        if not self.subject:
            return False
        
        # Code is required
        if not self.code:
            return False
        
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServiceRequest':
        """Create ServiceRequest from dictionary"""
        service_request = cls(id=data.get('id'))
        
        # Parse status, intent, and priority
        if 'status' in data:
            service_request.status = ServiceRequestStatus(data['status'])
        if 'intent' in data:
            service_request.intent = ServiceRequestIntent(data['intent'])
        if 'priority' in data:
            service_request.priority = ServiceRequestPriority(data['priority'])
        
        # Parse other fields
        if 'requisition' in data:
            service_request.requisition = FHIRIdentifier.from_dict(data['requisition'])
        if 'doNotPerform' in data:
            service_request.do_not_perform = FHIRBoolean(data['doNotPerform'])
        if 'code' in data:
            service_request.code = FHIRCodeableConcept.from_dict(data['code'])
        if 'subject' in data:
            service_request.subject = FHIRReference.from_dict(data['subject'])
        if 'encounter' in data:
            service_request.encounter = FHIRReference.from_dict(data['encounter'])
        if 'authoredOn' in data:
            service_request.authored_on = FHIRDateTime(data['authoredOn'])
        if 'requester' in data:
            service_request.requester = FHIRReference.from_dict(data['requester'])
        if 'performerType' in data:
            service_request.performer_type = FHIRCodeableConcept.from_dict(data['performerType'])
        if 'patientInstruction' in data:
            service_request.patient_instruction = FHIRString(data['patientInstruction'])
        
        # Parse choice types
        if 'occurrenceDateTime' in data:
            service_request.occurrence_date_time = FHIRDateTime(data['occurrenceDateTime'])
        elif 'occurrencePeriod' in data:
            service_request.occurrence_period = FHIRPeriod.from_dict(data['occurrencePeriod'])
        elif 'occurrenceTiming' in data:
            service_request.occurrence_timing = FHIRTiming.from_dict(data['occurrenceTiming'])
        
        if 'asNeededBoolean' in data:
            service_request.as_needed_boolean = FHIRBoolean(data['asNeededBoolean'])
        elif 'asNeededCodeableConcept' in data:
            service_request.as_needed_codeable_concept = FHIRCodeableConcept.from_dict(data['asNeededCodeableConcept'])
        
        # Parse arrays
        if 'identifier' in data:
            service_request.identifier = [FHIRIdentifier.from_dict(item) for item in data['identifier']]
        if 'category' in data:
            service_request.category = [FHIRCodeableConcept.from_dict(item) for item in data['category']]
        if 'performer' in data:
            service_request.performer = [FHIRReference.from_dict(item) for item in data['performer']]
        if 'reasonCode' in data:
            service_request.reason_code = [FHIRCodeableConcept.from_dict(item) for item in data['reasonCode']]
        if 'reasonReference' in data:
            service_request.reason_reference = [FHIRReference.from_dict(item) for item in data['reasonReference']]
        
        return service_request
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ServiceRequest to dictionary"""
        result = super().to_dict()
        result.update({
            'resourceType': self.resource_type,
            'status': self.status.value,
            'intent': self.intent.value,
            'priority': self.priority.value
        })
        
        if self.requisition:
            result['requisition'] = self.requisition.to_dict()
        if self.do_not_perform:
            result['doNotPerform'] = self.do_not_perform.value
        if self.code:
            result['code'] = self.code.to_dict()
        if self.subject:
            result['subject'] = self.subject.to_dict()
        if self.encounter:
            result['encounter'] = self.encounter.to_dict()
        if self.authored_on:
            result['authoredOn'] = self.authored_on.value
        if self.requester:
            result['requester'] = self.requester.to_dict()
        if self.performer_type:
            result['performerType'] = self.performer_type.to_dict()
        if self.patient_instruction:
            result['patientInstruction'] = self.patient_instruction.value
        
        # Choice types
        if self.occurrence_date_time:
            result['occurrenceDateTime'] = self.occurrence_date_time.value
        elif self.occurrence_period:
            result['occurrencePeriod'] = self.occurrence_period.to_dict()
        elif self.occurrence_timing:
            result['occurrenceTiming'] = self.occurrence_timing.to_dict()
        
        if self.as_needed_boolean:
            result['asNeededBoolean'] = self.as_needed_boolean.value
        elif self.as_needed_codeable_concept:
            result['asNeededCodeableConcept'] = self.as_needed_codeable_concept.to_dict()
        
        if self.identifier:
            result['identifier'] = [item.to_dict() for item in self.identifier]
        if self.category:
            result['category'] = [item.to_dict() for item in self.category]
        if self.performer:
            result['performer'] = [item.to_dict() for item in self.performer]
        if self.reason_code:
            result['reasonCode'] = [item.to_dict() for item in self.reason_code]
        if self.reason_reference:
            result['reasonReference'] = [item.to_dict() for item in self.reason_reference]
        
        return result