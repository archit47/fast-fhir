"""
FHIR R5 Care Provision Resource Deserializers
Converts JSON strings to FHIR resource objects using Pydantic validation
"""

import json
from typing import Union, Dict, Any, Optional, Type, TypeVar
from datetime import datetime

try:
    from .pydantic_care_provision import (
        HAS_PYDANTIC,
        CarePlanModel, CareTeamModel, GoalModel, ServiceRequestModel,
        NutritionOrderModel, RiskAssessmentModel, VisionPrescriptionModel
    )
    PYDANTIC_CARE_PROVISION_MODELS_AVAILABLE = True
except ImportError as e:
    # Pydantic models not available (version incompatibility or missing)
    HAS_PYDANTIC = False
    PYDANTIC_CARE_PROVISION_MODELS_AVAILABLE = False
    CarePlanModel = CareTeamModel = GoalModel = ServiceRequestModel = None
    NutritionOrderModel = RiskAssessmentModel = VisionPrescriptionModel = None

# Import the actual FHIR resource classes
from ..resources.care_plan import CarePlan, CarePlanStatus, CarePlanIntent, CarePlanActivity, CarePlanActivityDetail
from ..resources.care_team import CareTeam, CareTeamStatus, CareTeamParticipant
from ..resources.goal import Goal, GoalLifecycleStatus, GoalTarget
from ..resources.service_request import ServiceRequest, ServiceRequestStatus, ServiceRequestIntent, ServiceRequestPriority, ServiceRequestOrderDetail
from ..resources.nutrition_order import NutritionOrder, NutritionOrderStatus, NutritionOrderIntent
from ..resources.risk_assessment import RiskAssessment, RiskAssessmentStatus, RiskAssessmentPrediction
from ..resources.vision_prescription import VisionPrescription, VisionPrescriptionStatus, VisionEye, VisionBase, VisionPrescriptionLensSpecification, VisionPrescriptionPrism

# Import FHIR datatypes
from ..datatypes import (
    FHIRString, FHIRReference, FHIRCodeableConcept, FHIRDateTime, 
    FHIRPeriod, FHIRDecimal, FHIRBoolean, FHIRInteger, FHIRIdentifier,
    FHIRQuantity, FHIRAnnotation, FHIRTiming, FHIRContactPoint, FHIRRange
)

T = TypeVar('T')


class FHIRDeserializationError(Exception):
    """Exception raised when FHIR resource deserialization fails"""
    pass


