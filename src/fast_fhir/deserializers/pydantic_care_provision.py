"""
Pydantic models for FHIR R5 Care Provision resources
"""

from typing import List, Optional, Union, Dict, Any, Literal
from datetime import datetime

from .pydantic_models import (
    BaseModel, Field, validator, root_validator,
    FHIRResourceModel, FHIRElementModel,
    FHIRCodeableConceptModel, FHIRQuantityModel, FHIRIdentifierModel,
    FHIRReferenceModel, FHIRPeriodModel, FHIRAnnotationModel,
    FHIRTimingModel, FHIRContactPointModel, FHIRRangeModel,
    CarePlanStatusEnum, CarePlanIntentEnum,
    CareTeamStatusEnum,
    GoalLifecycleStatusEnum,
    ServiceRequestStatusEnum, ServiceRequestIntentEnum, ServiceRequestPriorityEnum,
    NutritionOrderStatusEnum, NutritionOrderIntentEnum,
    RiskAssessmentStatusEnum,
    VisionPrescriptionStatusEnum, VisionEyeEnum, VisionBaseEnum,
    StrictStr, StrictBool, StrictInt, StrictFloat,
    HAS_PYDANTIC
)


# CarePlan models
class CarePlanActivityDetailModel(FHIRElementModel):
    """Pydantic model for CarePlan activity detail"""
    kind: Optional[Literal["Appointment", "CommunicationRequest", "DeviceRequest", "MedicationRequest", "NutritionOrder", "Task", "ServiceRequest", "VisionPrescription"]] = None
    instantiatesCanonical: Optional[List[StrictStr]] = Field(default_factory=list)
    instantiatesUri: Optional[List[StrictStr]] = Field(default_factory=list)
    code: Optional[FHIRCodeableConceptModel] = None
    reasonCode: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    reasonReference: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    goal: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    status: Literal["not-started", "scheduled", "in-progress", "on-hold", "completed", "cancelled", "stopped", "unknown", "entered-in-error"]
    statusReason: Optional[FHIRCodeableConceptModel] = None
    doNotPerform: Optional[StrictBool] = None
    scheduledTiming: Optional[FHIRTimingModel] = None
    scheduledPeriod: Optional[FHIRPeriodModel] = None
    scheduledString: Optional[StrictStr] = None
    location: Optional[FHIRReferenceModel] = None
    performer: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    productCodeableConcept: Optional[FHIRCodeableConceptModel] = None
    productReference: Optional[FHIRReferenceModel] = None
    dailyAmount: Optional[FHIRQuantityModel] = None
    quantity: Optional[FHIRQuantityModel] = None
    description: Optional[StrictStr] = None


class CarePlanActivityModel(FHIRElementModel):
    """Pydantic model for CarePlan activity"""
    outcomeCodeableConcept: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    outcomeReference: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    progress: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)
    reference: Optional[FHIRReferenceModel] = None
    detail: Optional[CarePlanActivityDetailModel] = None


class CarePlanModel(FHIRResourceModel):
    """Pydantic model for CarePlan resource"""
    resourceType: Literal["CarePlan"] = "CarePlan"
    identifier: Optional[List[FHIRIdentifierModel]] = Field(default_factory=list)
    instantiatesCanonical: Optional[List[StrictStr]] = Field(default_factory=list)
    instantiatesUri: Optional[List[StrictStr]] = Field(default_factory=list)
    basedOn: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    replaces: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    partOf: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    status: CarePlanStatusEnum
    intent: CarePlanIntentEnum
    category: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    title: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    subject: FHIRReferenceModel
    encounter: Optional[FHIRReferenceModel] = None
    period: Optional[FHIRPeriodModel] = None
    created: Optional[StrictStr] = None
    author: Optional[FHIRReferenceModel] = None
    contributor: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    careTeam: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    addresses: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    supportingInfo: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    goal: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    activity: Optional[List[CarePlanActivityModel]] = Field(default_factory=list)
    note: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)


# CareTeam models
class CareTeamParticipantModel(FHIRElementModel):
    """Pydantic model for CareTeam participant"""
    role: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    member: Optional[FHIRReferenceModel] = None
    onBehalfOf: Optional[FHIRReferenceModel] = None
    coveragePeriod: Optional[FHIRPeriodModel] = None
    coverageTiming: Optional[FHIRTimingModel] = None


class CareTeamModel(FHIRResourceModel):
    """Pydantic model for CareTeam resource"""
    resourceType: Literal["CareTeam"] = "CareTeam"
    identifier: Optional[List[FHIRIdentifierModel]] = Field(default_factory=list)
    status: Optional[CareTeamStatusEnum] = None
    category: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    name: Optional[StrictStr] = None
    subject: Optional[FHIRReferenceModel] = None
    period: Optional[FHIRPeriodModel] = None
    participant: Optional[List[CareTeamParticipantModel]] = Field(default_factory=list)
    reasonCode: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    reasonReference: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    managingOrganization: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    telecom: Optional[List[FHIRContactPointModel]] = Field(default_factory=list)
    note: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)


