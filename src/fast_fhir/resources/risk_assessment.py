"""
FHIR R5 RiskAssessment Resource
An assessment of the likely outcome(s) for a patient or other subject as well as the likelihood of each outcome.
"""

from typing import List, Optional, Union, Dict, Any
from enum import Enum
from ..foundation import FHIRResource, FHIRElement
from ..datatypes import (
    FHIRIdentifier, FHIRReference, FHIRCodeableConcept, FHIRString, 
    FHIRDateTime, FHIRPeriod, FHIRDecimal, FHIRRange, FHIRAnnotation
)


class RiskAssessmentStatus(Enum):
    """RiskAssessment status enumeration"""
    REGISTERED = "registered"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class RiskAssessmentPrediction(FHIRElement):
    """RiskAssessment prediction information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outcome: Optional[FHIRCodeableConcept] = None
        
        # Probability (choice type)
        self.probability_decimal: Optional[FHIRDecimal] = None
        self.probability_range: Optional[FHIRRange] = None
        
        self.qualitative_risk: Optional[FHIRCodeableConcept] = None
        self.relative_risk: Optional[FHIRDecimal] = None
        
        # When (choice type)
        self.when_period: Optional[FHIRPeriod] = None
        self.when_range: Optional[FHIRRange] = None
        
        self.rationale: Optional[FHIRString] = None
    
    def get_probability_value(self) -> Optional[float]:
        """Get probability as a float value"""
        if self.probability_decimal:
            return self.probability_decimal.value
        elif self.probability_range and self.probability_range.high:
            return self.probability_range.high.value.value if self.probability_range.high.value else None
        return None


class RiskAssessment(FHIRResource):
    """
    FHIR R5 RiskAssessment resource
    
    An assessment of the likely outcome(s) for a patient or other subject as well as
    the likelihood of each outcome.
    """
    
    resource_type = "RiskAssessment"
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # RiskAssessment-specific fields
        self.identifier: List[FHIRIdentifier] = []
        self.based_on: Optional[FHIRReference] = None
        self.parent: Optional[FHIRReference] = None
        self.status: RiskAssessmentStatus = RiskAssessmentStatus.REGISTERED
        self.method: Optional[FHIRCodeableConcept] = None
        self.code: Optional[FHIRCodeableConcept] = None
        self.subject: Optional[FHIRReference] = None
        self.encounter: Optional[FHIRReference] = None
        
        # Occurrence (choice type)
        self.occurrence_date_time: Optional[FHIRDateTime] = None
        self.occurrence_period: Optional[FHIRPeriod] = None
        
        self.condition: Optional[FHIRReference] = None
        self.performer: Optional[FHIRReference] = None
        self.reason_code: List[FHIRCodeableConcept] = []
        self.reason_reference: List[FHIRReference] = []
        self.basis: List[FHIRReference] = []
        self.prediction: List[RiskAssessmentPrediction] = []
        self.mitigation: Optional[FHIRString] = None
        self.note: List[FHIRAnnotation] = []
    
    def is_active(self) -> bool:
        """Check if RiskAssessment is active"""
        return self.status in [RiskAssessmentStatus.FINAL, RiskAssessmentStatus.AMENDED, RiskAssessmentStatus.CORRECTED]
    
    def add_prediction(self, prediction: RiskAssessmentPrediction) -> None:
        """Add prediction to RiskAssessment"""
        self.prediction.append(prediction)
    
    def get_highest_risk_prediction(self) -> Optional[RiskAssessmentPrediction]:
        """Get prediction with highest risk"""
        if not self.prediction:
            return None
        
        highest_prediction = None
        highest_risk = 0.0
        
        for prediction in self.prediction:
            risk_value = prediction.get_probability_value()
            if risk_value and risk_value > highest_risk:
                highest_risk = risk_value
                highest_prediction = prediction
        
        return highest_prediction
    
    def is_high_risk(self, threshold: float = 0.7) -> bool:
        """Check if assessment indicates high risk"""
        for prediction in self.prediction:
            risk_value = prediction.get_probability_value()
            if risk_value and risk_value >= threshold:
                return True
        return False
    
    def get_display_name(self) -> str:
        """Get display name for RiskAssessment"""
        if self.code and self.code.text:
            return self.code.text.value
        return "RiskAssessment"
    
    def validate(self) -> bool:
        """Validate RiskAssessment resource"""
        if not super().validate():
            return False
        
        # Subject is required
        if not self.subject:
            return False
        
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RiskAssessment':
        """Create RiskAssessment from dictionary"""
        risk_assessment = cls(id=data.get('id'))
        
        # Parse status
        if 'status' in data:
            risk_assessment.status = RiskAssessmentStatus(data['status'])
        
        # Parse other fields
        if 'basedOn' in data:
            risk_assessment.based_on = FHIRReference.from_dict(data['basedOn'])
        if 'parent' in data:
            risk_assessment.parent = FHIRReference.from_dict(data['parent'])
        if 'method' in data:
            risk_assessment.method = FHIRCodeableConcept.from_dict(data['method'])
        if 'code' in data:
            risk_assessment.code = FHIRCodeableConcept.from_dict(data['code'])
        if 'subject' in data:
            risk_assessment.subject = FHIRReference.from_dict(data['subject'])
        if 'encounter' in data:
            risk_assessment.encounter = FHIRReference.from_dict(data['encounter'])
        if 'condition' in data:
            risk_assessment.condition = FHIRReference.from_dict(data['condition'])
        if 'performer' in data:
            risk_assessment.performer = FHIRReference.from_dict(data['performer'])
        if 'mitigation' in data:
            risk_assessment.mitigation = FHIRString(data['mitigation'])
        
        # Parse occurrence (choice type)
        if 'occurrenceDateTime' in data:
            risk_assessment.occurrence_date_time = FHIRDateTime(data['occurrenceDateTime'])
        elif 'occurrencePeriod' in data:
            risk_assessment.occurrence_period = FHIRPeriod.from_dict(data['occurrencePeriod'])
        
        # Parse arrays
        if 'identifier' in data:
            risk_assessment.identifier = [FHIRIdentifier.from_dict(item) for item in data['identifier']]
        if 'reasonCode' in data:
            risk_assessment.reason_code = [FHIRCodeableConcept.from_dict(item) for item in data['reasonCode']]
        if 'reasonReference' in data:
            risk_assessment.reason_reference = [FHIRReference.from_dict(item) for item in data['reasonReference']]
        if 'basis' in data:
            risk_assessment.basis = [FHIRReference.from_dict(item) for item in data['basis']]
        
        # Parse predictions
        if 'prediction' in data:
            for pred_data in data['prediction']:
                prediction = RiskAssessmentPrediction()
                if 'outcome' in pred_data:
                    prediction.outcome = FHIRCodeableConcept.from_dict(pred_data['outcome'])
                if 'probabilityDecimal' in pred_data:
                    prediction.probability_decimal = FHIRDecimal(pred_data['probabilityDecimal'])
                elif 'probabilityRange' in pred_data:
                    prediction.probability_range = FHIRRange.from_dict(pred_data['probabilityRange'])
                if 'qualitativeRisk' in pred_data:
                    prediction.qualitative_risk = FHIRCodeableConcept.from_dict(pred_data['qualitativeRisk'])
                if 'relativeRisk' in pred_data:
                    prediction.relative_risk = FHIRDecimal(pred_data['relativeRisk'])
                if 'rationale' in pred_data:
                    prediction.rationale = FHIRString(pred_data['rationale'])
                risk_assessment.prediction.append(prediction)
        
        return risk_assessment
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert RiskAssessment to dictionary"""
        result = super().to_dict()
        result.update({
            'resourceType': self.resource_type,
            'status': self.status.value
        })
        
        if self.based_on:
            result['basedOn'] = self.based_on.to_dict()
        if self.parent:
            result['parent'] = self.parent.to_dict()
        if self.method:
            result['method'] = self.method.to_dict()
        if self.code:
            result['code'] = self.code.to_dict()
        if self.subject:
            result['subject'] = self.subject.to_dict()
        if self.encounter:
            result['encounter'] = self.encounter.to_dict()
        if self.condition:
            result['condition'] = self.condition.to_dict()
        if self.performer:
            result['performer'] = self.performer.to_dict()
        if self.mitigation:
            result['mitigation'] = self.mitigation.value
        
        # Occurrence (choice type)
        if self.occurrence_date_time:
            result['occurrenceDateTime'] = self.occurrence_date_time.value
        elif self.occurrence_period:
            result['occurrencePeriod'] = self.occurrence_period.to_dict()
        
        if self.identifier:
            result['identifier'] = [item.to_dict() for item in self.identifier]
        if self.reason_code:
            result['reasonCode'] = [item.to_dict() for item in self.reason_code]
        if self.reason_reference:
            result['reasonReference'] = [item.to_dict() for item in self.reason_reference]
        if self.basis:
            result['basis'] = [item.to_dict() for item in self.basis]
        
        if self.prediction:
            result['prediction'] = []
            for prediction in self.prediction:
                pred_dict = {}
                if prediction.outcome:
                    pred_dict['outcome'] = prediction.outcome.to_dict()
                if prediction.probability_decimal:
                    pred_dict['probabilityDecimal'] = prediction.probability_decimal.value
                elif prediction.probability_range:
                    pred_dict['probabilityRange'] = prediction.probability_range.to_dict()
                if prediction.qualitative_risk:
                    pred_dict['qualitativeRisk'] = prediction.qualitative_risk.to_dict()
                if prediction.relative_risk:
                    pred_dict['relativeRisk'] = prediction.relative_risk.value
                if prediction.rationale:
                    pred_dict['rationale'] = prediction.rationale.value
                result['prediction'].append(pred_dict)
        
        return result