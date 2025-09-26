"""Tests for FHIR R5 Terminology resources with C extensions."""

import json
import pytest
from src.fhir.terminology import (
    FHIRCodeSystem, FHIRValueSet, FHIRConceptMap, FHIRBinary, FHIRBundle,
    is_terminology_resource
)
from src.fhir.foundation import HAS_C_FOUNDATION


class TestFHIRCodeSystem:
    """Test FHIR CodeSystem resource."""
    
    def test_code_system_creation(self):
        """Test CodeSystem resource creation."""
        code_system = FHIRCodeSystem("test-codesystem-1")
        result = code_system.to_dict()
        
        assert result["resourceType"] == "CodeSystem"
        assert result["id"] == "test-codesystem-1"
    
    def test_code_system_from_dict(self):
        """Test CodeSystem creation from dictionary."""
        data = {
            "resourceType": "CodeSystem",
            "id": "example-cs",
            "url": "http://example.org/codesystem",
            "version": "1.0.0",
            "name": "ExampleCodeSystem",
            "title": "Example Code System",
            "status": "active",
            "content": "complete",
            "concept": [
                {
                    "code": "active",
                    "display": "Active",
                    "definition": "The resource is active"
                },
                {
                    "code": "inactive",
                    "display": "Inactive",
                    "definition": "The resource is inactive"
                }
            ]
        }
        
        code_system = FHIRCodeSystem.from_dict(data)
        assert code_system.id == "example-cs"
        assert code_system.url == "http://example.org/codesystem"
        assert code_system.version == "1.0.0"
        assert code_system.name == "ExampleCodeSystem"
        assert code_system.status == "active"
        assert code_system.content == "complete"
        assert len(code_system.concept) == 2
    
    def test_code_system_from_json(self):
        """Test CodeSystem creation from JSON string."""
        json_data = {
            "resourceType": "CodeSystem",
            "id": "json-cs",
            "url": "http://example.org/json-cs",
            "status": "active",
            "content": "complete"
        }
        json_string = json.dumps(json_data)
        
        code_system = FHIRCodeSystem.from_json(json_string)
        assert code_system.id == "json-cs"
        assert code_system.url == "http://example.org/json-cs"
        assert code_system.status == "active"
        assert code_system.content == "complete"
    
    def test_code_system_lookup_display(self):
        """Test looking up display name for a code."""
        code_system = FHIRCodeSystem("test-cs")
        code_system.concept = [
            {"code": "active", "display": "Active Status"},
            {"code": "inactive", "display": "Inactive Status"}
        ]
        
        display = code_system.lookup_display("active")
        assert display == "Active Status"
        
        display = code_system.lookup_display("inactive")
        assert display == "Inactive Status"
        
        display = code_system.lookup_display("unknown")
        assert display is None


class TestFHIRValueSet:
    """Test FHIR ValueSet resource."""
    
    def test_value_set_creation(self):
        """Test ValueSet resource creation."""
        value_set = FHIRValueSet("test-valueset-1")
        result = value_set.to_dict()
        
        assert result["resourceType"] == "ValueSet"
        assert result["id"] == "test-valueset-1"
    
    def test_value_set_from_dict(self):
        """Test ValueSet creation from dictionary."""
        data = {
            "resourceType": "ValueSet",
            "id": "example-vs",
            "url": "http://example.org/valueset",
            "version": "1.0.0",
            "name": "ExampleValueSet",
            "title": "Example Value Set",
            "status": "active",
            "compose": {
                "include": [
                    {
                        "system": "http://example.org/codesystem",
                        "concept": [
                            {"code": "active", "display": "Active"},
                            {"code": "inactive", "display": "Inactive"}
                        ]
                    }
                ]
            }
        }
        
        value_set = FHIRValueSet.from_dict(data)
        assert value_set.id == "example-vs"
        assert value_set.url == "http://example.org/valueset"
        assert value_set.version == "1.0.0"
        assert value_set.name == "ExampleValueSet"
        assert value_set.status == "active"
        assert value_set.compose is not None
    
    def test_value_set_contains_code(self):
        """Test checking if ValueSet contains a code."""
        value_set = FHIRValueSet("test-vs")
        value_set.compose = {
            "include": [
                {
                    "system": "http://example.org/codesystem",
                    "concept": [
                        {"code": "active"},
                        {"code": "inactive"}
                    ]
                }
            ]
        }
        
        assert value_set.contains_code("http://example.org/codesystem", "active") is True
        assert value_set.contains_code("http://example.org/codesystem", "inactive") is True
        assert value_set.contains_code("http://example.org/codesystem", "unknown") is False
        assert value_set.contains_code("http://other.org/codesystem", "active") is False


