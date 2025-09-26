"""Tests for FHIR R5 Parser."""

import json
import pytest
from src.fhir.parser import FHIRParser
from src.fhir.resources.patient import Patient
from src.fhir.resources.observation import Observation


class TestFHIRParser:
    """Test cases for FHIR Parser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = FHIRParser()
    
    def test_parser_initialization(self):
        """Test parser initializes correctly."""
        assert self.parser.version == "5.0.0"
        assert 'Patient' in self.parser.RESOURCE_TYPES
        assert 'Observation' in self.parser.RESOURCE_TYPES
    
    def test_parse_patient_json_string(self):
        """Test parsing Patient from JSON string."""
        patient_json = json.dumps({
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
        })
        
        result = self.parser.parse(patient_json)
        assert isinstance(result, Patient)
        assert result.id == "example"
        assert result.active is True
        assert result.gender == "male"
        assert result.birth_date == "1974-12-25"
    
    def test_parse_patient_dict(self):
        """Test parsing Patient from dictionary."""
        patient_data = {
            "resourceType": "Patient",
            "id": "test-patient",
            "name": [{
                "text": "Jane Smith"
            }]
        }
        
        result = self.parser.parse(patient_data)
        assert isinstance(result, Patient)
        assert result.id == "test-patient"
        assert result.get_full_name() == "Jane Smith"
    
    def test_parse_observation(self):
        """Test parsing Observation resource."""
        obs_data = {
            "resourceType": "Observation",
            "id": "example-obs",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "15074-8",
                    "display": "Glucose"
                }]
            },
            "subject": {
                "reference": "Patient/example"
            },
            "valueQuantity": {
                "value": 6.3,
                "unit": "mmol/l",
                "system": "http://unitsofmeasure.org",
                "code": "mmol/L"
            }
        }
        
        result = self.parser.parse(obs_data)
        assert isinstance(result, Observation)
        assert result.id == "example-obs"
        assert result.status == "final"
    
    def test_parse_invalid_json(self):
        """Test parsing invalid JSON raises error."""
        with pytest.raises(ValueError, match="Invalid JSON"):
            self.parser.parse("invalid json")
    
    def test_parse_missing_resource_type(self):
        """Test parsing data without resourceType raises error."""
        with pytest.raises(ValueError, match="Missing resourceType"):
            self.parser.parse({"id": "test"})
    
    def test_parse_unsupported_resource_type(self):
        """Test parsing unsupported resource type raises error."""
        with pytest.raises(ValueError, match="Unsupported resource type"):
            self.parser.parse({"resourceType": "UnsupportedResource"})
    
    def test_parse_bundle(self):
        """Test parsing FHIR Bundle."""
        bundle_data = {
            "resourceType": "Bundle",
            "id": "example-bundle",
            "type": "searchset",
            "total": 1,
            "entry": [{
                "resource": {
                    "resourceType": "Patient",
                    "id": "bundle-patient",
                    "active": True
                }
            }]
        }
        
        result = self.parser.parse_bundle(bundle_data)
        assert result['resourceType'] == 'Bundle'
        assert result['id'] == 'example-bundle'
        assert result['type'] == 'searchset'
        assert result['total'] == 1
        assert len(result['entry']) == 1
        assert isinstance(result['entry'][0], Patient)