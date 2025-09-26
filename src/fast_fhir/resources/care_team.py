"""
FHIR R5 CareTeam Resource
The Care Team includes all the people and organizations who plan to participate in the coordination and delivery of care.
"""

from typing import List, Optional, Union, Dict, Any
from enum import Enum
from ..foundation import FHIRResource, FHIRElement
from ..datatypes import (
    FHIRIdentifier, FHIRReference, FHIRCodeableConcept, FHIRString, 
    FHIRPeriod, FHIRTiming, FHIRContactPoint, FHIRAnnotation
)


class CareTeamStatus(Enum):
    """CareTeam status enumeration"""
    PROPOSED = "proposed"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
    ENTERED_IN_ERROR = "entered-in-error"


class CareTeamParticipant(FHIRElement):
    """CareTeam participant information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role: List[FHIRCodeableConcept] = []
        self.member: Optional[FHIRReference] = None
        self.on_behalf_of: Optional[FHIRReference] = None
        self.coverage_period: Optional[FHIRPeriod] = None
        self.coverage_timing: Optional[FHIRTiming] = None


class CareTeam(FHIRResource):
    """
    FHIR R5 CareTeam resource
    
    The Care Team includes all the people and organizations who plan to participate
    in the coordination and delivery of care for a patient.
    """
    
    resource_type = "CareTeam"
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # CareTeam-specific fields
        self.identifier: List[FHIRIdentifier] = []
        self.status: CareTeamStatus = CareTeamStatus.PROPOSED
        self.category: List[FHIRCodeableConcept] = []
        self.name: Optional[FHIRString] = None
        self.subject: Optional[FHIRReference] = None
        self.period: Optional[FHIRPeriod] = None
        self.participant: List[CareTeamParticipant] = []
        self.reason_code: List[FHIRCodeableConcept] = []
        self.reason_reference: List[FHIRReference] = []
        self.managing_organization: List[FHIRReference] = []
        self.telecom: List[FHIRContactPoint] = []
        self.note: List[FHIRAnnotation] = []
    
    def is_active(self) -> bool:
        """Check if CareTeam is active"""
        return self.status == CareTeamStatus.ACTIVE
    
    def add_participant(self, participant: CareTeamParticipant) -> None:
        """Add participant to CareTeam"""
        self.participant.append(participant)
    
    def get_participants_by_role(self, role_code: str) -> List[CareTeamParticipant]:
        """Get participants by role code"""
        matching_participants = []
        for participant in self.participant:
            for role in participant.role:
                if role.has_coding_with_code(role_code):
                    matching_participants.append(participant)
                    break
        return matching_participants
    
    def get_display_name(self) -> str:
        """Get display name for CareTeam"""
        if self.name and self.name.value:
            return self.name.value
        return "CareTeam"
    
    def validate(self) -> bool:
        """Validate CareTeam resource"""
        if not super().validate():
            return False
        
        # CareTeam has no required fields beyond base resource
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CareTeam':
        """Create CareTeam from dictionary"""
        care_team = cls(id=data.get('id'))
        
        # Parse status
        if 'status' in data:
            care_team.status = CareTeamStatus(data['status'])
        
        # Parse other fields
        if 'name' in data:
            care_team.name = FHIRString(data['name'])
        if 'subject' in data:
            care_team.subject = FHIRReference.from_dict(data['subject'])
        if 'period' in data:
            care_team.period = FHIRPeriod.from_dict(data['period'])
        
        # Parse arrays
        if 'identifier' in data:
            care_team.identifier = [FHIRIdentifier.from_dict(item) for item in data['identifier']]
        if 'category' in data:
            care_team.category = [FHIRCodeableConcept.from_dict(item) for item in data['category']]
        if 'reasonCode' in data:
            care_team.reason_code = [FHIRCodeableConcept.from_dict(item) for item in data['reasonCode']]
        if 'reasonReference' in data:
            care_team.reason_reference = [FHIRReference.from_dict(item) for item in data['reasonReference']]
        if 'managingOrganization' in data:
            care_team.managing_organization = [FHIRReference.from_dict(item) for item in data['managingOrganization']]
        if 'telecom' in data:
            care_team.telecom = [FHIRContactPoint.from_dict(item) for item in data['telecom']]
        
        return care_team
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert CareTeam to dictionary"""
        result = super().to_dict()
        result.update({
            'resourceType': self.resource_type,
            'status': self.status.value
        })
        
        if self.name:
            result['name'] = self.name.value
        if self.subject:
            result['subject'] = self.subject.to_dict()
        if self.period:
            result['period'] = self.period.to_dict()
        
        if self.identifier:
            result['identifier'] = [item.to_dict() for item in self.identifier]
        if self.category:
            result['category'] = [item.to_dict() for item in self.category]
        if self.reason_code:
            result['reasonCode'] = [item.to_dict() for item in self.reason_code]
        if self.reason_reference:
            result['reasonReference'] = [item.to_dict() for item in self.reason_reference]
        if self.managing_organization:
            result['managingOrganization'] = [item.to_dict() for item in self.managing_organization]
        if self.telecom:
            result['telecom'] = [item.to_dict() for item in self.telecom]
        
        return result