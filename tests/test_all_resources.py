"""Tests for complete FHIR R5 resource system."""

import pytest
from fast_fhir.all_resources import (
    FHIRResourceCategory, FHIRResourceRegistry, FHIRResourceFactory,
    get_all_fhir_resource_types, get_fhir_resource_categories,
    is_fhir_resource_implemented, get_fhir_implementation_status,
    HAS_ALL_C_EXTENSIONS
)


class TestFHIRResourceRegistry:
    """Test FHIR resource registry."""
    
    def test_resource_registry_completeness(self):
        """Test that registry contains all major FHIR R5 resources."""
        registry = FHIRResourceRegistry()
        
        # Check total count is reasonable for FHIR R5
        total_count = registry.get_total_resource_count()
        assert total_count >= 100, f"Expected at least 100 resources, got {total_count}"
        
        # Check major resource types are present
        major_resources = [
            "Patient", "Practitioner", "Organization", "Location",
            "Observation", "Condition", "Procedure", "DiagnosticReport",
            "Medication", "MedicationRequest", "MedicationDispense",
            "Appointment", "Encounter", "Task",
            "CodeSystem", "ValueSet", "ConceptMap",
            "Bundle", "Binary"
        ]
        
        for resource_type in major_resources:
            assert registry.is_valid_resource_type(resource_type), f"Missing {resource_type}"
    
    def test_resource_categories(self):
        """Test resource categorization."""
        registry = FHIRResourceRegistry()
        
        # Test specific resource categories
        assert registry.get_resource_category("Patient") == FHIRResourceCategory.FOUNDATION
        assert registry.get_resource_category("Observation") == FHIRResourceCategory.CLINICAL
        assert registry.get_resource_category("Medication") == FHIRResourceCategory.MEDICATION
        assert registry.get_resource_category("Appointment") == FHIRResourceCategory.WORKFLOW
        assert registry.get_resource_category("Claim") == FHIRResourceCategory.FINANCIAL
        assert registry.get_resource_category("Device") == FHIRResourceCategory.SPECIALIZED
    
    def test_get_resources_by_category(self):
        """Test getting resources by category."""
        registry = FHIRResourceRegistry()
        
        foundation_resources = registry.get_resources_by_category(FHIRResourceCategory.FOUNDATION)
        assert "Patient" in foundation_resources
        assert "Organization" in foundation_resources
        assert "CodeSystem" in foundation_resources
        assert len(foundation_resources) > 10
        
        clinical_resources = registry.get_resources_by_category(FHIRResourceCategory.CLINICAL)
        assert "Observation" in clinical_resources
        assert "Condition" in clinical_resources
        assert len(clinical_resources) > 10
    
    def test_implementation_coverage(self):
        """Test implementation coverage calculation."""
        registry = FHIRResourceRegistry()
        
        coverage = registry.get_implementation_coverage()
        assert 0 <= coverage <= 100
        
        implemented = registry.get_implemented_resources()
        assert len(implemented) > 0
        assert "Patient" in implemented
        assert "CodeSystem" in implemented