# Goal models
class GoalTargetModel(FHIRElementModel):
    """Pydantic model for Goal target"""
    measure: Optional[FHIRCodeableConceptModel] = None
    detailQuantity: Optional[FHIRQuantityModel] = None
    detailRange: Optional[FHIRRangeModel] = None
    detailCodeableConcept: Optional[FHIRCodeableConceptModel] = None
    detailString: Optional[StrictStr] = None
    detailBoolean: Optional[StrictBool] = None
    detailInteger: Optional[StrictInt] = None
    detailRatio: Optional[Dict[str, Any]] = None
    dueDate: Optional[StrictStr] = None
    dueDuration: Optional[FHIRQuantityModel] = None


class GoalModel(FHIRResourceModel):
    """Pydantic model for Goal resource"""
    resourceType: Literal["Goal"] = "Goal"
    identifier: Optional[List[FHIRIdentifierModel]] = Field(default_factory=list)
    lifecycleStatus: GoalLifecycleStatusEnum
    achievementStatus: Optional[FHIRCodeableConceptModel] = None
    category: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    priority: Optional[FHIRCodeableConceptModel] = None
    description: FHIRCodeableConceptModel
    subject: FHIRReferenceModel
    startDate: Optional[StrictStr] = None
    startCodeableConcept: Optional[FHIRCodeableConceptModel] = None
    target: Optional[List[GoalTargetModel]] = Field(default_factory=list)
    statusDate: Optional[StrictStr] = None
    statusReason: Optional[StrictStr] = None
    expressedBy: Optional[FHIRReferenceModel] = None
    addresses: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    note: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)
    outcomeCode: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    outcomeReference: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)


# ServiceRequest models
class ServiceRequestOrderDetailModel(FHIRElementModel):
    """Pydantic model for ServiceRequest order detail"""
    parameterFocus: Optional[FHIRCodeableConceptModel] = None
    parameter: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class ServiceRequestModel(FHIRResourceModel):
    """Pydantic model for ServiceRequest resource"""
    resourceType: Literal["ServiceRequest"] = "ServiceRequest"
    identifier: Optional[List[FHIRIdentifierModel]] = Field(default_factory=list)
    instantiatesCanonical: Optional[List[StrictStr]] = Field(default_factory=list)
    instantiatesUri: Optional[List[StrictStr]] = Field(default_factory=list)
    basedOn: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    replaces: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    requisition: Optional[FHIRIdentifierModel] = None
    status: ServiceRequestStatusEnum
    intent: ServiceRequestIntentEnum
    category: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    priority: Optional[ServiceRequestPriorityEnum] = None
    doNotPerform: Optional[StrictBool] = None
    code: Optional[FHIRCodeableConceptModel] = None
    orderDetail: Optional[List[ServiceRequestOrderDetailModel]] = Field(default_factory=list)
    quantityQuantity: Optional[FHIRQuantityModel] = None
    quantityRatio: Optional[Dict[str, Any]] = None
    quantityRange: Optional[FHIRRangeModel] = None
    subject: FHIRReferenceModel
    encounter: Optional[FHIRReferenceModel] = None
    occurrenceDateTime: Optional[StrictStr] = None
    occurrencePeriod: Optional[FHIRPeriodModel] = None
    occurrenceTiming: Optional[FHIRTimingModel] = None
    asNeededBoolean: Optional[StrictBool] = None
    asNeededCodeableConcept: Optional[FHIRCodeableConceptModel] = None
    authoredOn: Optional[StrictStr] = None
    requester: Optional[FHIRReferenceModel] = None
    performerType: Optional[FHIRCodeableConceptModel] = None
    performer: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    locationCode: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    locationReference: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    reasonCode: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    reasonReference: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    insurance: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    supportingInfo: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    specimen: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    bodySite: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    note: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)
    patientInstruction: Optional[StrictStr] = None
    relevantHistory: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)


# NutritionOrder models
class NutritionOrderModel(FHIRResourceModel):
    """Pydantic model for NutritionOrder resource"""
    resourceType: Literal["NutritionOrder"] = "NutritionOrder"
    identifier: Optional[List[FHIRIdentifierModel]] = Field(default_factory=list)
    instantiatesCanonical: Optional[List[StrictStr]] = Field(default_factory=list)
    instantiatesUri: Optional[List[StrictStr]] = Field(default_factory=list)
    basedOn: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    groupIdentifier: Optional[FHIRIdentifierModel] = None
    status: NutritionOrderStatusEnum
    intent: NutritionOrderIntentEnum
    priority: Optional[FHIRCodeableConceptModel] = None
    subject: FHIRReferenceModel
    encounter: Optional[FHIRReferenceModel] = None
    supportingInformation: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    dateTime: Optional[StrictStr] = None
    orderer: Optional[FHIRReferenceModel] = None
    performer: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    allergyIntolerance: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    foodPreferenceModifier: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    excludeFoodModifier: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    outsideFoodAllowed: Optional[StrictBool] = None
    oralDiet: Optional[Dict[str, Any]] = None
    supplement: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    enteralFormula: Optional[Dict[str, Any]] = None
    note: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)


