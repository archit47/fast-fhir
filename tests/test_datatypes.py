"""Tests for FHIR R5 data types with C extensions."""

import json
import pytest
from src.fhir.datatypes import (
    FHIRString, FHIRBoolean, FHIRInteger, FHIRDecimal,
    FHIRCoding, FHIRCodeableConcept, FHIRQuantity, FHIRIdentifier, FHIRReference,
    validate_date, validate_time, validate_uri, validate_code,
    HAS_C_DATATYPES
)


class TestFHIRPrimitiveTypes:
    """Test FHIR primitive data types."""
    
    def test_fhir_string(self):
        """Test FHIR string data type."""
        fhir_str = FHIRString("Hello FHIR")
        result = fhir_str.to_dict()
        assert result["value"] == "Hello FHIR"
        
        # Test from_dict
        recreated = FHIRString.from_dict(result)
        assert recreated.value == "Hello FHIR"
    
    def test_fhir_boolean(self):
        """Test FHIR boolean data type."""
        fhir_bool = FHIRBoolean(True)
        result = fhir_bool.to_dict()
        assert result["value"] is True
        
        # Test from_dict
        recreated = FHIRBoolean.from_dict(result)
        assert recreated.value is True
    
    def test_fhir_integer(self):
        """Test FHIR integer data type."""
        fhir_int = FHIRInteger(42)
        result = fhir_int.to_dict()
        assert result["value"] == 42
        
        # Test from_dict
        recreated = FHIRInteger.from_dict(result)
        assert recreated.value == 42
    
    def test_fhir_decimal(self):
        """Test FHIR decimal data type."""
        fhir_decimal = FHIRDecimal(3.14159)
        result = fhir_decimal.to_dict()
        assert result["value"] == 3.14159
        
        # Test from_dict
        recreated = FHIRDecimal.from_dict(result)
        assert recreated.value == 3.14159


class TestFHIRComplexTypes:
    """Test FHIR complex data types."""
    
    def test_fhir_coding(self):
        """Test FHIR Coding data type."""
        coding = FHIRCoding(
            system="http://loinc.org",
            code="15074-8",
            display="Glucose",
            user_selected=True
        )
        
        result = coding.to_dict()
        assert result["system"] == "http://loinc.org"
        assert result["code"] == "15074-8"
        assert result["display"] == "Glucose"
        assert result["userSelected"] is True
        
        # Test from_dict
        recreated = FHIRCoding.from_dict(result)
        assert recreated.system == "http://loinc.org"
        assert recreated.code == "15074-8"
        assert recreated.display == "Glucose"
        assert recreated.user_selected is True
    
    def test_fhir_coding_from_json(self):
        """Test FHIR Coding from JSON string."""
        json_data = {
            "system": "http://snomed.info/sct",
            "code": "386661006",
            "display": "Fever"
        }
        json_string = json.dumps(json_data)
        
        coding = FHIRCoding.from_json(json_string)
        assert coding.system == "http://snomed.info/sct"
        assert coding.code == "386661006"
        assert coding.display == "Fever"
    
    def test_fhir_codeable_concept(self):
        """Test FHIR CodeableConcept data type."""
        coding1 = FHIRCoding("http://loinc.org", "15074-8", "Glucose")
        coding2 = FHIRCoding("http://snomed.info/sct", "33747000", "Glucose")
        
        concept = FHIRCodeableConcept(
            text="Blood glucose level",
            coding=[coding1, coding2]
        )
        
        result = concept.to_dict()
        assert result["text"] == "Blood glucose level"
        assert len(result["coding"]) == 2
        assert result["coding"][0]["system"] == "http://loinc.org"
        assert result["coding"][1]["system"] == "http://snomed.info/sct"
        
        # Test from_dict
        recreated = FHIRCodeableConcept.from_dict(result)
        assert recreated.text == "Blood glucose level"
        assert len(recreated.coding) == 2
    
    def test_fhir_quantity(self):
        """Test FHIR Quantity data type."""
        quantity = FHIRQuantity(
            value=6.3,
            unit="mmol/l",
            system="http://unitsofmeasure.org",
            code="mmol/L",
            comparator=">"
        )
        
        result = quantity.to_dict()
        assert result["value"] == 6.3
        assert result["unit"] == "mmol/l"
        assert result["system"] == "http://unitsofmeasure.org"
        assert result["code"] == "mmol/L"
        
        # Test from_dict
        recreated = FHIRQuantity.from_dict(result)
        assert recreated.value == 6.3
        assert recreated.unit == "mmol/l"
        assert recreated.system == "http://unitsofmeasure.org"
        assert recreated.code == "mmol/L"
    
    def test_fhir_quantity_from_json(self):
        """Test FHIR Quantity from JSON string."""
        json_data = {
            "value": 120,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        }
        json_string = json.dumps(json_data)
        
        quantity = FHIRQuantity.from_json(json_string)
        assert quantity.value == 120
        assert quantity.unit == "mmHg"
        assert quantity.system == "http://unitsofmeasure.org"
        assert quantity.code == "mm[Hg]"
    
    def test_fhir_identifier(self):
        """Test FHIR Identifier data type."""
        identifier = FHIRIdentifier(
            system="http://hospital.example.org",
            value="12345",
            use="usual"
        )
        
        result = identifier.to_dict()
        assert result["system"] == "http://hospital.example.org"
        assert result["value"] == "12345"
        assert result["use"] == "usual"
        
        # Test from_dict
        recreated = FHIRIdentifier.from_dict(result)
        assert recreated.system == "http://hospital.example.org"
        assert recreated.value == "12345"
        assert recreated.use == "usual"
    
    def test_fhir_reference(self):
        """Test FHIR Reference data type."""
        reference = FHIRReference(
            reference="Patient/example",
            display="John Doe"
        )
        
        result = reference.to_dict()
        assert result["reference"] == "Patient/example"
        assert result["display"] == "John Doe"
        
        # Test from_dict
        recreated = FHIRReference.from_dict(result)
        assert recreated.reference == "Patient/example"
        assert recreated.display == "John Doe"