class FHIRCareProvisionDeserializer:
    """
    Deserializer for FHIR R5 Care Provision resources
    Uses Pydantic for validation and converts to native FHIR resource objects
    """
    
    def __init__(self, use_pydantic_validation: bool = True):
        """
        Initialize the deserializer
        
        Args:
            use_pydantic_validation: Whether to use Pydantic validation (requires pydantic package)
        """
        self.use_pydantic_validation = use_pydantic_validation and HAS_PYDANTIC
        
        # Resource type mapping
        self.resource_models = {
            "CarePlan": CarePlanModel,
            "CareTeam": CareTeamModel,
            "Goal": GoalModel,
            "ServiceRequest": ServiceRequestModel,
            "NutritionOrder": NutritionOrderModel,
            "RiskAssessment": RiskAssessmentModel,
            "VisionPrescription": VisionPrescriptionModel
        }
        
        self.resource_classes = {
            "CarePlan": CarePlan,
            "CareTeam": CareTeam,
            "Goal": Goal,
            "ServiceRequest": ServiceRequest,
            "NutritionOrder": NutritionOrder,
            "RiskAssessment": RiskAssessment,
            "VisionPrescription": VisionPrescription
        }
    
    def deserialize(self, json_data: Union[str, Dict[str, Any]]) -> Union[CarePlan, CareTeam, Goal, ServiceRequest, NutritionOrder, RiskAssessment, VisionPrescription]:
        """
        Deserialize JSON data to a FHIR Care Provision resource
        
        Args:
            json_data: JSON string or dictionary containing FHIR resource data
            
        Returns:
            FHIR resource object
            
        Raises:
            FHIRDeserializationError: If deserialization fails
        """
        try:
            # Parse JSON if string
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data
            
            # Get resource type
            resource_type = data.get("resourceType")
            if not resource_type:
                raise FHIRDeserializationError("Missing resourceType in JSON data")
            
            if resource_type not in self.resource_classes:
                raise FHIRDeserializationError(f"Unsupported resource type: {resource_type}")
            
            # Validate with Pydantic if available
            if self.use_pydantic_validation:
                pydantic_model = self.resource_models[resource_type]
                validated_data = pydantic_model(**data)
                data = validated_data.dict()
            
            # Convert to FHIR resource object
            return self._convert_to_fhir_resource(resource_type, data)
            
        except json.JSONDecodeError as e:
            raise FHIRDeserializationError(f"Invalid JSON: {e}")
        except Exception as e:
            raise FHIRDeserializationError(f"Deserialization failed: {e}")
    
    def _convert_to_fhir_resource(self, resource_type: str, data: Dict[str, Any]) -> Any:
        """Convert validated data to FHIR resource object"""
        
        if resource_type == "CarePlan":
            return self._convert_care_plan(data)
        elif resource_type == "CareTeam":
            return self._convert_care_team(data)
        elif resource_type == "Goal":
            return self._convert_goal(data)
        elif resource_type == "ServiceRequest":
            return self._convert_service_request(data)
        elif resource_type == "NutritionOrder":
            return self._convert_nutrition_order(data)
        elif resource_type == "RiskAssessment":
            return self._convert_risk_assessment(data)
        elif resource_type == "VisionPrescription":
            return self._convert_vision_prescription(data)
        else:
            raise FHIRDeserializationError(f"Conversion not implemented for {resource_type}")
    
    def _convert_care_plan(self, data: Dict[str, Any]) -> CarePlan:
        """Convert data to CarePlan resource"""
        care_plan = CarePlan(id=data.get("id"))
        
        # Set status and intent
        if "status" in data:
            care_plan.status = CarePlanStatus(data["status"])
        if "intent" in data:
            care_plan.intent = CarePlanIntent(data["intent"])
        
        # Set basic fields
        if "title" in data:
            care_plan.title = FHIRString(data["title"])
        if "description" in data:
            care_plan.description = FHIRString(data["description"])
        if "subject" in data:
            care_plan.subject = self._convert_reference(data["subject"])
        if "encounter" in data:
            care_plan.encounter = self._convert_reference(data["encounter"])
        if "period" in data:
            care_plan.period = self._convert_period(data["period"])
        if "created" in data:
            care_plan.created = FHIRDateTime(data["created"])
        if "author" in data:
            care_plan.author = self._convert_reference(data["author"])
        
        # Set arrays
        if "identifier" in data:
            care_plan.identifier = [self._convert_identifier(item) for item in data["identifier"]]
        if "category" in data:
            care_plan.category = [self._convert_codeable_concept(item) for item in data["category"]]
        if "contributor" in data:
            care_plan.contributor = [self._convert_reference(item) for item in data["contributor"]]
        if "careTeam" in data:
            care_plan.care_team = [self._convert_reference(item) for item in data["careTeam"]]
        if "addresses" in data:
            care_plan.addresses = [self._convert_reference(item) for item in data["addresses"]]
        if "goal" in data:
            care_plan.goal = [self._convert_reference(item) for item in data["goal"]]
        if "note" in data:
            care_plan.note = [self._convert_annotation(item) for item in data["note"]]
        
        # Convert activities
        if "activity" in data:
            for activity_data in data["activity"]:
                activity = CarePlanActivity()
                if "detail" in activity_data:
                    detail = CarePlanActivityDetail()
                    detail_data = activity_data["detail"]
                    if "status" in detail_data:
                        detail.status = detail_data["status"]
                    if "code" in detail_data:
                        detail.code = self._convert_codeable_concept(detail_data["code"])
                    if "description" in detail_data:
                        detail.description = FHIRString(detail_data["description"])
                    activity.detail = detail
                care_plan.add_activity(activity)
        
        return care_plan
    
    def _convert_care_team(self, data: Dict[str, Any]) -> CareTeam:
        """Convert data to CareTeam resource"""
        care_team = CareTeam(id=data.get("id"))
        
        # Set status
        if "status" in data:
            care_team.status = CareTeamStatus(data["status"])
        
        # Set basic fields
        if "name" in data:
            care_team.name = FHIRString(data["name"])
        if "subject" in data:
            care_team.subject = self._convert_reference(data["subject"])
        if "period" in data:
            care_team.period = self._convert_period(data["period"])
        
        # Set arrays
        if "identifier" in data:
            care_team.identifier = [self._convert_identifier(item) for item in data["identifier"]]
        if "category" in data:
            care_team.category = [self._convert_codeable_concept(item) for item in data["category"]]
        if "reasonCode" in data:
            care_team.reason_code = [self._convert_codeable_concept(item) for item in data["reasonCode"]]
        if "reasonReference" in data:
            care_team.reason_reference = [self._convert_reference(item) for item in data["reasonReference"]]
        if "managingOrganization" in data:
            care_team.managing_organization = [self._convert_reference(item) for item in data["managingOrganization"]]
        if "telecom" in data:
            care_team.telecom = [self._convert_contact_point(item) for item in data["telecom"]]
        if "note" in data:
            care_team.note = [self._convert_annotation(item) for item in data["note"]]
        
        # Convert participants
        if "participant" in data:
            for participant_data in data["participant"]:
                participant = CareTeamParticipant()
                if "member" in participant_data:
                    participant.member = self._convert_reference(participant_data["member"])
                if "onBehalfOf" in participant_data:
                    participant.on_behalf_of = self._convert_reference(participant_data["onBehalfOf"])
                if "coveragePeriod" in participant_data:
                    participant.coverage_period = self._convert_period(participant_data["coveragePeriod"])
                if "role" in participant_data:
                    participant.role = [self._convert_codeable_concept(item) for item in participant_data["role"]]
                care_team.add_participant(participant)
        
        return care_team
    
    def _convert_goal(self, data: Dict[str, Any]) -> Goal:
        """Convert data to Goal resource"""
        goal = Goal(id=data.get("id"))
        
        # Set lifecycle status
        if "lifecycleStatus" in data:
            goal.lifecycle_status = GoalLifecycleStatus(data["lifecycleStatus"])
        
        # Set required fields
        if "description" in data:
            goal.description = self._convert_codeable_concept(data["description"])
        if "subject" in data:
            goal.subject = self._convert_reference(data["subject"])
        
        # Set optional fields
        if "achievementStatus" in data:
            goal.achievement_status = self._convert_codeable_concept(data["achievementStatus"])
        if "priority" in data:
            goal.priority = self._convert_codeable_concept(data["priority"])
        if "startDate" in data:
            goal.start_date = data["startDate"]
        if "startCodeableConcept" in data:
            goal.start_codeable_concept = self._convert_codeable_concept(data["startCodeableConcept"])
        if "statusDate" in data:
            goal.status_date = data["statusDate"]
        if "statusReason" in data:
            goal.status_reason = FHIRString(data["statusReason"])
        if "expressedBy" in data:
            goal.expressed_by = self._convert_reference(data["expressedBy"])
        
        # Set arrays
        if "identifier" in data:
            goal.identifier = [self._convert_identifier(item) for item in data["identifier"]]
        if "category" in data:
            goal.category = [self._convert_codeable_concept(item) for item in data["category"]]
        if "addresses" in data:
            goal.addresses = [self._convert_reference(item) for item in data["addresses"]]
        if "note" in data:
            goal.note = [self._convert_annotation(item) for item in data["note"]]
        if "outcomeCode" in data:
            goal.outcome_code = [self._convert_codeable_concept(item) for item in data["outcomeCode"]]
        if "outcomeReference" in data:
            goal.outcome_reference = [self._convert_reference(item) for item in data["outcomeReference"]]
        
        # Convert targets
        if "target" in data:
            for target_data in data["target"]:
                target = GoalTarget()
                if "measure" in target_data:
                    target.measure = self._convert_codeable_concept(target_data["measure"])
                if "dueDate" in target_data:
                    target.due_date = target_data["dueDate"]
                if "detailQuantity" in target_data:
                    target.detail_quantity = self._convert_quantity(target_data["detailQuantity"])
                if "detailRange" in target_data:
                    target.detail_range = self._convert_range(target_data["detailRange"])
                if "detailCodeableConcept" in target_data:
                    target.detail_codeable_concept = self._convert_codeable_concept(target_data["detailCodeableConcept"])
                if "detailString" in target_data:
                    target.detail_string = FHIRString(target_data["detailString"])
                if "detailBoolean" in target_data:
                    target.detail_boolean = FHIRBoolean(target_data["detailBoolean"])
                if "detailInteger" in target_data:
                    target.detail_integer = FHIRInteger(target_data["detailInteger"])
                goal.add_target(target)
        
        return goal
    
    def _convert_service_request(self, data: Dict[str, Any]) -> ServiceRequest:
        """Convert data to ServiceRequest resource"""
        service_request = ServiceRequest(id=data.get("id"))
        
        # Set status, intent, and priority
        if "status" in data:
            service_request.status = ServiceRequestStatus(data["status"])
        if "intent" in data:
            service_request.intent = ServiceRequestIntent(data["intent"])
        if "priority" in data:
            service_request.priority = ServiceRequestPriority(data["priority"])
        
        # Set required fields
        if "subject" in data:
            service_request.subject = self._convert_reference(data["subject"])
        
        # Set optional fields
        if "code" in data:
            service_request.code = self._convert_codeable_concept(data["code"])
        if "encounter" in data:
            service_request.encounter = self._convert_reference(data["encounter"])
        if "occurrenceDateTime" in data:
            service_request.occurrence_date_time = FHIRDateTime(data["occurrenceDateTime"])
        if "occurrencePeriod" in data:
            service_request.occurrence_period = self._convert_period(data["occurrencePeriod"])
        if "occurrenceTiming" in data:
            service_request.occurrence_timing = self._convert_timing(data["occurrenceTiming"])
        if "authoredOn" in data:
            service_request.authored_on = FHIRDateTime(data["authoredOn"])
        if "requester" in data:
            service_request.requester = self._convert_reference(data["requester"])
        if "performerType" in data:
            service_request.performer_type = self._convert_codeable_concept(data["performerType"])
        if "doNotPerform" in data:
            service_request.do_not_perform = FHIRBoolean(data["doNotPerform"])
        if "patientInstruction" in data:
            service_request.patient_instruction = FHIRString(data["patientInstruction"])
        
        # Set arrays
        if "identifier" in data:
            service_request.identifier = [self._convert_identifier(item) for item in data["identifier"]]
        if "category" in data:
            service_request.category = [self._convert_codeable_concept(item) for item in data["category"]]
        if "performer" in data:
            service_request.performer = [self._convert_reference(item) for item in data["performer"]]
        if "reasonCode" in data:
            service_request.reason_code = [self._convert_codeable_concept(item) for item in data["reasonCode"]]
        if "reasonReference" in data:
            service_request.reason_reference = [self._convert_reference(item) for item in data["reasonReference"]]
        if "note" in data:
            service_request.note = [self._convert_annotation(item) for item in data["note"]]
        
        return service_request
    
    def _convert_nutrition_order(self, data: Dict[str, Any]) -> NutritionOrder:
        """Convert data to NutritionOrder resource"""
        nutrition_order = NutritionOrder(id=data.get("id"))
        
        # Set status and intent
        if "status" in data:
            nutrition_order.status = NutritionOrderStatus(data["status"])
        if "intent" in data:
            nutrition_order.intent = NutritionOrderIntent(data["intent"])
        
        # Set required fields
        if "subject" in data:
            nutrition_order.subject = self._convert_reference(data["subject"])
        
        # Set optional fields
        if "encounter" in data:
            nutrition_order.encounter = self._convert_reference(data["encounter"])
        if "dateTime" in data:
            nutrition_order.date_time = FHIRDateTime(data["dateTime"])
        if "orderer" in data:
            nutrition_order.orderer = self._convert_reference(data["orderer"])
        if "priority" in data:
            nutrition_order.priority = self._convert_codeable_concept(data["priority"])
        if "outsideFoodAllowed" in data:
            nutrition_order.outside_food_allowed = FHIRBoolean(data["outsideFoodAllowed"])
        
        # Set arrays
        if "identifier" in data:
            nutrition_order.identifier = [self._convert_identifier(item) for item in data["identifier"]]
        if "performer" in data:
            nutrition_order.performer = [self._convert_reference(item) for item in data["performer"]]
        if "allergyIntolerance" in data:
            nutrition_order.allergy_intolerance = [self._convert_reference(item) for item in data["allergyIntolerance"]]
        if "foodPreferenceModifier" in data:
            nutrition_order.food_preference_modifier = [self._convert_codeable_concept(item) for item in data["foodPreferenceModifier"]]
        if "excludeFoodModifier" in data:
            nutrition_order.exclude_food_modifier = [self._convert_codeable_concept(item) for item in data["excludeFoodModifier"]]
        if "note" in data:
            nutrition_order.note = [self._convert_annotation(item) for item in data["note"]]
        
        return nutrition_order
    
    def _convert_risk_assessment(self, data: Dict[str, Any]) -> RiskAssessment:
        """Convert data to RiskAssessment resource"""
        risk_assessment = RiskAssessment(id=data.get("id"))
        
        # Set status
        if "status" in data:
            risk_assessment.status = RiskAssessmentStatus(data["status"])
        
        # Set required fields
        if "subject" in data:
            risk_assessment.subject = self._convert_reference(data["subject"])
        
        # Set optional fields
        if "basedOn" in data:
            risk_assessment.based_on = self._convert_reference(data["basedOn"])
        if "parent" in data:
            risk_assessment.parent = self._convert_reference(data["parent"])
        if "method" in data:
            risk_assessment.method = self._convert_codeable_concept(data["method"])
        if "code" in data:
            risk_assessment.code = self._convert_codeable_concept(data["code"])
        if "encounter" in data:
            risk_assessment.encounter = self._convert_reference(data["encounter"])
        if "occurrenceDateTime" in data:
            risk_assessment.occurrence_date_time = FHIRDateTime(data["occurrenceDateTime"])
        if "occurrencePeriod" in data:
            risk_assessment.occurrence_period = self._convert_period(data["occurrencePeriod"])
        if "condition" in data:
            risk_assessment.condition = self._convert_reference(data["condition"])
        if "performer" in data:
            risk_assessment.performer = self._convert_reference(data["performer"])
        if "mitigation" in data:
            risk_assessment.mitigation = FHIRString(data["mitigation"])
        
        # Set arrays
        if "identifier" in data:
            risk_assessment.identifier = [self._convert_identifier(item) for item in data["identifier"]]
        if "reasonCode" in data:
            risk_assessment.reason_code = [self._convert_codeable_concept(item) for item in data["reasonCode"]]
        if "reasonReference" in data:
            risk_assessment.reason_reference = [self._convert_reference(item) for item in data["reasonReference"]]
        if "basis" in data:
            risk_assessment.basis = [self._convert_reference(item) for item in data["basis"]]
        if "note" in data:
            risk_assessment.note = [self._convert_annotation(item) for item in data["note"]]
        
        # Convert predictions
        if "prediction" in data:
            for prediction_data in data["prediction"]:
                prediction = RiskAssessmentPrediction()
                if "outcome" in prediction_data:
                    prediction.outcome = self._convert_codeable_concept(prediction_data["outcome"])
                if "probabilityDecimal" in prediction_data:
                    prediction.probability_decimal = FHIRDecimal(prediction_data["probabilityDecimal"])
                if "probabilityRange" in prediction_data:
                    prediction.probability_range = self._convert_range(prediction_data["probabilityRange"])
                if "qualitativeRisk" in prediction_data:
                    prediction.qualitative_risk = self._convert_codeable_concept(prediction_data["qualitativeRisk"])
                if "relativeRisk" in prediction_data:
                    prediction.relative_risk = FHIRDecimal(prediction_data["relativeRisk"])
                if "rationale" in prediction_data:
                    prediction.rationale = FHIRString(prediction_data["rationale"])
                risk_assessment.add_prediction(prediction)
        
        return risk_assessment
    
    def _convert_vision_prescription(self, data: Dict[str, Any]) -> VisionPrescription:
        """Convert data to VisionPrescription resource"""
        vision_prescription = VisionPrescription(id=data.get("id"))
        
        # Set status
        if "status" in data:
            vision_prescription.status = VisionPrescriptionStatus(data["status"])
        
        # Set required fields
        if "patient" in data:
            vision_prescription.patient = self._convert_reference(data["patient"])
        if "prescriber" in data:
            vision_prescription.prescriber = self._convert_reference(data["prescriber"])
        
        # Set optional fields
        if "created" in data:
            vision_prescription.created = FHIRDateTime(data["created"])
        if "encounter" in data:
            vision_prescription.encounter = self._convert_reference(data["encounter"])
        if "dateWritten" in data:
            vision_prescription.date_written = FHIRDateTime(data["dateWritten"])
        
        # Set arrays
        if "identifier" in data:
            vision_prescription.identifier = [self._convert_identifier(item) for item in data["identifier"]]
        
        # Convert lens specifications
        if "lensSpecification" in data:
            for lens_data in data["lensSpecification"]:
                lens_spec = VisionPrescriptionLensSpecification()
                if "product" in lens_data:
                    lens_spec.product = self._convert_codeable_concept(lens_data["product"])
                if "eye" in lens_data:
                    lens_spec.eye = VisionEye(lens_data["eye"])
                if "sphere" in lens_data:
                    lens_spec.sphere = FHIRDecimal(lens_data["sphere"])
                if "cylinder" in lens_data:
                    lens_spec.cylinder = FHIRDecimal(lens_data["cylinder"])
                if "axis" in lens_data:
                    lens_spec.axis = FHIRInteger(lens_data["axis"])
                if "add" in lens_data:
                    lens_spec.add = FHIRDecimal(lens_data["add"])
                if "power" in lens_data:
                    lens_spec.power = FHIRDecimal(lens_data["power"])
                if "backCurve" in lens_data:
                    lens_spec.back_curve = FHIRDecimal(lens_data["backCurve"])
                if "diameter" in lens_data:
                    lens_spec.diameter = FHIRDecimal(lens_data["diameter"])
                if "color" in lens_data:
                    lens_spec.color = FHIRString(lens_data["color"])
                if "brand" in lens_data:
                    lens_spec.brand = FHIRString(lens_data["brand"])
                
                # Convert prism array
                if "prism" in lens_data:
                    for prism_data in lens_data["prism"]:
                        prism = VisionPrescriptionPrism()
                        if "amount" in prism_data:
                            prism.amount = FHIRDecimal(prism_data["amount"])
                        if "base" in prism_data:
                            prism.base = VisionBase(prism_data["base"])
                        lens_spec.prism.append(prism)
                
                vision_prescription.add_lens_specification(lens_spec)
        
        return vision_prescription
    
    # Helper methods for converting FHIR data types
    def _convert_reference(self, data: Dict[str, Any]) -> FHIRReference:
        """Convert reference data to FHIRReference"""
        reference = FHIRReference()
        if "reference" in data:
            reference.reference = FHIRString(data["reference"])
        if "display" in data:
            reference.display = FHIRString(data["display"])
        if "identifier" in data:
            reference.identifier = self._convert_identifier(data["identifier"])
        return reference
    
    def _convert_codeable_concept(self, data: Dict[str, Any]) -> FHIRCodeableConcept:
        """Convert codeable concept data to FHIRCodeableConcept"""
        concept = FHIRCodeableConcept()
        if "text" in data:
            concept.text = FHIRString(data["text"])
        # Note: coding array conversion would be added here in a full implementation
        return concept
    
    def _convert_identifier(self, data: Dict[str, Any]) -> FHIRIdentifier:
        """Convert identifier data to FHIRIdentifier"""
        identifier = FHIRIdentifier()
        if "system" in data:
            identifier.system = FHIRString(data["system"])
        if "value" in data:
            identifier.value = FHIRString(data["value"])
        if "use" in data:
            identifier.use = data["use"]
        return identifier
    
    def _convert_period(self, data: Dict[str, Any]) -> FHIRPeriod:
        """Convert period data to FHIRPeriod"""
        return FHIRPeriod(
            start=data.get("start"),
            end=data.get("end")
        )
    
    def _convert_quantity(self, data: Dict[str, Any]) -> FHIRQuantity:
        """Convert quantity data to FHIRQuantity"""
        return FHIRQuantity(
            value=data.get("value"),
            unit=data.get("unit"),
            system=data.get("system"),
            code=data.get("code")
        )
    
    def _convert_annotation(self, data: Dict[str, Any]) -> FHIRAnnotation:
        """Convert annotation data to FHIRAnnotation"""
        author_ref = None
        if "authorReference" in data:
            author_ref = self._convert_reference(data["authorReference"])
        
        return FHIRAnnotation(
            text=data.get("text", ""),
            author_reference=author_ref,
            author_string=data.get("authorString"),
            time=data.get("time")
        )
    
    def _convert_timing(self, data: Dict[str, Any]) -> FHIRTiming:
        """Convert timing data to FHIRTiming"""
        code = None
        if "code" in data:
            code = self._convert_codeable_concept(data["code"])
        
        return FHIRTiming(
            event=data.get("event", []),
            repeat=data.get("repeat"),
            code=code
        )
    
    def _convert_contact_point(self, data: Dict[str, Any]) -> FHIRContactPoint:
        """Convert contact point data to FHIRContactPoint"""
        period = None
        if "period" in data:
            period = self._convert_period(data["period"])
        
        return FHIRContactPoint(
            system=data.get("system"),
            value=data.get("value"),
            use=data.get("use"),
            rank=data.get("rank"),
            period=period
        )
    
    def _convert_range(self, data: Dict[str, Any]) -> FHIRRange:
        """Convert range data to FHIRRange"""
        low = None
        if "low" in data:
            low = self._convert_quantity(data["low"])
        
        high = None
        if "high" in data:
            high = self._convert_quantity(data["high"])
        
        return FHIRRange(low=low, high=high)


