#!/usr/bin/env python3

"""
Comprehensive Fast-FHIR System Demonstration
Shows all major features and capabilities of the Fast-FHIR R5 implementation
"""

import sys
import os
import json
sys.path.insert(0, os.path.abspath('..'))

from src.fhir.parser import FHIRParser
from src.fhir.fast_parser import FastFHIRParser
from src.fhir.datatypes import (
    FHIRString, FHIRCoding, FHIRQuantity, HAS_C_DATATYPES,
    validate_date, validate_time
)
from src.fhir.foundation import (
    FHIRPatient, FHIRPractitioner, FHIROrganization, HAS_C_FOUNDATION,
    is_foundation_resource
)
from src.fhir.resources import (
    Patient, Practitioner, PractitionerRole, RelatedPerson,
    Organization, Encounter, Group, Person, Location, Task,
    HealthcareService, Endpoint, Appointment, Slot, Schedule,
    Flag, Device, Substance, ListResource, Library
)
from src.fhir.terminology import (
    FHIRCodeSystem, FHIRValueSet, FHIRBundle, is_terminology_resource
)
from src.fhir.all_resources import (
    FHIRResourceFactory, get_all_fhir_resource_types, 
    get_fhir_implementation_status, HAS_ALL_C_EXTENSIONS
)


def demo_parsers():
    """Demonstrate FHIR parsers initialization and capabilities"""
    print("=== FHIR Parsers Demo ===")
    
    # Initialize both parsers
    standard_parser = FHIRParser()
    fast_parser = FastFHIRParser()
    
    print("FHIR R5 Parser initialized")
    print(f"C data types available: {HAS_C_DATATYPES}")
    print(f"C foundation resources available: {HAS_C_FOUNDATION}")
    print(f"Fast parser performance info: {fast_parser.get_performance_info()}")
    print()


def demo_datatypes():
    """Demonstrate FHIR data types"""
    print("=== FHIR Data Types Demo ===")
    
    # Create FHIR data types
    fhir_string = FHIRString("Hello FHIR R5")
    print(f"FHIR String: {fhir_string.to_dict()}")
    
    coding = FHIRCoding(
        system="http://loinc.org",
        code="15074-8",
        display="Glucose"
    )
    print(f"FHIR Coding: {coding.to_dict()}")
    
    quantity = FHIRQuantity(
        value=6.3,
        unit="mmol/l",
        system="http://unitsofmeasure.org",
        code="mmol/L"
    )
    print(f"FHIR Quantity: {quantity.to_dict()}")
    print()


def demo_validation():
    """Demonstrate FHIR validation functions"""
    print("=== FHIR Validation Demo ===")
    
    print(f"Valid date '2023-12-25': {validate_date('2023-12-25')}")
    print(f"Invalid date '2023-13-01': {validate_date('2023-13-01')}")
    print(f"Valid time '14:30:00': {validate_time('14:30:00')}")
    print(f"Invalid time '25:00:00': {validate_time('25:00:00')}")
    print()


def demo_foundation_resources():
    """Demonstrate DRY-based Foundation resources"""
    print("=== DRY-based FHIR Resources Demo ===")
    
    # Create Patient using new DRY architecture
    patient = Patient("dry-patient-1")
    patient.active = True
    patient.gender = "male"
    patient.birth_date = "1974-12-25"
    patient.name = [{
        "use": "official",
        "family": "Doe",
        "given": ["John", "William"]
    }]
    
    print(f"DRY Patient: {patient.to_dict()}")
    print(f"Patient full name: {patient.get_full_name()}")
    print(f"Patient is active: {patient.is_active()}")
    print(f"Patient is valid: {patient.validate()}")
    
    # Create Practitioner using DRY architecture
    practitioner = Practitioner("dry-practitioner-1")
    practitioner.active = True
    practitioner.gender = "female"
    practitioner.name = [{
        "family": "Smith",
        "given": ["Dr. Jane"],
        "prefix": ["Dr."]
    }]
    practitioner.qualification = [{
        "code": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
                "code": "MD",
                "display": "Doctor of Medicine"
            }]
        }
    }]
    
    print(f"DRY Practitioner: {practitioner.to_dict()}")
    print(f"Has MD qualification: {practitioner.has_qualification('MD')}")
    
    # Create Organization using DRY architecture
    organization = Organization("dry-org-1")
    organization.active = True
    organization.name = "Example Healthcare System"
    organization.description = "A comprehensive healthcare organization"
    organization.type = [{
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/organization-type",
            "code": "prov",
            "display": "Healthcare Provider"
        }]
    }]
    
    print(f"DRY Organization: {organization.to_dict()}")
    print(f"Has provider type: {organization.has_type('prov')}")
    
    return patient, practitioner, organization


