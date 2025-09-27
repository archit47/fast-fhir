#!/usr/bin/env python3

"""
Demonstration of Fast-FHIR Care Provision resource deserializers
Shows how to convert JSON strings to FHIR resource objects with validation
"""

import sys
import os
import json

# Add the src directory to the path so we can import fast_fhir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fast_fhir.deserializers import (
    FHIRCareProvisionDeserializer, FHIRDeserializationError,
    deserialize_care_plan, deserialize_care_team, deserialize_goal,
    deserialize_service_request, deserialize_nutrition_order,
    deserialize_risk_assessment, deserialize_vision_prescription,
    PYDANTIC_AVAILABLE
)

# Use the new PYDANTIC_AVAILABLE flag
HAS_PYDANTIC = PYDANTIC_AVAILABLE


def demo_care_plan_deserialization():
    """Demonstrate CarePlan JSON deserialization"""
    print("=== CarePlan Deserialization Demo ===")
    
    care_plan_json = {
        "resourceType": "CarePlan",
        "id": "careplan-diabetes-001",
        "status": "active",
        "intent": "plan",
        "title": "Comprehensive Diabetes Management Plan",
        "description": "A comprehensive care plan for managing Type 2 diabetes",
        "subject": {
            "reference": "Patient/patient-123",
            "display": "John Doe"
        },
        "period": {
            "start": "2024-01-01",
            "end": "2024-12-31"
        },
        "created": "2024-01-01T09:00:00Z",
        "author": {
            "reference": "Practitioner/prac-001",
            "display": "Dr. Smith"
        },
        "category": [
            {
                "text": "Diabetes Management"
            }
        ],
        "goal": [
            {
                "reference": "Goal/goal-hba1c",
                "display": "HbA1c < 7%"
            }
        ],
        "activity": [
            {
                "detail": {
                    "status": "in-progress",
                    "code": {
                        "text": "Blood glucose monitoring"
                    },
                    "description": "Monitor blood glucose levels twice daily"
                }
            },
            {
                "detail": {
                    "status": "scheduled",
                    "code": {
                        "text": "Medication review"
                    },
                    "description": "Review diabetes medications monthly"
                }
            }
        ],
        "note": [
            {
                "text": "Patient is motivated and compliant with treatment plan",
                "time": "2024-01-01T09:00:00Z"
            }
        ]
    }
    
    try:
        # Deserialize using convenience function
        care_plan = deserialize_care_plan(care_plan_json)
        
        print(f"✅ Successfully deserialized CarePlan:")
        print(f"   ID: {care_plan.id}")
        print(f"   Title: {care_plan.title.value if care_plan.title else 'N/A'}")
        print(f"   Status: {care_plan.status.value}")
        print(f"   Intent: {care_plan.intent.value}")
        print(f"   Subject: {care_plan.subject.display.value if care_plan.subject.display else care_plan.subject.reference.value}")
        print(f"   Activities: {len(care_plan.activity)}")
        print(f"   Is Active: {care_plan.is_active()}")
        print(f"   Valid: {care_plan.validate()}")
        
        # Show activity details
        for i, activity in enumerate(care_plan.activity):
            if activity.detail:
                print(f"   Activity {i+1}: {activity.detail.code.text.value if activity.detail.code else 'N/A'} ({activity.detail.status})")
        
    except FHIRDeserializationError as e:
        print(f"❌ Deserialization failed: {e}")
    
    print()


def demo_care_team_deserialization():
    """Demonstrate CareTeam JSON deserialization"""
    print("=== CareTeam Deserialization Demo ===")
    
    care_team_json = {
        "resourceType": "CareTeam",
        "id": "careteam-diabetes-001",
        "status": "active",
        "name": "John's Diabetes Care Team",
        "subject": {
            "reference": "Patient/patient-123",
            "display": "John Doe"
        },
        "period": {
            "start": "2024-01-01"
        },
        "category": [
            {
                "text": "Diabetes Care"
            }
        ],
        "participant": [
            {
                "role": [
                    {
                        "text": "Primary Care Physician"
                    }
                ],
                "member": {
                    "reference": "Practitioner/prac-001",
                    "display": "Dr. Smith"
                },
                "coveragePeriod": {
                    "start": "2024-01-01"
                }
            },
            {
                "role": [
                    {
                        "text": "Endocrinologist"
                    }
                ],
                "member": {
                    "reference": "Practitioner/prac-002",
                    "display": "Dr. Johnson"
                }
            },
            {
                "role": [
                    {
                        "text": "Diabetes Educator"
                    }
                ],
                "member": {
                    "reference": "Practitioner/prac-003",
                    "display": "Sarah Wilson, RN"
                }
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": "+1-555-0123",
                "use": "work"
            }
        ]
    }
    
    try:
        care_team = deserialize_care_team(care_team_json)
        
        print(f"✅ Successfully deserialized CareTeam:")
        print(f"   ID: {care_team.id}")
        print(f"   Name: {care_team.name.value if care_team.name else 'N/A'}")
        print(f"   Status: {care_team.status.value}")
        print(f"   Subject: {care_team.subject.display.value if care_team.subject.display else care_team.subject.reference.value}")
        print(f"   Participants: {len(care_team.participant)}")
        print(f"   Is Active: {care_team.is_active()}")
        print(f"   Valid: {care_team.validate()}")
        
        # Show participant details
        for i, participant in enumerate(care_team.participant):
            role = participant.role[0].text.value if participant.role and participant.role[0].text else "Unknown Role"
            member = participant.member.display.value if participant.member.display else participant.member.reference.value
            print(f"   Participant {i+1}: {member} ({role})")
        
    except FHIRDeserializationError as e:
        print(f"❌ Deserialization failed: {e}")
    
    print()