# RiskAssessment models
class RiskAssessmentPredictionModel(FHIRElementModel):
    """Pydantic model for RiskAssessment prediction"""
    outcome: Optional[FHIRCodeableConceptModel] = None
    probabilityDecimal: Optional[StrictFloat] = None
    probabilityRange: Optional[FHIRRangeModel] = None
    qualitativeRisk: Optional[FHIRCodeableConceptModel] = None
    relativeRisk: Optional[StrictFloat] = None
    whenPeriod: Optional[FHIRPeriodModel] = None
    whenRange: Optional[FHIRRangeModel] = None
    rationale: Optional[StrictStr] = None


class RiskAssessmentModel(FHIRResourceModel):
    """Pydantic model for RiskAssessment resource"""
    resourceType: Literal["RiskAssessment"] = "RiskAssessment"
    identifier: Optional[List[FHIRIdentifierModel]] = Field(default_factory=list)
    basedOn: Optional[FHIRReferenceModel] = None
    parent: Optional[FHIRReferenceModel] = None
    status: RiskAssessmentStatusEnum
    method: Optional[FHIRCodeableConceptModel] = None
    code: Optional[FHIRCodeableConceptModel] = None
    subject: FHIRReferenceModel
    encounter: Optional[FHIRReferenceModel] = None
    occurrenceDateTime: Optional[StrictStr] = None
    occurrencePeriod: Optional[FHIRPeriodModel] = None
    condition: Optional[FHIRReferenceModel] = None
    performer: Optional[FHIRReferenceModel] = None
    reasonCode: Optional[List[FHIRCodeableConceptModel]] = Field(default_factory=list)
    reasonReference: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    basis: Optional[List[FHIRReferenceModel]] = Field(default_factory=list)
    prediction: Optional[List[RiskAssessmentPredictionModel]] = Field(default_factory=list)
    mitigation: Optional[StrictStr] = None
    note: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)


# VisionPrescription models
class VisionPrescriptionPrismModel(FHIRElementModel):
    """Pydantic model for VisionPrescription prism"""
    amount: Optional[StrictFloat] = None
    base: Optional[VisionBaseEnum] = None


class VisionPrescriptionLensSpecificationModel(FHIRElementModel):
    """Pydantic model for VisionPrescription lens specification"""
    product: Optional[FHIRCodeableConceptModel] = None
    eye: Optional[VisionEyeEnum] = None
    sphere: Optional[StrictFloat] = None
    cylinder: Optional[StrictFloat] = None
    axis: Optional[StrictInt] = None
    prism: Optional[List[VisionPrescriptionPrismModel]] = Field(default_factory=list)
    add: Optional[StrictFloat] = None
    power: Optional[StrictFloat] = None
    backCurve: Optional[StrictFloat] = None
    diameter: Optional[StrictFloat] = None
    duration: Optional[FHIRQuantityModel] = None
    color: Optional[StrictStr] = None
    brand: Optional[StrictStr] = None
    note: Optional[List[FHIRAnnotationModel]] = Field(default_factory=list)


class VisionPrescriptionModel(FHIRResourceModel):
    """Pydantic model for VisionPrescription resource"""
    resourceType: Literal["VisionPrescription"] = "VisionPrescription"
    identifier: Optional[List[FHIRIdentifierModel]] = Field(default_factory=list)
    status: VisionPrescriptionStatusEnum
    created: Optional[StrictStr] = None
    patient: FHIRReferenceModel
    encounter: Optional[FHIRReferenceModel] = None
    dateWritten: Optional[StrictStr] = None
    prescriber: FHIRReferenceModel
    lensSpecification: List[VisionPrescriptionLensSpecificationModel]
    
    @validator('lensSpecification')
    def validate_lens_specification(cls, v):
        if not v:
            raise ValueError("At least one lens specification is required")
        return v


# Export all Pydantic models
__all__ = [
    'HAS_PYDANTIC',
    'CarePlanModel', 'CarePlanActivityModel', 'CarePlanActivityDetailModel',
    'CareTeamModel', 'CareTeamParticipantModel',
    'GoalModel', 'GoalTargetModel',
    'ServiceRequestModel', 'ServiceRequestOrderDetailModel',
    'NutritionOrderModel',
    'RiskAssessmentModel', 'RiskAssessmentPredictionModel',
    'VisionPrescriptionModel', 'VisionPrescriptionLensSpecificationModel', 'VisionPrescriptionPrismModel'
]