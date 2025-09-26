"""Tests for FHIR R5 Foundation resources with C extensions."""

import json
import pytest
from src.fhir.foundation import (
    FHIRPatient, FHIRPractitioner, FHIROrganization,
    is_foundation_resource, get_resource_type, HAS_C_FOUNDATION
)


class TestFHIRPatient:
    """Test FHIR Patient resource."""
    
    def test_patient_creation(self):
        """Test Patient resource creation."""
        patient = FHIRPatient("test-patient-1")
        result = patient.to_dict()
        
        assert result["resourceType"] == "Patient"
        assert result["id"] == "test-patient-1"
    
    def test_patient_from_dict(self):
        """Test Patient creation from dictionary."""
        data = {
            "resourceType": "Patient",
            "id": "example",
            "active": True,
            "name": [{
                "use": "official",
                "family": "Doe",
                "given": ["John"]
            }],
            "gender": "male",
            "birthDate": "1974-12-25"
        }
        
        patient = FHIRPatient.from_dict(data)
        assert patient.id == "example"
        assert patient.active is True
        assert patient.gender == "male"
        assert patient.birth_date == "1974-12-25"
        assert len(patient.name) == 1
    
    def test_patient_from_json(self):
        """Test Patient creation from JSON string."""
        json_data = {
            "resourceType": "Patient",
            "id": "json-patient",
            "active": True,
            "name": [{
                "text": "Jane Smith"
            }],
            "gender": "female"
        }
        json_string = json.dumps(json_data)
        
        patient = FHIRPatient.from_json(json_string)
        assert patient.id == "json-patient"
        assert patient.active is True
        assert patient.gender == "female"
    
    def test_patient_get_full_name(self):
        """Test getting patient full name."""
        # Test with text field
        patient = FHIRPatient("test-1")
        patient.name = [{"text": "John Doe"}]
        
        full_name = patient.get_full_name()
        assert full_name == "John Doe"
        
        # Test with given and family names
        patient2 = FHIRPatient("test-2")
        patient2.name = [{
            "given": ["Jane", "Marie"],
            "family": "Smith"
        }]
        
        full_name2 = patient2.get_full_name()
        assert full_name2 == "Jane Marie Smith"
    
    def test_patient_is_active(self):
        """Test patient active status."""
        # Test explicit active = True
        patient1 = FHIRPatient("test-1")
        patient1.active = True
        assert patient1.is_active() is True
        
        # Test explicit active = False
        patient2 = FHIRPatient("test-2")
        patient2.active = False
        assert patient2.is_active() is False
        
        # Test default (should be True)
        patient3 = FHIRPatient("test-3")
        assert patient3.is_active() is True
    
    def test_patient_validation(self):
        """Test patient validation."""
        # Valid patient
        patient1 = FHIRPatient("test-1")
        patient1.gender = "male"
        assert patient1.validate() is True
        
        # Invalid gender
        patient2 = FHIRPatient("test-2")
        patient2.gender = "invalid-gender"
        assert patient2.validate() is False
        
        # Valid gender options
        valid_genders = ["male", "female", "other", "unknown"]
        for gender in valid_genders:
            patient = FHIRPatient("test")
            patient.gender = gender
            assert patient.validate() is True


class TestFHIRPractitioner:
    """Test FHIR Practitioner resource."""
    
    def test_practitioner_creation(self):
        """Test Practitioner resource creation."""
        practitioner = FHIRPractitioner("test-practitioner-1")
        result = practitioner.to_dict()
        
        assert result["resourceType"] == "Practitioner"
        assert result["id"] == "test-practitioner-1"
    
    def test_practitioner_from_dict(self):
        """Test Practitioner creation from dictionary."""
        data = {
            "resourceType": "Practitioner",
            "id": "example-practitioner",
            "active": True,
            "name": [{
                "family": "Smith",
                "given": ["Dr. John"]
            }],
            "gender": "male"
        }
        
        practitioner = FHIRPractitioner.from_dict(data)
        assert practitioner.id == "example-practitioner"
        assert practitioner.active is True
        assert practitioner.gender == "male"
        assert len(practitioner.name) == 1


