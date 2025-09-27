#!/usr/bin/env python3
"""
Demo script for FHIR R5 Foundation Resource Deserializers

This script demonstrates how to use the foundation deserializers to convert
JSON FHIR resources (Patient, Practitioner, Encounter, etc.) to Python objects.
"""

import sys
import os
import json
from datetime import datetime, date

# Add the src directory to the path so we can import fast_fhir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from fast_fhir.deserializers import (
        FHIRFoundationDeserializer,
        deserialize_patient,
        deserialize_practitioner,
        deserialize_practitioner_role,
        deserialize_encounter,
        deserialize_person,
        deserialize_related_person,
        PYDANTIC_FOUNDATION_AVAILABLE
    )
    print("✅ Successfully imported foundation deserializers")
except ImportError as e:
    print(f"❌ Failed to import foundation deserializers: {e}")
    sys.exit(1)

def demo_patient_deserialization():
    """Demonstrate Patient resource deserialization"""
    print("\n🏥 Patient Resource Deserialization Demo")
    print("=" * 50)
    
    # Sample Patient JSON
    patient_json = {
        "resourceType": "Patient",
        "id": "example-patient",
        "identifier": [
            {
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR"
                        }
                    ]
                },
                "system": "urn:oid:1.2.36.146.595.217.0.1",
                "value": "12345"
            }
        ],
        "active": True,
        "name": [
            {
                "use": "official",
                "family": "Doe",
                "given": ["John", "Michael"],
                "prefix": ["Mr."]
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": "+1-555-123-4567",
                "use": "home"
            },
            {
                "system": "email",
                "value": "john.doe@example.com",
                "use": "home"
            }
        ],
        "gender": "male",
        "birthDate": "1980-05-15",
        "address": [
            {
                "use": "home",
                "type": "both",
                "text": "123 Main St, Anytown, ST 12345",
                "line": ["123 Main St"],
                "city": "Anytown",
                "state": "ST",
                "postalCode": "12345",
                "country": "US"
            }
        ],
        "maritalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                    "code": "M",
                    "display": "Married"
                }
            ]
        }
    }
    
    try:
        # Deserialize using convenience function
        patient = deserialize_patient(patient_json)
        print(f"✅ Patient deserialized successfully")
        print(f"   ID: {getattr(patient, 'id', 'N/A')}")
        print(f"   Resource Type: {getattr(patient, 'resourceType', 'N/A')}")
        print(f"   Active: {getattr(patient, 'active', 'N/A')}")
        print(f"   Gender: {getattr(patient, 'gender', 'N/A')}")
        print(f"   Birth Date: {getattr(patient, 'birthDate', 'N/A')}")
        
        # Test with Pydantic validation disabled
        patient_no_validation = deserialize_patient(patient_json, use_pydantic_validation=False)
        print(f"✅ Patient deserialized without Pydantic validation")
        
    except Exception as e:
        print(f"❌ Patient deserialization failed: {e}")

def demo_practitioner_deserialization():
    """Demonstrate Practitioner resource deserialization"""
    print("\n👨‍⚕️ Practitioner Resource Deserialization Demo")
    print("=" * 55)
    
    # Sample Practitioner JSON
    practitioner_json = {
        "resourceType": "Practitioner",
        "id": "example-practitioner",
        "identifier": [
            {
                "use": "official",
                "system": "http://www.acme.org/practitioners",
                "value": "23"
            }
        ],
        "active": True,
        "name": [
            {
                "use": "official",
                "family": "Smith",
                "given": ["Jane", "Elizabeth"],
                "prefix": ["Dr."],
                "suffix": ["MD"]
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": "+1-555-987-6543",
                "use": "work"
            }
        ],
        "address": [
            {
                "use": "work",
                "line": ["456 Medical Center Dr"],
                "city": "Healthcare City",
                "state": "HC",
                "postalCode": "54321"
            }
        ],
        "gender": "female",
        "birthDate": "1975-03-20",
        "qualification": [
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0360/2.7",
                            "code": "MD",
                            "display": "Doctor of Medicine"
                        }
                    ]
                },
                "period": {
                    "start": "2000-06-15"
                },
                "issuer": {
                    "display": "Medical University"
                }
            }
        ]
    }
    
    try:
        practitioner = deserialize_practitioner(practitioner_json)
        print(f"✅ Practitioner deserialized successfully")
        print(f"   ID: {getattr(practitioner, 'id', 'N/A')}")
        print(f"   Active: {getattr(practitioner, 'active', 'N/A')}")
        print(f"   Gender: {getattr(practitioner, 'gender', 'N/A')}")
        print(f"   Birth Date: {getattr(practitioner, 'birthDate', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Practitioner deserialization failed: {e}")

