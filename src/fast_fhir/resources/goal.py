"""
FHIR R5 Goal Resource
Describes the intended objective(s) for a patient, group or organization care.
"""

from typing import List, Optional, Union, Dict, Any
from enum import Enum
from ..foundation import FHIRResource, FHIRElement
from ..datatypes import (
    FHIRIdentifier, FHIRReference, FHIRCodeableConcept, FHIRString, 
    FHIRDate, FHIRBoolean, FHIRQuantity, FHIRRange, FHIRRatio,
    FHIRInteger, FHIRDuration, FHIRAnnotation
)


class GoalLifecycleStatus(Enum):
    """Goal lifecycle status enumeration"""
    PROPOSED = "proposed"
    PLANNED = "planned"
    ACCEPTED = "accepted"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    REJECTED = "rejected"


class GoalAchievementStatus(Enum):
    """Goal achievement status enumeration"""
    IN_PROGRESS = "in-progress"
    IMPROVING = "improving"
    WORSENING = "worsening"
    NO_CHANGE = "no-change"
    ACHIEVED = "achieved"
    SUSTAINING = "sustaining"
    NOT_ACHIEVED = "not-achieved"
    NO_PROGRESS = "no-progress"
    NOT_ATTAINABLE = "not-attainable"


class GoalTarget(FHIRElement):
    """Goal target information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.measure: Optional[FHIRCodeableConcept] = None
        
        # Detail (choice type)
        self.detail_quantity: Optional[FHIRQuantity] = None
        self.detail_range: Optional[FHIRRange] = None
        self.detail_codeable_concept: Optional[FHIRCodeableConcept] = None
        self.detail_string: Optional[FHIRString] = None
        self.detail_boolean: Optional[FHIRBoolean] = None
        self.detail_integer: Optional[FHIRInteger] = None
        self.detail_ratio: Optional[FHIRRatio] = None
        
        # Due (choice type)
        self.due_date: Optional[FHIRDate] = None
        self.due_duration: Optional[FHIRDuration] = None


class Goal(FHIRResource):
    """
    FHIR R5 Goal resource
    
    Describes the intended objective(s) for a patient, group or organization care,
    for example, weight loss, restoring an activity of daily living, obtaining herd immunity via immunization, meeting a process improvement objective, etc.
    """
    
    resource_type = "Goal"
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # Goal-specific fields
        self.identifier: List[FHIRIdentifier] = []
        self.lifecycle_status: GoalLifecycleStatus = GoalLifecycleStatus.PROPOSED
        self.achievement_status: Optional[FHIRCodeableConcept] = None
        self.category: List[FHIRCodeableConcept] = []
        self.continuous: Optional[FHIRBoolean] = None
        self.priority: Optional[FHIRCodeableConcept] = None
        self.description: Optional[FHIRCodeableConcept] = None
        self.subject: Optional[FHIRReference] = None
        
        # Start (choice type)
        self.start_date: Optional[FHIRDate] = None
        self.start_codeable_concept: Optional[FHIRCodeableConcept] = None
        
        self.target: List[GoalTarget] = []
        self.status_date: Optional[FHIRDate] = None
        self.status_reason: Optional[FHIRString] = None
        self.source: Optional[FHIRReference] = None
        self.addresses: List[FHIRReference] = []
        self.note: List[FHIRAnnotation] = []
        self.outcome_code: List[FHIRCodeableConcept] = []
        self.outcome_reference: List[FHIRReference] = []
    
    def is_active(self) -> bool:
        """Check if Goal is active"""
        return self.lifecycle_status == GoalLifecycleStatus.ACTIVE
    
    def is_achieved(self) -> bool:
        """Check if Goal is achieved"""
        if self.achievement_status:
            # Check if achievement status indicates achievement
            if self.achievement_status.text:
                achievement_text = self.achievement_status.text.value
                return "achieved" in achievement_text.lower() or "sustaining" in achievement_text.lower()
        return self.lifecycle_status == GoalLifecycleStatus.COMPLETED
    
    def add_target(self, target: GoalTarget) -> None:
        """Add target to Goal"""
        self.target.append(target)
    
    def get_display_name(self) -> str:
        """Get display name for Goal"""
        if self.description and self.description.text:
            return self.description.text.value
        return "Goal"
    
    def validate(self) -> bool:
        """Validate Goal resource"""
        if not super().validate():
            return False
        
        # Subject is required
        if not self.subject:
            return False
        
        # Description is required
        if not self.description:
            return False
        
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Goal':
        """Create Goal from dictionary"""
        goal = cls(id=data.get('id'))
        
        # Parse lifecycle status
        if 'lifecycleStatus' in data:
            goal.lifecycle_status = GoalLifecycleStatus(data['lifecycleStatus'])
        
        # Parse other fields
        if 'achievementStatus' in data:
            goal.achievement_status = FHIRCodeableConcept.from_dict(data['achievementStatus'])
        if 'continuous' in data:
            goal.continuous = FHIRBoolean(data['continuous'])
        if 'priority' in data:
            goal.priority = FHIRCodeableConcept.from_dict(data['priority'])
        if 'description' in data:
            goal.description = FHIRCodeableConcept.from_dict(data['description'])
        if 'subject' in data:
            goal.subject = FHIRReference.from_dict(data['subject'])
        if 'statusDate' in data:
            goal.status_date = FHIRDate(data['statusDate'])
        if 'statusReason' in data:
            goal.status_reason = FHIRString(data['statusReason'])
        if 'source' in data:
            goal.source = FHIRReference.from_dict(data['source'])
        
        # Parse start (choice type)
        if 'startDate' in data:
            goal.start_date = FHIRDate(data['startDate'])
        elif 'startCodeableConcept' in data:
            goal.start_codeable_concept = FHIRCodeableConcept.from_dict(data['startCodeableConcept'])
        
        # Parse arrays
        if 'identifier' in data:
            goal.identifier = [FHIRIdentifier.from_dict(item) for item in data['identifier']]
        if 'category' in data:
            goal.category = [FHIRCodeableConcept.from_dict(item) for item in data['category']]
        if 'addresses' in data:
            goal.addresses = [FHIRReference.from_dict(item) for item in data['addresses']]
        if 'outcomeCode' in data:
            goal.outcome_code = [FHIRCodeableConcept.from_dict(item) for item in data['outcomeCode']]
        if 'outcomeReference' in data:
            goal.outcome_reference = [FHIRReference.from_dict(item) for item in data['outcomeReference']]
        
        return goal
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Goal to dictionary"""
        result = super().to_dict()
        result.update({
            'resourceType': self.resource_type,
            'lifecycleStatus': self.lifecycle_status.value
        })
        
        if self.achievement_status:
            result['achievementStatus'] = self.achievement_status.to_dict()
        if self.continuous:
            result['continuous'] = self.continuous.value
        if self.priority:
            result['priority'] = self.priority.to_dict()
        if self.description:
            result['description'] = self.description.to_dict()
        if self.subject:
            result['subject'] = self.subject.to_dict()
        if self.status_date:
            result['statusDate'] = self.status_date.value
        if self.status_reason:
            result['statusReason'] = self.status_reason.value
        if self.source:
            result['source'] = self.source.to_dict()
        
        # Start (choice type)
        if self.start_date:
            result['startDate'] = self.start_date.value
        elif self.start_codeable_concept:
            result['startCodeableConcept'] = self.start_codeable_concept.to_dict()
        
        if self.identifier:
            result['identifier'] = [item.to_dict() for item in self.identifier]
        if self.category:
            result['category'] = [item.to_dict() for item in self.category]
        if self.addresses:
            result['addresses'] = [item.to_dict() for item in self.addresses]
        if self.outcome_code:
            result['outcomeCode'] = [item.to_dict() for item in self.outcome_code]
        if self.outcome_reference:
            result['outcomeReference'] = [item.to_dict() for item in self.outcome_reference]
        
        return result