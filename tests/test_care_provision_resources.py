#!/usr/bin/env python3

"""
Test suite for FHIR R5 Care Provision resources Python implementation
"""

import unittest
import json
from datetime import datetime

from src.fhir.resources.care_plan import CarePlan, CarePlanStatus, CarePlanIntent, CarePlanActivity
from src.fhir.resources.care_team import CareTeam, CareTeamStatus, CareTeamParticipant
from src.fhir.resources.goal import Goal, GoalLifecycleStatus, GoalTarget
from src.fhir.resources.service_request import ServiceRequest, ServiceRequestStatus, ServiceRequestIntent, ServiceRequestPriority
from src.fhir.resources.nutrition_order import NutritionOrder, NutritionOrderStatus, NutritionOrderIntent
from src.fhir.resources.risk_assessment import RiskAssessment, RiskAssessmentStatus, RiskAssessmentPrediction
from src.fhir.resources.vision_prescription import VisionPrescription, VisionPrescriptionStatus, VisionEye, VisionPrescriptionLensSpecification

from src.fhir.datatypes import (
    FHIRString, FHIRReference, FHIRCodeableConcept, FHIRDateTime, 
    FHIRPeriod, FHIRDecimal, FHIRBoolean, FHIRInteger
)


class TestCarePlan(unittest.TestCase):
    """Test CarePlan resource"""
    
    def setUp(self):
        self.care_plan = CarePlan(id="careplan-123")
    
    def test_creation(self):
        """Test CarePlan creation and default values"""
        self.assertEqual(self.care_plan.id, "careplan-123")
        self.assertEqual(self.care_plan.resource_type, "CarePlan")
        self.assertEqual(self.care_plan.status, CarePlanStatus.DRAFT)
        self.assertEqual(self.care_plan.intent, CarePlanIntent.PLAN)
        self.assertFalse(self.care_plan.is_active())
    
    def test_status_management(self):
        """Test CarePlan status management"""
        self.care_plan.status = CarePlanStatus.ACTIVE
        self.assertTrue(self.care_plan.is_active())
        
        self.care_plan.status = CarePlanStatus.COMPLETED
        self.assertFalse(self.care_plan.is_active())
    
    def test_activity_management(self):
        """Test CarePlan activity management"""
        activity = CarePlanActivity()
        self.care_plan.add_activity(activity)
        self.assertEqual(len(self.care_plan.activity), 1)
    
    def test_validation(self):
        """Test CarePlan validation"""
        # Should fail without subject
        self.assertFalse(self.care_plan.validate())
        
        # Should pass with subject
        self.care_plan.subject = FHIRReference()
        self.care_plan.subject.reference = FHIRString("Patient/patient-123")
        self.assertTrue(self.care_plan.validate())
    
    def test_serialization(self):
        """Test CarePlan JSON serialization"""
        self.care_plan.title = FHIRString("Comprehensive Care Plan")
        self.care_plan.status = CarePlanStatus.ACTIVE
        self.care_plan.intent = CarePlanIntent.PLAN
        
        data = self.care_plan.to_dict()
        self.assertEqual(data['resourceType'], 'CarePlan')
        self.assertEqual(data['id'], 'careplan-123')
        self.assertEqual(data['status'], 'active')
        self.assertEqual(data['intent'], 'plan')
        self.assertEqual(data['title'], 'Comprehensive Care Plan')
    
    def test_deserialization(self):
        """Test CarePlan JSON deserialization"""
        data = {
            'id': 'careplan-456',
            'resourceType': 'CarePlan',
            'status': 'active',
            'intent': 'order',
            'title': 'Test Care Plan',
            'subject': {
                'reference': 'Patient/patient-456'
            }
        }
        
        care_plan = CarePlan.from_dict(data)
        self.assertEqual(care_plan.id, 'careplan-456')
        self.assertEqual(care_plan.status, CarePlanStatus.ACTIVE)
        self.assertEqual(care_plan.intent, CarePlanIntent.ORDER)
        self.assertEqual(care_plan.title.value, 'Test Care Plan')
        self.assertTrue(care_plan.is_active())


class TestCareTeam(unittest.TestCase):
    """Test CareTeam resource"""
    
    def setUp(self):
        self.care_team = CareTeam(id="careteam-123")
    
    def test_creation(self):
        """Test CareTeam creation and default values"""
        self.assertEqual(self.care_team.id, "careteam-123")
        self.assertEqual(self.care_team.resource_type, "CareTeam")
        self.assertEqual(self.care_team.status, CareTeamStatus.PROPOSED)
        self.assertFalse(self.care_team.is_active())
    
    def test_status_management(self):
        """Test CareTeam status management"""
        self.care_team.status = CareTeamStatus.ACTIVE
        self.assertTrue(self.care_team.is_active())
    
    def test_participant_management(self):
        """Test CareTeam participant management"""
        participant = CareTeamParticipant()
        participant.member = FHIRReference()
        participant.member.reference = FHIRString("Practitioner/prac-123")
        
        self.care_team.add_participant(participant)
        self.assertEqual(len(self.care_team.participant), 1)


