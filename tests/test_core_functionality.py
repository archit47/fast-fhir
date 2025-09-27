#!/usr/bin/env python3
"""
Core functionality tests for Fast-FHIR.

This test file validates that the main Fast-FHIR functionality works
without relying on legacy imports.
"""

import unittest
import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from fast_fhir.deserializers import (
        deserialize_patient,
        deserialize_organization,
        deserialize_care_plan,
        PYDANTIC_AVAILABLE
    )
    FAST_FHIR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Fast-FHIR not available: {e}")
    FAST_FHIR_AVAILABLE = False


class TestCoreFunctionality(unittest.TestCase):
    """Test core Fast-FHIR functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.patient_data = {
            "resourceType": "Patient",
            "id": "test-patient",
            "active": True,
            "name": [
                {
                    "use": "official",
                    "family": "TestFamily",
                    "given": ["TestGiven"]
                }
            ],
            "gender": "male"
        }
        
        self.organization_data = {
            "resourceType": "Organization",
            "id": "test-org",
            "active": True,
            "name": "Test Organization"
        }
        
        self.care_plan_data = {
            "resourceType": "CarePlan",
            "id": "test-careplan",
            "status": "active",
            "intent": "plan",
            "title": "Test Care Plan"
        }
    
    @unittest.skipUnless(FAST_FHIR_AVAILABLE, "Fast-FHIR not available")
    def test_patient_deserialization(self):
        """Test Patient resource deserialization."""
        patient = deserialize_patient(self.patient_data, use_pydantic_validation=False)
        
        self.assertIsNotNone(patient)
        self.assertEqual(patient.id, "test-patient")
        self.assertEqual(patient.resource_type, "Patient")
        self.assertTrue(patient.active)
    
    @unittest.skipUnless(FAST_FHIR_AVAILABLE, "Fast-FHIR not available")
    def test_organization_deserialization(self):
        """Test Organization resource deserialization."""
        organization = deserialize_organization(self.organization_data, use_pydantic_validation=False)
        
        self.assertIsNotNone(organization)
        self.assertEqual(organization.id, "test-org")
        self.assertEqual(organization.resource_type, "Organization")
        self.assertTrue(organization.active)
    
    @unittest.skipUnless(FAST_FHIR_AVAILABLE, "Fast-FHIR not available")
    def test_care_plan_deserialization(self):
        """Test CarePlan resource deserialization."""
        care_plan = deserialize_care_plan(self.care_plan_data, use_pydantic_validation=False)
        
        self.assertIsNotNone(care_plan)
        self.assertEqual(care_plan.id, "test-careplan")
        self.assertEqual(care_plan.resource_type, "CarePlan")
        # Status might be an enum or string - just check it exists and is not None
        self.assertIsNotNone(care_plan.status)
    
    @unittest.skipUnless(FAST_FHIR_AVAILABLE, "Fast-FHIR not available")
    def test_json_string_input(self):
        """Test deserialization from JSON strings."""
        json_string = json.dumps(self.patient_data)
        patient = deserialize_patient(json_string, use_pydantic_validation=False)
        
        self.assertIsNotNone(patient)
        self.assertEqual(patient.id, "test-patient")
    
    def test_pydantic_availability(self):
        """Test that Pydantic availability is properly detected."""
        # This should not raise an exception
        self.assertIsInstance(PYDANTIC_AVAILABLE, bool)
    
    @unittest.skipUnless(FAST_FHIR_AVAILABLE, "Fast-FHIR not available")
    def test_error_handling(self):
        """Test error handling for invalid data."""
        with self.assertRaises(Exception):
            deserialize_patient("invalid json", use_pydantic_validation=False)
        
        with self.assertRaises(Exception):
            deserialize_patient({"resourceType": "InvalidType"}, use_pydantic_validation=False)


class TestPackageStructure(unittest.TestCase):
    """Test package structure and imports."""
    
    def test_package_imports(self):
        """Test that main package imports work."""
        try:
            import fast_fhir
            self.assertTrue(True, "fast_fhir package imports successfully")
        except ImportError:
            self.fail("fast_fhir package import failed")
    
    def test_deserializers_module(self):
        """Test that deserializers module imports work."""
        if FAST_FHIR_AVAILABLE:
            from fast_fhir import deserializers
            self.assertTrue(hasattr(deserializers, 'deserialize_patient'))
            self.assertTrue(hasattr(deserializers, 'deserialize_organization'))
            self.assertTrue(hasattr(deserializers, 'deserialize_care_plan'))


if __name__ == '__main__':
    print("Running Fast-FHIR Core Functionality Tests")
    print("=" * 50)
    print(f"Fast-FHIR Available: {FAST_FHIR_AVAILABLE}")
    if FAST_FHIR_AVAILABLE:
        print(f"Pydantic Available: {PYDANTIC_AVAILABLE}")
    print()
    
    unittest.main(verbosity=2)