def demo_encounter_deserialization():
    """Demonstrate Encounter resource deserialization"""
    print("\n🏥 Encounter Resource Deserialization Demo")
    print("=" * 50)
    
    # Sample Encounter JSON
    encounter_json = {
        "resourceType": "Encounter",
        "id": "example-encounter",
        "identifier": [
            {
                "use": "official",
                "system": "http://www.amc.nl/zorgportal/identifiers/visits",
                "value": "v1451"
            }
        ],
        "status": "completed",
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": "AMB",
            "display": "ambulatory"
        },
        "type": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "270427003",
                        "display": "Patient-initiated encounter"
                    }
                ]
            }
        ],
        "subject": {
            "reference": "Patient/example-patient",
            "display": "John Doe"
        },
        "participant": [
            {
                "type": [
                    {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                "code": "ATND",
                                "display": "attender"
                            }
                        ]
                    }
                ],
                "individual": {
                    "reference": "Practitioner/example-practitioner",
                    "display": "Dr. Jane Smith"
                }
            }
        ],
        "period": {
            "start": "2023-01-15T09:00:00Z",
            "end": "2023-01-15T10:30:00Z"
        },
        "reasonCode": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "25064002",
                        "display": "Headache"
                    }
                ]
            }
        ]
    }
    
    try:
        encounter = deserialize_encounter(encounter_json)
        print(f"✅ Encounter deserialized successfully")
        print(f"   ID: {getattr(encounter, 'id', 'N/A')}")
        print(f"   Status: {getattr(encounter, 'status', 'N/A')}")
        print(f"   Subject: {getattr(encounter, 'subject', {}).get('display', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Encounter deserialization failed: {e}")

def demo_foundation_deserializer_class():
    """Demonstrate using the FHIRFoundationDeserializer class directly"""
    print("\n🔧 Foundation Deserializer Class Demo")
    print("=" * 45)
    
    # Create deserializer instance
    deserializer = FHIRFoundationDeserializer(use_pydantic_validation=True)
    
    # Sample resources
    resources = [
        {
            "resourceType": "Person",
            "id": "example-person",
            "identifier": [
                {
                    "use": "usual",
                    "system": "urn:oid:2.16.840.1.113883.2.4.6.3",
                    "value": "738472983"
                }
            ],
            "name": [
                {
                    "use": "official",
                    "family": "Johnson",
                    "given": ["Robert"]
                }
            ],
            "gender": "male",
            "birthDate": "1985-12-10",
            "active": True
        },
        {
            "resourceType": "RelatedPerson",
            "id": "example-related-person",
            "identifier": [
                {
                    "use": "usual",
                    "system": "urn:oid:2.16.840.1.113883.2.4.6.3",
                    "value": "444222222"
                }
            ],
            "active": True,
            "patient": {
                "reference": "Patient/example-patient"
            },
            "relationship": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                            "code": "WIFE",
                            "display": "wife"
                        }
                    ]
                }
            ],
            "name": [
                {
                    "use": "official",
                    "family": "Doe",
                    "given": ["Mary"]
                }
            ],
            "gender": "female"
        }
    ]
    
    for resource_data in resources:
        try:
            resource = deserializer.deserialize_foundation_resource(resource_data)
            resource_type = resource_data['resourceType']
            print(f"✅ {resource_type} deserialized successfully")
            print(f"   ID: {getattr(resource, 'id', 'N/A')}")
            print(f"   Active: {getattr(resource, 'active', 'N/A')}")
            
        except Exception as e:
            print(f"❌ {resource_data['resourceType']} deserialization failed: {e}")

def demo_error_handling():
    """Demonstrate error handling in deserialization"""
    print("\n⚠️  Error Handling Demo")
    print("=" * 30)
    
    # Test invalid JSON
    try:
        deserialize_patient("invalid json")
    except Exception as e:
        print(f"✅ Caught invalid JSON error: {type(e).__name__}")
    
    # Test missing resourceType
    try:
        deserialize_patient({"id": "test"})
    except Exception as e:
        print(f"✅ Caught missing resourceType error: {type(e).__name__}")
    
    # Test unsupported resource type
    try:
        deserializer = FHIRFoundationDeserializer()
        deserializer.deserialize_foundation_resource({"resourceType": "UnsupportedResource"})
    except Exception as e:
        print(f"✅ Caught unsupported resource error: {type(e).__name__}")

def main():
    """Main demo function"""
    print("🚀 FHIR R5 Foundation Deserializers Demo")
    print("=" * 45)
    
    print(f"📦 Pydantic Foundation Available: {PYDANTIC_FOUNDATION_AVAILABLE}")
    
    # Run all demos
    demo_patient_deserialization()
    demo_practitioner_deserialization()
    demo_encounter_deserialization()
    demo_foundation_deserializer_class()
    demo_error_handling()
    
    print("\n🎉 Foundation deserializers demo completed!")
    print("\n📋 Summary:")
    print("   ✅ Patient deserialization")
    print("   ✅ Practitioner deserialization")
    print("   ✅ Encounter deserialization")
    print("   ✅ Person and RelatedPerson deserialization")
    print("   ✅ Error handling")
    print("\n💡 The foundation deserializers support:")
    print("   - Patient, Practitioner, PractitionerRole")
    print("   - Encounter, Person, RelatedPerson")
    print("   - Pydantic validation (optional)")
    print("   - Comprehensive error handling")
    print("   - Both JSON strings and dictionaries")

if __name__ == "__main__":
    main()