class TestGoal(unittest.TestCase):
    """Test Goal resource"""
    
    def setUp(self):
        self.goal = Goal(id="goal-123")
    
    def test_creation(self):
        """Test Goal creation and default values"""
        self.assertEqual(self.goal.id, "goal-123")
        self.assertEqual(self.goal.resource_type, "Goal")
        self.assertEqual(self.goal.lifecycle_status, GoalLifecycleStatus.PROPOSED)
        self.assertFalse(self.goal.is_active())
    
    def test_status_management(self):
        """Test Goal status management"""
        self.goal.lifecycle_status = GoalLifecycleStatus.ACTIVE
        self.assertTrue(self.goal.is_active())
        
        self.goal.lifecycle_status = GoalLifecycleStatus.COMPLETED
        self.assertFalse(self.goal.is_active())
        self.assertTrue(self.goal.is_achieved())
    
    def test_target_management(self):
        """Test Goal target management"""
        target = GoalTarget()
        target.measure = FHIRCodeableConcept()
        
        self.goal.add_target(target)
        self.assertEqual(len(self.goal.target), 1)
    
    def test_validation(self):
        """Test Goal validation"""
        # Should fail without subject and description
        self.assertFalse(self.goal.validate())
        
        # Should pass with subject and description
        self.goal.subject = FHIRReference()
        self.goal.subject.reference = FHIRString("Patient/patient-123")
        self.goal.description = FHIRCodeableConcept()
        self.assertTrue(self.goal.validate())


class TestServiceRequest(unittest.TestCase):
    """Test ServiceRequest resource"""
    
    def setUp(self):
        self.service_request = ServiceRequest(id="servicerequest-123")
    
    def test_creation(self):
        """Test ServiceRequest creation and default values"""
        self.assertEqual(self.service_request.id, "servicerequest-123")
        self.assertEqual(self.service_request.resource_type, "ServiceRequest")
        self.assertEqual(self.service_request.status, ServiceRequestStatus.DRAFT)
        self.assertEqual(self.service_request.intent, ServiceRequestIntent.PROPOSAL)
        self.assertEqual(self.service_request.priority, ServiceRequestPriority.ROUTINE)
        self.assertFalse(self.service_request.is_active())
        self.assertFalse(self.service_request.is_urgent())
    
    def test_status_management(self):
        """Test ServiceRequest status management"""
        self.service_request.status = ServiceRequestStatus.ACTIVE
        self.assertTrue(self.service_request.is_active())
    
    def test_priority_management(self):
        """Test ServiceRequest priority management"""
        self.service_request.priority = ServiceRequestPriority.URGENT
        self.assertTrue(self.service_request.is_urgent())
        
        self.service_request.priority = ServiceRequestPriority.STAT
        self.assertTrue(self.service_request.is_urgent())
        
        self.service_request.priority = ServiceRequestPriority.ROUTINE
        self.assertFalse(self.service_request.is_urgent())
    
    def test_validation(self):
        """Test ServiceRequest validation"""
        # Should fail without subject and code
        self.assertFalse(self.service_request.validate())
        
        # Should pass with subject and code
        self.service_request.subject = FHIRReference()
        self.service_request.subject.reference = FHIRString("Patient/patient-123")
        self.service_request.code = FHIRCodeableConcept()
        self.assertTrue(self.service_request.validate())


class TestNutritionOrder(unittest.TestCase):
    """Test NutritionOrder resource"""
    
    def setUp(self):
        self.nutrition_order = NutritionOrder(id="nutritionorder-123")
    
    def test_creation(self):
        """Test NutritionOrder creation and default values"""
        self.assertEqual(self.nutrition_order.id, "nutritionorder-123")
        self.assertEqual(self.nutrition_order.resource_type, "NutritionOrder")
        self.assertEqual(self.nutrition_order.status, NutritionOrderStatus.DRAFT)
        self.assertEqual(self.nutrition_order.intent, NutritionOrderIntent.PROPOSAL)
        self.assertFalse(self.nutrition_order.is_active())
    
    def test_status_management(self):
        """Test NutritionOrder status management"""
        self.nutrition_order.status = NutritionOrderStatus.ACTIVE
        self.assertTrue(self.nutrition_order.is_active())
    
    def test_validation(self):
        """Test NutritionOrder validation"""
        # Should fail without subject
        self.assertFalse(self.nutrition_order.validate())
        
        # Should pass with subject
        self.nutrition_order.subject = FHIRReference()
        self.nutrition_order.subject.reference = FHIRString("Patient/patient-123")
        self.assertTrue(self.nutrition_order.validate())


