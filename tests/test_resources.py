"""Tests for FHIR R5 resources following DRY principles."""

import json
import pytest
from src.fhir.resources import (
    Patient, Practitioner, PractitionerRole, RelatedPerson,
    Organization, Encounter, Group, Person
)


class TestPatient:
    """Test Patient resource."""
    
    def test_patient_creation(self):
        """Test Patient creation."""
        patient = Patient("test-patient-1")
        assert patient.resource_type == "Patient"
        assert patient.id == "test-patient-1"
    
    def test_patient_from_dict(self):
        """Test Patient from dictionary."""
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
        
        patient = Patient.from_dict(data)
        assert patient.id == "example"
        assert patient.active is True
        assert patient.gender == "male"
        assert patient.birth_date == "1974-12-25"
        assert patient.get_full_name() == "John Doe"
    
    def test_patient_validation(self):
        """Test Patient validation."""
        patient = Patient("test-patient")
        patient.gender = "male"
        assert patient.validate() is True
        
        patient.gender = "invalid-gender"
        assert patient.validate() is False


class TestPractitioner:
    """Test Practitioner resource."""
    
    def test_practitioner_creation(self):
        """Test Practitioner creation."""
        practitioner = Practitioner("test-practitioner-1")
        assert practitioner.resource_type == "Practitioner"
        assert practitioner.id == "test-practitioner-1"
    
    def test_practitioner_qualifications(self):
        """Test Practitioner qualifications."""
        practitioner = Practitioner("test-practitioner")
        practitioner.qualification = [{
            "code": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
                    "code": "MD",
                    "display": "Doctor of Medicine"
                }]
            }
        }]
        
        assert practitioner.has_qualification("MD") is True
        assert practitioner.has_qualification("RN") is False


class TestPractitionerRole:
    """Test PractitionerRole resource."""
    
    def test_practitioner_role_creation(self):
        """Test PractitionerRole creation."""
        role = PractitionerRole("test-role-1")
        assert role.resource_type == "PractitionerRole"
        assert role.id == "test-role-1"
    
    def test_practitioner_role_validation(self):
        """Test PractitionerRole validation."""
        role = PractitionerRole("test-role")
        
        # Should fail without practitioner or organization
        assert role.validate() is False
        
        # Should pass with practitioner
        role.practitioner = {"reference": "Practitioner/123"}
        assert role.validate() is True


class TestRelatedPerson:
    """Test RelatedPerson resource."""
    
    def test_related_person_creation(self):
        """Test RelatedPerson creation."""
        related = RelatedPerson("test-related-1")
        assert related.resource_type == "RelatedPerson"
        assert related.id == "test-related-1"
    
    def test_related_person_validation(self):
        """Test RelatedPerson validation."""
        related = RelatedPerson("test-related")
        
        # Should fail without patient reference
        assert related.validate() is False
        
        # Should pass with patient reference
        related.patient = {"reference": "Patient/123"}
        assert related.validate() is True
    
    def test_related_person_relationships(self):
        """Test RelatedPerson relationships."""
        related = RelatedPerson("test-related")
        related.relationship = [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                "code": "WIFE",
                "display": "Wife"
            }]
        }]
        
        assert related.has_relationship("WIFE") is True
        assert related.has_relationship("HUSB") is False


class TestOrganization:
    """Test Organization resource."""
    
    def test_organization_creation(self):
        """Test Organization creation."""
        org = Organization("test-org-1")
        assert org.resource_type == "Organization"
        assert org.id == "test-org-1"
    
    def test_organization_validation(self):
        """Test Organization validation."""
        org = Organization("test-org")
        
        # Should fail without name
        assert org.validate() is False
        
        # Should pass with name
        org.name = "Test Hospital"
        assert org.validate() is True
    
    def test_organization_types(self):
        """Test Organization types."""
        org = Organization("test-org")
        org.type = [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                "code": "prov",
                "display": "Healthcare Provider"
            }]
        }]
        
        assert org.has_type("prov") is True
        assert org.has_type("ins") is False


