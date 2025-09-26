#!/usr/bin/env python3

"""
Demonstration of FHIR R5 Care Provision resources
"""

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from src.fhir.resources.care_plan import CarePlan, CarePlanStatus, CarePlanIntent, CarePlanActivity
from src.fhir.resources.care_team import CareTeam, CareTeamStatus, CareTeamParticipant
from src.fhir.resources.goal import Goal, GoalLifecycleStatus, GoalTarget
from src.fhir.resources.service_request import ServiceRequest, ServiceRequestStatus, ServiceRequestIntent, ServiceRequestPriority
from src.fhir.resources.nutrition_order import NutritionOrder, NutritionOrderStatus, NutritionOrderIntent
from src.fhir.resources.risk_assessment import RiskAssessment, RiskAssessmentStatus, RiskAssessmentPrediction
from src.fhir.resources.vision_prescription import VisionPrescription, VisionPrescriptionStatus, VisionEye, VisionPrescriptionLensSpecification

from src.fhir.datatypes import (
    FHIRString, FHIRReference, FHIRCodeableConcept, FHIRDateTime, 
    FHIRDecimal, FHIRBoolean, FHIRInteger
)

def demo_care_plan():
    """Demonstrate CarePlan resource"""
    print("=== CarePlan Demo ===")
    
    # Create a care plan
    care_plan = CarePlan(id="careplan-diabetes-001")
    care_plan.status = CarePlanStatus.ACTIVE
    care_plan.intent = CarePlanIntent.PLAN
    care_plan.title = FHIRString("Diabetes Management Plan")
    care_plan.description = FHIRString("Comprehensive diabetes care plan for patient")
    
    # Set subject (patient)
    care_plan.subject = FHIRReference()
    care_plan.subject.reference = FHIRString("Patient/patient-123")
    care_plan.subject.display = FHIRString("John Doe")
    
    # Add activity
    activity = CarePlanActivity()
    care_plan.add_activity(activity)
    
    print(f"Created CarePlan: {care_plan.get_display_name()}")
    print(f"Status: {care_plan.status.value}")
    print(f"Is Active: {care_plan.is_active()}")
    print(f"Activities: {len(care_plan.activity)}")
    print(f"Valid: {care_plan.validate()}")
    print()

def demo_care_team():
    """Demonstrate CareTeam resource"""
    print("=== CareTeam Demo ===")
    
    # Create a care team
    care_team = CareTeam(id="careteam-diabetes-001")
    care_team.status = CareTeamStatus.ACTIVE
    care_team.name = FHIRString("Diabetes Care Team")
    
    # Set subject (patient)
    care_team.subject = FHIRReference()
    care_team.subject.reference = FHIRString("Patient/patient-123")
    care_team.subject.display = FHIRString("John Doe")
    
    # Add participants
    # Primary care physician
    pcp = CareTeamParticipant()
    pcp.member = FHIRReference()
    pcp.member.reference = FHIRString("Practitioner/prac-001")
    pcp.member.display = FHIRString("Dr. Smith")
    care_team.add_participant(pcp)
    
    # Endocrinologist
    endo = CareTeamParticipant()
    endo.member = FHIRReference()
    endo.member.reference = FHIRString("Practitioner/prac-002")
    endo.member.display = FHIRString("Dr. Johnson")
    care_team.add_participant(endo)
    
    print(f"Created CareTeam: {care_team.get_display_name()}")
    print(f"Status: {care_team.status.value}")
    print(f"Is Active: {care_team.is_active()}")
    print(f"Participants: {len(care_team.participant)}")
    print(f"Valid: {care_team.validate()}")
    print()

def demo_goal():
    """Demonstrate Goal resource"""
    print("=== Goal Demo ===")
    
    # Create a goal
    goal = Goal(id="goal-hba1c-001")
    goal.lifecycle_status = GoalLifecycleStatus.ACTIVE
    
    # Set description
    goal.description = FHIRCodeableConcept()
    goal.description.text = FHIRString("Maintain HbA1c below 7%")
    
    # Set subject (patient)
    goal.subject = FHIRReference()
    goal.subject.reference = FHIRString("Patient/patient-123")
    goal.subject.display = FHIRString("John Doe")
    
    # Add target
    target = GoalTarget()
    target.measure = FHIRCodeableConcept()
    target.measure.text = FHIRString("HbA1c level")
    goal.add_target(target)
    
    print(f"Created Goal: {goal.get_display_name()}")
    print(f"Status: {goal.lifecycle_status.value}")
    print(f"Is Active: {goal.is_active()}")
    print(f"Is Achieved: {goal.is_achieved()}")
    print(f"Targets: {len(goal.target)}")
    print(f"Valid: {goal.validate()}")
    print()

def demo_service_request():
    """Demonstrate ServiceRequest resource"""
    print("=== ServiceRequest Demo ===")
    
    # Create a service request
    service_request = ServiceRequest(id="servicerequest-lab-001")
    service_request.status = ServiceRequestStatus.ACTIVE
    service_request.intent = ServiceRequestIntent.ORDER
    service_request.priority = ServiceRequestPriority.ROUTINE
    
    # Set code
    service_request.code = FHIRCodeableConcept()
    service_request.code.text = FHIRString("HbA1c test")
    
    # Set subject (patient)
    service_request.subject = FHIRReference()
    service_request.subject.reference = FHIRString("Patient/patient-123")
    service_request.subject.display = FHIRString("John Doe")
    
    print(f"Created ServiceRequest: {service_request.get_display_name()}")
    print(f"Status: {service_request.status.value}")
    print(f"Priority: {service_request.priority.value}")
    print(f"Is Active: {service_request.is_active()}")
    print(f"Is Urgent: {service_request.is_urgent()}")
    print(f"Valid: {service_request.validate()}")
    print()