def demo_goal_deserialization():
    """Demonstrate Goal JSON deserialization"""
    print("=== Goal Deserialization Demo ===")
    
    goal_json = {
        "resourceType": "Goal",
        "id": "goal-hba1c-001",
        "lifecycleStatus": "active",
        "achievementStatus": {
            "text": "In Progress"
        },
        "category": [
            {
                "text": "Diabetes Management"
            }
        ],
        "priority": {
            "text": "High"
        },
        "description": {
            "text": "Maintain HbA1c level below 7%"
        },
        "subject": {
            "reference": "Patient/patient-123",
            "display": "John Doe"
        },
        "startDate": "2024-01-01",
        "target": [
            {
                "measure": {
                    "text": "Hemoglobin A1c level"
                },
                "detailQuantity": {
                    "value": 7.0,
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
                },
                "dueDate": "2024-06-01"
            }
        ],
        "statusDate": "2024-01-01",
        "expressedBy": {
            "reference": "Practitioner/prac-001",
            "display": "Dr. Smith"
        },
        "addresses": [
            {
                "reference": "Condition/diabetes-type2",
                "display": "Type 2 Diabetes Mellitus"
            }
        ],
        "note": [
            {
                "text": "Patient committed to lifestyle changes and medication adherence",
                "time": "2024-01-01T09:00:00Z"
            }
        ]
    }
    
    try:
        goal = deserialize_goal(goal_json)
        
        print(f"✅ Successfully deserialized Goal:")
        print(f"   ID: {goal.id}")
        print(f"   Description: {goal.description.text.value}")
        print(f"   Lifecycle Status: {goal.lifecycle_status.value}")
        print(f"   Subject: {goal.subject.display.value if goal.subject.display else goal.subject.reference.value}")
        print(f"   Start Date: {goal.start_date if goal.start_date else 'N/A'}")
        print(f"   Targets: {len(goal.target)}")
        print(f"   Is Active: {goal.is_active()}")
        print(f"   Is Achieved: {goal.is_achieved()}")
        print(f"   Valid: {goal.validate()}")
        
        # Show target details
        for i, target in enumerate(goal.target):
            measure = target.measure.text.value if target.measure and target.measure.text else "Unknown Measure"
            value = f"{target.detail_quantity.value} {target.detail_quantity.unit}" if target.detail_quantity else "N/A"
            due = target.due_date if target.due_date else "N/A"
            print(f"   Target {i+1}: {measure} = {value} (Due: {due})")
        
    except FHIRDeserializationError as e:
        print(f"❌ Deserialization failed: {e}")
    
    print()