# Convenience functions
def deserialize_care_provision_resource(json_data: Union[str, Dict[str, Any]], 
                                       use_pydantic_validation: bool = True) -> Union[CarePlan, CareTeam, Goal, ServiceRequest, NutritionOrder, RiskAssessment, VisionPrescription]:
    """
    Convenience function to deserialize a FHIR Care Provision resource
    
    Args:
        json_data: JSON string or dictionary containing FHIR resource data
        use_pydantic_validation: Whether to use Pydantic validation
        
    Returns:
        FHIR resource object
    """
    deserializer = FHIRCareProvisionDeserializer(use_pydantic_validation=use_pydantic_validation)
    return deserializer.deserialize(json_data)


def deserialize_care_plan(json_data: Union[str, Dict[str, Any]], use_pydantic_validation: bool = True) -> CarePlan:
    """Deserialize CarePlan from JSON"""
    resource = deserialize_care_provision_resource(json_data, use_pydantic_validation)
    if not isinstance(resource, CarePlan):
        raise FHIRDeserializationError(f"Expected CarePlan, got {type(resource).__name__}")
    return resource


def deserialize_care_team(json_data: Union[str, Dict[str, Any]], use_pydantic_validation: bool = True) -> CareTeam:
    """Deserialize CareTeam from JSON"""
    resource = deserialize_care_provision_resource(json_data, use_pydantic_validation)
    if not isinstance(resource, CareTeam):
        raise FHIRDeserializationError(f"Expected CareTeam, got {type(resource).__name__}")
    return resource