class TestFHIRConceptMap:
    """Test FHIR ConceptMap resource."""
    
    def test_concept_map_creation(self):
        """Test ConceptMap resource creation."""
        concept_map = FHIRConceptMap("test-conceptmap-1")
        result = concept_map.to_dict()
        
        assert result["resourceType"] == "ConceptMap"
        assert result["id"] == "test-conceptmap-1"
    
    def test_concept_map_from_dict(self):
        """Test ConceptMap creation from dictionary."""
        data = {
            "resourceType": "ConceptMap",
            "id": "example-cm",
            "url": "http://example.org/conceptmap",
            "version": "1.0.0",
            "name": "ExampleConceptMap",
            "status": "active",
            "sourceUri": "http://example.org/source",
            "targetUri": "http://example.org/target",
            "group": [
                {
                    "source": "http://example.org/source",
                    "target": "http://example.org/target",
                    "element": [
                        {
                            "code": "active",
                            "target": [
                                {"code": "A", "equivalence": "equivalent"}
                            ]
                        }
                    ]
                }
            ]
        }
        
        concept_map = FHIRConceptMap.from_dict(data)
        assert concept_map.id == "example-cm"
        assert concept_map.url == "http://example.org/conceptmap"
        assert concept_map.source_uri == "http://example.org/source"
        assert concept_map.target_uri == "http://example.org/target"
        assert len(concept_map.group) == 1
    
    def test_concept_map_translate(self):
        """Test translating codes using ConceptMap."""
        concept_map = FHIRConceptMap("test-cm")
        concept_map.group = [
            {
                "source": "http://example.org/source",
                "target": "http://example.org/target",
                "element": [
                    {
                        "code": "active",
                        "target": [{"code": "A"}]
                    },
                    {
                        "code": "inactive",
                        "target": [{"code": "I"}]
                    }
                ]
            }
        ]
        
        translated = concept_map.translate("http://example.org/source", "active")
        assert translated == "A"
        
        translated = concept_map.translate("http://example.org/source", "inactive")
        assert translated == "I"
        
        translated = concept_map.translate("http://example.org/source", "unknown")
        assert translated is None


class TestFHIRBinary:
    """Test FHIR Binary resource."""
    
    def test_binary_creation(self):
        """Test Binary resource creation."""
        binary = FHIRBinary("test-binary-1")
        result = binary.to_dict()
        
        assert result["resourceType"] == "Binary"
        assert result["id"] == "test-binary-1"
    
    def test_binary_from_dict(self):
        """Test Binary creation from dictionary."""
        data = {
            "resourceType": "Binary",
            "id": "example-binary",
            "contentType": "application/pdf",
            "data": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwo+PgplbmRvYmoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tpZHMgWzMgMCBSXQovQ291bnQgMQo+PgplbmRvYmoK"
        }
        
        binary = FHIRBinary.from_dict(data)
        assert binary.id == "example-binary"
        assert binary.content_type == "application/pdf"
        assert binary.data is not None