def demo_service_request_deserialization():
    """Demonstrate ServiceRequest JSON deserialization"""
    print("=== ServiceRequest Deserialization Demo ===")
    
    service_request_json = {
        "resourceType": "ServiceRequest",
        "id": "servicerequest-hba1c-001",
        "status": "active",
        "intent": "order",
        "priority": "routine",
        "category": [
            {
                "text": "Laboratory"
            }
        ],
        "code": {
            "text": "Hemoglobin A1c measurement"
        },
        "subject": {
            "reference": "Patient/patient-123",
            "display": "John Doe"
        },
        "encounter": {
            "reference": "Encounter/encounter-001"
        },
        "occurrenceDateTime": "2024-02-01T09:00:00Z",
        "authoredOn": "2024-01-15T14:30:00Z",
        "requester": {
            "reference": "Practitioner/prac-001",
            "display": "Dr. Smith"
        },
        "performer": [
            {
                "reference": "Organization/lab-001",
                "display": "City Lab Services"
            }
        ],
        "reasonCode": [
            {
                "text": "Diabetes monitoring"
            }
        ],
        "reasonReference": [
            {
                "reference": "Condition/diabetes-type2",
                "display": "Type 2 Diabetes Mellitus"
            }
        ],
        "note": [
            {
                "text": "Fasting sample preferred",
                "time": "2024-01-15T14:30:00Z"
            }
        ],
        "patientInstruction": "Please fast for 8 hours before the test"
    }
    
    try:
        service_request = deserialize_service_request(service_request_json)
        
        print(f"✅ Successfully deserialized ServiceRequest:")
        print(f"   ID: {service_request.id}")
        print(f"   Code: {service_request.code.text.value if service_request.code else 'N/A'}")
        print(f"   Status: {service_request.status.value}")
        print(f"   Intent: {service_request.intent.value}")
        print(f"   Priority: {service_request.priority.value}")
        print(f"   Subject: {service_request.subject.display.value if service_request.subject.display else service_request.subject.reference.value}")
        print(f"   Requester: {service_request.requester.display.value if service_request.requester and service_request.requester.display else 'N/A'}")
        print(f"   Is Active: {service_request.is_active()}")
        print(f"   Is Urgent: {service_request.is_urgent()}")
        print(f"   Valid: {service_request.validate()}")
        print(f"   Patient Instructions: {service_request.patient_instruction.value if service_request.patient_instruction else 'None'}")
        
    except FHIRDeserializationError as e:
        print(f"❌ Deserialization failed: {e}")
    
    print()


def demo_risk_assessment_deserialization():
    """Demonstrate RiskAssessment JSON deserialization"""
    print("=== RiskAssessment Deserialization Demo ===")
    
    risk_assessment_json = {
        "resourceType": "RiskAssessment",
        "id": "riskassessment-diabetes-complications",
        "status": "final",
        "method": {
            "text": "UKPDS Risk Engine"
        },
        "code": {
            "text": "Diabetes complications risk assessment"
        },
        "subject": {
            "reference": "Patient/patient-123",
            "display": "John Doe"
        },
        "encounter": {
            "reference": "Encounter/encounter-001"
        },
        "occurrenceDateTime": "2024-01-15T10:00:00Z",
        "performer": {
            "reference": "Practitioner/prac-001",
            "display": "Dr. Smith"
        },
        "basis": [
            {
                "reference": "Observation/hba1c-latest",
                "display": "Latest HbA1c result"
            },
            {
                "reference": "Observation/blood-pressure-latest",
                "display": "Latest blood pressure"
            }
        ],
        "prediction": [
            {
                "outcome": {
                    "text": "Diabetic retinopathy"
                },
                "probabilityDecimal": 0.25,
                "qualitativeRisk": {
                    "text": "Moderate risk"
                },
                "whenPeriod": {
                    "start": "2024-01-15",
                    "end": "2034-01-15"
                },
                "rationale": "Based on current HbA1c level of 8.2% and 5-year diabetes duration"
            },
            {
                "outcome": {
                    "text": "Diabetic nephropathy"
                },
                "probabilityDecimal": 0.15,
                "qualitativeRisk": {
                    "text": "Low-moderate risk"
                },
                "rationale": "Normal kidney function currently, but elevated HbA1c increases risk"
            },
            {
                "outcome": {
                    "text": "Cardiovascular disease"
                },
                "probabilityDecimal": 0.35,
                "qualitativeRisk": {
                    "text": "High risk"
                },
                "rationale": "Multiple risk factors: diabetes, hypertension, elevated cholesterol"
            }
        ],
        "mitigation": "Improve glycemic control, blood pressure management, and lipid control",
        "note": [
            {
                "text": "Risk assessment based on current clinical parameters. Regular monitoring recommended.",
                "time": "2024-01-15T10:00:00Z"
            }
        ]
    }
    
    try:
        risk_assessment = deserialize_risk_assessment(risk_assessment_json)
        
        print(f"✅ Successfully deserialized RiskAssessment:")
        print(f"   ID: {risk_assessment.id}")
        print(f"   Code: {risk_assessment.code.text.value if risk_assessment.code else 'N/A'}")
        print(f"   Status: {risk_assessment.status.value}")
        print(f"   Subject: {risk_assessment.subject.display.value if risk_assessment.subject.display else risk_assessment.subject.reference.value}")
        print(f"   Performer: {risk_assessment.performer.display.value if risk_assessment.performer and risk_assessment.performer.display else 'N/A'}")
        print(f"   Predictions: {len(risk_assessment.prediction)}")
        print(f"   Is Active: {risk_assessment.is_active()}")
        print(f"   Is High Risk (>20%): {risk_assessment.is_high_risk(0.2)}")
        print(f"   Valid: {risk_assessment.validate()}")
        print(f"   Mitigation: {risk_assessment.mitigation.value if risk_assessment.mitigation else 'None specified'}")
        
        # Show prediction details
        for i, prediction in enumerate(risk_assessment.prediction):
            outcome = prediction.outcome.text.value if prediction.outcome and prediction.outcome.text else "Unknown"
            probability = f"{prediction.probability_decimal.value * 100:.1f}%" if prediction.probability_decimal else "N/A"
            risk_level = prediction.qualitative_risk.text.value if prediction.qualitative_risk and prediction.qualitative_risk.text else "N/A"
            print(f"   Prediction {i+1}: {outcome} - {probability} ({risk_level})")
        
        # Show highest risk prediction
        highest = risk_assessment.get_highest_risk_prediction()
        if highest:
            outcome = highest.outcome.text.value if highest.outcome and highest.outcome.text else "Unknown"
            probability = f"{highest.probability_decimal.value * 100:.1f}%" if highest.probability_decimal else "N/A"
            print(f"   Highest Risk: {outcome} at {probability}")
        
    except FHIRDeserializationError as e:
        print(f"❌ Deserialization failed: {e}")
    
    print()


