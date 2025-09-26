"""
FHIR R5 VisionPrescription Resource
An authorization for the provision of glasses and/or contact lenses to a patient.
"""

from typing import List, Optional, Union, Dict, Any
from enum import Enum
from ..foundation import FHIRResource, FHIRElement
from ..datatypes import (
    FHIRIdentifier, FHIRReference, FHIRCodeableConcept, FHIRString, 
    FHIRDateTime, FHIRDecimal, FHIRInteger, FHIRQuantity, FHIRAnnotation
)


class VisionPrescriptionStatus(Enum):
    """VisionPrescription status enumeration"""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    DRAFT = "draft"
    ENTERED_IN_ERROR = "entered-in-error"


class VisionEye(Enum):
    """Vision eye enumeration"""
    RIGHT = "right"
    LEFT = "left"


class VisionBase(Enum):
    """Vision base enumeration"""
    UP = "up"
    DOWN = "down"
    IN = "in"
    OUT = "out"


class VisionPrescriptionPrism(FHIRElement):
    """VisionPrescription prism information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.amount: Optional[FHIRDecimal] = None
        self.base: Optional[VisionBase] = None


class VisionPrescriptionLensSpecification(FHIRElement):
    """VisionPrescription lens specification information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product: Optional[FHIRCodeableConcept] = None
        self.eye: Optional[VisionEye] = None
        self.sphere: Optional[FHIRDecimal] = None
        self.cylinder: Optional[FHIRDecimal] = None
        self.axis: Optional[FHIRInteger] = None
        self.prism: List[VisionPrescriptionPrism] = []
        self.add: Optional[FHIRDecimal] = None
        self.power: Optional[FHIRDecimal] = None
        self.back_curve: Optional[FHIRDecimal] = None
        self.diameter: Optional[FHIRDecimal] = None
        self.duration: Optional[FHIRQuantity] = None
        self.color: Optional[FHIRString] = None
        self.brand: Optional[FHIRString] = None
        self.note: List[FHIRAnnotation] = []
    
    def is_for_glasses(self) -> bool:
        """Check if lens specification is for glasses"""
        if self.product:
            # Check product coding for glasses indication
            # This would need proper coding system checks in a real implementation
            return True  # Simplified for example
        return False
    
    def is_for_contacts(self) -> bool:
        """Check if lens specification is for contact lenses"""
        if self.product:
            # Check product coding for contact lens indication
            # This would need proper coding system checks in a real implementation
            return False  # Simplified for example
        return False