class TestRiskAssessment(unittest.TestCase):
    """Test RiskAssessment resource"""
    
    def setUp(self):
        self.risk_assessment = RiskAssessment(id="riskassessment-123")
    
    def test_creation(self):
        """Test RiskAssessment creation and default values"""
        self.assertEqual(self.risk_assessment.id, "riskassessment-123")
        self.assertEqual(self.risk_assessment.resource_type, "RiskAssessment")
        self.assertEqual(self.risk_assessment.status, RiskAssessmentStatus.REGISTERED)
        self.assertFalse(self.risk_assessment.is_active())
    
    def test_status_management(self):
        """Test RiskAssessment status management"""
        self.risk_assessment.status = RiskAssessmentStatus.FINAL
        self.assertTrue(self.risk_assessment.is_active())
    
    def test_prediction_management(self):
        """Test RiskAssessment prediction management"""
        prediction = RiskAssessmentPrediction()
        prediction.probability_decimal = FHIRDecimal(0.75)
        
        self.risk_assessment.add_prediction(prediction)
        self.assertEqual(len(self.risk_assessment.prediction), 1)
        
        # Test high risk detection
        self.assertTrue(self.risk_assessment.is_high_risk(0.7))
        self.assertFalse(self.risk_assessment.is_high_risk(0.8))
        
        # Test highest risk prediction
        highest = self.risk_assessment.get_highest_risk_prediction()
        self.assertIsNotNone(highest)
        self.assertEqual(highest.get_probability_value(), 0.75)
    
    def test_validation(self):
        """Test RiskAssessment validation"""
        # Should fail without subject
        self.assertFalse(self.risk_assessment.validate())
        
        # Should pass with subject
        self.risk_assessment.subject = FHIRReference()
        self.risk_assessment.subject.reference = FHIRString("Patient/patient-123")
        self.assertTrue(self.risk_assessment.validate())


class TestVisionPrescription(unittest.TestCase):
    """Test VisionPrescription resource"""
    
    def setUp(self):
        self.vision_prescription = VisionPrescription(id="visionprescription-123")
    
    def test_creation(self):
        """Test VisionPrescription creation and default values"""
        self.assertEqual(self.vision_prescription.id, "visionprescription-123")
        self.assertEqual(self.vision_prescription.resource_type, "VisionPrescription")
        self.assertEqual(self.vision_prescription.status, VisionPrescriptionStatus.DRAFT)
        self.assertFalse(self.vision_prescription.is_active())
    
    def test_status_management(self):
        """Test VisionPrescription status management"""
        self.vision_prescription.status = VisionPrescriptionStatus.ACTIVE
        self.assertTrue(self.vision_prescription.is_active())
    
    def test_lens_specification_management(self):
        """Test VisionPrescription lens specification management"""
        # Create lens specification for right eye
        right_lens = VisionPrescriptionLensSpecification()
        right_lens.eye = VisionEye.RIGHT
        right_lens.sphere = FHIRDecimal(-2.5)
        right_lens.cylinder = FHIRDecimal(-0.5)
        right_lens.axis = FHIRInteger(90)
        
        # Create lens specification for left eye
        left_lens = VisionPrescriptionLensSpecification()
        left_lens.eye = VisionEye.LEFT
        left_lens.sphere = FHIRDecimal(-2.0)
        left_lens.cylinder = FHIRDecimal(-0.25)
        left_lens.axis = FHIRInteger(85)
        
        self.vision_prescription.add_lens_specification(right_lens)
        self.vision_prescription.add_lens_specification(left_lens)
        
        self.assertEqual(len(self.vision_prescription.lens_specification), 2)
        
        # Test getting lens for specific eye
        right_retrieved = self.vision_prescription.get_lens_for_eye(VisionEye.RIGHT)
        self.assertIsNotNone(right_retrieved)
        self.assertEqual(right_retrieved.sphere.value, -2.5)
        
        left_retrieved = self.vision_prescription.get_lens_for_eye(VisionEye.LEFT)
        self.assertIsNotNone(left_retrieved)
        self.assertEqual(left_retrieved.sphere.value, -2.0)
    
    def test_validation(self):
        """Test VisionPrescription validation"""
        # Should fail without patient, prescriber, and lens specifications
        self.assertFalse(self.vision_prescription.validate())
        
        # Add required fields
        self.vision_prescription.patient = FHIRReference()
        self.vision_prescription.patient.reference = FHIRString("Patient/patient-123")
        self.vision_prescription.prescriber = FHIRReference()
        self.vision_prescription.prescriber.reference = FHIRString("Practitioner/prac-123")
        
        # Still should fail without lens specifications
        self.assertFalse(self.vision_prescription.validate())
        
        # Add lens specification
        lens_spec = VisionPrescriptionLensSpecification()
        lens_spec.eye = VisionEye.RIGHT
        self.vision_prescription.add_lens_specification(lens_spec)
        
        # Now should pass
        self.assertTrue(self.vision_prescription.validate())