class TestFHIRBundle:
    """Test FHIR Bundle resource."""
    
    def test_bundle_creation(self):
        """Test Bundle resource creation."""
        bundle = FHIRBundle("test-bundle-1")
        result = bundle.to_dict()
        
        assert result["resourceType"] == "Bundle"
        assert result["id"] == "test-bundle-1"
    
    def test_bundle_from_dict(self):
        """Test Bundle creation from dictionary."""
        data = {
            "resourceType": "Bundle",
            "id": "example-bundle",
            "type": "searchset",
            "total": 2,
            "entry": [
                {
                    "fullUrl": "http://example.org/Patient/1",
                    "resource": {
                        "resourceType": "Patient",
                        "id": "1",
                        "active": True
                    }
                },
                {
                    "fullUrl": "http://example.org/Patient/2",
                    "resource": {
                        "resourceType": "Patient",
                        "id": "2",
                        "active": False
                    }
                }
            ]
        }
        
        bundle = FHIRBundle.from_dict(data)
        assert bundle.id == "example-bundle"
        assert bundle.type == "searchset"
        assert bundle.total == 2
        assert len(bundle.entry) == 2
    
    def test_bundle_from_json(self):
        """Test Bundle creation from JSON string."""
        json_data = {
            "resourceType": "Bundle",
            "id": "json-bundle",
            "type": "collection",
            "entry": []
        }
        json_string = json.dumps(json_data)
        
        bundle = FHIRBundle.from_json(json_string)
        assert bundle.id == "json-bundle"
        assert bundle.type == "collection"
        assert len(bundle.entry) == 0
    
    def test_bundle_get_entry_count(self):
        """Test getting bundle entry count."""
        bundle = FHIRBundle("test-bundle")
        bundle.entry = [
            {"resource": {"resourceType": "Patient", "id": "1"}},
            {"resource": {"resourceType": "Patient", "id": "2"}}
        ]
        
        count = bundle.get_entry_count()
        assert count == 2
    
    def test_bundle_add_entry(self):
        """Test adding entries to bundle."""
        bundle = FHIRBundle("test-bundle")
        
        patient_resource = {
            "resourceType": "Patient",
            "id": "new-patient",
            "active": True
        }
        
        bundle.add_entry(patient_resource, "http://example.org/Patient/new-patient")
        
        assert len(bundle.entry) == 1
        assert bundle.total == 1
        assert bundle.entry[0]["fullUrl"] == "http://example.org/Patient/new-patient"
        assert bundle.entry[0]["resource"]["id"] == "new-patient"
    
    def test_bundle_get_resources_by_type(self):
        """Test getting resources by type from bundle."""
        bundle = FHIRBundle("test-bundle")
        bundle.entry = [
            {"resource": {"resourceType": "Patient", "id": "1"}},
            {"resource": {"resourceType": "Practitioner", "id": "1"}},
            {"resource": {"resourceType": "Patient", "id": "2"}}
        ]
        
        patients = bundle.get_resources_by_type("Patient")
        assert len(patients) == 2
        assert patients[0]["id"] == "1"
        assert patients[1]["id"] == "2"
        
        practitioners = bundle.get_resources_by_type("Practitioner")
        assert len(practitioners) == 1
        assert practitioners[0]["id"] == "1"
        
        organizations = bundle.get_resources_by_type("Organization")
        assert len(organizations) == 0


class TestTerminologyUtilities:
    """Test Terminology resource utilities."""
    
    def test_is_terminology_resource(self):
        """Test terminology resource type detection."""
        # Terminology resource types
        terminology_types = ["CodeSystem", "ValueSet", "ConceptMap", "NamingSystem"]
        
        for resource_type in terminology_types:
            assert is_terminology_resource(resource_type) is True
        
        # Non-terminology resource types
        non_terminology_types = ["Patient", "Practitioner", "Organization", "Observation"]
        
        for resource_type in non_terminology_types:
            assert is_terminology_resource(resource_type) is False


class TestCExtensionIntegration:
    """Test C extension integration for Terminology resources."""
    
    def test_c_extension_availability(self):
        """Test C extension availability reporting."""
        assert isinstance(HAS_C_FOUNDATION, bool)
        print(f"C Foundation extensions available: {HAS_C_FOUNDATION}")
    
    def test_fallback_behavior(self):
        """Test fallback to Python when C extensions fail."""
        # Create resources with C extensions disabled
        code_system = FHIRCodeSystem("fallback-cs", use_c_extensions=False)
        code_system.status = "active"
        code_system.content = "complete"
        
        result = code_system.to_dict()
        assert result["resourceType"] == "CodeSystem"
        assert result["id"] == "fallback-cs"
        assert result["status"] == "active"
        assert result["content"] == "complete"
        
        # Test Bundle fallback
        bundle = FHIRBundle("fallback-bundle", use_c_extensions=False)
        bundle.type = "collection"
        
        result = bundle.to_dict()
        assert result["resourceType"] == "Bundle"
        assert result["id"] == "fallback-bundle"
        assert result["type"] == "collection"