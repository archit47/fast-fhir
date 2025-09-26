"""
FHIR R5 CarePlan Resource
Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community.
"""

from typing import List, Optional, Union, Dict, Any
from enum import Enum
from ..foundation import FHIRResource, FHIRElement
from ..datatypes import (
    FHIRIdentifier, FHIRReference, FHIRCodeableConcept, FHIRString, 
    FHIRPeriod, FHIRDateTime, FHIRAnnotation, FHIRQuantity, FHIRTiming,
    FHIRBoolean, FHIRDuration
)


class CarePlanStatus(Enum):
    """CarePlan status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    REVOKED = "revoked"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class CarePlanIntent(Enum):
    """CarePlan intent enumeration"""
    PROPOSAL = "proposal"
    PLAN = "plan"
    ORDER = "order"
    OPTION = "option"
    DIRECTIVE = "directive"


class CarePlanActivityStatus(Enum):
    """CarePlan activity status enumeration"""
    NOT_STARTED = "not-started"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in-progress"
    ON_HOLD = "on-hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    STOPPED = "stopped"
    UNKNOWN = "unknown"
    ENTERED_IN_ERROR = "entered-in-error"


class CarePlanActivityDetail(FHIRElement):
    """CarePlan activity detail information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kind: Optional[FHIRCodeableConcept] = None
        self.instantiates_canonical: List[FHIRReference] = []
        self.instantiates_uri: List[FHIRReference] = []
        self.code: Optional[FHIRCodeableConcept] = None
        self.reason_code: List[FHIRCodeableConcept] = []
        self.reason_reference: List[FHIRReference] = []
        self.goal: List[FHIRReference] = []
        self.status: Optional[CarePlanActivityStatus] = None
        self.status_reason: Optional[FHIRCodeableConcept] = None
        self.do_not_perform: Optional[FHIRBoolean] = None
        self.scheduled_timing: Optional[FHIRTiming] = None
        self.scheduled_period: Optional[FHIRPeriod] = None
        self.scheduled_string: Optional[FHIRString] = None
        self.location: Optional[FHIRReference] = None
        self.reported_boolean: List[FHIRCodeableConcept] = []
        self.reported_reference: Optional[FHIRReference] = None
        self.performer: List[FHIRReference] = []
        self.product_codeable_concept: Optional[FHIRCodeableConcept] = None
        self.product_reference: Optional[FHIRReference] = None
        self.daily_amount: Optional[FHIRQuantity] = None
        self.quantity: Optional[FHIRQuantity] = None
        self.description: Optional[FHIRString] = None


class CarePlanActivity(FHIRElement):
    """CarePlan activity information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outcome_codeable_concept: List[FHIRCodeableConcept] = []
        self.outcome_reference: List[FHIRReference] = []
        self.progress: List[FHIRAnnotation] = []
        self.reference: Optional[FHIRReference] = None
        self.detail: Optional[CarePlanActivityDetail] = None


class CarePlan(FHIRResource):
    """
    FHIR R5 CarePlan resource
    
    Describes the intention of how one or more practitioners intend to deliver care
    for a particular patient, group or community for some or all of their problems.
    """
    
    resource_type = "CarePlan"
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # CarePlan-specific fields
        self.identifier: List[FHIRIdentifier] = []
        self.instantiates_canonical: List[FHIRReference] = []
        self.instantiates_uri: List[FHIRReference] = []
        self.based_on: List[FHIRReference] = []
        self.replaces: List[FHIRReference] = []
        self.part_of: List[FHIRReference] = []
        self.status: CarePlanStatus = CarePlanStatus.DRAFT
        self.intent: CarePlanIntent = CarePlanIntent.PLAN
        self.category: List[FHIRCodeableConcept] = []
        self.title: Optional[FHIRString] = None
        self.description: Optional[FHIRString] = None
        self.subject: Optional[FHIRReference] = None
        self.encounter: Optional[FHIRReference] = None
        self.period: Optional[FHIRPeriod] = None
        self.created: Optional[FHIRDateTime] = None
        self.custodian: List[FHIRReference] = []
        self.contributor: List[FHIRReference] = []
        self.care_team: List[FHIRReference] = []
        self.addresses: List[FHIRReference] = []
        self.supporting_info: List[FHIRReference] = []
        self.goal: List[FHIRReference] = []
        self.activity: List[CarePlanActivity] = []
        self.note: List[FHIRAnnotation] = []
    
    def is_active(self) -> bool:
        """Check if CarePlan is active"""
        return self.status == CarePlanStatus.ACTIVE
    
    def add_activity(self, activity: CarePlanActivity) -> None:
        """Add activity to CarePlan"""
        self.activity.append(activity)
    
    def get_display_name(self) -> str:
        """Get display name for CarePlan"""
        if self.title and self.title.value:
            return self.title.value
        return "CarePlan"
    
    def validate(self) -> bool:
        """Validate CarePlan resource"""
        if not super().validate():
            return False
        
        # Subject is required
        if not self.subject:
            return False
        
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CarePlan':
        """Create CarePlan from dictionary"""
        care_plan = cls(id=data.get('id'))
        
        # Parse status and intent
        if 'status' in data:
            care_plan.status = CarePlanStatus(data['status'])
        if 'intent' in data:
            care_plan.intent = CarePlanIntent(data['intent'])
        
        # Parse other fields
        if 'title' in data:
            care_plan.title = FHIRString(data['title'])
        if 'description' in data:
            care_plan.description = FHIRString(data['description'])
        if 'subject' in data:
            care_plan.subject = FHIRReference.from_dict(data['subject'])
        if 'encounter' in data:
            care_plan.encounter = FHIRReference.from_dict(data['encounter'])
        if 'period' in data:
            care_plan.period = FHIRPeriod.from_dict(data['period'])
        if 'created' in data:
            care_plan.created = FHIRDateTime(data['created'])
        
        # Parse arrays
        if 'identifier' in data:
            care_plan.identifier = [FHIRIdentifier.from_dict(item) for item in data['identifier']]
        if 'category' in data:
            care_plan.category = [FHIRCodeableConcept.from_dict(item) for item in data['category']]
        if 'goal' in data:
            care_plan.goal = [FHIRReference.from_dict(item) for item in data['goal']]
        if 'careTeam' in data:
            care_plan.care_team = [FHIRReference.from_dict(item) for item in data['careTeam']]
        
        return care_plan
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert CarePlan to dictionary"""
        result = super().to_dict()
        result.update({
            'resourceType': self.resource_type,
            'status': self.status.value,
            'intent': self.intent.value
        })
        
        if self.title:
            result['title'] = self.title.value
        if self.description:
            result['description'] = self.description.value
        if self.subject:
            result['subject'] = self.subject.to_dict()
        if self.encounter:
            result['encounter'] = self.encounter.to_dict()
        if self.period:
            result['period'] = self.period.to_dict()
        if self.created:
            result['created'] = self.created.value
        
        if self.identifier:
            result['identifier'] = [item.to_dict() for item in self.identifier]
        if self.category:
            result['category'] = [item.to_dict() for item in self.category]
        if self.goal:
            result['goal'] = [item.to_dict() for item in self.goal]
        if self.care_team:
            result['careTeam'] = [item.to_dict() for item in self.care_team]
        
        return result