def demo_workflow_resources(patient, practitioner):
    """Demonstrate workflow resources"""
    print("=== Workflow Resources Demo ===")
    
    # Create Location
    location = Location("dry-location-1")
    location.status = "active"
    location.name = "Main Hospital Building"
    location.mode = "instance"
    location.set_coordinates(-122.4194, 37.7749)
    
    print(f"DRY Location: {location.to_dict()}")
    print(f"Location coordinates: {location.get_coordinates()}")
    
    # Create Task
    task = Task("dry-task-1")
    task.status = "completed"
    task.intent = "order"
    task.description = "Review patient chart"
    task.add_input("patient", {"reference": f"Patient/{patient.id}"})
    task.add_output("result", {"valueString": "Chart reviewed successfully"})
    
    print(f"DRY Task: {task.to_dict()}")
    print(f"Task completed: {task.is_completed()}")
    
    # Create Appointment
    appointment = Appointment("dry-appointment-1")
    appointment.status = "booked"
    appointment.start = "2023-12-25T10:00:00Z"
    appointment.end = "2023-12-25T11:00:00Z"
    appointment.add_participant(f"Patient/{patient.id}")
    appointment.add_participant(f"Practitioner/{practitioner.id}")
    
    print(f"DRY Appointment: {appointment.to_dict()}")
    print(f"Appointment booked: {appointment.is_booked()}")
    
    # Create Schedule
    schedule = Schedule("dry-schedule-1")
    schedule.active = True
    schedule.name = "Dr. Smith's Schedule"
    schedule.add_actor(f"Practitioner/{practitioner.id}")
    schedule.add_actor(f"Location/{location.id}")
    
    print(f"DRY Schedule: {schedule.to_dict()}")
    print(f"Schedule actors: {len(schedule.get_actors())}")
    print()


def demo_device_resources(patient):
    """Demonstrate device and group resources"""
    print("=== Device and Group Resources Demo ===")
    
    # Create Device
    device = Device("dry-device-1")
    device.status = "active"
    device.display_name = "Blood Pressure Monitor"
    device.manufacturer = "Example Medical Devices Inc."
    device.udi_carrier = [{"deviceIdentifier": "12345-ABCDE"}]
    
    print(f"DRY Device: {device.to_dict()}")
    print(f"Device name: {device.get_device_name()}")
    print(f"Device UDI: {device.get_udi_device_identifier()}")
    
    # Create Group
    group = Group("dry-group-1")
    group.type = "person"
    group.actual = True
    group.name = "Example Patient Group"
    group.add_member(f"Patient/{patient.id}")
    
    print(f"DRY Group: {group.to_dict()}")
    print(f"Group member count: {group.get_member_count()}")
    print(f"Has patient member: {group.has_member(f'Patient/{patient.id}')}")
    print()


def demo_terminology_resources(patient, practitioner):
    """Demonstrate terminology resources"""
    print("=== FHIR Terminology Resources Demo ===")
    
    # Create CodeSystem
    code_system = FHIRCodeSystem("demo-codesystem-1")
    code_system.url = "http://example.org/codesystem"
    code_system.status = "active"
    code_system.content = "complete"
    code_system.concept = [
        {"code": "active", "display": "Active Status"},
        {"code": "inactive", "display": "Inactive Status"}
    ]
    
    print(f"CodeSystem: {code_system.to_dict()}")
    print(f"Lookup 'active': {code_system.lookup_display('active')}")
    
    # Create ValueSet
    value_set = FHIRValueSet("demo-valueset-1")
    value_set.url = "http://example.org/valueset"
    value_set.status = "active"
    value_set.compose = {
        "include": [{
            "system": "http://example.org/codesystem",
            "concept": [
                {"code": "active"},
                {"code": "inactive"}
            ]
        }]
    }
    
    print(f"ValueSet: {value_set.to_dict()}")
    print(f"Contains 'active': {value_set.contains_code('http://example.org/codesystem', 'active')}")
    
    # Create Bundle
    bundle = FHIRBundle("demo-bundle-1")
    bundle.type = "collection"
    bundle.add_entry(patient.to_dict(), "http://example.org/Patient/demo-patient-1")
    bundle.add_entry(practitioner.to_dict(), "http://example.org/Practitioner/demo-practitioner-1")
    
    print(f"Bundle entry count: {bundle.get_entry_count()}")
    print(f"Bundle patients: {len(bundle.get_resources_by_type('Patient'))}")
    print()