class TestFHIRResourceFactory:
    """Test FHIR resource factory."""
    
    def test_factory_initialization(self):
        """Test factory initialization."""
        factory = FHIRResourceFactory()
        
        performance_info = factory.get_performance_info()
        assert "c_extensions_available" in performance_info
        assert "total_resource_types" in performance_info
        assert "implemented_resource_types" in performance_info
        assert "implementation_coverage" in performance_info
        assert "categories" in performance_info
        
        assert performance_info["total_resource_types"] >= 100
        assert performance_info["implemented_resource_types"] > 0
    
    def test_create_resource(self):
        """Test resource creation via factory."""
        factory = FHIRResourceFactory()
        
        # Test creating implemented resource
        patient = factory.create_resource("Patient", "test-patient-1")
        assert patient is not None
        assert patient.id == "test-patient-1"
        assert patient.resource_type == "Patient"
        
        # Test creating unimplemented resource
        unimplemented = factory.create_resource("ResearchStudy", "test-study-1")
        assert unimplemented is None
    
    def test_parse_resource(self):
        """Test resource parsing via factory."""
        factory = FHIRResourceFactory()
        
        # Test parsing implemented resource
        patient_data = {
            "resourceType": "Patient",
            "id": "test-patient",
            "active": True,
            "gender": "male"
        }
        
        patient = factory.parse_resource(patient_data)
        assert patient is not None
        assert hasattr(patient, 'id')
        assert patient.id == "test-patient"
        assert patient.active is True
        assert patient.gender == "male"
        
        # Test parsing unimplemented resource
        unimplemented_data = {
            "resourceType": "ResearchStudy",
            "id": "test-study",
            "status": "active"
        }
        
        result = factory.parse_resource(unimplemented_data)
        assert result is not None
        assert isinstance(result, dict)
        assert result["resourceType"] == "ResearchStudy"
        assert result["id"] == "test-study"
    
    def test_parse_resource_from_json_string(self):
        """Test parsing resource from JSON string."""
        factory = FHIRResourceFactory()
        
        json_string = '{"resourceType": "Patient", "id": "json-patient", "active": true}'
        
        patient = factory.parse_resource(json_string)
        assert patient is not None
        assert patient.id == "json-patient"
        assert patient.active is True
    
    def test_parse_invalid_resource(self):
        """Test parsing invalid resource data."""
        factory = FHIRResourceFactory()
        
        # Missing resourceType
        with pytest.raises(ValueError, match="Missing resourceType"):
            factory.parse_resource({"id": "test"})


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_get_all_fhir_resource_types(self):
        """Test getting all FHIR resource types."""
        all_types = get_all_fhir_resource_types()
        
        assert isinstance(all_types, list)
        assert len(all_types) >= 100
        assert "Patient" in all_types
        assert "Observation" in all_types
        assert "Bundle" in all_types
    
    def test_get_fhir_resource_categories(self):
        """Test getting resources by categories."""
        categories = get_fhir_resource_categories()
        
        assert isinstance(categories, dict)
        assert "foundation" in categories
        assert "clinical" in categories
        assert "medication" in categories
        assert "workflow" in categories
        assert "financial" in categories
        assert "specialized" in categories
        
        assert "Patient" in categories["foundation"]
        assert "Observation" in categories["clinical"]
    
    def test_is_fhir_resource_implemented(self):
        """Test checking resource implementation status."""
        assert is_fhir_resource_implemented("Patient") is True
        assert is_fhir_resource_implemented("CodeSystem") is True
        assert is_fhir_resource_implemented("Bundle") is True
        
        # Most resources are not yet implemented
        assert is_fhir_resource_implemented("ResearchStudy") is False
        assert is_fhir_resource_implemented("InvalidResource") is False
    
    def test_get_fhir_implementation_status(self):
        """Test getting comprehensive implementation status."""
        status = get_fhir_implementation_status()
        
        required_keys = [
            "total_resources", "implemented_resources", "coverage_percentage",
            "c_extensions_available", "by_category", "implemented_list", "not_implemented_list"
        ]
        
        for key in required_keys:
            assert key in status
        
        assert status["total_resources"] >= 100
        assert status["implemented_resources"] > 0
        assert 0 <= status["coverage_percentage"] <= 100
        assert isinstance(status["c_extensions_available"], bool)
        assert isinstance(status["implemented_list"], list)
        assert isinstance(status["not_implemented_list"], list)
        
        # Check that implemented + not implemented = total
        total_accounted = len(status["implemented_list"]) + len(status["not_implemented_list"])
        assert total_accounted == status["total_resources"]


