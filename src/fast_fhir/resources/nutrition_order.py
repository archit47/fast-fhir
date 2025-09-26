"""
FHIR R5 NutritionOrder Resource
A request to supply a diet, formula feeding (enteral) or oral nutritional supplement to a patient/resident.
"""

from typing import List, Optional, Union, Dict, Any
from enum import Enum
from ..foundation import FHIRResource, FHIRElement
from ..datatypes import (
    FHIRIdentifier, FHIRReference, FHIRCodeableConcept, FHIRString, 
    FHIRBoolean, FHIRQuantity, FHIRTiming, FHIRDateTime, FHIRAnnotation
)


class NutritionOrderStatus(Enum):
    """NutritionOrder status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    REVOKED = "revoked"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class NutritionOrderIntent(Enum):
    """NutritionOrder intent enumeration"""
    PROPOSAL = "proposal"
    PLAN = "plan"
    DIRECTIVE = "directive"
    ORDER = "order"
    ORIGINAL_ORDER = "original-order"
    REFLEX_ORDER = "reflex-order"
    FILLER_ORDER = "filler-order"
    INSTANCE_ORDER = "instance-order"
    OPTION = "option"


class NutritionOrderOralDietNutrient(FHIRElement):
    """NutritionOrder oral diet nutrient information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier: Optional[FHIRCodeableConcept] = None
        self.amount: Optional[FHIRQuantity] = None


class NutritionOrderOralDietTexture(FHIRElement):
    """NutritionOrder oral diet texture information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modifier: Optional[FHIRCodeableConcept] = None
        self.food_type: Optional[FHIRCodeableConcept] = None


class NutritionOrderOralDiet(FHIRElement):
    """NutritionOrder oral diet information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type: List[FHIRCodeableConcept] = []
        self.schedule: List[FHIRTiming] = []
        self.nutrient: List[NutritionOrderOralDietNutrient] = []
        self.texture: List[NutritionOrderOralDietTexture] = []
        self.fluid_consistency_type: List[FHIRCodeableConcept] = []
        self.instruction: Optional[FHIRString] = None


class NutritionOrderSupplement(FHIRElement):
    """NutritionOrder supplement information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type: Optional[FHIRCodeableConcept] = None
        self.product_name: Optional[FHIRString] = None
        self.schedule: List[FHIRTiming] = []
        self.quantity: Optional[FHIRQuantity] = None
        self.instruction: Optional[FHIRString] = None


class NutritionOrderEnteralFormulaAdditive(FHIRElement):
    """NutritionOrder enteral formula additive information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type: Optional[FHIRCodeableConcept] = None
        self.product_name: Optional[FHIRString] = None
        self.quantity: Optional[FHIRQuantity] = None


class NutritionOrderEnteralFormulaAdministration(FHIRElement):
    """NutritionOrder enteral formula administration information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.schedule: Optional[FHIRTiming] = None
        self.quantity: Optional[FHIRQuantity] = None
        self.rate_quantity: Optional[FHIRQuantity] = None


class NutritionOrderEnteralFormula(FHIRElement):
    """NutritionOrder enteral formula information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_formula_type: Optional[FHIRCodeableConcept] = None
        self.base_formula_product_name: Optional[FHIRString] = None
        self.additive: List[NutritionOrderEnteralFormulaAdditive] = []
        self.caloric_density: Optional[FHIRQuantity] = None
        self.routeof_administration: Optional[FHIRCodeableConcept] = None
        self.administration: List[NutritionOrderEnteralFormulaAdministration] = []
        self.max_volume_to_deliver: Optional[FHIRQuantity] = None
        self.administration_instruction: Optional[FHIRString] = None


