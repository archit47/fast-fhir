"""FHIR R5 Medication Resource."""

from typing import Dict, Any, Optional
from ..foundation import FHIRResource


class Medication(FHIRResource):
    """FHIR R5 Medication resource."""
    
    def __init__(self, id: Optional[str] = None):
        """Initialize Medication resource."""
        super().__init__('Medication', id)
        self.identifier = []
        self.code = None
        self.status = None
        self.market_authorization_holder = None
        self.dose_form = None
        self.total_volume = None
        self.ingredient = []
        self.batch = None
        self.definition = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Medication':
        """Create Medication from dictionary data."""
        medication = cls(data.get('id'))
        medication._parse_meta(data)
        
        # Parse Medication-specific fields
        medication.identifier = data.get('identifier', [])
        medication.code = data.get('code')
        medication.status = data.get('status')
        medication.market_authorization_holder = data.get('marketAuthorizationHolder')
        medication.dose_form = data.get('doseForm')
        medication.total_volume = data.get('totalVolume')
        medication.ingredient = data.get('ingredient', [])
        medication.batch = data.get('batch')
        medication.definition = data.get('definition')
        
        return medication
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Medication to dictionary."""
        result = self._base_to_dict()
        
        if self.identifier:
            result['identifier'] = self.identifier
        if self.code:
            result['code'] = self.code
        if self.status:
            result['status'] = self.status
        if self.market_authorization_holder:
            result['marketAuthorizationHolder'] = self.market_authorization_holder
        if self.dose_form:
            result['doseForm'] = self.dose_form
        if self.total_volume:
            result['totalVolume'] = self.total_volume
        if self.ingredient:
            result['ingredient'] = self.ingredient
        if self.batch:
            result['batch'] = self.batch
        if self.definition:
            result['definition'] = self.definition
        
        return result