class TestCareProvisionIntegration(unittest.TestCase):
    """Test integration between Care Provision resources"""
    
    def test_care_plan_with_goals_and_activities(self):
        """Test CarePlan with associated Goals and Activities"""
        # Create a care plan
        care_plan = CarePlan(id="careplan-integration")
        care_plan.status = CarePlanStatus.ACTIVE
        care_plan.intent = CarePlanIntent.PLAN
        care_plan.title = FHIRString("Diabetes Management Plan")
        care_plan.subject = FHIRReference()
        care_plan.subject.reference = FHIRString("Patient/patient-123")
        
        # Create goals
        goal1 = Goal(id="goal-hba1c")
        goal1.lifecycle_status = GoalLifecycleStatus.ACTIVE
        goal1.description = FHIRCodeableConcept()
        goal1.description.text = FHIRString("Maintain HbA1c below 7%")
        goal1.subject = FHIRReference()
        goal1.subject.reference = FHIRString("Patient/patient-123")
        
        goal2 = Goal(id="goal-weight")
        goal2.lifecycle_status = GoalLifecycleStatus.ACTIVE
        goal2.description = FHIRCodeableConcept()
        goal2.description.text = FHIRString("Lose 10 pounds")
        goal2.subject = FHIRReference()
        goal2.subject.reference = FHIRString("Patient/patient-123")
        
        # Create activities
        activity1 = CarePlanActivity()
        activity1.detail = CarePlanActivity()  # Simplified for test
        
        activity2 = CarePlanActivity()
        activity2.detail = CarePlanActivity()  # Simplified for test
        
        care_plan.add_activity(activity1)
        care_plan.add_activity(activity2)
        
        # Verify integration
        self.assertTrue(care_plan.is_active())
        self.assertTrue(goal1.is_active())
        self.assertTrue(goal2.is_active())
        self.assertEqual(len(care_plan.activity), 2)
        
        # Test serialization
        care_plan_data = care_plan.to_dict()
        goal1_data = goal1.to_dict()
        goal2_data = goal2.to_dict()
        
        self.assertEqual(care_plan_data['resourceType'], 'CarePlan')
        self.assertEqual(goal1_data['resourceType'], 'Goal')
        self.assertEqual(goal2_data['resourceType'], 'Goal')
    
    def test_service_request_workflow(self):
        """Test ServiceRequest workflow with different priorities"""
        # Create routine service request
        routine_request = ServiceRequest(id="service-routine")
        routine_request.status = ServiceRequestStatus.ACTIVE
        routine_request.intent = ServiceRequestIntent.ORDER
        routine_request.priority = ServiceRequestPriority.ROUTINE
        routine_request.code = FHIRCodeableConcept()
        routine_request.code.text = FHIRString("Blood glucose monitoring")
        routine_request.subject = FHIRReference()
        routine_request.subject.reference = FHIRString("Patient/patient-123")
        
        # Create urgent service request
        urgent_request = ServiceRequest(id="service-urgent")
        urgent_request.status = ServiceRequestStatus.ACTIVE
        urgent_request.intent = ServiceRequestIntent.ORDER
        urgent_request.priority = ServiceRequestPriority.URGENT
        urgent_request.code = FHIRCodeableConcept()
        urgent_request.code.text = FHIRString("Emergency glucose check")
        urgent_request.subject = FHIRReference()
        urgent_request.subject.reference = FHIRString("Patient/patient-123")
        
        # Verify workflow
        self.assertTrue(routine_request.is_active())
        self.assertFalse(routine_request.is_urgent())
        
        self.assertTrue(urgent_request.is_active())
        self.assertTrue(urgent_request.is_urgent())
        
        # Test validation
        self.assertTrue(routine_request.validate())
        self.assertTrue(urgent_request.validate())


if __name__ == '__main__':
    unittest.main()