class NutritionOrder(FHIRResource):
    """
    FHIR R5 NutritionOrder resource
    
    A request to supply a diet, formula feeding (enteral) or oral nutritional supplement
    to a patient/resident.
    """
    
    resource_type = "NutritionOrder"
    
    def __init__(self, id: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # NutritionOrder-specific fields
        self.identifier: List[FHIRIdentifier] = []
        self.instantiates_canonical: List[FHIRReference] = []
        self.instantiates_uri: List[FHIRReference] = []
        self.based_on: List[FHIRReference] = []
        self.group_identifier: Optional[FHIRIdentifier] = None
        self.status: NutritionOrderStatus = NutritionOrderStatus.DRAFT
        self.intent: NutritionOrderIntent = NutritionOrderIntent.PROPOSAL
        self.priority: Optional[FHIRCodeableConcept] = None
        self.subject: Optional[FHIRReference] = None
        self.encounter: Optional[FHIRReference] = None
        self.supporting_information: List[FHIRReference] = []
        self.date_time: Optional[FHIRDateTime] = None
        self.orderer: Optional[FHIRReference] = None
        self.performer: List[FHIRReference] = []
        self.allergy_intolerance: List[FHIRReference] = []
        self.food_preference_modifier: List[FHIRCodeableConcept] = []
        self.exclude_food_modifier: List[FHIRCodeableConcept] = []
        self.outside_food_allowed: Optional[FHIRBoolean] = None
        self.oral_diet: Optional[NutritionOrderOralDiet] = None
        self.supplement: List[NutritionOrderSupplement] = []
        self.enteral_formula: Optional[NutritionOrderEnteralFormula] = None
        self.note: List[FHIRAnnotation] = []
    
    def is_active(self) -> bool:
        """Check if NutritionOrder is active"""
        return self.status == NutritionOrderStatus.ACTIVE
    
    def add_supplement(self, supplement: NutritionOrderSupplement) -> None:
        """Add supplement to NutritionOrder"""
        self.supplement.append(supplement)
    
    def get_display_name(self) -> str:
        """Get display name for NutritionOrder"""
        if self.oral_diet and self.oral_diet.type:
            for diet_type in self.oral_diet.type:
                if diet_type.text:
                    return f"Nutrition Order: {diet_type.text.value}"
        return "NutritionOrder"
    
    def validate(self) -> bool:
        """Validate NutritionOrder resource"""
        if not super().validate():
            return False
        
        # Subject is required
        if not self.subject:
            return False
        
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NutritionOrder':
        """Create NutritionOrder from dictionary"""
        nutrition_order = cls(id=data.get('id'))
        
        # Parse status and intent
        if 'status' in data:
            nutrition_order.status = NutritionOrderStatus(data['status'])
        if 'intent' in data:
            nutrition_order.intent = NutritionOrderIntent(data['intent'])
        
        # Parse other fields
        if 'groupIdentifier' in data:
            nutrition_order.group_identifier = FHIRIdentifier.from_dict(data['groupIdentifier'])
        if 'priority' in data:
            nutrition_order.priority = FHIRCodeableConcept.from_dict(data['priority'])
        if 'subject' in data:
            nutrition_order.subject = FHIRReference.from_dict(data['subject'])
        if 'encounter' in data:
            nutrition_order.encounter = FHIRReference.from_dict(data['encounter'])
        if 'dateTime' in data:
            nutrition_order.date_time = FHIRDateTime(data['dateTime'])
        if 'orderer' in data:
            nutrition_order.orderer = FHIRReference.from_dict(data['orderer'])
        if 'outsideFoodAllowed' in data:
            nutrition_order.outside_food_allowed = FHIRBoolean(data['outsideFoodAllowed'])
        
        # Parse arrays
        if 'identifier' in data:
            nutrition_order.identifier = [FHIRIdentifier.from_dict(item) for item in data['identifier']]
        if 'performer' in data:
            nutrition_order.performer = [FHIRReference.from_dict(item) for item in data['performer']]
        if 'allergyIntolerance' in data:
            nutrition_order.allergy_intolerance = [FHIRReference.from_dict(item) for item in data['allergyIntolerance']]
        if 'foodPreferenceModifier' in data:
            nutrition_order.food_preference_modifier = [FHIRCodeableConcept.from_dict(item) for item in data['foodPreferenceModifier']]
        if 'excludeFoodModifier' in data:
            nutrition_order.exclude_food_modifier = [FHIRCodeableConcept.from_dict(item) for item in data['excludeFoodModifier']]
        
        return nutrition_order
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert NutritionOrder to dictionary"""
        result = super().to_dict()
        result.update({
            'resourceType': self.resource_type,
            'status': self.status.value,
            'intent': self.intent.value
        })
        
        if self.group_identifier:
            result['groupIdentifier'] = self.group_identifier.to_dict()
        if self.priority:
            result['priority'] = self.priority.to_dict()
        if self.subject:
            result['subject'] = self.subject.to_dict()
        if self.encounter:
            result['encounter'] = self.encounter.to_dict()
        if self.date_time:
            result['dateTime'] = self.date_time.value
        if self.orderer:
            result['orderer'] = self.orderer.to_dict()
        if self.outside_food_allowed:
            result['outsideFoodAllowed'] = self.outside_food_allowed.value
        
        if self.identifier:
            result['identifier'] = [item.to_dict() for item in self.identifier]
        if self.performer:
            result['performer'] = [item.to_dict() for item in self.performer]
        if self.allergy_intolerance:
            result['allergyIntolerance'] = [item.to_dict() for item in self.allergy_intolerance]
        if self.food_preference_modifier:
            result['foodPreferenceModifier'] = [item.to_dict() for item in self.food_preference_modifier]
        if self.exclude_food_modifier:
            result['excludeFoodModifier'] = [item.to_dict() for item in self.exclude_food_modifier]
        
        return result