#!/usr/bin/env python3

"""
Test suite for FHIR R5 Care Provision resource deserializers
"""

import unittest
import json
from datetime import datetime

from src.fhir.deserializers import (
    FHIRCareProvisionDeserializer, FHIRDeserializationError,
    deserialize_care_provision_resource,
    deserialize_care_plan, deserialize_care_team, deserialize_goal,
    deserialize_service_request, deserialize_nutrition_order,
    deserialize_risk_assessment, deserialize_vision_prescription
)

from src.fhir.resources.care_plan import CarePlan, CarePlanStatus, CarePlanIntent
from src.fhir.resources.care_team import CareTeam, CareTeamStatus
from src.fhir.resources.goal import Goal, GoalLifecycleStatus
from src.fhir.resources.service_request import ServiceRequest, ServiceRequestStatus, ServiceRequestIntent, ServiceRequestPriority
from src.fhir.resources.nutrition_order import NutritionOrder, NutritionOrderStatus, NutritionOrderIntent
from src.fhir.resources.risk_assessment import RiskAssessment, RiskAssessmentStatus
from src.fhir.resources.vision_prescription import VisionPrescription, VisionPrescriptionStatus, VisionEye


class TestFHIRCareProvisionDeserializer(unittest.TestCase):
    """Test FHIR Care Provision deserializer"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_deserializer_initialization(self):
        """Test deserializer initialization"""
        deserializer = FHIRCareProvisionDeserializer(use_pydantic_validation=True)
        self.assertIsInstance(deserializer, FHIRCareProvisionDeserializer)
        
        deserializer_no_pydantic = FHIRCareProvisionDeserializer(use_pydantic_validation=False)
        self.assertIsInstance(deserializer_no_pydantic, FHIRCareProvisionDeserializer)
    
    def test_missing_resource_type(self):
        """Test error handling for missing resourceType"""
        invalid_data = {"id": "test-123"}
        
        with self.assertRaises(FHIRDeserializationError) as context:
            self.deserializer.deserialize(invalid_data)
        
        self.assertIn("Missing resourceType", str(context.exception))
    
    def test_unsupported_resource_type(self):
        """Test error handling for unsupported resource type"""
        invalid_data = {"resourceType": "UnsupportedResource", "id": "test-123"}
        
        with self.assertRaises(FHIRDeserializationError) as context:
            self.deserializer.deserialize(invalid_data)
        
        self.assertIn("Unsupported resource type", str(context.exception))
    
    def test_invalid_json(self):
        """Test error handling for invalid JSON"""
        invalid_json = '{"resourceType": "CarePlan", "id": "test-123"'  # Missing closing brace
        
        with self.assertRaises(FHIRDeserializationError) as context:
            self.deserializer.deserialize(invalid_json)
        
        self.assertIn("Invalid JSON", str(context.exception))


class TestCarePlanDeserialization(unittest.TestCase):
    """Test CarePlan deserialization"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_basic_care_plan_deserialization(self):
        """Test basic CarePlan deserialization"""
        care_plan_json = {
            "resourceType": "CarePlan",
            "id": "careplan-123",
            "status": "active",
            "intent": "plan",
            "title": "Diabetes Management Plan",
            "description": "Comprehensive diabetes care plan",
            "subject": {
                "reference": "Patient/patient-123",
                "display": "John Doe"
            }
        }
        
        care_plan = self.deserializer.deserialize(care_plan_json)
        
        self.assertIsInstance(care_plan, CarePlan)
        self.assertEqual(care_plan.id, "careplan-123")
        self.assertEqual(care_plan.status, CarePlanStatus.ACTIVE)
        self.assertEqual(care_plan.intent, CarePlanIntent.PLAN)
        self.assertEqual(care_plan.title.value, "Diabetes Management Plan")
        self.assertEqual(care_plan.description.value, "Comprehensive diabetes care plan")
        self.assertEqual(care_plan.subject.reference.value, "Patient/patient-123")
        self.assertEqual(care_plan.subject.display.value, "John Doe")
        self.assertTrue(care_plan.validate())
    
    def test_care_plan_with_activities(self):
        """Test CarePlan deserialization with activities"""
        care_plan_json = {
            "resourceType": "CarePlan",
            "id": "careplan-456",
            "status": "active",
            "intent": "plan",
            "subject": {
                "reference": "Patient/patient-456"
            },
            "activity": [
                {
                    "detail": {
                        "status": "in-progress",
                        "code": {
                            "text": "Blood glucose monitoring"
                        },
                        "description": "Monitor blood glucose daily"
                    }
                }
            ]
        }
        
        care_plan = self.deserializer.deserialize(care_plan_json)
        
        self.assertIsInstance(care_plan, CarePlan)
        self.assertEqual(len(care_plan.activity), 1)
        self.assertEqual(care_plan.activity[0].detail.status, "in-progress")
        self.assertEqual(care_plan.activity[0].detail.description.value, "Monitor blood glucose daily")
    
    def test_care_plan_convenience_function(self):
        """Test CarePlan convenience deserialization function"""
        care_plan_json = {
            "resourceType": "CarePlan",
            "id": "careplan-789",
            "status": "draft",
            "intent": "proposal",
            "subject": {
                "reference": "Patient/patient-789"
            }
        }
        
        care_plan = deserialize_care_plan(care_plan_json)
        
        self.assertIsInstance(care_plan, CarePlan)
        self.assertEqual(care_plan.id, "careplan-789")
        self.assertEqual(care_plan.status, CarePlanStatus.DRAFT)
        self.assertEqual(care_plan.intent, CarePlanIntent.PROPOSAL)


