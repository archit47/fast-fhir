#!/usr/bin/env python3
"""
Demo script for FHIR R5 Entities Resource Deserializers

This script demonstrates how to use the entities deserializers to convert
JSON FHIR resources (Organization, Location, Device, etc.) to Python objects.
"""

import sys
import os
import json
from datetime import datetime, date

# Add the src directory to the path so we can import fast_fhir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from fast_fhir.deserializers import (
        FHIREntitiesDeserializer,
        deserialize_organization,
        deserialize_location,
        deserialize_healthcare_service,
        deserialize_endpoint,
        deserialize_device,
        deserialize_substance,
        deserialize_organization_affiliation,
        PYDANTIC_ENTITIES_AVAILABLE
    )
    print("✅ Successfully imported entities deserializers")
except ImportError as e:
    print(f"❌ Failed to import entities deserializers: {e}")
    sys.exit(1)

def demo_organization_deserialization():
    """Demonstrate Organization resource deserialization"""
    print("\n🏢 Organization Resource Deserialization Demo")
    print("=" * 55)
    
    # Sample Organization JSON
    organization_json = {
        "resourceType": "Organization",
        "id": "example-hospital",
        "identifier": [
            {
                "use": "official",
                "system": "http://www.acme.org/organization",
                "value": "HL7"
            }
        ],
        "active": True,
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                        "code": "prov",
                        "display": "Healthcare Provider"
                    }
                ]
            }
        ],
        "name": "Acme Healthcare System",
        "alias": ["Acme Hospital", "AHS"],
        "description": "A comprehensive healthcare system providing quality care",
        "telecom": [
            {
                "system": "phone",
                "value": "+1-555-HOSPITAL",
                "use": "work"
            },
            {
                "system": "email",
                "value": "info@acmehealthcare.org",
                "use": "work"
            }
        ],
        "address": [
            {
                "use": "work",
                "type": "both",
                "line": ["123 Healthcare Blvd"],
                "city": "Medical City",
                "state": "HC",
                "postalCode": "12345",
                "country": "US"
            }
        ],
        "contact": [
            {
                "purpose": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/contactentity-type",
                            "code": "ADMIN"
                        }
                    ]
                },
                "name": {
                    "use": "official",
                    "family": "Administrator",
                    "given": ["Chief"]
                },
                "telecom": [
                    {
                        "system": "phone",
                        "value": "+1-555-ADMIN"
                    }
                ]
            }
        ]
    }
    
    try:
        organization = deserialize_organization(organization_json)
        print(f"✅ Organization deserialized successfully")
        print(f"   ID: {getattr(organization, 'id', 'N/A')}")
        print(f"   Name: {getattr(organization, 'name', 'N/A')}")
        print(f"   Active: {getattr(organization, 'active', 'N/A')}")
        print(f"   Aliases: {getattr(organization, 'alias', [])}")
        
    except Exception as e:
        print(f"❌ Organization deserialization failed: {e}")

def demo_location_deserialization():
    """Demonstrate Location resource deserialization"""
    print("\n📍 Location Resource Deserialization Demo")
    print("=" * 50)
    
    # Sample Location JSON
    location_json = {
        "resourceType": "Location",
        "id": "example-location",
        "identifier": [
            {
                "use": "official",
                "system": "http://www.acme.org/location",
                "value": "B1-S.F2"
            }
        ],
        "status": "active",
        "name": "South Wing, second floor",
        "alias": ["BU MC, SW, F2", "Burgers University Medical Center, South Wing, 2nd floor"],
        "description": "Second floor of the Old South Wing, formerly in use by Psychiatry",
        "mode": "instance",
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                        "code": "HOSP",
                        "display": "Hospital"
                    }
                ]
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": "+1-555-SOUTH-WING",
                "use": "work"
            }
        ],
        "address": {
            "use": "work",
            "line": ["Galapagosweg 91, Building A"],
            "city": "Den Burg",
            "postalCode": "9105 PZ",
            "country": "NLD"
        },
        "physicalType": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                    "code": "wi",
                    "display": "Wing"
                }
            ]
        },
        "position": {
            "longitude": -83.6945691,
            "latitude": 42.25475478,
            "altitude": 0
        },
        "managingOrganization": {
            "reference": "Organization/example-hospital"
        },
        "hoursOfOperation": [
            {
                "daysOfWeek": ["mon", "tue", "wed", "thu", "fri"],
                "allDay": False,
                "openingTime": "08:30:00",
                "closingTime": "17:30:00"
            }
        ]
    }
    
    try:
        location = deserialize_location(location_json)
        print(f"✅ Location deserialized successfully")
        print(f"   ID: {getattr(location, 'id', 'N/A')}")
        print(f"   Name: {getattr(location, 'name', 'N/A')}")
        print(f"   Status: {getattr(location, 'status', 'N/A')}")
        print(f"   Mode: {getattr(location, 'mode', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Location deserialization failed: {e}")