def demo_risk_assessment():
    """Demonstrate RiskAssessment resource"""
    print("=== RiskAssessment Demo ===")
    
    # Create a risk assessment
    risk_assessment = RiskAssessment(id="riskassessment-diabetes-001")
    risk_assessment.status = RiskAssessmentStatus.FINAL
    
    # Set code
    risk_assessment.code = FHIRCodeableConcept()
    risk_assessment.code.text = FHIRString("Diabetes complications risk")
    
    # Set subject (patient)
    risk_assessment.subject = FHIRReference()
    risk_assessment.subject.reference = FHIRString("Patient/patient-123")
    risk_assessment.subject.display = FHIRString("John Doe")
    
    # Add prediction
    prediction = RiskAssessmentPrediction()
    prediction.outcome = FHIRCodeableConcept()
    prediction.outcome.text = FHIRString("Diabetic retinopathy")
    prediction.probability_decimal = FHIRDecimal(0.25)  # 25% risk
    risk_assessment.add_prediction(prediction)
    
    print(f"Created RiskAssessment: {risk_assessment.get_display_name()}")
    print(f"Status: {risk_assessment.status.value}")
    print(f"Is Active: {risk_assessment.is_active()}")
    print(f"Predictions: {len(risk_assessment.prediction)}")
    print(f"Is High Risk (>20%): {risk_assessment.is_high_risk(0.2)}")
    print(f"Valid: {risk_assessment.validate()}")
    print()

def demo_vision_prescription():
    """Demonstrate VisionPrescription resource"""
    print("=== VisionPrescription Demo ===")
    
    # Create a vision prescription
    vision_prescription = VisionPrescription(id="visionprescription-001")
    vision_prescription.status = VisionPrescriptionStatus.ACTIVE
    vision_prescription.created = FHIRDateTime("2024-01-15T10:30:00Z")
    
    # Set patient
    vision_prescription.patient = FHIRReference()
    vision_prescription.patient.reference = FHIRString("Patient/patient-456")
    vision_prescription.patient.display = FHIRString("Jane Smith")
    
    # Set prescriber
    vision_prescription.prescriber = FHIRReference()
    vision_prescription.prescriber.reference = FHIRString("Practitioner/prac-003")
    vision_prescription.prescriber.display = FHIRString("Dr. Wilson")
    
    # Add lens specifications
    # Right eye
    right_lens = VisionPrescriptionLensSpecification()
    right_lens.eye = VisionEye.RIGHT
    right_lens.sphere = FHIRDecimal(-2.5)
    right_lens.cylinder = FHIRDecimal(-0.5)
    right_lens.axis = FHIRInteger(90)
    vision_prescription.add_lens_specification(right_lens)
    
    # Left eye
    left_lens = VisionPrescriptionLensSpecification()
    left_lens.eye = VisionEye.LEFT
    left_lens.sphere = FHIRDecimal(-2.0)
    left_lens.cylinder = FHIRDecimal(-0.25)
    left_lens.axis = FHIRInteger(85)
    vision_prescription.add_lens_specification(left_lens)
    
    print(f"Created VisionPrescription: {vision_prescription.get_display_name()}")
    print(f"Status: {vision_prescription.status.value}")
    print(f"Is Active: {vision_prescription.is_active()}")
    print(f"Lens Specifications: {len(vision_prescription.lens_specification)}")
    print(f"Valid: {vision_prescription.validate()}")
    print()

def demo_nutrition_order():
    """Demonstrate NutritionOrder resource"""
    print("=== NutritionOrder Demo ===")
    
    # Create a nutrition order
    nutrition_order = NutritionOrder(id="nutritionorder-001")
    nutrition_order.status = NutritionOrderStatus.ACTIVE
    nutrition_order.intent = NutritionOrderIntent.ORDER
    
    # Set subject (patient)
    nutrition_order.subject = FHIRReference()
    nutrition_order.subject.reference = FHIRString("Patient/patient-123")
    nutrition_order.subject.display = FHIRString("John Doe")
    
    # Set orderer
    nutrition_order.orderer = FHIRReference()
    nutrition_order.orderer.reference = FHIRString("Practitioner/prac-001")
    nutrition_order.orderer.display = FHIRString("Dr. Smith")
    
    print(f"Created NutritionOrder: {nutrition_order.get_display_name()}")
    print(f"Status: {nutrition_order.status.value}")
    print(f"Intent: {nutrition_order.intent.value}")
    print(f"Is Active: {nutrition_order.is_active()}")
    print(f"Valid: {nutrition_order.validate()}")
    print()

def main():
    """Run all demonstrations"""
    print("FHIR R5 Care Provision Resources Demonstration")
    print("=" * 50)
    print()
    
    demo_care_plan()
    demo_care_team()
    demo_goal()
    demo_service_request()
    demo_risk_assessment()
    demo_vision_prescription()
    demo_nutrition_order()
    
    print("All Care Provision resources demonstrated successfully!")

if __name__ == "__main__":
    main()