class TestCareTeamDeserialization(unittest.TestCase):
    """Test CareTeam deserialization"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_basic_care_team_deserialization(self):
        """Test basic CareTeam deserialization"""
        care_team_json = {
            "resourceType": "CareTeam",
            "id": "careteam-123",
            "status": "active",
            "name": "Diabetes Care Team",
            "subject": {
                "reference": "Patient/patient-123",
                "display": "John Doe"
            }
        }
        
        care_team = self.deserializer.deserialize(care_team_json)
        
        self.assertIsInstance(care_team, CareTeam)
        self.assertEqual(care_team.id, "careteam-123")
        self.assertEqual(care_team.status, CareTeamStatus.ACTIVE)
        self.assertEqual(care_team.name.value, "Diabetes Care Team")
        self.assertEqual(care_team.subject.reference.value, "Patient/patient-123")
        self.assertTrue(care_team.validate())
    
    def test_care_team_with_participants(self):
        """Test CareTeam deserialization with participants"""
        care_team_json = {
            "resourceType": "CareTeam",
            "id": "careteam-456",
            "status": "active",
            "subject": {
                "reference": "Patient/patient-456"
            },
            "participant": [
                {
                    "member": {
                        "reference": "Practitioner/prac-001",
                        "display": "Dr. Smith"
                    },
                    "role": [
                        {
                            "text": "Primary Care Physician"
                        }
                    ]
                },
                {
                    "member": {
                        "reference": "Practitioner/prac-002",
                        "display": "Dr. Johnson"
                    }
                }
            ]
        }
        
        care_team = self.deserializer.deserialize(care_team_json)
        
        self.assertIsInstance(care_team, CareTeam)
        self.assertEqual(len(care_team.participant), 2)
        self.assertEqual(care_team.participant[0].member.reference.value, "Practitioner/prac-001")
        self.assertEqual(care_team.participant[0].member.display.value, "Dr. Smith")


class TestGoalDeserialization(unittest.TestCase):
    """Test Goal deserialization"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_basic_goal_deserialization(self):
        """Test basic Goal deserialization"""
        goal_json = {
            "resourceType": "Goal",
            "id": "goal-123",
            "lifecycleStatus": "active",
            "description": {
                "text": "Maintain HbA1c below 7%"
            },
            "subject": {
                "reference": "Patient/patient-123",
                "display": "John Doe"
            }
        }
        
        goal = self.deserializer.deserialize(goal_json)
        
        self.assertIsInstance(goal, Goal)
        self.assertEqual(goal.id, "goal-123")
        self.assertEqual(goal.lifecycle_status, GoalLifecycleStatus.ACTIVE)
        self.assertEqual(goal.description.text.value, "Maintain HbA1c below 7%")
        self.assertEqual(goal.subject.reference.value, "Patient/patient-123")
        self.assertTrue(goal.validate())
    
    def test_goal_with_targets(self):
        """Test Goal deserialization with targets"""
        goal_json = {
            "resourceType": "Goal",
            "id": "goal-456",
            "lifecycleStatus": "active",
            "description": {
                "text": "Weight loss goal"
            },
            "subject": {
                "reference": "Patient/patient-456"
            },
            "target": [
                {
                    "measure": {
                        "text": "Body weight"
                    },
                    "detailQuantity": {
                        "value": 70,
                        "unit": "kg"
                    },
                    "dueDate": "2024-12-31"
                }
            ]
        }
        
        goal = self.deserializer.deserialize(goal_json)
        
        self.assertIsInstance(goal, Goal)
        self.assertEqual(len(goal.target), 1)
        self.assertEqual(goal.target[0].measure.text.value, "Body weight")
        self.assertEqual(goal.target[0].detail_quantity.value, 70)
        self.assertEqual(goal.target[0].detail_quantity.unit, "kg")
        self.assertEqual(goal.target[0].due_date, "2024-12-31")


