"""
Pydantic models for FHIR R5 Care Provision resources
Provides JSON deserialization with validation and type checking
"""

from typing import List, Optional, Union, Dict, Any, Literal
from datetime import datetime
from enum import Enum
import json

try:
    from pydantic import BaseModel, Field, validator, root_validator
    from pydantic.types import StrictStr, StrictBool, StrictInt, StrictFloat
    HAS_PYDANTIC = True
except ImportError:
    # Fallback base class if Pydantic is not available
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    def Field(**kwargs):
        return None
    
    def validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    def root_validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    StrictStr = str
    StrictBool = bool
    StrictInt = int
    StrictFloat = float
    HAS_PYDANTIC = False


# Base FHIR data type models
class FHIRElementModel(BaseModel):
    """Base Pydantic model for FHIR elements"""
    id: Optional[StrictStr] = None
    extension: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    
    class Config:
        extra = "forbid"
        validate_assignment = True


class FHIRResourceModel(FHIRElementModel):
    """Base Pydantic model for FHIR resources"""
    resourceType: StrictStr
    id: Optional[StrictStr] = None
    meta: Optional[Dict[str, Any]] = None
    implicitRules: Optional[StrictStr] = None
    language: Optional[StrictStr] = None
    text: Optional[Dict[str, Any]] = None
    contained: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    modifierExtension: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


# FHIR data type models
class FHIRCodingModel(BaseModel):
    """Pydantic model for FHIR Coding"""
    system: Optional[StrictStr] = None
    version: Optional[StrictStr] = None
    code: Optional[StrictStr] = None
    display: Optional[StrictStr] = None
    userSelected: Optional[StrictBool] = None


class FHIRCodeableConceptModel(BaseModel):
    """Pydantic model for FHIR CodeableConcept"""
    coding: Optional[List[FHIRCodingModel]] = Field(default_factory=list)
    text: Optional[StrictStr] = None


class FHIRQuantityModel(BaseModel):
    """Pydantic model for FHIR Quantity"""
    value: Optional[StrictFloat] = None
    comparator: Optional[Literal["<", "<=", ">=", ">"]] = None
    unit: Optional[StrictStr] = None
    system: Optional[StrictStr] = None
    code: Optional[StrictStr] = None


class FHIRIdentifierModel(BaseModel):
    """Pydantic model for FHIR Identifier"""
    use: Optional[Literal["usual", "official", "temp", "secondary", "old"]] = None
    type: Optional[FHIRCodeableConceptModel] = None
    system: Optional[StrictStr] = None
    value: Optional[StrictStr] = None
    period: Optional[Dict[str, Any]] = None
    assigner: Optional[Dict[str, Any]] = None


class FHIRReferenceModel(BaseModel):
    """Pydantic model for FHIR Reference"""
    reference: Optional[StrictStr] = None
    type: Optional[StrictStr] = None
    identifier: Optional[FHIRIdentifierModel] = None
    display: Optional[StrictStr] = None


class FHIRPeriodModel(BaseModel):
    """Pydantic model for FHIR Period"""
    start: Optional[StrictStr] = None
    end: Optional[StrictStr] = None
    
    @validator('start', 'end')
    def validate_datetime(cls, v):
        if v is not None:
            # Basic datetime format validation
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Invalid datetime format: {v}")
        return v


class FHIRAnnotationModel(BaseModel):
    """Pydantic model for FHIR Annotation"""
    authorReference: Optional[FHIRReferenceModel] = None
    authorString: Optional[StrictStr] = None
    time: Optional[StrictStr] = None
    text: StrictStr
    
    @validator('time')
    def validate_time(cls, v):
        if v is not None:
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Invalid datetime format: {v}")
        return v


class FHIRTimingModel(BaseModel):
    """Pydantic model for FHIR Timing"""
    event: Optional[List[StrictStr]] = Field(default_factory=list)
    repeat: Optional[Dict[str, Any]] = None
    code: Optional[FHIRCodeableConceptModel] = None