class VisionPrescription(FHIRResource):
    """
    FHIR R5 VisionPrescription resource
    
    An authorization for the provision of glasses and/or contact lenses to a patient.
    """
    
    resource_type = "VisionPrescription"
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # VisionPrescription-specific fields
        self.identifier: List[FHIRIdentifier] = []
        self.status: VisionPrescriptionStatus = VisionPrescriptionStatus.DRAFT
        self.created: Optional[FHIRDateTime] = None
        self.patient: Optional[FHIRReference] = None
        self.encounter: Optional[FHIRReference] = None
        self.date_written: Optional[FHIRDateTime] = None
        self.prescriber: Optional[FHIRReference] = None
        self.lens_specification: List[VisionPrescriptionLensSpecification] = []
    
    def is_active(self) -> bool:
        """Check if VisionPrescription is active"""
        return self.status == VisionPrescriptionStatus.ACTIVE
    
    def add_lens_specification(self, lens_spec: VisionPrescriptionLensSpecification) -> None:
        """Add lens specification to VisionPrescription"""
        self.lens_specification.append(lens_spec)
    
    def get_lens_for_eye(self, eye: VisionEye) -> Optional[VisionPrescriptionLensSpecification]:
        """Get lens specification for specific eye"""
        for lens_spec in self.lens_specification:
            if lens_spec.eye == eye:
                return lens_spec
        return None
    
    def is_for_glasses(self) -> bool:
        """Check if prescription is for glasses"""
        return any(lens.is_for_glasses() for lens in self.lens_specification)
    
    def is_for_contacts(self) -> bool:
        """Check if prescription is for contact lenses"""
        return any(lens.is_for_contacts() for lens in self.lens_specification)
    
    def get_display_name(self) -> str:
        """Get display name for VisionPrescription"""
        if self.is_for_glasses():
            return "Vision Prescription (Glasses)"
        elif self.is_for_contacts():
            return "Vision Prescription (Contacts)"
        return "VisionPrescription"
    
    def validate(self) -> bool:
        """Validate VisionPrescription resource"""
        if not super().validate():
            return False
        
        # Patient is required
        if not self.patient:
            return False
        
        # Prescriber is required
        if not self.prescriber:
            return False
        
        # At least one lens specification is required
        if not self.lens_specification:
            return False
        
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VisionPrescription':
        """Create VisionPrescription from dictionary"""
        vision_prescription = cls(id=data.get('id'))
        
        # Parse status
        if 'status' in data:
            vision_prescription.status = VisionPrescriptionStatus(data['status'])
        
        # Parse other fields
        if 'created' in data:
            vision_prescription.created = FHIRDateTime(data['created'])
        if 'patient' in data:
            vision_prescription.patient = FHIRReference.from_dict(data['patient'])
        if 'encounter' in data:
            vision_prescription.encounter = FHIRReference.from_dict(data['encounter'])
        if 'dateWritten' in data:
            vision_prescription.date_written = FHIRDateTime(data['dateWritten'])
        if 'prescriber' in data:
            vision_prescription.prescriber = FHIRReference.from_dict(data['prescriber'])
        
        # Parse arrays
        if 'identifier' in data:
            vision_prescription.identifier = [FHIRIdentifier.from_dict(item) for item in data['identifier']]
        
        # Parse lens specifications
        if 'lensSpecification' in data:
            for lens_data in data['lensSpecification']:
                lens_spec = VisionPrescriptionLensSpecification()
                if 'product' in lens_data:
                    lens_spec.product = FHIRCodeableConcept.from_dict(lens_data['product'])
                if 'eye' in lens_data:
                    lens_spec.eye = VisionEye(lens_data['eye'])
                if 'sphere' in lens_data:
                    lens_spec.sphere = FHIRDecimal(lens_data['sphere'])
                if 'cylinder' in lens_data:
                    lens_spec.cylinder = FHIRDecimal(lens_data['cylinder'])
                if 'axis' in lens_data:
                    lens_spec.axis = FHIRInteger(lens_data['axis'])
                if 'add' in lens_data:
                    lens_spec.add = FHIRDecimal(lens_data['add'])
                if 'power' in lens_data:
                    lens_spec.power = FHIRDecimal(lens_data['power'])
                if 'backCurve' in lens_data:
                    lens_spec.back_curve = FHIRDecimal(lens_data['backCurve'])
                if 'diameter' in lens_data:
                    lens_spec.diameter = FHIRDecimal(lens_data['diameter'])
                if 'duration' in lens_data:
                    lens_spec.duration = FHIRQuantity.from_dict(lens_data['duration'])
                if 'color' in lens_data:
                    lens_spec.color = FHIRString(lens_data['color'])
                if 'brand' in lens_data:
                    lens_spec.brand = FHIRString(lens_data['brand'])
                
                # Parse prism array
                if 'prism' in lens_data:
                    for prism_data in lens_data['prism']:
                        prism = VisionPrescriptionPrism()
                        if 'amount' in prism_data:
                            prism.amount = FHIRDecimal(prism_data['amount'])
                        if 'base' in prism_data:
                            prism.base = VisionBase(prism_data['base'])
                        lens_spec.prism.append(prism)
                
                vision_prescription.lens_specification.append(lens_spec)
        
        return vision_prescription
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert VisionPrescription to dictionary"""
        result = super().to_dict()
        result.update({
            'resourceType': self.resource_type,
            'status': self.status.value
        })
        
        if self.created:
            result['created'] = self.created.value
        if self.patient:
            result['patient'] = self.patient.to_dict()
        if self.encounter:
            result['encounter'] = self.encounter.to_dict()
        if self.date_written:
            result['dateWritten'] = self.date_written.value
        if self.prescriber:
            result['prescriber'] = self.prescriber.to_dict()
        
        if self.identifier:
            result['identifier'] = [item.to_dict() for item in self.identifier]
        
        if self.lens_specification:
            result['lensSpecification'] = []
            for lens_spec in self.lens_specification:
                lens_dict = {}
                if lens_spec.product:
                    lens_dict['product'] = lens_spec.product.to_dict()
                if lens_spec.eye:
                    lens_dict['eye'] = lens_spec.eye.value
                if lens_spec.sphere:
                    lens_dict['sphere'] = lens_spec.sphere.value
                if lens_spec.cylinder:
                    lens_dict['cylinder'] = lens_spec.cylinder.value
                if lens_spec.axis:
                    lens_dict['axis'] = lens_spec.axis.value
                if lens_spec.add:
                    lens_dict['add'] = lens_spec.add.value
                if lens_spec.power:
                    lens_dict['power'] = lens_spec.power.value
                if lens_spec.back_curve:
                    lens_dict['backCurve'] = lens_spec.back_curve.value
                if lens_spec.diameter:
                    lens_dict['diameter'] = lens_spec.diameter.value
                if lens_spec.duration:
                    lens_dict['duration'] = lens_spec.duration.to_dict()
                if lens_spec.color:
                    lens_dict['color'] = lens_spec.color.value
                if lens_spec.brand:
                    lens_dict['brand'] = lens_spec.brand.value
                
                if lens_spec.prism:
                    lens_dict['prism'] = []
                    for prism in lens_spec.prism:
                        prism_dict = {}
                        if prism.amount:
                            prism_dict['amount'] = prism.amount.value
                        if prism.base:
                            prism_dict['base'] = prism.base.value
                        lens_dict['prism'].append(prism_dict)
                
                result['lensSpecification'].append(lens_dict)
        
        return result