class TestFHIROrganization:
    """Test FHIR Organization resource."""
    
    def test_organization_creation(self):
        """Test Organization resource creation."""
        organization = FHIROrganization("test-org-1")
        result = organization.to_dict()
        
        assert result["resourceType"] == "Organization"
        assert result["id"] == "test-org-1"
    
    def test_organization_from_dict(self):
        """Test Organization creation from dictionary."""
        data = {
            "resourceType": "Organization",
            "id": "example-org",
            "active": True,
            "name": "Example Healthcare",
            "description": "A healthcare organization"
        }
        
        organization = FHIROrganization.from_dict(data)
        assert organization.id == "example-org"
        assert organization.active is True
        assert organization.name == "Example Healthcare"
        assert organization.description == "A healthcare organization"


class TestFoundationUtilities:
    """Test Foundation resource utilities."""
    
    def test_is_foundation_resource(self):
        """Test foundation resource type detection."""
        # Foundation resource types
        foundation_types = [
            "Patient", "Practitioner", "PractitionerRole", "Organization",
            "Location", "HealthcareService", "Endpoint", "RelatedPerson",
            "Person", "Group"
        ]
        
        for resource_type in foundation_types:
            assert is_foundation_resource(resource_type) is True
        
        # Non-foundation resource types
        non_foundation_types = [
            "Observation", "Medication", "Condition", "Procedure",
            "DiagnosticReport", "Encounter"
        ]
        
        for resource_type in non_foundation_types:
            assert is_foundation_resource(resource_type) is False
    
    def test_get_resource_type(self):
        """Test resource type extraction from JSON."""
        json_data = {
            "resourceType": "Patient",
            "id": "example"
        }
        json_string = json.dumps(json_data)
        
        resource_type = get_resource_type(json_string)
        assert resource_type == "Patient"
        
        # Test with invalid JSON
        invalid_json = "invalid json"
        resource_type = get_resource_type(invalid_json)
        assert resource_type is None
        
        # Test with missing resourceType
        json_data_no_type = {"id": "example"}
        json_string_no_type = json.dumps(json_data_no_type)
        resource_type = get_resource_type(json_string_no_type)
        assert resource_type is None


class TestCExtensionIntegration:
    """Test C extension integration for Foundation resources."""
    
    def test_c_extension_availability(self):
        """Test C extension availability reporting."""
        assert isinstance(HAS_C_FOUNDATION, bool)
        print(f"C Foundation extensions available: {HAS_C_FOUNDATION}")
    
    def test_fallback_behavior(self):
        """Test fallback to Python when C extensions fail."""
        # Create patient with C extensions disabled
        patient = FHIRPatient("fallback-test", use_c_extensions=False)
        patient.active = True
        patient.gender = "male"
        
        result = patient.to_dict()
        assert result["resourceType"] == "Patient"
        assert result["id"] == "fallback-test"
        assert result["active"] is True
        assert result["gender"] == "male"
        
        # Test validation fallback
        assert patient.validate() is True
        
        # Test invalid gender with fallback
        patient.gender = "invalid"
        assert patient.validate() is False
    
    def test_performance_comparison(self):
        """Test performance difference between C and Python implementations."""
        import time
        
        # Create test data
        patient_data = {
            "resourceType": "Patient",
            "id": "performance-test",
            "active": True,
            "name": [{
                "family": "TestPatient",
                "given": ["Performance"]
            }],
            "gender": "unknown"
        }
        json_string = json.dumps(patient_data)
        
        # Test C extension performance (if available)
        if HAS_C_FOUNDATION:
            start_time = time.time()
            for _ in range(100):
                patient_c = FHIRPatient.from_json(json_string)
                patient_c.get_full_name()
                patient_c.is_active()
                patient_c.validate()
            c_time = time.time() - start_time
            print(f"C extension time for 100 operations: {c_time:.4f}s")
        
        # Test Python fallback performance
        start_time = time.time()
        for _ in range(100):
            patient_py = FHIRPatient(use_c_extensions=False)
            patient_py = FHIRPatient.from_dict(patient_data)
            patient_py.get_full_name()
            patient_py.is_active()
            patient_py.validate()
        py_time = time.time() - start_time
        print(f"Python fallback time for 100 operations: {py_time:.4f}s")
        
        if HAS_C_FOUNDATION:
            speedup = py_time / c_time
            print(f"C extension speedup: {speedup:.2f}x")
            # C extensions should be faster
            assert c_time < py_time