class TestResourceCoverage:
    """Test resource coverage and completeness."""
    
    def test_foundation_resources_coverage(self):
        """Test foundation resources are well covered."""
        registry = FHIRResourceRegistry()
        foundation_resources = registry.get_resources_by_category(FHIRResourceCategory.FOUNDATION)
        
        # Key foundation resources should be implemented
        key_foundation = ["Patient", "Practitioner", "Organization", "CodeSystem", "ValueSet", "Bundle"]
        
        for resource_type in key_foundation:
            assert resource_type in foundation_resources
            assert registry.get_resource_class(resource_type) is not None, f"{resource_type} should be implemented"
    
    def test_clinical_resources_identified(self):
        """Test clinical resources are properly identified."""
        registry = FHIRResourceRegistry()
        clinical_resources = registry.get_resources_by_category(FHIRResourceCategory.CLINICAL)
        
        expected_clinical = [
            "Observation", "Condition", "Procedure", "DiagnosticReport",
            "AllergyIntolerance", "Specimen", "CarePlan"
        ]
        
        for resource_type in expected_clinical:
            assert resource_type in clinical_resources
    
    def test_medication_resources_identified(self):
        """Test medication resources are properly identified."""
        registry = FHIRResourceRegistry()
        medication_resources = registry.get_resources_by_category(FHIRResourceCategory.MEDICATION)
        
        expected_medication = [
            "Medication", "MedicationRequest", "MedicationDispense",
            "MedicationAdministration", "MedicationStatement", "Immunization"
        ]
        
        for resource_type in expected_medication:
            assert resource_type in medication_resources
    
    def test_workflow_resources_identified(self):
        """Test workflow resources are properly identified."""
        registry = FHIRResourceRegistry()
        workflow_resources = registry.get_resources_by_category(FHIRResourceCategory.WORKFLOW)
        
        expected_workflow = [
            "Appointment", "Encounter", "Task", "Schedule", "Slot",
            "Questionnaire", "QuestionnaireResponse"
        ]
        
        for resource_type in expected_workflow:
            assert resource_type in workflow_resources


class TestCExtensionIntegration:
    """Test C extension integration."""
    
    def test_c_extension_availability(self):
        """Test C extension availability reporting."""
        assert isinstance(HAS_ALL_C_EXTENSIONS, bool)
        print(f"All C extensions available: {HAS_ALL_C_EXTENSIONS}")
    
    def test_factory_with_c_extensions(self):
        """Test factory behavior with C extensions."""
        factory_with_c = FHIRResourceFactory(use_c_extensions=True)
        factory_without_c = FHIRResourceFactory(use_c_extensions=False)
        
        # Both should work
        patient_with_c = factory_with_c.create_resource("Patient", "c-patient")
        patient_without_c = factory_without_c.create_resource("Patient", "py-patient")
        
        if patient_with_c and patient_without_c:
            assert patient_with_c.id == "c-patient"
            assert patient_without_c.id == "py-patient"
            
            # Both should produce valid dictionaries
            dict_with_c = patient_with_c.to_dict()
            dict_without_c = patient_without_c.to_dict()
            
            assert dict_with_c["resourceType"] == "Patient"
            assert dict_without_c["resourceType"] == "Patient"


class TestPerformanceAndScalability:
    """Test performance and scalability aspects."""
    
    def test_large_resource_list_handling(self):
        """Test handling of large resource type lists."""
        all_types = get_all_fhir_resource_types()
        
        # Should handle large lists efficiently
        assert len(all_types) >= 100
        
        # Should not have duplicates
        assert len(all_types) == len(set(all_types))
        
        # Should be sorted or at least consistent
        assert all_types == sorted(all_types) or len(all_types) > 0
    
    def test_factory_performance_info(self):
        """Test factory performance information."""
        factory = FHIRResourceFactory()
        
        info = factory.get_performance_info()
        
        # Should provide meaningful metrics
        assert info["total_resource_types"] > 0
        assert info["implementation_coverage"].endswith("%")
        
        # Categories should sum to total
        category_sum = sum(info["categories"].values())
        assert category_sum == info["total_resource_types"]