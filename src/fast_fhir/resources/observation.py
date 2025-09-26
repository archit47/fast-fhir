"""FHIR R5 Observation Resource."""

from typing import Dict, Any, Optional
from ..foundation import FHIRResource


class Observation(FHIRResource):
    """FHIR R5 Observation resource."""
    
    def __init__(self, id: Optional[str] = None):
        """Initialize Observation resource."""
        super().__init__('Observation', id)
        self.identifier = []
        self.instantiates_canonical = []
        self.instantiates_reference = []
        self.based_on = []
        self.triggered_by = []
        self.part_of = []
        self.status = None  # Required
        self.category = []
        self.code = None  # Required
        self.subject = None
        self.focus = []
        self.encounter = None
        self.effective = None
        self.issued = None
        self.performer = []
        self.value = None
        self.data_absent_reason = None
        self.interpretation = []
        self.note = []
        self.body_site = None
        self.body_structure = None
        self.method = None
        self.specimen = None
        self.device = None
        self.reference_range = []
        self.has_member = []
        self.derived_from = []
        self.component = []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Observation':
        """Create Observation from dictionary data."""
        observation = cls(data.get('id'))
        observation._parse_meta(data)
        
        # Parse Observation-specific fields
        observation.identifier = data.get('identifier', [])
        observation.instantiates_canonical = data.get('instantiatesCanonical', [])
        observation.instantiates_reference = data.get('instantiatesReference', [])
        observation.based_on = data.get('basedOn', [])
        observation.triggered_by = data.get('triggeredBy', [])
        observation.part_of = data.get('partOf', [])
        observation.status = data.get('status')
        observation.category = data.get('category', [])
        observation.code = data.get('code')
        observation.subject = data.get('subject')
        observation.focus = data.get('focus', [])
        observation.encounter = data.get('encounter')
        observation.effective = data.get('effective')
        observation.issued = data.get('issued')
        observation.performer = data.get('performer', [])
        observation.value = data.get('value')
        observation.data_absent_reason = data.get('dataAbsentReason')
        observation.interpretation = data.get('interpretation', [])
        observation.note = data.get('note', [])
        observation.body_site = data.get('bodySite')
        observation.body_structure = data.get('bodyStructure')
        observation.method = data.get('method')
        observation.specimen = data.get('specimen')
        observation.device = data.get('device')
        observation.reference_range = data.get('referenceRange', [])
        observation.has_member = data.get('hasMember', [])
        observation.derived_from = data.get('derivedFrom', [])
        observation.component = data.get('component', [])
        
        return observation
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Observation to dictionary."""
        result = self._base_to_dict()
        
        if self.identifier:
            result['identifier'] = self.identifier
        if self.instantiates_canonical:
            result['instantiatesCanonical'] = self.instantiates_canonical
        if self.instantiates_reference:
            result['instantiatesReference'] = self.instantiates_reference
        if self.based_on:
            result['basedOn'] = self.based_on
        if self.triggered_by:
            result['triggeredBy'] = self.triggered_by
        if self.part_of:
            result['partOf'] = self.part_of
        if self.status:
            result['status'] = self.status
        if self.category:
            result['category'] = self.category
        if self.code:
            result['code'] = self.code
        if self.subject:
            result['subject'] = self.subject
        if self.focus:
            result['focus'] = self.focus
        if self.encounter:
            result['encounter'] = self.encounter
        if self.effective:
            result['effective'] = self.effective
        if self.issued:
            result['issued'] = self.issued
        if self.performer:
            result['performer'] = self.performer
        if self.value:
            result['value'] = self.value
        if self.data_absent_reason:
            result['dataAbsentReason'] = self.data_absent_reason
        if self.interpretation:
            result['interpretation'] = self.interpretation
        if self.note:
            result['note'] = self.note
        if self.body_site:
            result['bodySite'] = self.body_site
        if self.body_structure:
            result['bodyStructure'] = self.body_structure
        if self.method:
            result['method'] = self.method
        if self.specimen:
            result['specimen'] = self.specimen
        if self.device:
            result['device'] = self.device
        if self.reference_range:
            result['referenceRange'] = self.reference_range
        if self.has_member:
            result['hasMember'] = self.has_member
        if self.derived_from:
            result['derivedFrom'] = self.derived_from
        if self.component:
            result['component'] = self.component
        
        return result