def demo_vision_prescription_deserialization():
    """Demonstrate VisionPrescription JSON deserialization"""
    print("=== VisionPrescription Deserialization Demo ===")
    
    vision_prescription_json = {
        "resourceType": "VisionPrescription",
        "id": "visionprescription-001",
        "status": "active",
        "created": "2024-01-15T14:30:00Z",
        "patient": {
            "reference": "Patient/patient-456",
            "display": "Jane Smith"
        },
        "encounter": {
            "reference": "Encounter/encounter-002"
        },
        "dateWritten": "2024-01-15T14:30:00Z",
        "prescriber": {
            "reference": "Practitioner/prac-ophthalmologist",
            "display": "Dr. Wilson, Ophthalmologist"
        },
        "lensSpecification": [
            {
                "product": {
                    "text": "Eyeglasses"
                },
                "eye": "right",
                "sphere": -2.5,
                "cylinder": -0.5,
                "axis": 90,
                "add": 1.5,
                "prism": [
                    {
                        "amount": 0.5,
                        "base": "in"
                    }
                ]
            },
            {
                "product": {
                    "text": "Eyeglasses"
                },
                "eye": "left",
                "sphere": -2.0,
                "cylinder": -0.25,
                "axis": 85,
                "add": 1.5
            }
        ]
    }
    
    try:
        vision_prescription = deserialize_vision_prescription(vision_prescription_json)
        
        print(f"✅ Successfully deserialized VisionPrescription:")
        print(f"   ID: {vision_prescription.id}")
        print(f"   Status: {vision_prescription.status.value}")
        print(f"   Patient: {vision_prescription.patient.display.value if vision_prescription.patient.display else vision_prescription.patient.reference.value}")
        print(f"   Prescriber: {vision_prescription.prescriber.display.value if vision_prescription.prescriber.display else vision_prescription.prescriber.reference.value}")
        print(f"   Created: {vision_prescription.created.value if vision_prescription.created else 'N/A'}")
        print(f"   Lens Specifications: {len(vision_prescription.lens_specification)}")
        print(f"   Is Active: {vision_prescription.is_active()}")
        print(f"   Valid: {vision_prescription.validate()}")
        
        # Show lens specification details
        for i, lens_spec in enumerate(vision_prescription.lens_specification):
            eye = lens_spec.eye.value if lens_spec.eye else "Unknown"
            sphere = lens_spec.sphere.value if lens_spec.sphere else "N/A"
            cylinder = lens_spec.cylinder.value if lens_spec.cylinder else "N/A"
            axis = lens_spec.axis.value if lens_spec.axis else "N/A"
            add = lens_spec.add.value if lens_spec.add else "N/A"
            print(f"   {eye.title()} Eye: Sphere {sphere}, Cylinder {cylinder}, Axis {axis}°, Add {add}")
            
            if lens_spec.prism:
                for j, prism in enumerate(lens_spec.prism):
                    amount = prism.amount.value if prism.amount else "N/A"
                    base = prism.base.value if prism.base else "N/A"
                    print(f"     Prism {j+1}: {amount} {base}")
        
    except FHIRDeserializationError as e:
        print(f"❌ Deserialization failed: {e}")
    
    print()