def deserialize_goal(json_data: Union[str, Dict[str, Any]], use_pydantic_validation: bool = True) -> Goal:
    """Deserialize Goal from JSON"""
    resource = deserialize_care_provision_resource(json_data, use_pydantic_validation)
    if not isinstance(resource, Goal):
        raise FHIRDeserializationError(f"Expected Goal, got {type(resource).__name__}")
    return resource


def deserialize_service_request(json_data: Union[str, Dict[str, Any]], use_pydantic_validation: bool = True) -> ServiceRequest:
    """Deserialize ServiceRequest from JSON"""
    resource = deserialize_care_provision_resource(json_data, use_pydantic_validation)
    if not isinstance(resource, ServiceRequest):
        raise FHIRDeserializationError(f"Expected ServiceRequest, got {type(resource).__name__}")
    return resource


def deserialize_nutrition_order(json_data: Union[str, Dict[str, Any]], use_pydantic_validation: bool = True) -> NutritionOrder:
    """Deserialize NutritionOrder from JSON"""
    resource = deserialize_care_provision_resource(json_data, use_pydantic_validation)
    if not isinstance(resource, NutritionOrder):
        raise FHIRDeserializationError(f"Expected NutritionOrder, got {type(resource).__name__}")
    return resource


def deserialize_risk_assessment(json_data: Union[str, Dict[str, Any]], use_pydantic_validation: bool = True) -> RiskAssessment:
    """Deserialize RiskAssessment from JSON"""
    resource = deserialize_care_provision_resource(json_data, use_pydantic_validation)
    if not isinstance(resource, RiskAssessment):
        raise FHIRDeserializationError(f"Expected RiskAssessment, got {type(resource).__name__}")
    return resource


def deserialize_vision_prescription(json_data: Union[str, Dict[str, Any]], use_pydantic_validation: bool = True) -> VisionPrescription:
    """Deserialize VisionPrescription from JSON"""
    resource = deserialize_care_provision_resource(json_data, use_pydantic_validation)
    if not isinstance(resource, VisionPrescription):
        raise FHIRDeserializationError(f"Expected VisionPrescription, got {type(resource).__name__}")
    return resource


# Export all public functions and classes
__all__ = [
    'FHIRDeserializationError',
    'FHIRCareProvisionDeserializer',
    'deserialize_care_provision_resource',
    'deserialize_care_plan',
    'deserialize_care_team',
    'deserialize_goal',
    'deserialize_service_request',
    'deserialize_nutrition_order',
    'deserialize_risk_assessment',
    'deserialize_vision_prescription'
]