class TestFHIRValidation:
    """Test FHIR validation functions."""
    
    def test_validate_date(self):
        """Test FHIR date validation."""
        assert validate_date("2023") is True
        assert validate_date("2023-12") is True
        assert validate_date("2023-12-25") is True
        assert validate_date("invalid") is False
        assert validate_date("2023-13-01") is False  # Invalid month
        assert validate_date("2023-12-32") is False  # Invalid day
    
    def test_validate_time(self):
        """Test FHIR time validation."""
        assert validate_time("14:30:00") is True
        assert validate_time("14:30:00.123") is True
        assert validate_time("invalid") is False
        assert validate_time("25:00:00") is False  # Invalid hour
        assert validate_time("14:60:00") is False  # Invalid minute
    
    def test_validate_uri(self):
        """Test FHIR URI validation."""
        assert validate_uri("http://example.com") is True
        assert validate_uri("urn:oid:1.2.3.4") is True
        assert validate_uri("fhir:Patient") is True
        assert validate_uri("invalid") is False
    
    def test_validate_code(self):
        """Test FHIR code validation."""
        assert validate_code("active") is True
        assert validate_code("male") is True
        assert validate_code("123") is True
        assert validate_code("") is False
        assert validate_code("invalid code") is False  # Contains space


class TestCExtensionIntegration:
    """Test C extension integration."""
    
    def test_c_extension_availability(self):
        """Test C extension availability reporting."""
        # This test just checks that the flag is properly set
        assert isinstance(HAS_C_DATATYPES, bool)
        print(f"C extensions available: {HAS_C_DATATYPES}")
    
    def test_fallback_behavior(self):
        """Test that fallback to Python works when C extensions fail."""
        # Create data types with C extensions disabled
        fhir_str = FHIRString("test", use_c_extensions=False)
        result = fhir_str.to_dict()
        assert result["value"] == "test"
        
        # Test validation fallback
        assert validate_date("2023-12-25") is True
        assert validate_time("14:30:00") is True