class FHIRContactPointModel(BaseModel):
    """Pydantic model for FHIR ContactPoint"""
    system: Optional[Literal["phone", "fax", "email", "pager", "url", "sms", "other"]] = None
    value: Optional[StrictStr] = None
    use: Optional[Literal["home", "work", "temp", "old", "mobile"]] = None
    rank: Optional[StrictInt] = None
    period: Optional[FHIRPeriodModel] = None


class FHIRRangeModel(BaseModel):
    """Pydantic model for FHIR Range"""
    low: Optional[FHIRQuantityModel] = None
    high: Optional[FHIRQuantityModel] = None


# Care Provision resource status enums
class CarePlanStatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    REVOKED = "revoked"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class CarePlanIntentEnum(str, Enum):
    PROPOSAL = "proposal"
    PLAN = "plan"
    ORDER = "order"
    OPTION = "option"


class CareTeamStatusEnum(str, Enum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
    ENTERED_IN_ERROR = "entered-in-error"


class GoalLifecycleStatusEnum(str, Enum):
    PROPOSED = "proposed"
    PLANNED = "planned"
    ACCEPTED = "accepted"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    REJECTED = "rejected"


class ServiceRequestStatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    REVOKED = "revoked"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class ServiceRequestIntentEnum(str, Enum):
    PROPOSAL = "proposal"
    PLAN = "plan"
    DIRECTIVE = "directive"
    ORDER = "order"
    ORIGINAL_ORDER = "original-order"
    REFLEX_ORDER = "reflex-order"
    FILLER_ORDER = "filler-order"
    INSTANCE_ORDER = "instance-order"
    OPTION = "option"


class ServiceRequestPriorityEnum(str, Enum):
    ROUTINE = "routine"
    URGENT = "urgent"
    ASAP = "asap"
    STAT = "stat"


class NutritionOrderStatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ON_HOLD = "on-hold"
    REVOKED = "revoked"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class NutritionOrderIntentEnum(str, Enum):
    PROPOSAL = "proposal"
    PLAN = "plan"
    DIRECTIVE = "directive"
    ORDER = "order"
    ORIGINAL_ORDER = "original-order"
    REFLEX_ORDER = "reflex-order"
    FILLER_ORDER = "filler-order"
    INSTANCE_ORDER = "instance-order"
    OPTION = "option"


class RiskAssessmentStatusEnum(str, Enum):
    REGISTERED = "registered"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered-in-error"
    UNKNOWN = "unknown"


class VisionPrescriptionStatusEnum(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    DRAFT = "draft"
    ENTERED_IN_ERROR = "entered-in-error"


class VisionEyeEnum(str, Enum):
    RIGHT = "right"
    LEFT = "left"


class VisionBaseEnum(str, Enum):
    UP = "up"
    DOWN = "down"
    IN = "in"
    OUT = "out"


# Export all models and utilities
__all__ = [
    'HAS_PYDANTIC',
    'FHIRElementModel', 'FHIRResourceModel',
    'FHIRCodingModel', 'FHIRCodeableConceptModel', 'FHIRQuantityModel',
    'FHIRIdentifierModel', 'FHIRReferenceModel', 'FHIRPeriodModel',
    'FHIRAnnotationModel', 'FHIRTimingModel', 'FHIRContactPointModel', 'FHIRRangeModel',
    'CarePlanStatusEnum', 'CarePlanIntentEnum',
    'CareTeamStatusEnum',
    'GoalLifecycleStatusEnum',
    'ServiceRequestStatusEnum', 'ServiceRequestIntentEnum', 'ServiceRequestPriorityEnum',
    'NutritionOrderStatusEnum', 'NutritionOrderIntentEnum',
    'RiskAssessmentStatusEnum',
    'VisionPrescriptionStatusEnum', 'VisionEyeEnum', 'VisionBaseEnum'
]