def demo_healthcare_service_deserialization():
    """Demonstrate HealthcareService resource deserialization"""
    print("\n🏥 HealthcareService Resource Deserialization Demo")
    print("=" * 60)
    
    # Sample HealthcareService JSON
    healthcare_service_json = {
        "resourceType": "HealthcareService",
        "id": "example-service",
        "identifier": [
            {
                "system": "http://example.org/shared-ids",
                "value": "HS-12"
            }
        ],
        "active": True,
        "providedBy": {
            "reference": "Organization/example-hospital",
            "display": "Acme Healthcare System"
        },
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/service-category",
                        "code": "8",
                        "display": "Counselling"
                    }
                ],
                "text": "Counselling"
            }
        ],
        "type": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "394913002",
                        "display": "Psychotherapy"
                    }
                ]
            }
        ],
        "specialty": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "47505003",
                        "display": "Posttraumatic stress disorder"
                    }
                ]
            }
        ],
        "location": [
            {
                "reference": "Location/example-location"
            }
        ],
        "name": "Consulting psychologists and/or psychology services",
        "comment": "Providing Specialist psychology services to the greater Den Burg area",
        "telecom": [
            {
                "system": "phone",
                "value": "+1-555-PSYCH",
                "use": "work"
            }
        ],
        "appointmentRequired": True,
        "availableTime": [
            {
                "daysOfWeek": ["wed"],
                "allDay": False,
                "availableStartTime": "08:30:00",
                "availableEndTime": "05:30:00"
            },
            {
                "daysOfWeek": ["mon", "tue", "thu", "fri"],
                "allDay": False,
                "availableStartTime": "09:00:00",
                "availableEndTime": "16:30:00"
            }
        ],
        "notAvailable": [
            {
                "description": "Christmas/Boxing Day",
                "during": {
                    "start": "2015-12-25",
                    "end": "2015-12-26"
                }
            }
        ]
    }
    
    try:
        healthcare_service = deserialize_healthcare_service(healthcare_service_json)
        print(f"✅ HealthcareService deserialized successfully")
        print(f"   ID: {getattr(healthcare_service, 'id', 'N/A')}")
        print(f"   Name: {getattr(healthcare_service, 'name', 'N/A')}")
        print(f"   Active: {getattr(healthcare_service, 'active', 'N/A')}")
        print(f"   Appointment Required: {getattr(healthcare_service, 'appointment_required', 'N/A')}")
        
    except Exception as e:
        print(f"❌ HealthcareService deserialization failed: {e}")

def demo_device_deserialization():
    """Demonstrate Device resource deserialization"""
    print("\n🔧 Device Resource Deserialization Demo")
    print("=" * 45)
    
    # Sample Device JSON
    device_json = {
        "resourceType": "Device",
        "id": "example-device",
        "identifier": [
            {
                "system": "http://goodcare.org/devices/id",
                "value": "345675"
            }
        ],
        "definition": {
            "reference": "DeviceDefinition/example"
        },
        "udiCarrier": [
            {
                "deviceIdentifier": "09504000059118",
                "issuer": "http://hl7.org/fhir/NamingSystem/fda-udi",
                "jurisdiction": "http://hl7.org/fhir/NamingSystem/fda-udi",
                "carrierHRF": "(01)09504000059118(17)141120(10)7654321D(21)10987654d321",
                "entryType": "barcode"
            }
        ],
        "status": "active",
        "manufacturer": "Acme Devices, Inc",
        "manufactureDate": "2013-02-01T00:00:00Z",
        "expirationDate": "2014-02-01T00:00:00Z",
        "lotNumber": "43453424",
        "serialNumber": "AIDC78361",
        "deviceName": [
            {
                "name": "Acme Tono 2000",
                "type": "user-friendly-name"
            }
        ],
        "modelNumber": "T2000",
        "type": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "86184003",
                    "display": "Electrocardiographic monitor and recorder"
                }
            ],
            "text": "ECG"
        },
        "patient": {
            "reference": "Patient/example-patient"
        },
        "owner": {
            "reference": "Organization/example-hospital"
        },
        "location": {
            "reference": "Location/example-location"
        },
        "safety": [
            {
                "coding": [
                    {
                        "system": "urn:oid:2.16.840.1.113883.3.26.1.1",
                        "code": "mr-unsafe",
                        "display": "MR Unsafe"
                    }
                ],
                "text": "MR Unsafe"
            }
        ]
    }
    
    try:
        device = deserialize_device(device_json)
        print(f"✅ Device deserialized successfully")
        print(f"   ID: {getattr(device, 'id', 'N/A')}")
        print(f"   Manufacturer: {getattr(device, 'manufacturer', 'N/A')}")
        print(f"   Model Number: {getattr(device, 'model_number', 'N/A')}")
        print(f"   Status: {getattr(device, 'status', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Device deserialization failed: {e}")