class TestServiceRequestDeserialization(unittest.TestCase):
    """Test ServiceRequest deserialization"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_basic_service_request_deserialization(self):
        """Test basic ServiceRequest deserialization"""
        service_request_json = {
            "resourceType": "ServiceRequest",
            "id": "servicerequest-123",
            "status": "active",
            "intent": "order",
            "priority": "routine",
            "code": {
                "text": "HbA1c test"
            },
            "subject": {
                "reference": "Patient/patient-123",
                "display": "John Doe"
            }
        }
        
        service_request = self.deserializer.deserialize(service_request_json)
        
        self.assertIsInstance(service_request, ServiceRequest)
        self.assertEqual(service_request.id, "servicerequest-123")
        self.assertEqual(service_request.status, ServiceRequestStatus.ACTIVE)
        self.assertEqual(service_request.intent, ServiceRequestIntent.ORDER)
        self.assertEqual(service_request.priority, ServiceRequestPriority.ROUTINE)
        self.assertEqual(service_request.code.text.value, "HbA1c test")
        self.assertEqual(service_request.subject.reference.value, "Patient/patient-123")
        self.assertTrue(service_request.validate())
    
    def test_urgent_service_request(self):
        """Test urgent ServiceRequest deserialization"""
        service_request_json = {
            "resourceType": "ServiceRequest",
            "id": "servicerequest-urgent",
            "status": "active",
            "intent": "order",
            "priority": "urgent",
            "code": {
                "text": "Emergency glucose check"
            },
            "subject": {
                "reference": "Patient/patient-123"
            },
            "authoredOn": "2024-01-15T10:30:00Z"
        }
        
        service_request = self.deserializer.deserialize(service_request_json)
        
        self.assertIsInstance(service_request, ServiceRequest)
        self.assertEqual(service_request.priority, ServiceRequestPriority.URGENT)
        self.assertTrue(service_request.is_urgent())
        self.assertEqual(service_request.authored_on.value, "2024-01-15T10:30:00Z")


class TestRiskAssessmentDeserialization(unittest.TestCase):
    """Test RiskAssessment deserialization"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_basic_risk_assessment_deserialization(self):
        """Test basic RiskAssessment deserialization"""
        risk_assessment_json = {
            "resourceType": "RiskAssessment",
            "id": "riskassessment-123",
            "status": "final",
            "code": {
                "text": "Diabetes complications risk"
            },
            "subject": {
                "reference": "Patient/patient-123",
                "display": "John Doe"
            }
        }
        
        risk_assessment = self.deserializer.deserialize(risk_assessment_json)
        
        self.assertIsInstance(risk_assessment, RiskAssessment)
        self.assertEqual(risk_assessment.id, "riskassessment-123")
        self.assertEqual(risk_assessment.status, RiskAssessmentStatus.FINAL)
        self.assertEqual(risk_assessment.code.text.value, "Diabetes complications risk")
        self.assertEqual(risk_assessment.subject.reference.value, "Patient/patient-123")
        self.assertTrue(risk_assessment.validate())
    
    def test_risk_assessment_with_predictions(self):
        """Test RiskAssessment deserialization with predictions"""
        risk_assessment_json = {
            "resourceType": "RiskAssessment",
            "id": "riskassessment-456",
            "status": "final",
            "subject": {
                "reference": "Patient/patient-456"
            },
            "prediction": [
                {
                    "outcome": {
                        "text": "Diabetic retinopathy"
                    },
                    "probabilityDecimal": 0.25,
                    "rationale": "Based on current HbA1c levels"
                },
                {
                    "outcome": {
                        "text": "Diabetic nephropathy"
                    },
                    "probabilityDecimal": 0.15
                }
            ]
        }
        
        risk_assessment = self.deserializer.deserialize(risk_assessment_json)
        
        self.assertIsInstance(risk_assessment, RiskAssessment)
        self.assertEqual(len(risk_assessment.prediction), 2)
        self.assertEqual(risk_assessment.prediction[0].outcome.text.value, "Diabetic retinopathy")
        self.assertEqual(risk_assessment.prediction[0].probability_decimal.value, 0.25)
        self.assertEqual(risk_assessment.prediction[0].rationale.value, "Based on current HbA1c levels")
        self.assertTrue(risk_assessment.is_high_risk(0.2))


