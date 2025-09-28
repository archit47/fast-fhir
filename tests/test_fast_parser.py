"""Tests for Fast FHIR Parser with C extensions."""

import json
import pytest
from fast_fhir.fast_parser import FastFHIRParser
from fast_fhir.resources.patient import Patient


class TestFastFHIRParser:
    """Test cases for Fast FHIR Parser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = FastFHIRParser()
    
    def test_parser_initialization(self):
        """Test fast parser initializes correctly."""
        assert self.parser.version == "5.0.0"
        info = self.parser.get_performance_info()
        assert 'c_extensions_available' in info
        assert 'version' in info
    
    def test_parse_patient_with_fast_parser(self):
        """Test parsing Patient with fast parser."""
        patient_json = json.dumps({
            "resourceType": "Patient",
            "id": "fast-example",
            "active": True,
            "name": [{
                "use": "official",
                "family": "FastTest",
                "given": ["Speed"]
            }],
            "gender": "unknown",
            "birthDate": "1990-01-01"
        })
        
        result = self.parser.parse(patient_json)
        assert isinstance(result, Patient)
        assert result.id == "fast-example"
        assert result.active is True
        assert result.gender == "unknown"
        assert result.birth_date == "1990-01-01"
    
    def test_fast_field_extraction(self):
        """Test fast field extraction method."""
        json_data = json.dumps({
            "resourceType": "Patient",
            "id": "test-123",
            "active": True,
            "gender": "male"
        })
        
        # Test string field
        resource_type = self.parser.extract_field_fast(json_data, "resourceType")
        assert resource_type == "Patient"
        
        # Test string field
        patient_id = self.parser.extract_field_fast(json_data, "id")
        assert patient_id == "test-123"
        
        # Test boolean field
        active = self.parser.extract_field_fast(json_data, "active")
        assert active is True
        
        # Test missing field
        missing = self.parser.extract_field_fast(json_data, "nonexistent")
        assert missing is None
    
    def test_parse_bundle_fast(self):
        """Test fast bundle parsing."""
        bundle_data = {
            "resourceType": "Bundle",
            "id": "fast-bundle",
            "type": "searchset",
            "total": 2,
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": "patient-1",
                        "active": True
                    }
                },
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": "patient-2",
                        "active": False
                    }
                }
            ]
        }
        
        result = self.parser.parse_bundle(bundle_data)
        assert result['resourceType'] == 'Bundle'
        assert result['id'] == 'fast-bundle'
        assert result['total'] == 2
        assert len(result['entry']) == 2
        
        # Check parsed resources
        for entry in result['entry']:
            assert isinstance(entry, Patient)
    
    def test_performance_info(self):
        """Test performance information retrieval."""
        info = self.parser.get_performance_info()
        
        required_keys = ['c_extensions_available', 'c_extensions_enabled', 'version', 'features']
        for key in required_keys:
            assert key in info
        
        assert info['version'] == "5.0.0"
        assert isinstance(info['features'], list)
        assert len(info['features']) > 0
    
    def test_fallback_behavior(self):
        """Test that parser falls back gracefully when C extensions fail."""
        # This test ensures the parser works even without C extensions
        original_setting = self.parser.use_c_extensions
        
        try:
            # Temporarily disable C extensions
            self.parser.use_c_extensions = False
            
            patient_data = {
                "resourceType": "Patient",
                "id": "fallback-test",
                "active": True
            }
            
            result = self.parser.parse(patient_data)
            assert isinstance(result, Patient)
            assert result.id == "fallback-test"
            
        finally:
            # Restore original setting
            self.parser.use_c_extensions = original_setting
    
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON with fast parser."""
        with pytest.raises(ValueError):
            self.parser.parse("invalid json string")
    
    def test_missing_resource_type_handling(self):
        """Test handling of missing resourceType with fast parser."""
        with pytest.raises(ValueError, match="Missing resourceType"):
            self.parser.parse({"id": "test", "active": True})