class TestEncounter:
    """Test Encounter resource."""
    
    def test_encounter_creation(self):
        """Test Encounter creation."""
        encounter = Encounter("test-encounter-1")
        assert encounter.resource_type == "Encounter"
        assert encounter.id == "test-encounter-1"
    
    def test_encounter_validation(self):
        """Test Encounter validation."""
        encounter = Encounter("test-encounter")
        
        # Should fail without status and class
        assert encounter.validate() is False
        
        # Should pass with required fields
        encounter.status = "completed"
        encounter.class_element = {"code": "AMB", "display": "Ambulatory"}
        assert encounter.validate() is True
    
    def test_encounter_participants(self):
        """Test Encounter participants."""
        encounter = Encounter("test-encounter")
        encounter.add_participant("Practitioner/123", [{"coding": [{"code": "ATND"}]}])
        
        participants = encounter.get_participants()
        assert len(participants) == 1
        assert participants[0]["actor"]["reference"] == "Practitioner/123"
    
    def test_encounter_diagnoses(self):
        """Test Encounter diagnoses."""
        encounter = Encounter("test-encounter")
        encounter.add_diagnosis("Condition/456", "AD", 1)
        
        diagnoses = encounter.get_diagnoses()
        assert len(diagnoses) == 1
        assert diagnoses[0]["condition"][0]["reference"] == "Condition/456"


class TestGroup:
    """Test Group resource."""
    
    def test_group_creation(self):
        """Test Group creation."""
        group = Group("test-group-1")
        assert group.resource_type == "Group"
        assert group.id == "test-group-1"
    
    def test_group_validation(self):
        """Test Group validation."""
        group = Group("test-group")
        
        # Should fail without type and actual
        assert group.validate() is False
        
        # Should pass with required fields
        group.type = "person"
        group.actual = True
        assert group.validate() is True
    
    def test_group_members(self):
        """Test Group members."""
        group = Group("test-group")
        group.type = "person"
        group.actual = True
        
        group.add_member("Patient/123")
        group.add_member("Patient/456")
        
        assert group.get_member_count() == 2
        assert group.has_member("Patient/123") is True
        assert group.has_member("Patient/789") is False
        
        # Remove member
        assert group.remove_member("Patient/123") is True
        assert group.get_member_count() == 1


class TestPerson:
    """Test Person resource."""
    
    def test_person_creation(self):
        """Test Person creation."""
        person = Person("test-person-1")
        assert person.resource_type == "Person"
        assert person.id == "test-person-1"
    
    def test_person_links(self):
        """Test Person links."""
        person = Person("test-person")
        person.link = [{
            "target": {"reference": "Patient/123"},
            "assurance": "level2"
        }]
        
        assert person.has_link_to_resource("Patient/123") is True
        assert person.has_link_to_resource("Patient/456") is False


class TestDRYPrinciples:
    """Test DRY principles implementation."""
    
    def test_person_mixin_reuse(self):
        """Test that person mixin is properly reused."""
        # All person-like resources should have common methods
        patient = Patient("test-patient")
        practitioner = Practitioner("test-practitioner")
        related_person = RelatedPerson("test-related")
        person = Person("test-person")
        
        # Set common data
        name_data = [{"family": "Smith", "given": ["John"]}]
        
        for resource in [patient, practitioner, related_person, person]:
            resource.name = name_data
            resource.active = True
            resource.gender = "male"
            
            # All should have common methods
            assert resource.get_full_name() == "John Smith"
            assert resource.is_active() is True
            assert hasattr(resource, '_validate_person_fields')
    
    def test_base_class_functionality(self):
        """Test base class provides common functionality."""
        resources = [
            Patient("p1"), Practitioner("pr1"), Organization("o1"),
            Encounter("e1"), Group("g1")
        ]
        
        for resource in resources:
            # All should have common base functionality
            assert hasattr(resource, 'to_dict')
            assert hasattr(resource, 'validate')
            assert hasattr(resource, 'resource_type')
            assert hasattr(resource, 'id')
            
            # All should produce valid dictionaries
            result = resource.to_dict()
            assert isinstance(result, dict)
            assert result.get("resourceType") == resource.resource_type
            assert result.get("id") == resource.id
    
    def test_validation_consistency(self):
        """Test validation is consistent across resources."""
        # Create resources with invalid data
        patient = Patient("p1")
        patient.gender = "invalid"
        
        practitioner = Practitioner("pr1")
        practitioner.gender = "invalid"
        
        # Both should fail validation for same reason
        assert patient.validate() is False
        assert practitioner.validate() is False
        
        # Fix the data
        patient.gender = "male"
        practitioner.gender = "male"
        
        # Both should pass validation
        assert patient.validate() is True
        assert practitioner.validate() is True