class TestVisionPrescriptionDeserialization(unittest.TestCase):
    """Test VisionPrescription deserialization"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_basic_vision_prescription_deserialization(self):
        """Test basic VisionPrescription deserialization"""
        vision_prescription_json = {
            "resourceType": "VisionPrescription",
            "id": "visionprescription-123",
            "status": "active",
            "created": "2024-01-15T10:30:00Z",
            "patient": {
                "reference": "Patient/patient-123",
                "display": "Jane Smith"
            },
            "prescriber": {
                "reference": "Practitioner/prac-003",
                "display": "Dr. Wilson"
            },
            "lensSpecification": [
                {
                    "eye": "right",
                    "sphere": -2.5,
                    "cylinder": -0.5,
                    "axis": 90
                }
            ]
        }
        
        vision_prescription = self.deserializer.deserialize(vision_prescription_json)
        
        self.assertIsInstance(vision_prescription, VisionPrescription)
        self.assertEqual(vision_prescription.id, "visionprescription-123")
        self.assertEqual(vision_prescription.status, VisionPrescriptionStatus.ACTIVE)
        self.assertEqual(vision_prescription.created.value, "2024-01-15T10:30:00Z")
        self.assertEqual(vision_prescription.patient.reference.value, "Patient/patient-123")
        self.assertEqual(vision_prescription.prescriber.reference.value, "Practitioner/prac-003")
        self.assertEqual(len(vision_prescription.lens_specification), 1)
        self.assertEqual(vision_prescription.lens_specification[0].eye, VisionEye.RIGHT)
        self.assertEqual(vision_prescription.lens_specification[0].sphere.value, -2.5)
        self.assertTrue(vision_prescription.validate())
    
    def test_vision_prescription_both_eyes(self):
        """Test VisionPrescription deserialization with both eyes"""
        vision_prescription_json = {
            "resourceType": "VisionPrescription",
            "id": "visionprescription-456",
            "status": "active",
            "patient": {
                "reference": "Patient/patient-456"
            },
            "prescriber": {
                "reference": "Practitioner/prac-003"
            },
            "lensSpecification": [
                {
                    "eye": "right",
                    "sphere": -2.5,
                    "cylinder": -0.5,
                    "axis": 90
                },
                {
                    "eye": "left",
                    "sphere": -2.0,
                    "cylinder": -0.25,
                    "axis": 85
                }
            ]
        }
        
        vision_prescription = self.deserializer.deserialize(vision_prescription_json)
        
        self.assertIsInstance(vision_prescription, VisionPrescription)
        self.assertEqual(len(vision_prescription.lens_specification), 2)
        
        right_lens = vision_prescription.get_lens_for_eye(VisionEye.RIGHT)
        left_lens = vision_prescription.get_lens_for_eye(VisionEye.LEFT)
        
        self.assertIsNotNone(right_lens)
        self.assertIsNotNone(left_lens)
        self.assertEqual(right_lens.sphere.value, -2.5)
        self.assertEqual(left_lens.sphere.value, -2.0)


class TestNutritionOrderDeserialization(unittest.TestCase):
    """Test NutritionOrder deserialization"""
    
    def setUp(self):
        self.deserializer = FHIRCareProvisionDeserializer()
    
    def test_basic_nutrition_order_deserialization(self):
        """Test basic NutritionOrder deserialization"""
        nutrition_order_json = {
            "resourceType": "NutritionOrder",
            "id": "nutritionorder-123",
            "status": "active",
            "intent": "order",
            "subject": {
                "reference": "Patient/patient-123",
                "display": "John Doe"
            },
            "orderer": {
                "reference": "Practitioner/prac-001",
                "display": "Dr. Smith"
            }
        }
        
        nutrition_order = self.deserializer.deserialize(nutrition_order_json)
        
        self.assertIsInstance(nutrition_order, NutritionOrder)
        self.assertEqual(nutrition_order.id, "nutritionorder-123")
        self.assertEqual(nutrition_order.status, NutritionOrderStatus.ACTIVE)
        self.assertEqual(nutrition_order.intent, NutritionOrderIntent.ORDER)
        self.assertEqual(nutrition_order.subject.reference.value, "Patient/patient-123")
        self.assertEqual(nutrition_order.orderer.reference.value, "Practitioner/prac-001")
        self.assertTrue(nutrition_order.validate())


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience deserialization functions"""
    
    def test_deserialize_care_provision_resource(self):
        """Test generic care provision resource deserialization"""
        care_plan_json = {
            "resourceType": "CarePlan",
            "id": "careplan-generic",
            "status": "active",
            "intent": "plan",
            "subject": {"reference": "Patient/patient-123"}
        }
        
        resource = deserialize_care_provision_resource(care_plan_json)
        self.assertIsInstance(resource, CarePlan)
        
        goal_json = {
            "resourceType": "Goal",
            "id": "goal-generic",
            "lifecycleStatus": "active",
            "description": {"text": "Test goal"},
            "subject": {"reference": "Patient/patient-123"}
        }
        
        resource = deserialize_care_provision_resource(goal_json)
        self.assertIsInstance(resource, Goal)
    
    def test_type_specific_convenience_functions(self):
        """Test type-specific convenience functions"""
        # Test each convenience function
        care_team_json = {
            "resourceType": "CareTeam",
            "id": "careteam-conv",
            "status": "active",
            "subject": {"reference": "Patient/patient-123"}
        }
        
        care_team = deserialize_care_team(care_team_json)
        self.assertIsInstance(care_team, CareTeam)
        
        # Test type validation
        with self.assertRaises(FHIRDeserializationError):
            deserialize_care_team({
                "resourceType": "Goal",  # Wrong type
                "id": "wrong-type",
                "lifecycleStatus": "active",
                "description": {"text": "Test"},
                "subject": {"reference": "Patient/patient-123"}
            })


class TestJSONStringDeserialization(unittest.TestCase):
    """Test deserialization from JSON strings"""
    
    def test_json_string_deserialization(self):
        """Test deserialization from JSON string"""
        care_plan_json_str = json.dumps({
            "resourceType": "CarePlan",
            "id": "careplan-json-str",
            "status": "active",
            "intent": "plan",
            "subject": {"reference": "Patient/patient-123"}
        })
        
        care_plan = deserialize_care_plan(care_plan_json_str)
        self.assertIsInstance(care_plan, CarePlan)
        self.assertEqual(care_plan.id, "careplan-json-str")


if __name__ == '__main__':
    unittest.main()