def demo_error_handling():
    """Demonstrate error handling in deserialization"""
    print("=== Error Handling Demo ===")
    
    # Test missing resourceType
    print("1. Testing missing resourceType:")
    try:
        deserializer = FHIRCareProvisionDeserializer()
        deserializer.deserialize({"id": "test-123"})
    except FHIRDeserializationError as e:
        print(f"   ✅ Caught expected error: {e}")
    
    # Test unsupported resource type
    print("2. Testing unsupported resource type:")
    try:
        deserializer = FHIRCareProvisionDeserializer()
        deserializer.deserialize({"resourceType": "UnsupportedResource", "id": "test-123"})
    except FHIRDeserializationError as e:
        print(f"   ✅ Caught expected error: {e}")
    
    # Test invalid JSON
    print("3. Testing invalid JSON string:")
    try:
        deserializer = FHIRCareProvisionDeserializer()
        deserializer.deserialize('{"resourceType": "CarePlan", "id": "test-123"')  # Missing closing brace
    except FHIRDeserializationError as e:
        print(f"   ✅ Caught expected error: {e}")
    
    # Test type mismatch in convenience function
    print("4. Testing type mismatch in convenience function:")
    try:
        deserialize_care_plan({
            "resourceType": "Goal",  # Wrong type
            "id": "wrong-type",
            "lifecycleStatus": "active",
            "description": {"text": "Test"},
            "subject": {"reference": "Patient/patient-123"}
        })
    except FHIRDeserializationError as e:
        print(f"   ✅ Caught expected error: {e}")
    
    print()


def demo_json_string_deserialization():
    """Demonstrate deserialization from JSON strings"""
    print("=== JSON String Deserialization Demo ===")
    
    nutrition_order_json_str = json.dumps({
        "resourceType": "NutritionOrder",
        "id": "nutritionorder-json-string",
        "status": "active",
        "intent": "order",
        "subject": {
            "reference": "Patient/patient-123",
            "display": "John Doe"
        },
        "orderer": {
            "reference": "Practitioner/prac-001",
            "display": "Dr. Smith"
        },
        "dateTime": "2024-01-15T09:00:00Z",
        "priority": {
            "text": "Routine"
        },
        "foodPreferenceModifier": [
            {
                "text": "Vegetarian"
            }
        ],
        "excludeFoodModifier": [
            {
                "text": "Nuts"
            }
        ],
        "outsideFoodAllowed": False,
        "note": [
            {
                "text": "Patient has nut allergy - ensure all meals are nut-free",
                "time": "2024-01-15T09:00:00Z"
            }
        ]
    })
    
    try:
        nutrition_order = deserialize_nutrition_order(nutrition_order_json_str)
        
        print(f"✅ Successfully deserialized NutritionOrder from JSON string:")
        print(f"   ID: {nutrition_order.id}")
        print(f"   Status: {nutrition_order.status.value}")
        print(f"   Intent: {nutrition_order.intent.value}")
        print(f"   Subject: {nutrition_order.subject.display.value if nutrition_order.subject.display else nutrition_order.subject.reference.value}")
        print(f"   Orderer: {nutrition_order.orderer.display.value if nutrition_order.orderer and nutrition_order.orderer.display else 'N/A'}")
        print(f"   Outside Food Allowed: {nutrition_order.outside_food_allowed.value if nutrition_order.outside_food_allowed else 'N/A'}")
        print(f"   Is Active: {nutrition_order.is_active()}")
        print(f"   Valid: {nutrition_order.validate()}")
        
    except FHIRDeserializationError as e:
        print(f"❌ Deserialization failed: {e}")
    
    print()


def main():
    """Run all demonstrations"""
    print("Fast-FHIR Care Provision Resource Deserializers Demonstration")
    print("=" * 65)
    print(f"Pydantic Available: {HAS_PYDANTIC}")
    print()
    
    demo_care_plan_deserialization()
    demo_care_team_deserialization()
    demo_goal_deserialization()
    demo_service_request_deserialization()
    demo_risk_assessment_deserialization()
    demo_vision_prescription_deserialization()
    demo_json_string_deserialization()
    demo_error_handling()
    
    print("All deserializer demonstrations completed successfully!")
    print()
    print("Key Features Demonstrated:")
    print("• JSON to FHIR resource object conversion")
    print("• Pydantic validation (when available)")
    print("• Type-specific convenience functions")
    print("• Comprehensive error handling")
    print("• Support for both JSON strings and dictionaries")
    print("• Full FHIR R5 Care Provision resource coverage")


if __name__ == "__main__":
    main()