def demo_entities_deserializer_class():
    """Demonstrate using the FHIREntitiesDeserializer class directly"""
    print("\n🔧 Entities Deserializer Class Demo")
    print("=" * 45)
    
    # Create deserializer instance
    deserializer = FHIREntitiesDeserializer(use_pydantic_validation=True)
    
    # Sample resources
    resources = [
        {
            "resourceType": "Substance",
            "id": "example-substance",
            "instance": True,
            "status": "active",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/substance-category",
                            "code": "chemical",
                            "display": "Chemical"
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "88480006",
                        "display": "Potassium"
                    }
                ]
            },
            "description": "High purity potassium for medical use"
        }
    ]
    
    for resource_data in resources:
        try:
            resource = deserializer.deserialize_entities_resource(resource_data)
            resource_type = resource_data['resourceType']
            print(f"✅ {resource_type} deserialized successfully")
            print(f"   ID: {getattr(resource, 'id', 'N/A')}")
            
            if hasattr(resource, 'active'):
                print(f"   Active: {getattr(resource, 'active', 'N/A')}")
            if hasattr(resource, 'name'):
                print(f"   Name: {getattr(resource, 'name', 'N/A')}")
            
        except Exception as e:
            print(f"❌ {resource_data['resourceType']} deserialization failed: {e}")

def demo_error_handling():
    """Demonstrate error handling in deserialization"""
    print("\n⚠️  Error Handling Demo")
    print("=" * 30)
    
    # Test invalid JSON
    try:
        deserialize_organization("invalid json")
    except Exception as e:
        print(f"✅ Caught invalid JSON error: {type(e).__name__}")
    
    # Test missing resourceType
    try:
        deserializer = FHIREntitiesDeserializer()
        deserializer.deserialize_entities_resource({"id": "test"})
    except Exception as e:
        print(f"✅ Caught missing resourceType error: {type(e).__name__}")
    
    # Test unsupported resource type
    try:
        deserializer = FHIREntitiesDeserializer()
        deserializer.deserialize_entities_resource({"resourceType": "UnsupportedResource"})
    except Exception as e:
        print(f"✅ Caught unsupported resource error: {type(e).__name__}")

def main():
    """Main demo function"""
    print("🚀 FHIR R5 Entities Deserializers Demo")
    print("=" * 50)
    
    print(f"📦 Pydantic Entities Available: {PYDANTIC_ENTITIES_AVAILABLE}")
    
    # Run all demos
    demo_organization_deserialization()
    demo_location_deserialization()
    demo_healthcare_service_deserialization()
    demo_device_deserialization()
    demo_entities_deserializer_class()
    demo_error_handling()
    
    print("\n🎉 Entities deserializers demo completed!")
    print("\n📋 Summary:")
    print("   ✅ Organization deserialization")
    print("   ✅ Location deserialization")
    print("   ✅ HealthcareService deserialization")
    print("   ✅ Device deserialization")
    print("   ✅ Substance deserialization")
    print("   ✅ Error handling")
    print("\n💡 The entities deserializers support:")
    print("   - Organization, Location, HealthcareService, Endpoint")
    print("   - Device, Substance, OrganizationAffiliation")
    print("   - BiologicallyDerivedProduct, NutritionProduct, DeviceMetric")
    print("   - Pydantic validation (optional)")
    print("   - Comprehensive error handling")
    print("   - Both JSON strings and dictionaries")

if __name__ == "__main__":
    main()