def demo_resource_detection():
    """Demonstrate resource type detection"""
    print("=== Resource Type Detection ===")
    
    print(f"'Patient' is foundation resource: {is_foundation_resource('Patient')}")
    print(f"'CodeSystem' is foundation resource: {is_foundation_resource('CodeSystem')}")
    print(f"'CodeSystem' is terminology resource: {is_terminology_resource('CodeSystem')}")
    print(f"'Observation' is foundation resource: {is_foundation_resource('Observation')}")
    print()


def demo_fast_parser():
    """Demonstrate fast parser capabilities"""
    print("=== Fast Parser Demo ===")
    
    fast_parser = FastFHIRParser()
    
    # Example FHIR Patient data for fast parser
    patient_data = {
        "resourceType": "Patient",
        "id": "example-patient",
        "active": True,
        "name": [{
            "use": "official",
            "family": "Doe",
            "given": ["John", "William"]
        }],
        "gender": "male",
        "birthDate": "1974-12-25"
    }
    
    # Parse with fast parser
    parsed_patient = fast_parser.parse(patient_data)
    print(f"Parsed patient: {parsed_patient.get_full_name()}")
    print(f"Patient ID: {parsed_patient.id}")
    print(f"Gender: {parsed_patient.gender}")
    print()


def demo_resource_system():
    """Demonstrate complete FHIR R5 resource system"""
    print("=== Complete FHIR R5 Resource System ===")
    
    # Initialize resource factory
    factory = FHIRResourceFactory()
    factory_info = factory.get_performance_info()
    
    print(f"Total FHIR R5 resource types: {factory_info['total_resource_types']}")
    print(f"Implemented resource types: {factory_info['implemented_resource_types']}")
    print(f"Implementation coverage: {factory_info['implementation_coverage']}")
    print(f"All C extensions available: {HAS_ALL_C_EXTENSIONS}")
    
    # Show resource categories
    print("\nResource categories:")
    for category, count in factory_info['categories'].items():
        print(f"  {category.title()}: {count} resources")
    
    # Get comprehensive implementation status
    status = get_fhir_implementation_status()
    print(f"\nImplemented resources: {', '.join(status['implemented_list'][:10])}...")
    print()


def demo_resource_factory():
    """Demonstrate resource factory capabilities"""
    print("=== Resource Factory Demo ===")
    
    factory = FHIRResourceFactory()
    
    # Create resources using factory
    factory_patient = factory.create_resource("Patient", "factory-patient-1")
    if factory_patient:
        factory_patient.active = True
        factory_patient.gender = "female"
        print(f"Factory-created patient: {factory_patient.to_dict()}")
    
    # Parse resource using factory
    sample_data = {
        "resourceType": "CodeSystem",
        "id": "factory-cs-1",
        "status": "active",
        "content": "complete"
    }
    
    parsed_resource = factory.parse_resource(sample_data)
    if hasattr(parsed_resource, 'to_dict'):
        print(f"Factory-parsed CodeSystem: {parsed_resource.to_dict()}")
    else:
        print(f"Factory-parsed (generic): {parsed_resource}")
    
    print(f"\nTotal FHIR R5 resource types available: {len(get_all_fhir_resource_types())}")
    print()


def main():
    """Run comprehensive Fast-FHIR system demonstration"""
    print("Fast-FHIR Comprehensive System Demonstration")
    print("=" * 50)
    print()
    
    # Run all demonstrations
    demo_parsers()
    demo_datatypes()
    demo_validation()
    
    patient, practitioner, organization = demo_foundation_resources()
    demo_workflow_resources(patient, practitioner)
    demo_device_resources(patient)
    demo_terminology_resources(patient, practitioner)
    demo_resource_detection()
    demo_fast_parser()
    demo_resource_system()
    demo_resource_factory()
    
    print("🎉 All Fast-FHIR system demonstrations completed successfully!")
    print("\nReady to parse ALL FHIR R5 resources with high-performance capabilities!")


if __name__ == "__main__":
    main()